import requests
import json

from bs4 import BeautifulSoup

def get_item_name(name: str) -> str:
    roman_numerals = ["i", 
                      "ii", 
                      "iii", 
                      "iv", 
                      "v", 
                      "vi", 
                      "vii", 
                      "viii", 
                      "ix", 
                      "x"
                    ]
    if not name:
        raise ValueError("No input provided")
    split_name = name.lower().split(" ")
    if len(split_name) == 1:
        return split_name[0]
    for roman_numeral in roman_numerals:
        if roman_numeral in split_name[-1]:
            split_name[-1] = split_name[-1].upper()
    return " ".join(split_name)

def get_url(input:str) -> str:
    url = ""
    split_input = input.split(" ")
    if len(split_input) == 1:
        url = f"https://runescape.wiki/api.php?action=parse&page={input}&format=json"
    else:
        combined_input = "_".join(split_input)
        url = f"https://runescape.wiki/api.php?action=parse&page={combined_input}&format=json"
    return url

def request_page(url: str) -> requests.Response:
    headers = {'user-agent' : 'recipe-calculator'}
    r = requests.get(
        url,
        headers=headers,
    )
    return r

def get_item_list(r: requests.Response) -> list[tuple[str, int]]:
    items_needed = []
    parsed_rows = []

    json_query = json.loads(r.text)
    json_parsed = json_query['parse']
    json_text = json_parsed['text']
    json_final = json_text['*']

    html_doc = BeautifulSoup(json_final, 'html.parser')
    table = html_doc.find('div', {"class": "recipe-table"})
    if not table:
        return items_needed
    rows = table.find_all("tr")
    
    for i in rows:
        table_data = i.find_all('td')
        data = [j.text for j in table_data]
        parsed_rows.append(data)
    for row in parsed_rows:
        if "Transmutation" in html_doc:
            break
        if "Cursed magic logs" in row:
            break
        if row == [] and len(items_needed) != 0:
            break
        if row == []:
            continue
        if row[0] == '':
            items_needed.append((row[1], row[2]))
    return items_needed