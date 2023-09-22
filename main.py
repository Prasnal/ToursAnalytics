import requests
from bs4 import BeautifulSoup

#print("hello!")

r = requests.get("https://r.pl/wycieczki-objazdowe")
soup = BeautifulSoup(r.text)

tours=soup.findAll("script")[-4].string

print(tours)