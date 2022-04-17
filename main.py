import requests
import urllib.request, urllib.parse, urllib.error
import ssl
import os
from bs4 import BeautifulSoup

link = input("Enter link")
base = "https://commons.wikimedia.org"

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Finds the content title
html = urllib.request.urlopen(link, context=ctx).read()
soup = BeautifulSoup(html,'lxml')
title = soup.find('h1', id="firstHeading").get_text()
cont = title.split("Category:")[-1]
# If folder doesn't exist, then it's created.
try:
    os.mkdir(cont)
except:
    pass

# Finds all the links of images
links = []
gallery = soup.find_all('li',class_="gallerybox")
for i in range(0,len(gallery)):
    pack = gallery[i].find('a')['href']
    links.append((base+pack))

# Navigates through links, finds original size links
for i in links:
    html = urllib.request.urlopen(i, context=ctx).read()
    soup = BeautifulSoup(html,'lxml')
    actual = soup.find_all('div',class_="fullImageLink")

    # Fetches the images
    for i in range(0,len(actual)):
        actuallink = actual[i].find('a')['href']
        with open(f"{cont}\{actuallink.split('/')[-1]}","wb") as handle:
            response = requests.get(actuallink, headers={'User-Agent': 'Mozilla/6.0'}).content
            handle.write(response)
            handle.close()