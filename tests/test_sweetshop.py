import unittest
from app.sweet import Sweet

class TestSweet(unittest.TestCase):

    def test_sweet_creation(self):
        sweet = Sweet(1001, "Kaju Katli", "Nut-Based", 50, 20)
        self.assertEqual(sweet.sweet_id, 1001)
        self.assertEqual(sweet.name, "Kaju Katli")
        self.assertEqual(sweet.category, "Nut-Based")
        self.assertEqual(sweet.price, 50)
        self.assertEqual(sweet.quantity, 20)

if __name__ == '__main__':
    unittest.main()

from app.sweetshop import SweetShop

class TestSweetShop(unittest.TestCase):

    def setUp(self):
        self.shop = SweetShop()

    def test_add_sweet(self):
        sweet = Sweet(1001, "Kaju Katli", "Nut-Based", 50, 20)
        self.shop.add_sweet(sweet)
        self.assertEqual(len(self.shop.sweets), 1)
        self.assertEqual(self.shop.sweets[0].name, "Kaju Katli")

    def test_add_duplicate_id(self):
        sweet1 = Sweet(1001, "Kaju Katli", "Nut-Based", 50, 20)
        sweet2 = Sweet(1001, "Gulab Jamun", "Milk-Based", 40, 10)
        self.shop.add_sweet(sweet1)
        with self.assertRaises(ValueError):
            self.shop.add_sweet(sweet2)

    def test_view_sweets(self):
        sweet1 = Sweet(1001, "Kaju Katli", "Nut-Based", 50, 20)
        sweet2 = Sweet(1002, "Gulab Jamun", "Milk-Based", 40, 10)
        self.shop.add_sweet(sweet1)
        self.shop.add_sweet(sweet2)
        sweets = self.shop.view_sweets()
        self.assertEqual(len(sweets), 2)
        self.assertIn(sweet1, sweets)
        self.assertIn(sweet2, sweets)

    def test_delete_sweet(self):
        sweet1 = Sweet(1001, "Kaju Katli", "Nut-Based", 50, 20)
        sweet2 = Sweet(1002, "Gulab Jamun", "Milk-Based", 40, 10)
        self.shop.add_sweet(sweet1)
        self.shop.add_sweet(sweet2)
        self.shop.delete_sweet(1001)
        self.assertEqual(len(self.shop.sweets), 1)
        self.assertEqual(self.shop.sweets[0].sweet_id, 1002)

    def test_delete_nonexistent_sweet(self):
        with self.assertRaises(ValueError):
            self.shop.delete_sweet(9999)

    def test_search_by_name(self):
        sweet1 = Sweet(1001, "Kaju Katli", "Nut-Based", 50, 20)
        sweet2 = Sweet(1002, "Gulab Jamun", "Milk-Based", 40, 10)
        self.shop.add_sweet(sweet1)
        self.shop.add_sweet(sweet2)
        results = self.shop.search_sweets(name="kaju")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "Kaju Katli")

    def test_search_by_category(self):
        sweet1 = Sweet(1001, "Kaju Katli", "Nut-Based", 50, 20)
        sweet2 = Sweet(1002, "Gulab Jamun", "Milk-Based", 40, 10)
        self.shop.add_sweet(sweet1)
        self.shop.add_sweet(sweet2)
        results = self.shop.search_sweets(category="Milk-Based")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "Gulab Jamun")

    def test_search_by_price_range(self):
        sweet1 = Sweet(1001, "Kaju Katli", "Nut-Based", 50, 20)
        sweet2 = Sweet(1002, "Gulab Jamun", "Milk-Based", 10, 10)
        sweet3 = Sweet(1003, "Rasgulla", "Milk-Based", 25, 10)
        self.shop.add_sweet(sweet1)
        self.shop.add_sweet(sweet2)
        self.shop.add_sweet(sweet3)
        results = self.shop.search_sweets(price_min=10, price_max=30)
        self.assertEqual(len(results), 2)
        names = [s.name for s in results]
        self.assertIn("Gulab Jamun", names)
        self.assertIn("Rasgulla", names)

def test_purchase_sweet(self):
    sweet = Sweet(1001, "Kaju Katli", "Nut-Based", 50, 20)
    self.shop.add_sweet(sweet)
    self.shop.purchase_sweet(1001, 5)
    self.assertEqual(sweet.quantity, 15)

def test_purchase_more_than_stock(self):
    sweet = Sweet(1001, "Kaju Katli", "Nut-Based", 50, 3)
    self.shop.add_sweet(sweet)
    with self.assertRaises(ValueError):
        self.shop.purchase_sweet(1001, 5)

def test_purchase_nonexistent_sweet(self):
    with self.assertRaises(ValueError):
        self.shop.purchase_sweet(9999, 1)

def test_restock_sweet(self):
    sweet = Sweet(1002, "Gulab Jamun", "Milk-Based", 10, 10)
    self.shop.add_sweet(sweet)
    self.shop.restock_sweet(1002, 5)
    self.assertEqual(sweet.quantity, 15)

def test_restock_nonexistent_sweet(self):
    with self.assertRaises(ValueError):
        self.shop.restock_sweet(9999, 10)
