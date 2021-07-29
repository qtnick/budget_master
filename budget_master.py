import sqlite3
import datetime
from prettytable import from_db_cursor
from os.path import exists as file_exists

conn = sqlite3.connect('expenses.db')

c = conn.cursor()

prompt = ("What would you like to do?\n1 - add expense\n"
		"2 - remove expense\n3 - search for expense\n"
		"4 - list expenses\n"
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
	# c.execute("""SELECT tableName FROM sqlite_master WHERE type='table'
	# 		AND tableName='expenses';""").fetchall()


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


def search_expenses(seller):
	c.execute("SELECT rowid, * FROM expenses WHERE seller=:seller", {'seller': seller})
	print(c.fetchall())

def list_expenses():
	c.execute("SELECT * FROM expenses")
	mytable = from_db_cursor(c)
	result = c.fetchall()
	print(mytable)
	for row in result:
		print(row, '\n')

	# for expense in expenses:
	# 	for key, value in expense.items():
	# 		print(f'{key}: {value}')

def is_valid_date(input_date):
	# day, month, year = input_date.split('-')

	# isValidDate = True
	# try:
		datetime.datetime.strptime(input_date, '%d-%m-%Y')
	# except ValueError:
	# 	isValidDate = False

	# return isValidDate


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
			input_date = input('Enter the date of trasaction (dd-mm-yyyy): ')
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
		seller = input("Enter seller name: ")
		search_expenses(seller)
	elif str(message) == '4':
		list_expenses()
