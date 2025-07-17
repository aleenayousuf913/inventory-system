import csv
from datetime import datetime, timedelta
import random

ingredients = [
    "Italian Bread", "Turkey Breast", "Lettuce", "Tomato", "Provolone Cheese",
    "Mayonnaise", "Pickles", "Black Forest Ham", "Red Onions", "Black Olives",
    "Green Peppers", "Cucumbers", "Spinach", "Bacon", "Avocado",
    "Yellow Mustard", "Salt", "Black Pepper", "Ranch Dressing"
]

def generate_deliveries_csv(filename, num_entries=25):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['ingredient', 'quantity', 'delivery_date', 'expiration_date'])

        today = datetime.now()
        for _ in range(num_entries):
            ingredient = random.choice(ingredients)
            # Smaller deliveries to allow low stock
            if ingredient == "Italian Bread":
                quantity = random.randint(50, 150)
            elif ingredient in ["Salt", "Black Pepper", "Yellow Mustard", "Mayonnaise", "Ranch Dressing"]:
                quantity = random.randint(3, 10)
            else:
                quantity = random.randint(40, 150)

            delivery_date = today - timedelta(days=random.randint(0, 5))
            expiration_date = delivery_date + timedelta(days=random.randint(3, 15))
            writer.writerow([
                ingredient,
                quantity,
                delivery_date.strftime("%Y-%m-%d"),
                expiration_date.strftime("%Y-%m-%d"),
            ])

def generate_sales_csv(filename, num_entries=20):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['ingredient', 'quantity'])

        today = datetime.now()
        for _ in range(num_entries):
            ingredient = random.choice(ingredients)
            # Sales can sometimes exceed deliveries to force low stock
            if ingredient == "Italian Bread":
                quantity = random.randint(70, 180)
            elif ingredient in ["Salt", "Black Pepper", "Yellow Mustard", "Mayonnaise", "Ranch Dressing"]:
                quantity = random.randint(2, 8)
            else:
                quantity = random.randint(30, 160)
            writer.writerow([ingredient, quantity])

if __name__ == "__main__":
    generate_deliveries_csv('deliveries.csv')
    generate_sales_csv('sales.csv')
    print("Updated sample deliveries.csv and sales.csv generated with low stock cases.")
