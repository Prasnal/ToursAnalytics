import requests
#from bs4 import BeautifulSoup
from scrapers import rainbow_without_parsing


rainbow_without_parsing.main_rainbow(save_to_json=True, save_to_db=False)

#print("hello!")

# r = requests.get("https://r.pl/wycieczki-objazdowe")
# soup = BeautifulSoup(r.text)
#
# tours=soup.findAll("script")[-4].string
#
# print(tours)