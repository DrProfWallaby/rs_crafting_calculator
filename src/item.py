import math

from api_query import get_url, request_page, get_recipe_data, get_item_name

class Item:
    BASE_MATERIALS = {
        "ashes",
        "vial",
        "vial of water",
        "pale energy",
        "flickering energy",
        "bright energy",
        "glowing energy",
        "sparkling energy",
        "gleaming energy",
        "vibrant energy",
        "lustrous energy",
        "elder energy",
        "brilliant energy",
        "radiant energy",
        "luminous energy",
        "incandescent energy"
    }

    def __init__(self, name: str, amount: int, price: int = 0):
        self.name = get_item_name(name)
        self.price = price
        self.required_items: list[Item] = []
        self.amount = int(amount)
        self.output_quantity = 1
        if self.name in self.BASE_MATERIALS:
            self.url = None
            self.raw_required_items = []
        else:
            self.url = get_url(self.name)
            raw, out_q, is_herb, page_title = get_recipe_data(request_page(self.url), self.name)
            self.raw_required_items = raw
            self.output_quantity = out_q

            # Prefer 3-dose Herblore recipes when the wiki defaults to 4-dose pages
            if is_herb and self.output_quantity == 4:
                alt_candidates = []
                # If the page title explicitly contains (4), try (3)
                if '(4)' in page_title:
                    alt_candidates.append(page_title.replace('(4)', '(3)'))
                # Also try appending a (3) dose variant to the normalized name
                alt_candidates.append(f"{self.name} (3)")

                for alt in alt_candidates:
                    alt_url = get_url(alt)
                    alt_raw, alt_out_q, _, _ = get_recipe_data(request_page(alt_url), alt)
                    if alt_raw:
                        self.raw_required_items = alt_raw
                        self.output_quantity = alt_out_q
                        break

    def __eq__(self, other):
        return isinstance(other, Item) and self.name == other.name and self.amount == other.amount

    def __hash__(self):
        return hash((self.name, self.amount))

    def __repr__(self):
        return f"Item(name={self.name!r}, amount={self.amount}, output_quantity={self.output_quantity})"

    def add_required_items(self, item: str | "Item", amount: int, path=None) -> None:
        if path is None:
            path = []
        if self.raw_required_items == []:
            return

        if isinstance(item, Item):
            normalized_item = item.name
            new_item = Item(item.name, amount)
        else:
            normalized_item = get_item_name(item)
            new_item = Item(item, amount)

        if normalized_item in path:
            return

        self.required_items.append(new_item)
        if new_item.name in self.BASE_MATERIALS:
            return

        child_path = path + [self.name]
        for needed_item in new_item.raw_required_items:
            new_item.add_required_items(needed_item[0], needed_item[1], child_path)

    def total_item_count(self, counts=None, multiplier=None, path=None) -> dict[str, int]:
        if counts is None:
            counts = {}
        if multiplier is None:
            multiplier = self.amount
        if path is None:
            path = []
        if self.name in path:
            return counts

        output_q = self.output_quantity or 1
        batch_count = math.ceil(multiplier / output_q)
        next_path = path + [self.name]

        for item in self.required_items:
            required_amount = item.amount * batch_count
            if item.raw_required_items == []:
                counts[item.name] = counts.get(item.name, 0) + required_amount
            else:
                item.total_item_count(counts, required_amount, next_path)
        return counts

    def intermediate_counts(self, counts=None, multiplier=None, path=None) -> dict[str, int]:
        if counts is None:
            counts = {}
        if multiplier is None:
            multiplier = self.amount
        if path is None:
            path = []
        if self.name in path:
            return counts

        output_q = self.output_quantity or 1
        batch_count = math.ceil(multiplier / output_q)
        next_path = path + [self.name]

        for item in self.required_items:
            required_amount = item.amount * batch_count
            if item.raw_required_items:
                counts[item.name] = counts.get(item.name, 0) + required_amount
                item.intermediate_counts(counts, required_amount, next_path)
        return counts
