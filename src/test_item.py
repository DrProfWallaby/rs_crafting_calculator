import unittest
from item import Item

class TestItem(unittest.TestCase):
    def test_add_required_items(self):
        item = Item("Cooked meat", 221)
        item_raw = Item("Raw beef", 904)
        item.add_required_items(item_raw, 1)
        self.assertListEqual(item.required_items, [(item_raw, 1)])
    
    def test_add_required_items_duplicate(self):
        item = Item("Cooked meat", 221)
        item_raw = Item("Raw beef", 904)
        item.add_required_items(item_raw, 1)
        with self.assertRaises(Exception):
            item.add_required_items(item_raw, 1)