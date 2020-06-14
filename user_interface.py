from pizzapy import Customer, StoreLocator, Order
from os import walk
from pathlib import Path
import math

country = "US"

def get_new_customer() -> Customer:
    """
    Collects information from console input and returns a new
    Customer object
    :return: Customer
    """
    print("\n-- PERSONAL INFORMATION --")
    print("To start an order you must provide the following details.\n")

    print("- NAME -")
    first_name = get_valid_input("Please type your FIRST NAME: ", validate_name)
    last_name = get_valid_input("Please type your LAST NAME: ", validate_name)

    print("\n- CONTACT -")
    email = get_valid_input("Please type your EMAIL address: ", validate_email)
    phone = get_valid_input("Please type your PHONE NUMBER: ", validate_phone).replace("-","").replace("(", "").replace(")", "")

    print("\n- ADDRESS -")
    print("Please type your ADDRESS using the following form.")
    print("HOUSE # Street Name, City, State/Province, ZIP/Postal Code")
    print("EXAMPLE: 700 Pennsylvania Avenue NW, Washington, DC, 20408")

    address = get_valid_input("ADDRESS: ", validate_address)

    customer = Customer(last_name, first_name, email, phone, address)
    return customer



def get_valid_input(question:str, validation_function) -> str:
    """
    Will get valid input from the user and return it.
    :param validation_function: python function object used to validate input
    """
    while True:
        inp = input(question).strip()
        if validation_function(inp): break
        else:
            print("Invalid input, please try again.")

    return inp

def validate_email(email:str) -> bool:
    """
    returns if the given email is valid
    """
    return email.count("@") == 1 and email.count(".") >= 1 and len(email) > 6

def validate_address(address:str) -> bool:
    """
    returns if an address is valid
    """
    return True

def validate_phone(phone:str) -> bool:
    """
    returns if the given phone number is valid
    """
    phone = phone.replace("-", "").replace("(", "").replace(")", "")
    return phone.isdigit() and len(phone) == 10

def validate_name(name:str) -> bool:
    """
    a name is valid if it contains no spaces,
    no special chars and is longer than one character
    """
    return name.isalpha() and name.count(" ") == 0 and len(name) >= 2

def get_credit_card():
    """
    gets a valid credit card from the user via console
    """
    print("- PAYMENT INFORMATION -")
    print("Please enter your credit card information. This information will NOT be saved.\n")
    card_number = input("Please type your CREDIT CARD NUMBER: ").strip()
    card_expiry= input("Please type the EXPIRY DATE (MM/YY): ").strip().replace("/","")
    cvv = input("Please type the 3 digit SECURITY CODE: ").strip()
    zip_code = input("Please type your ZIP/POSTAL CODE: ").strip()

    try:
        card = CreditCard(card_number, card_expiry, cvv, zip_code)
    except Exception as e:
        print("Card details INVALID, please try again. \n", e)
        return get_credit_card()

    return card

def searchMenu(menu):
	print("You are now searching the menu...")
	item = input("Type an item to look for: ").strip().lower()

	if len(item) > 1:
		item = item[0].upper() + item[1:]
		print(f"Results for: {item}\n")
		menu.search(Name = item)
		print()
	else:
		print("No Results Found")

def addToOrder(order):
	print("Please type the code of the items you'd like to order...")
	print("Press ENTER twice to stop ordering or press ENTER once if you haven't ordered anything yet.")
	while True:
		item = input("Code: ").upper()
		try:
			order.add_item(item)
		except:
			if item == "":
				break
			print("Invalid Code...")

def removeFromOrder(order):
	print("Please type the code of the items you'd like to remove...")
	print("Press ENTER twice to stop removing items or press ENTER once if you haven't removed anything yet.")
	while True:
		item = input("Code: ").upper()
		try:
			order.remove_item(item)
		except:
			if item == "":
				break
			print("Invalid Code...")

def round_down(price, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(float(price) * multiplier) / multiplier

customer = get_new_customer()

my_local_dominos = StoreLocator.find_closest_store_to_customer(customer)
print("\nClosest Store: ")
print(my_local_dominos)

ans = input("Would you like to order from this store? (Y/N)")
if ans.lower() not in ["yes", "y"]:
	print("Goodbye!")
	quit()

print("\nMENU\n")

menu = my_local_dominos.get_menu()
order = Order.begin_customer_order(customer, my_local_dominos, "us")

while True:
	searchMenu(menu)
	addToOrder(order)
	answer = input("Would you like to add more items (y/n)? ")
	if answer.lower() not in ["yes", "y"]:
		i = input("Would you like to remove an item (y/n)? ")
		if i.lower not in ["yes", "y"]:
			break
		else:
			removeFromOrder(order)


total = 0
print("\nYour order is as follows: ")
for item in order.data["Products"]:
	price = item["Price"]
	print(item["Name"] + " $" + price)
	total += round_down(price, 2)

print("\nYour order total is: $" + str(total) + " + TAX")

payment = input("\nWill you be paying with CASH or CREDIT? (CASH, CREDIT CARD)")
if payment.lower() in ["credit", "credit card"]:
	card = get_credit_card()
else:
	card = False	

ans = input("Would you like to place this order? (y/n)")
if ans.lower in ["y", "yes"]:
	order.place(card)
	my_local_dominos.place_order(order, card)
	print("Order Placed!")
else:
	print("Goodbye!")