require('dotenv').config();

const path = require('path');
const { writeFile } = require('fs');

const fetch = require('node-fetch');
const puppeteer = require('puppeteer');
const { wait, pageUrl } = require('./util');

const parseArgv = require('./argv');
const { product: productNum, folder: dir, delay } = parseArgv();

(async () => {
    // check for login credentials
    const { USERNAME, PASSWORD } = process.env;
    if (!USERNAME || !PASSWORD) {
        console.log('Username and password not present. Please set in `.env` file.');
        return;
    }

    // confirmation
    console.log('Starting job.');

    const browser = await puppeteer.launch({
        headless: false,
        defaultViewport: null,
        args: ['--window-size=1920,1080']
    });
    const page = await browser.newPage();

    // login
    await page.goto(pageUrl(productNum, 1), { waitUntil: 'networkidle2' });
    await page.waitForSelector('input#username', { visible: true });

    await page.type('input#username', USERNAME, { delay: 100 });
    await page.type('input#password', PASSWORD, { delay: 100 });

    await Promise.all([
        page.waitForNavigation({ waitUntil: 'networkidle2' }),
        page.keyboard.press('Enter')
    ]);
    await wait(3000);
    console.log('Finished login.');

    // open navigation slider
    await page.evaluate(() => {
        [...document.querySelectorAll('div.MuiListItem-button-1194[aria-label]')]
            .find(btn => btn.ariaLabel === 'Scrubber Navigation')
            .click();
    });
    await wait(2000);
    await dragToBottom('span.thumbCircle');
    await wait(2000);

    // get last page, base image url, and cookie
    const { lastPage, baseUrl, cookie } = await page.evaluate(() => {
        const path = new URL(window.location.href).pathname.split('/');
        const img = new URL(document.getElementById('docViewer_ViewContainer_BG_0').src);
        return {
            lastPage: parseInt(path[path.length - 1]),
            cookie: document.cookie,
            baseUrl: (img.origin + img.pathname).replace(/[0-9]+$/, '')
        };
    });

    // cleanup
    await browser.close();

    // downloading
    for (let i = 1; i <= lastPage; i++) {
        const res = await fetch(baseUrl + i, { headers: { cookie } });
        await writeFile(path.join(dir, `${i}.png`), Buffer.from(await res.arrayBuffer()), () => {});
        if (i % 10 === 0) console.log(`Downloaded page ${i}.`);
        await wait(delay); // delay before downloading next page; highly recommended not to change
    }
    if (lastPage % 10) console.log(`Downloaded page ${lastPage}.`);


    // utility function
    async function dragToBottom(selector) {
        const rect = await page.$eval(selector, elem => {
            const { top, left, width, height } = elem.getBoundingClientRect();
            return { top, left, width, height, clientHeight: document.documentElement.clientHeight };
        });
        await page.mouse.move(rect.left + rect.width / 2, rect.top + rect.height / 2);
        await page.mouse.down();
        await page.mouse.move(rect.left + rect.width / 2, rect.clientHeight - 5);
        await page.mouse.up();
    };

    console.log('Finished job.');
})();