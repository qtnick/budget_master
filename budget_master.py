import sqlite3
import datetime
from prettytable import from_db_cursor
from os.path import exists as file_exists

conn = sqlite3.connect('expenses.db')

c = conn.cursor()

prompt = ("What would you like to do?\n1 - add expense\n"
		"2 - remove expense\n3 - edit expense\n"
		"4 - search for expense\n5 - list expenses\n"
)
message = ""

expenses = []


def create_database():
	c.execute("""CREATE TABLE expenses (
		seller text,
		type text,
		price integer,
		transaction_date text
		)""")


def add_expense(seller, expense_type, price, transaction_date):
	new_id = len(expenses) + 1
	with conn:
		c.execute("""INSERT INTO expenses VALUES
			(:seller, :expense_type, :price, :transaction_date)""", 
			{'seller': seller, 'expense_type': expense_type, 'price': price, 'transaction_date': transaction_date})
	new_expense = {'id': new_id, seller: price}
	expenses.append(new_expense)


def remove_expense(rowid):
	with conn:
		c.execute("DELETE from expenses WHERE rowid=:rowid", {'rowid': rowid})


def edit_expense(rowid):
	answer = input("Which column would you like to edit? ")
	
	if answer == "seller":
		new_seller = input("Enter new seller: ")
		with conn:
			c.execute("UPDATE expenses SET seller=:seller WHERE rowid=:rowid", {'seller': new_seller, 'rowid': rowid})
	elif answer == "expense_type":
		new_type == input("Enter new expense type: ")
		with conn:
			c.execute("UPDATE expenses SET expense_type=:expense_type WHERE rowid=:rowid", {'expense_type': new_type, 'rowid': rowid})
	elif answer == "price":
		new_price = input("Enter new price: ")
		with conn:
			c.execute("UPDATE expenses SET price=:price WHERE rowid=:rowid", {'price': new_price, 'rowid': rowid})
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
	if not file_exists('expenses.db'):
		create_database()
	message = input(prompt)

	if message == "quit":
		active = False
		conn.close()
	elif str(message) == '1':
		seller = input('Name the seller: ')
		expense_type = input('Name the type of expense: ')
		price = input('Name the price: ')
		transaction_date = None
		while True:
			input_date = input('Enter the date of trasaction (yyyy-mm-dd): ')
			try:
				is_valid_date(input_date)
			except ValueError:
				print("This is not a properly formatted date.")
				continue
			else:
				transaction_date = input_date
				break
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
