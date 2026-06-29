import requests
import json

from bs4 import BeautifulSoup

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
    rows = table.find_all("tr")
    
    for i in rows:
        table_data = i.find_all('td')
        data = [j.text for j in table_data]
        parsed_rows.append(data)
    for row in parsed_rows:
        row_index = len(parsed_rows) - 1
        if row == [] and len(items_needed) != 0:
            break
        if row == []:
            continue
        if row[0] == '' and row != parsed_rows[row_index - 1]:
            items_needed.append((row[1], row[2]))
    return items_needed

#url_split = url.split('&')
#page_name = url_split[1].split('=')
#split_name = page_name[1].split('_')
#name = " ".join(split_name)

#print(f"Items needed for {name}:")
#print(items_needed)