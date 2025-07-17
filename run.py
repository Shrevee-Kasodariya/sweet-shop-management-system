from app.sweet import Sweet
from app.sweetshop import SweetShop

def main():
    shop = SweetShop()

    while True:
        print("\n--- Sweet Shop Menu ---")
        print("1. Add Sweet")
        print("2. View Sweets")
        print("3. Delete Sweet")
        print("4. Search Sweets")
        print("5. Purchase Sweet")
        print("6. Restock Sweet")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            try:
                sweet_id = int(input("Enter Sweet ID: "))
                name = input("Enter Sweet Name: ")
                category = input("Enter Category (e.g., Chocolate, Nut-Based): ")
                price = float(input("Enter Price: "))
                quantity = int(input("Enter Quantity: "))
                sweet = Sweet(sweet_id, name, category, price, quantity)
                shop.add_sweet(sweet)
                print("✅ Sweet added successfully!")
            except Exception as e:
                print(f"❌ Error: {e}")

        elif choice == "2":
            sweets = shop.view_sweets()
            if not sweets:
                print("⚠️ No sweets available.")
            for s in sweets:
                print(f"- {s}")

        elif choice == "3":
            try:
                sweet_id = int(input("Enter Sweet ID to delete: "))
                shop.delete_sweet(sweet_id)
                print("🗑️ Sweet deleted.")
            except Exception as e:
                print(f"❌ Error: {e}")

        elif choice == "4":
            print("\n🔍 Search Options:")
            name = input("Search by Name (leave blank if not): ")
            category = input("Search by Category (leave blank if not): ")
            price_min = input("Minimum Price (leave blank if not): ")
            price_max = input("Maximum Price (leave blank if not): ")

            price_min = float(price_min) if price_min else None
            price_max = float(price_max) if price_max else None

            results = shop.search_sweets(
                name=name if name else None,
                category=category if category else None,
                price_min=price_min,
                price_max=price_max
            )

            if results:
                for s in results:
                    print(f"- {s}")
            else:
                print("⚠️ No sweets matched your search.")

        elif choice == "5":
            try:
                sweet_id = int(input("Enter Sweet ID to purchase: "))
                qty = int(input("Enter quantity to purchase: "))
                shop.purchase_sweet(sweet_id, qty)
                print("✅ Sweet purchased successfully!")
            except Exception as e:
                print(f"❌ Error: {e}")

        elif choice == "6":
            try:
                sweet_id = int(input("Enter Sweet ID to restock: "))
                qty = int(input("Enter quantity to add: "))
                shop.restock_sweet(sweet_id, qty)
                print("✅ Restocked successfully!")
            except Exception as e:
                print(f"❌ Error: {e}")

        elif choice == "0":
            print("👋 Exiting Sweet Shop. Bye!")
            break

        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
