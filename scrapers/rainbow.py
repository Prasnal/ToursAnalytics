import datetime
import requests
from bs4 import BeautifulSoup
import json

def parse(el, full_json):
    if type(el) == list:
        parsed_list = list()
        for l in el:
            if type(l) == int:
                if l < len(full_json):
                    parsed = parse(full_json[l], full_json)
                    parsed_list.append(parsed)
                else:
                    raise ("ERROR!")
            else:
                parsed_list.append(l)
        return parsed_list
    elif type(el) == dict:
        parsed_dict = dict()
        for key in el:
            parsed_dict[parse(key, full_json)] = parse(full_json[el[key]], full_json)
        return parsed_dict
    else:
        return el


def parse_json(json_text):
    parsed_json = list()
    for el in json_text:
        parsed = parse(el, json_text)
        parsed_json.append(parsed)
    return parsed_json


r = requests.get("https://r.pl/wycieczki-objazdowe")
soup = BeautifulSoup(r.text)

#tours=soup.findAll("script")[-7].string
codes = soup.findAll("script")[-4].string
codes_json = json.loads(codes)
result = parse_json(codes_json)

print(json.dumps(result,indent=2))
