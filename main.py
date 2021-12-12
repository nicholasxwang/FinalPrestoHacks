from pyvirtualdisplay import Display
display = Display(visible=0, size=(800, 600))
display.start()
from selenium import webdriver
import time
browser = webdriver.Firefox()
from __future__ import unicode_literals
import youtube_dl

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

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
def main_program(file_name):
  import io
  import os
  os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./festive-freedom-309323-0124a1c976ae.json"
  from google.cloud import vision
  client = vision.ImageAnnotatorClient()
  file_name = os.path.abspath(file_name)
  # Loads the image into memory
  with io.open(file_name, 'rb') as image_file:
      content = image_file.read()
  image = vision.Image(content=content)

  #Logos
  logo_list = []
  response = client.logo_detection(image=image)
  logos = response.logo_annotations
  for logo in logos:
      logo_list.append(logo.description)

  if (len(logo_list)>0):
    return logo_list
  response = client.landmark_detection(image=image)
  landmarks = response.landmark_annotations
  landmark_list = []
  for landmark in landmarks:
      landmark_list.append(landmark.description)


  if (len(landmark_list)>0):
    return landmark_list

  #General
  response = client.label_detection(image=image)
  labels = response.label_annotations
  general_list = []

  for label in labels:
      general_list.append(label.description)

  return general_list


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
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'heic', 'webm'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        #return str(request.files)
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            a = main_program(os.path.join(UPLOAD_FOLDER, filename))
            return str(a)

            
#Run
serve(app, host="0.0.0.0", port=8080)