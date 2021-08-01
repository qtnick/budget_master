import sqlite3
import datetime
from prettytable import from_db_cursor
from os.path import exists as file_exists

conn = sqlite3.connect('expenses.db')

c = conn.cursor()

prompt = ("What would you like to do?\n1 - add expense\n"
		"2 - remove expense\n3 - edit expense\n"
		"4 - search for expense\n5 - list expenses\n"
		"6 - sort expenses\n"
)
message = ""

expenses = []


def create_database():
	c.execute("""CREATE TABLE if not exists expenses (
		seller text,
		type text,
		price integer,
		currency text,
		transaction_date text
		)""")


def add_expense(seller, expense_type, price, transaction_date, currency="PLN"):
	new_id = len(expenses) + 1
	with conn:
		c.execute("""INSERT INTO expenses VALUES
			(:seller, :expense_type, :price, :currency, :transaction_date)""", 
			{'seller': seller, 'expense_type': expense_type, 'price': price, 'currency': currency, 'transaction_date': transaction_date})


def remove_expense(rowid):
	with conn:
		c.execute("DELETE from expenses WHERE rowid=:rowid", {'rowid': rowid})


def edit_expense(rowid):
	answer = input("Which column would you like to edit? ")
	
	if answer == "seller":
		new_seller = input("Enter new seller: ")
		with conn:
			c.execute("UPDATE expenses SET seller=:seller WHERE rowid=:rowid", {'seller': new_seller, 'rowid': rowid})
	elif answer == "type":
		new_type = input("Enter new expense type: ")
		with conn:
			c.execute("UPDATE expenses SET type=:type WHERE rowid=:rowid", {'type': new_type, 'rowid': rowid})
	elif answer == "price":
		new_price = input("Enter new price: ")
		with conn:
			c.execute("UPDATE expenses SET price=:price WHERE rowid=:rowid", {'price': new_price, 'rowid': rowid})
	elif answer == "currency":
		new_currency = input("Enter new currency: ")
		with conn:
			c.execute("UPDATE expenses SET currency=:currency WHERE rowid=:rowid", {'currency': new_currency, 'rowid': rowid})
	elif answer == "transaction_date":
		new_date = input("Enter new date: ")
		with conn:
			c.execute("UPDATE expenses SET transaction_date=:transaction_date WHERE rowid=:rowid", {'transaction_date': new_date, 'rowid': rowid})
	else:
		print("\nWrong column name.\n")


def search_expenses(seller):
	c.execute("SELECT rowid, * FROM expenses WHERE seller=:seller", {'seller': seller})
	mytable = from_db_cursor(c)
	result = c.fetchall()
	print(mytable)


def list_expenses():
	c.execute("SELECT rowid, * FROM expenses ORDER BY transaction_date DESC")
	mytable = from_db_cursor(c)
	result = c.fetchall()
	print(mytable)
	for row in result:
		print(row, '\n')


def sort_expenses_by_seller():
	sorted_seller = input("Which seller would you like to sort by? ")
	c.execute("SELECT rowid, * FROM expenses WHERE seller=:seller", {'seller': sorted_seller})
	mytable = from_db_cursor(c)
	print(mytable)


def sort_expenses_by_type():
	sorted_type = input("Which type would you like to sort by? ")
	c.execute("SELECT rowid, * FROM expenses WHERE type=:type", {'type': sorted_type})
	mytable = from_db_cursor(c)
	print(mytable)


def is_valid_date(input_date):
	datetime.datetime.strptime(input_date, '%Y-%m-%d')


def is_valid_id(rowid):
	with conn:
		c.execute("SELECT rowid FROM expenses")
	rowids = c.fetchall()
	result = [row[0] for row in rowids]
	
	if int(rowid) in result:
		return True
	else:
		return False


active = True

while active:
	create_database()
	message = input(prompt)

	if message == "quit":
		active = False
		conn.close()
	elif str(message) == '1':
		seller = input('Enter the seller: ')
		expense_type = input('Enter the type of expense: ')
		price = input('Enter the price: ')
		default_currency = input('Default currency (PLN) (y/n): ')
		if default_currency == 'y':
			currency = None
		elif default_currency == 'n':
			currency = input('Enter the currency: ')
		transaction_date = None
		while True:
			default_date = input('Default date (today) (y/n): ')
			if default_date == 'y':
				input_date = str(datetime.date.today())
			elif default_date == 'n':
				input_date = input('Enter the date of trasaction (yyyy-mm-dd): ')
			try:
				is_valid_date(input_date)
			except ValueError:
				print("This is not a properly formatted date.")
				continue
			else:
				transaction_date = input_date
				break
		if currency:
			add_expense(seller, expense_type, price, transaction_date, currency)
		else:
			add_expense(seller, expense_type, price, transaction_date)
	elif str(message) == '2':
		expense_id = input("Which item would you like to delete? ")
		remove_expense(expense_id)
	elif str(message) == '3':
		expense_id = input("Which item expense would you like to edit? ")
		if is_valid_id(expense_id):
			edit_expense(expense_id)
		else:
			print("\nThere is no such item.\n")
	elif str(message) == '4':
		seller = input("Enter seller name: ")
		search_expenses(seller)
	elif str(message) == '5':
		list_expenses()
	elif str(message) == '6':
		sort_by = input('Would you like to sort expenses by seller or type? ')
		if sort_by == 'seller':
			sort_expenses_by_seller()
		elif sort_by == 'type':
			sort_expenses_by_type()
