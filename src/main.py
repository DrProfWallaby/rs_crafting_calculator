from item import Item
from api_query import get_url, request_page, get_item_name

def main():
    print("What item are you making?")
    item = input()
    print("How many do you want to make?")
    amount = input()

    wanted_item = Item(item, 1)
    # ensure we have the latest recipe data for the root item (parse the
    # recipe table directly here to avoid subtle module-level differences)
    url = get_url(wanted_item.name)
    r = request_page(url)
    try:
        data = __import__('json').loads(r.text)
        html = data['parse']['text']['*']
    except Exception:
        html = ''
    if html:
        from bs4 import BeautifulSoup
        import re
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('div', {'class': 'recipe-table'})
        raw_items = []
        if table:
            rows = table.find_all('tr')
            dose_strip = re.compile(r"\s*\(\d+\)$")
            normalized_target = wanted_item.name
            for row in rows:
                cols = [td.text.strip() for td in row.find_all('td')]
                if len(cols) >= 3 and cols[0].strip() == '':
                    name = cols[1].strip()
                    qty = 0
                    for ch in cols[2]:
                        if ch.isdigit():
                            qty = qty * 10 + int(ch)
                    # ignore rows that are the output row (match without dose)
                    short_name = dose_strip.sub('', get_item_name(name))
                    if short_name != normalized_target:
                        raw_items.append((name, qty))
        wanted_item.raw_required_items = raw_items
    requested_amount = int(amount)
    for raw_item in wanted_item.raw_required_items:
        wanted_item.add_required_items(raw_item[0], raw_item[1])

    all_items = wanted_item.total_item_count(multiplier=requested_amount)
    if amount != "1":
        print(f"Items needed to make {amount} {wanted_item.name}s:")
    else:
        print(f"Items needed to make {amount} {wanted_item.name}:")

    intermediates = wanted_item.intermediate_counts(multiplier=requested_amount)
    if intermediates:
        for item_name, total_amount in intermediates.items():
            print(f"{item_name}: {total_amount}")
    for item_name, total_amount in all_items.items():
        print(f"{item_name}: {total_amount}")

if __name__ == "__main__":
    main()