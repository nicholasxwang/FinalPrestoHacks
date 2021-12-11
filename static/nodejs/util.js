const wait = require('util').promisify(setTimeout);

/**
 * Generates a URL that leads to a textbook page.
 * @param {String} product Product (textbook) number.
 * @param {String} pageNum Page number.
 * @returns {String} Resulting url.
 */
const pageUrl = (product, pageNum) =>
    `https://plus.pearson.com/products/${product}/pages/${pageNum}`;

module.exports = { wait, pageUrl };
© 2021 GitHub, Inc.
Terms
Privacy
Security
