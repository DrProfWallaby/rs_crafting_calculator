import re
import requests
import json
import sys

from urllib.parse import quote
from bs4 import BeautifulSoup

BASE_OUTPUT_SUFFIXES = {"(item)", "(scenery)"}


def get_item_name(name: str) -> str:
    roman_numerals = {
        "i",
        "ii",
        "iii",
        "iv",
        "v",
        "vi",
        "vii",
        "viii",
        "ix",
        "x",
    }
    if not name or not name.strip():
        raise ValueError("No input provided")

    name = re.sub(r"\+\s*(\d+)", r"+\1", name.strip())
    split_name = name.split()
    normalized = []
    for index, token in enumerate(split_name):
        lower_token = token.lower()
        if index == len(split_name) - 1 and lower_token in roman_numerals:
            normalized.append(lower_token.upper())
        else:
            normalized.append(lower_token)
    if normalized and normalized[-1] in BASE_OUTPUT_SUFFIXES:
        normalized.pop()
    return " ".join(normalized)

def get_url(input: str) -> str:
    page = quote(input.replace(' ', '_'), safe='_')
    return f"https://runescape.wiki/api.php?action=parse&page={page}&format=json&redirects=1"

def request_page(url: str) -> requests.Response:
    headers = {'user-agent' : 'recipe-calculator'}
    r = requests.get(
        url,
        headers=headers,
    )
    return r

def parse_quantity(value: str) -> int:
    digits = "".join(ch for ch in value if ch.isdigit())
    return int(digits) if digits else 0


def get_recipe_data(r: requests.Response, target_name: str) -> tuple[list[tuple[str, int]], int, bool, str]:
    """
    Parse a MediaWiki parse API response to extract recipe ingredients.
    Returns: (items_needed, output_quantity, is_herblore, page_title)
    """
    items_needed: list[tuple[str, int]] = []
    output_quantity = 1
    is_herblore = False
    page_title = ""

    try:
        json_query = json.loads(r.text)
    except json.JSONDecodeError:
        return items_needed, output_quantity, is_herblore, page_title

    if 'error' in json_query or 'parse' not in json_query:
        return items_needed, output_quantity, is_herblore, page_title

    json_parsed = json_query['parse']
    page_title = json_parsed.get('title', '')
    html = json_parsed['text']['*']

    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('div', {'class': 'recipe-table'})
    if not table:
        return items_needed, output_quantity, is_herblore, page_title

    page_text = soup.get_text(separator=' ')
    is_herblore = 'herblore' in page_text.lower()
    # Skip transmutation/necromancy-like pages
    if 'transmutation' in page_text.lower() or 'ritual component info' in page_text.lower() or 'necromancy' in page_text.lower():
        return items_needed, output_quantity, is_herblore, page_title

    rows = table.find_all('tr')
    dose_strip = re.compile(r"\s*\(\d+\)$")
    normalized_target = get_item_name(target_name)

    for row in rows:
        cols = [td.text.strip() for td in row.find_all('td')]
        if not cols:
            continue
        if len(cols) >= 3 and cols[0].strip() == '':
            name = cols[1].strip()
            amount = parse_quantity(cols[2])
            normalized_name = get_item_name(name)
            short_name = dose_strip.sub('', normalized_name)
            if short_name == normalized_target:
                if amount > 0:
                    output_quantity = amount
            else:
                items_needed.append((name, amount))

    return items_needed, output_quantity, is_herblore, page_title
