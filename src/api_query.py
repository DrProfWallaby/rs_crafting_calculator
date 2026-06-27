import requests
import json

from bs4 import BeautifulSoup, SoupStrainer

url = 'https://runescape.wiki/api.php?action=parse&page=High_priest_orb&format=json'
headers = {'user-agent' : 'recipe-calculator'}
r = requests.get(
    url,
    headers=headers,
)

url_split = url.split('&')
page_name = url_split[1].split('=')
split_name = page_name[1].split('_')
name = " ".join(split_name)

json_query = json.loads(r.text)
json_parsed = json_query['parse']
json_text = json_parsed['text']
json_final = json_text['*']

html_doc = BeautifulSoup(json_final, 'html.parser')

table = html_doc.find('div', {"class": "recipe-table"})
items_needed = []
rows = table.find_all("tr")
parsed_rows = []
for i in rows:
    table_data = i.find_all('td')
    data = [j.text for j in table_data]
    parsed_rows.append(data)
for row in parsed_rows:
    row_index = len(parsed_rows) - 1
    if row == []:
        continue
    if row[0] == '' and row != parsed_rows[row_index]:
        items_needed.append((row[1], row[2]))
print(f"Items needed for {name}:")
print(items_needed)