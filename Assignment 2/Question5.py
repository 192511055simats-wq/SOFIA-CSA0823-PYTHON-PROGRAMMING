# Canteen Order System
# Buggy function: uses a mutable default list
def add_item_buggy(item, order=[]):
    order.append(item)
    return order
# Correct function
def add_item(item, order=None):
    if order is None:
        order = []
    order.append(item)
    return order
# Function to calculate total and GST
def calculate_bill(amount, gst_rate=5):
    gst = amount * gst_rate / 100
    total = amount + gst
    return total, gst
# Local and global scope
canteen_name = "ABC Canteen"
def display_canteen():
    local_message = "Welcome!"
    print(local_message)
    print(canteen_name)
# Nonlocal scope
def customer_counter():
    count = 0
    def increase():
        nonlocal count
        count += 1
        print("Customer count:", count)
    increase()
    increase()
# Test buggy function
print("--- Buggy Function ---")
print(add_item_buggy("Tea"))
print(add_item_buggy("Vada"))
print("Default values:", add_item_buggy.__defaults__)
# Test corrected function
print("\n--- Correct Function ---")
customer1 = add_item("Tea")
customer1 = add_item("Sandwich", customer1)
customer2 = add_item("Coffee")
customer2 = add_item("Burger", customer2)
customer3 = add_item("Juice")
print("Customer 1:", customer1)
print("Customer 2:", customer2)
print("Customer 3:", customer3)
# Calculate bill
print("\n--- Bill Calculation ---")
total, gst = calculate_bill(200)
print("GST:", gst)
print("Total Amount:", total)
# Scope demonstration
print("\n--- Scope Demonstration ---")
display_canteen()
customer_counter()
# Explicit global modification
count = 0
def update_count():
    global count
    count += 1
update_count()
print("Global count:", count)