#!/usr/bin/env python
#import urllib.request
import requests

#with urllib.request.urlopen('https://codeload.github.com/home-assistant/brands/zip/refs/heads/master') as f:
#    html = f.read().decode('utf-8')

url = 'https://codeload.github.com/home-assistant/brands/zip/refs/heads/master'
r = requests.get(url, allow_redirects=True)

open('facebook.zip', 'wb').write(r.content)
