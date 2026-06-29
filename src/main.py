from api_query import get_url, get_item_list, request_page

def main():
    print("What item are you making?")
    item = input()
    print("How many do you want to make?")
    amount = input()
    url = get_url(item)
    r = request_page(url)
    items_needed = get_item_list(r)
    if amount != 1:
        print(f"Items needed to make {amount} {item}s:")
    else:
        print(f"Items needed to make {amount} {item}:")
    for item in items_needed:
        prereqs = int(item[1])
        prereqs_needed = prereqs * int(amount)
        print(f"{item[0]}: {(prereqs_needed)}")

if __name__ == "__main__":
    main()