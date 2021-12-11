import requests
from bs4 import BeautifulSoup as bS
song = input("What song: ")
resp = requests.get(f"https://musixmatch.com/search/{song}/tracks")
print(f"https://musixmatch.com/search/{song}/tracks")
print(resp)
a = bS(resp.text, 'html.parser')
#a = a.find_all('div', class_="empty")
print(a)

