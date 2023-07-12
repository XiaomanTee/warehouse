class Warehouse:
    def __init__(self):
        self.balance = 0.0
        self.inventory = {}
        self.history = []

    def review(self):
        from_indices = input("Enter 'From' index (Empty for the beginning): ")
        to_indices = input("Enter 'To' index (Empty for the beginning): ")

        if from_indices == "":
            from_indices = 0
        else:
            from_indices = int(from_indices)

        if to_indices == "":
            to_indices = len(self.history)
        else:
            to_indices = int(to_indices)

        if from_indices < 0 or from_indices > to_indices or to_indices > len(self.history):
            print(f"Error: Invalid range! Please enter between From: 0; To: {len(self.history)}")
        else:
            print(f"Recorded operations (From {from_indices} to {to_indices}): ")
            for review in range(from_indices, to_indices):
                print(self.history[review])


class Purchase:
    def __init__(self):
        self.product_name = ""
        self.product_price = 0.0
        self.product_quantity = 0

    def user_input(self):
        self.product_name = input("Enter the name of the product: ")
        self.product_price = float(input("Enter the price of the product: "))
        self.product_quantity = int(input("Enter the quantity of the product: "))

    def run(self, warehouse):
        if self.product_quantity < 1 or self.product_price <= 0:
            print("Invalid input")
            return

        if warehouse.balance < self.product_price * self.product_quantity:
            print("Purchase error: Insufficient balance!")
        else:
            warehouse.balance -= self.product_price * self.product_quantity

        if self.product_name in warehouse.inventory:
            if warehouse.inventory[self.product_name]['price'] == self.product_price:
                warehouse.inventory[self.product_name]['quantity'] += self.product_quantity
            elif warehouse.inventory[self.product_name]['quantity'] == 0:
                warehouse.inventory[self.product_name].update(
                    {"price": self.product_price, "quantity": self.product_quantity})
        else:
            warehouse.inventory[self.product_name] = {"price": self.product_price, "quantity": self.product_quantity}

        warehouse.history.append(self)

    def print_output(self, warehouse):
        print(
            f"Purchased {self.product_quantity} of {self.product_name} with {self.product_quantity * self.product_price}. Balance: {warehouse.balance}")


class Sales:
    def __init__(self):
        self.product_name = ""
        self.product_price = 0.0
        self.product_quantity = 0

    def user_input(self):
        self.product_name = input("Enter the name of the product: ")
        self.product_price = float(input("Enter the price of the product: "))
        self.product_quantity = int(input("Enter the quantity of the product: "))

    def run(self, warehouse):
        if self.product_quantity < 1 or self.product_price <= 0:
            print("Invalid input")
            return

        if self.product_name in warehouse.inventory and warehouse.inventory[self.product_name]['quantity'] >= self.product_quantity:
            warehouse.balance += self.product_price * self.product_quantity
            warehouse.inventory[self.product_name]['quantity'] -= self.product_quantity
            warehouse.history.append(self)
        elif self.product_name not in warehouse.inventory:
            print(f"Sales error: {self.product_name} not available in warehouse.")
        else:
            print("Sales error: Not enough quantity.")

    def print_output(self, warehouse):
        print(f"Sold {self.product_quantity} of {self.product_name} with {self.product_price * self.product_quantity}. Balance: {warehouse.balance}")


def store_balance(warehouse):
    with open('balance.txt', 'w') as fd:
        fd.write(str(warehouse.balance))


def store_inventory(warehouse):
    with open('inventory.txt', 'w') as fd:
        for product, details in warehouse.inventory.items():
            price = details['price']
            quantity = details['quantity']
            fd.write(f"{product}: {price}, {quantity}\n")


def store_history(warehouse):
    with open('history.txt', 'w') as fd:
        for history in warehouse.history:
            fd.write(str(history) + '\n')


def read_balance(warehouse):
    try:
        with open('balance.txt', 'r') as fd:
            warehouse.balance = float(fd.read().strip())
    except FileNotFoundError:
        print("Balance file not found.")


def read_inventory(warehouse):
    try:
        with open('inventory.txt', 'r') as fd:
            for line in fd:
                product, price, quantity = line.strip().split(':')
                warehouse.inventory[product] = {
                    'price': float(price.strip()),
                    'quantity': int(quantity.strip())
                }
    except FileNotFoundError:
        print("Inventory file not found.")


def read_history(warehouse):
    try:
        with open('history.txt', 'r') as fd:
            for line in fd:
                if line.strip():
                    history_item = eval(line.strip())
                    if isinstance(history_item, Purchase) or isinstance(history_item, Sales):
                        warehouse.history.append(history_item)
    except FileNotFoundError:
        print("History file not found.")


if __name__ == '__main__':
    warehouse = Warehouse()

    read_balance(warehouse)
    read_inventory(warehouse)
    read_history(warehouse)

    print("Data loaded successfully!")

    while True:
        choice = input("Enter 'P' for Purchase, 'S' for Sales, 'R' for Review, or 'Q' to quit: ")

        if choice.upper() == 'P':
            purchase = Purchase()
            purchase.user_input()
            purchase.run(warehouse)
            purchase.print_output(warehouse)
        elif choice.upper() == 'S':
            sales = Sales()
            sales.user_input()
            sales.run(warehouse)
            sales.print_output(warehouse)
        elif choice.upper() == 'R':
            warehouse.review()
        elif choice.upper() == 'Q':
            store_balance(warehouse)
            store_inventory(warehouse)
            store_history(warehouse)
            print("Data saved successfully!")
            break
        else:
            print("Invalid choice. Please try again.")
