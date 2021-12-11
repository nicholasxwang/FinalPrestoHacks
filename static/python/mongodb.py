import pymongo
import os
from werkzeug.security import generate_password_hash, check_password_hash
db =pymongo.MongoClient(os.environ['token']).MusiqueWorld.Users
def getUsers():
  users = []
  for i in db.find({}):
    users.append(i)
def addUser(email, password, username, beta_code):
  count = 0
  for a in db.find({}):
    if a["email"] == email:
      return 1 #email taken
    if a["username"] == username:
      return 2 #username taken
    count+=1
  db.insert_one({"_id":count,"email":email,"password":generate_password_hash(password),"username":username})
  return 0 #success