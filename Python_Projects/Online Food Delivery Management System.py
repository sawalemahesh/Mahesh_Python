import uuid
import json
import os


# -------------------- MODELS --------------------

class Restaurant:
    def __init__(self, restaurant_id, name, menu, is_open=True):
        self.restaurant_id = restaurant_id
        self.name = name
        self.menu = menu
        self.is_open = is_open


class Customer:
    def __init__(self, customer_id, name, wallet_balance):
        self.customer_id = customer_id
        self.name = name
        self.wallet_balance = wallet_balance
        self.order_history = []


class Order:
    def __init__(self, order_id, customer_id, restaurant_id, items_ordered, total_amount):
        self.order_id = order_id
        self.customer_id = customer_id
        self.restaurant_id = restaurant_id
        self.items_ordered = items_ordered
        self.total_amount = total_amount
        self.order_status = "PLACED"


# -------------------- MAIN SYSTEM --------------------

class FoodDeliverySystem:
    def __init__(self):
        self.restaurants = {}
        self.customers = {}
        self.orders = {}
        self.load_orders_from_file()

    # ---------- Restaurant ----------
    def add_restaurant(self, restaurant_id, name, menu):
        if restaurant_id in self.restaurants:
            raise ValueError("Restaurant ID already exists")
        self.restaurants[restaurant_id] = Restaurant(restaurant_id, name, menu)

    # ---------- Customer ----------
    def register_customer(self, customer_id, name, wallet_balance):
        if customer_id in self.customers:
            raise ValueError("Customer ID already exists")
        self.customers[customer_id] = Customer(customer_id, name, wallet_balance)

    # ---------- Order ----------
    def place_order(self, customer_id, restaurant_id, items_ordered):
        if customer_id not in self.customers:
            raise ValueError("Customer not found")

        if restaurant_id not in self.restaurants:
            raise ValueError("Restaurant not found")

        restaurant = self.restaurants[restaurant_id]
        customer = self.customers[customer_id]

        if not restaurant.is_open:
            raise ValueError("Restaurant is closed")

        total_amount = 0
        for item, qty in items_ordered.items():
            if item not in restaurant.menu:
                raise ValueError(f"{item} not available in menu")
            total_amount += restaurant.menu[item] * qty

        if customer.wallet_balance < total_amount:
            raise ValueError("Insufficient wallet balance")

        customer.wallet_balance -= total_amount

        order_id = str(uuid.uuid4())[:8]
        order = Order(order_id, customer_id, restaurant_id, items_ordered, total_amount)
        self.orders[order_id] = order
        customer.order_history.append(order_id)

        self.save_orders_to_file()
        return order_id

    # ---------- Cancel Order ----------
    def cancel_order(self, order_id):
        if order_id not in self.orders:
            raise ValueError("Order not found")

        order = self.orders[order_id]

        if order.order_status != "PLACED":
            raise ValueError("Only placed orders can be cancelled")

        customer = self.customers[order.customer_id]
        customer.wallet_balance += order.total_amount
        order.order_status = "CANCELLED"

        self.save_orders_to_file()

    # ---------- Deliver Order ----------
    def deliver_order(self, order_id):
        if order_id not in self.orders:
            raise ValueError("Order not found")

        order = self.orders[order_id]

        if order.order_status != "PLACED":
            raise ValueError("Only placed orders can be delivered")

        order.order_status = "DELIVERED"
        self.save_orders_to_file()

    # ---------- Reports ----------
    def restaurant_revenue(self, restaurant_id):
        revenue = 0
        for order in self.orders.values():
            if order.restaurant_id == restaurant_id and order.order_status == "DELIVERED":
                revenue += order.total_amount
        return revenue

    def customer_orders(self, customer_id):
        if customer_id not in self.customers:
            raise ValueError("Customer not found")
        return self.customers[customer_id].order_history

    def top_selling_items(self):
        item_count = {}
        for order in self.orders.values():
            if order.order_status == "DELIVERED":
                for item, qty in order.items_ordered.items():
                    item_count[item] = item_count.get(item, 0) + qty
        return sorted(item_count.items(), key=lambda x: x[1], reverse=True)

    def low_wallet_customers(self, threshold):
        return [
            customer.name
            for customer in self.customers.values()
            if customer.wallet_balance < threshold
        ]

    # ---------- File Handling ----------
    def save_orders_to_file(self):
        data = {}
        for oid, order in self.orders.items():
            data[oid] = {
                "customer_id": order.customer_id,
                "restaurant_id": order.restaurant_id,
                "items_ordered": order.items_ordered,
                "total_amount": order.total_amount,
                "order_status": order.order_status
            }
        with open("../orders.txt", "w") as file:
            json.dump(data, file)

    def load_orders_from_file(self):
        if not os.path.exists("../orders.txt"):
            return
        with open("../orders.txt", "r") as file:
            data = json.load(file)
            for oid, o in data.items():
                order = Order(
                    oid,
                    o["customer_id"],
                    o["restaurant_id"],
                    o["items_ordered"],
                    o["total_amount"]
                )
                order.order_status = o["order_status"]
                self.orders[oid] = order


# -------------------- DEMO USAGE --------------------

if __name__ == "__main__":
    system = FoodDeliverySystem()

    system.add_restaurant(
        "R1",
        "Food Plaza",
        {"Burger": 120, "Pizza": 250, "Pasta": 200}
    )

    system.register_customer("C1", "Rahul", 1000)

    order_id = system.place_order(
        "C1",
        "R1",
        {"Burger": 2, "Pizza": 1}
    )

    system.deliver_order(order_id)

    print("Restaurant Revenue:", system.restaurant_revenue("R1"))
    print("Customer Orders:", system.customer_orders("C1"))
    print("Top Selling Items:", system.top_selling_items())
    print("Low Wallet Customers:", system.low_wallet_customers(500))
