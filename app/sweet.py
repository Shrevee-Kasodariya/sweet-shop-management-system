class Sweet:
    def __init__(self, sweet_id, name, category, price, quantity):
        self.sweet_id = sweet_id
        self.name = name
        self.category = category
        self.price = price
        self.quantity = quantity

    def __repr__(self):
        return f"{self.name} ({self.category}) - ₹{self.price} [{self.quantity} left]"

    def to_dict(self):
        return {
            'sweet_id': self.sweet_id,
            'name': self.name,
            'category': self.category,
            'price': self.price,
            'quantity': self.quantity
        }
