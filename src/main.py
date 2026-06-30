from item import Item

def main():
    print("What item are you making?")
    item = input()
    print("How many do you want to make?")
    amount = input()

    wanted_item = Item(item)
    for raw_item in wanted_item.raw_required_items:
        wanted_item.add_required_items(raw_item[0], raw_item[1])

    if amount != "1":
        print(f"Items needed to make {amount} {wanted_item.name}s:")
    else:
        print(f"Items needed to make {amount} {wanted_item.name}:")

    for required_item in wanted_item.required_items:
        prereqs = int(required_item[1])
        prereqs_needed = prereqs * int(amount)
        print(f"{required_item[0].name}: {(prereqs_needed)}")

if __name__ == "__main__":
    main()