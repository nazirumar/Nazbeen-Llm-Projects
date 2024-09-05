from bs4 import BeautifulSoup
from urllib.request import Request, urlopen


url = "https://community.dataquest.io/c/share/guided-project/55"
html = urlopen(url)
soup = BeautifulSoup(html, 'html.parser')

print