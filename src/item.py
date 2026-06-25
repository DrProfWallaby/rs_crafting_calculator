class Item:
    def __init__(self, name: str, price: int = 0):
        self.name = name
        self.price = price
        self.required_items: list[tuple[Item, int]] = []

    def add_required_items(self, item: Item, amount: int) -> None:
        if (item, amount) in self.required_items:
            raise Exception("Error: Item already added.")
        self.required_items.append((item, amount))

#    def get_required_items(self):
#        if not self.required_items:
#            return
#        total_required_items: list[tuple[Item, int]] = []
#        for item_tuple in self.required_items:
#            item = item_tuple[0]
#            if item.required_items:
#                item.get_required_items()
#            total_required_items.append(item_tuple)
#        return total_required_items