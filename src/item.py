from api_query import get_url, request_page, get_item_list, get_item_name

class Item:
    def __init__(self, name: str, price: int = 0):
        self.name = get_item_name(name)
        self.price = price
        self.required_items: list[tuple[Item, int]] = []
        self.url = get_url(self.name)
        self.raw_required_items: list[tuple[str, int]] = get_item_list(request_page(self.url))
        

    def add_required_items(self, item: str, amount: int) -> None:
        if self.raw_required_items == []:
            return
        new_item = Item(item)
        for needed_item in self.raw_required_items:
            new_item.add_required_items(needed_item[0], needed_item[1])
        self.required_items.append((new_item, amount))

