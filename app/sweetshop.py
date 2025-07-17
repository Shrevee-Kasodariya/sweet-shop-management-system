from app.sweet import Sweet

class SweetShop:
    def __init__(self):
        self.sweets = []

    def add_sweet(self, sweet):
        # Ensure sweet_id is unique
        for existing in self.sweets:
            if existing.sweet_id == sweet.sweet_id:
                raise ValueError("Sweet ID must be unique")
        self.sweets.append(sweet)

    def view_sweets(self):
        return self.sweets

    def delete_sweet(self, sweet_id):
        for sweet in self.sweets:
            if sweet.sweet_id == sweet_id:
                self.sweets.remove(sweet)
                return
        raise ValueError("Sweet not found")

    def search_sweets(self, name=None, category=None, price_min=None, price_max=None):
        results = self.sweets
        if name:
            results = [s for s in results if name.lower() in s.name.lower()]
        if category:
            results = [s for s in results if category.lower() == s.category.lower()]
        if price_min is not None:
            results = [s for s in results if s.price >= price_min]
        if price_max is not None:
            results = [s for s in results if s.price <= price_max]
        return results

    def purchase_sweet(self, sweet_id, quantity):
        for sweet in self.sweets:
            if sweet.sweet_id == sweet_id:
                if sweet.quantity >= quantity:
                    sweet.quantity -= quantity
                    return
                else:
                    raise ValueError("Not enough stock available")
        raise ValueError("Sweet not found")

    def restock_sweet(self, sweet_id, quantity):
        for sweet in self.sweets:
            if sweet.sweet_id == sweet_id:
                sweet.quantity += quantity
                return
        raise ValueError("Sweet not found")
