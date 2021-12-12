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
    return "Sorry, I could not find any song related to your picture. How about, try Head Up by The Score!"
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
    return "I found what your picture is thanks to my smart AI but I could not find any songs. How about, try AJR's Bang? Synonyms include "+str(synonyms)+"\n We ignored: "+str(ignored)
  else:
    return "Yay! The best result is \""+str(songs[0])+"\" \nOur Synonym list include: " + str(synonyms)+"\nOther results include: "+str(songs[1:len(songs)])+"\n We ignored: "+str(ignored)

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
from flask import Flask, render_template, request
from waitress import serve
import os
from flask_mail import Mail, Message

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

@app.route("/")
#Run
serve(app, host="0.0.0.0", port=8080)
