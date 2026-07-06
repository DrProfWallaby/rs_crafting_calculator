import unittest
from api_query import get_item_name
from item import Item

class TestItem(unittest.TestCase):
    def test_add_required_items(self):
        item = Item("Cooked meat", 221)
        item_raw = Item("Raw beef", 904)
        item.add_required_items(item_raw, 1)
        self.assertListEqual(item.required_items, [item_raw])

    def test_add_required_items_accepts_duplicates(self):
        item = Item("Cooked meat", 221)
        item_raw = Item("Raw beef", 904)
        item.add_required_items(item_raw, 1)
        item.add_required_items(item_raw, 1)
        self.assertEqual(len(item.required_items), 2)

    def test_total_item_count_scales_by_output_quantity(self):
        recipe = Item("Cooked meat", 1)
        ingredient = Item("Vial", 2)
        recipe.required_items = [ingredient]
        recipe.output_quantity = 100

        counts = recipe.total_item_count(multiplier=100)
        self.assertEqual(counts.get("vial"), 2)

        counts = recipe.total_item_count(multiplier=101)
        self.assertEqual(counts.get("vial"), 4)

    def test_total_item_count_returns_integers(self):
        recipe = Item("Cooked meat", 1)
        ingredient = Item("Vial", 2)
        recipe.required_items = [ingredient]
        recipe.output_quantity = 2

        counts = recipe.total_item_count(multiplier=3)
        self.assertEqual(counts.get("vial"), 4)
        self.assertIsInstance(counts.get("vial"), int)

    def test_necromancy_rituals_are_ignored(self):
        ritual = Item("Lesser necroplasm", 1)
        self.assertEqual(ritual.raw_required_items, [])

    def test_get_item_name_normalizes_plus_suffix(self):
        self.assertEqual(get_item_name("Mithril platebody + 2"), "mithril platebody +2")
        self.assertEqual(get_item_name("Mithril platebody +2"), "mithril platebody +2")

    def test_get_item_name_normalizes_plus_suffix(self):
        self.assertEqual(get_item_name("Mithril platebody + 2"), "mithril platebody +2")
        self.assertEqual(get_item_name("Mithril platebody +2"), "mithril platebody +2")
