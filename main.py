from pyvirtualdisplay import Display
display = Display(visible=0, size=(800, 600))
display.start()
from selenium import webdriver
import time
browser = webdriver.Firefox()


ignore = [
  "wallpaper",
  "picture",
  "landscape",
  "mac",
  "macos",
  "os",
  "windows",
  "windowsos",
  "linux",
  "linuxos",
  "profile",
  "avatar",
  "1k",
  "2k",
  "3k",
  "4k",
  "5k",
  "6k",
  "7k",
  "8k",
  "the",
  "an",
  "a",
  "and",
  "or"
]
def main_program(image):
  a = str(get_image_name(image))
  #Check if it exists
  if a == "n":
    #return "Sorry, I could not find any song related to your picture. How about, try Head Up by The Score!"
    return []
  #split into words
  word = a.split(" ")
  songs = []
  ignored = []
  import nltk
  nltk.download('wordnet')
  from nltk.corpus import wordnet
  for i in word:
    if i.lower() in ignore:
      ignored.append(i.lower())
      continue
    #Find Synonyms
    synonyms = []
    antonyms = []
      
    for syn in wordnet.synsets(i):
        for l in syn.lemmas():
            synonyms.append(l.name())
            if l.antonyms():
                antonyms.append(l.antonyms()[0].name())
      
    for x in range(0,len(synonyms)):
      synonyms[x] = synonyms[x].replace("_"," ")
    synonyms = set(synonyms)
    #Search for songs
    synonyms = list(synonyms)
    synonyms = [i]+synonyms
    
    for j in synonyms:
      temp = find_music(j)
      if not (temp=="n"):
        for j in temp:
          songs.append(j.text)

  if len(songs) == 0:
    #return "I found what your picture is thanks to my smart AI but I could not find any songs. How about, try AJR's Bang? Synonyms include "+str(synonyms)+"\n We ignored: "+str(ignored)
    return []
  else:
    #return "Yay! The best result is \""+str(songs[0])+"\" \nOur Synonym list include: " + str(synonyms)+"\nOther results include: "+str(songs[1:len(songs)])+"\n We ignored: "+str(ignored)
    return str(songs)

def get_image_name(image_url):
  browser.get("https://www.google.com/searchbyimage?site=search&sa=X&image_url="+image_url)
  time.sleep(2)
  try:
    parsed = browser.find_elements_by_class_name("fKDtNb")[0].text
  except Exception as e:
    parsed = "n"
  return parsed

def find_music(query):
  browser.get(f"https://www.musixmatch.com/search/{query}/tracks")
  time.sleep(2)
  try:
    a = browser.find_elements_by_class_name("title")
  except:
    return "n"
  return a
  


#Permissions Fix: chmod +x geckodriver

#Imports
from flask import Flask, render_template, request, flash, redirect, url_for
from waitress import serve
import os
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename

#Inits
app = Flask('app')
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'virtualholidaysmidnighthacks@gmail.com'
app.config['MAIL_PASSWORD'] = os.getenv('psw')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

#Routing
@app.route('/')
def main():
  return render_template('index.html')
app.secret_key = 'github'
UPLOAD_FOLDER = './static/images'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        #return str(request.files)
        # check if the post request has the file part
        if 'file' not in request.files:
            #return '1'
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            #return '2'
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            #return '3'
            filename = secure_filename(file.filename)
            #os.mkdir(os.path.join(UPLOAD_FOLDER, filename))
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            x=os.path.join(UPLOAD_FOLDER, filename)
            #return redirect(url_for('upload_file', name=filename))
            print(get_image_name(x))
            return str(get_image_name(x))
#Run
serve(app, host="0.0.0.0", port=8080)