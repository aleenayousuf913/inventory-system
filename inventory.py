import csv
from datetime import datetime

class InventoryBatch:
    def __init__(self, quantity, delivery_date, expiration_date):
        self.quantity = quantity
        self.delivery_date = delivery_date      # datetime object
        self.expiration_date = expiration_date  # datetime object

    def __repr__(self):
        del_str = self.delivery_date.strftime("%Y-%m-%d")
        exp_str = self.expiration_date.strftime("%Y-%m-%d")
        return f"{self.quantity} units (delivered {del_str}, expires {exp_str})"

class InventoryItem:
    def __init__(self, name):
        self.name = name
        self.batches = []  # list of InventoryBatch objects

    def add_stock(self, amount, delivery_date, expiration_date):
        self.batches.append(InventoryBatch(amount, delivery_date, expiration_date))
        # Sort batches by expiration date (earliest expiry first)
        self.batches.sort(key=lambda b: b.expiration_date)

    def total_quantity(self, current_date=None):
        if not current_date:
            current_date = datetime.now()
        # Sum only non-expired batches
        return sum(batch.quantity for batch in self.batches if batch.expiration_date >= current_date)

    def expired_quantity(self, current_date=None):
        if not current_date:
            current_date = datetime.now()
        return sum(batch.quantity for batch in self.batches if batch.expiration_date < current_date)

    def remove_stock(self, amount, current_date=None):
        if not current_date:
            current_date = datetime.now()
        remaining = amount
        # Remove only from non-expired batches
        valid_batches = [b for b in self.batches if b.expiration_date >= current_date]
        for batch in valid_batches:
            if remaining <= 0:
                break
            if batch.quantity > remaining:
                batch.quantity -= remaining
                remaining = 0
            else:
                remaining -= batch.quantity
                batch.quantity = 0
        # Remove batches with zero quantity
        self.batches = [b for b in self.batches if b.quantity > 0]

    def __repr__(self):
        now = datetime.now()
        total_qty = self.total_quantity(now)
        expired_qty = self.expired_quantity(now)
        return f"{self.name}: {total_qty} units (Expired: {expired_qty}) across {len(self.batches)} batch(es)"

class InventorySystem:
    def __init__(self, low_stock_threshold=10):
        self.items = {}
        self.low_stock_threshold = low_stock_threshold

    def add_item_if_missing(self, item_name):
        if item_name not in self.items:
            self.items[item_name] = InventoryItem(item_name)

    def process_delivery_file(self, filepath):
        with open(filepath, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                item = row['ingredient']
                qty = int(row['quantity'])

                delivery_str = row['delivery_date']
                expiration_str = row['expiration_date']

                delivery_date = datetime.strptime(delivery_str, "%Y-%m-%d")
                expiration_date = datetime.strptime(expiration_str, "%Y-%m-%d")

                self.add_item_if_missing(item)
                self.items[item].add_stock(qty, delivery_date, expiration_date)

    def process_sales_file(self, filepath):
        with open(filepath, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                item = row['ingredient']
                qty = int(row['quantity'])
                self.add_item_if_missing(item)
                self.items[item].remove_stock(qty)

    def report_stock(self):
        print("Inventory Status:")
        now = datetime.now()
        for item in self.items.values():
            expired_qty = item.expired_quantity(now)
            total_qty = item.total_quantity(now)
            status = "LOW STOCK" if total_qty <= self.low_stock_threshold else "OK"
            expiry_warning = ""
            if expired_qty > 0:
                expiry_warning = f" - EXPIRED: {expired_qty} units"
            print(f" - {item} [{status}]{expiry_warning}")

    def get_low_stock_items(self):
        now = datetime.now()
        return [item for item in self.items.values() if item.total_quantity(now) <= self.low_stock_threshold]

if __name__ == "__main__":
    inventory = InventorySystem(low_stock_threshold=15)

    delivery_csv = 'deliveries.csv'  # must have delivery_date and expiration_date columns
    sales_csv = 'sales.csv'

    inventory.process_delivery_file(delivery_csv)
    inventory.process_sales_file(sales_csv)

    inventory.report_stock()

    low_stock = inventory.get_low_stock_items()
    if low_stock:
        print("\nLow stock alert:")
        for item in low_stock:
            print(f" - {item.name}: {item.total_quantity()} units left")
