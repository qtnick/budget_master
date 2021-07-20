prompt = "What would you like to do?\n1 - add expense\n2 - remove expense\n3 - list expenses\n"
message = ""

expenses = []

def add_expense(seller, price):
	new_id = len(expenses) + 1
	new_expense = {'id': new_id, seller: price}
	expenses.append(new_expense)


def remove_expense():
	expense_id = input('Enter id of the expense to delete: ')
	del expenses[int(expense_id) - 1]


def list_expenses(expenses):
	for expense in expenses:
		for key, value in expense.items():
			print(f'{key}: {value}')


while message != 'quit':
	message = input(prompt)

	if str(message) == '1':
		seller = input('Name the seller: ')
		price = input('Name the price: ')
		add_expense(seller, price)
	elif str(message) == '2':
		remove_expense()
	elif str(message) == '3':
		list_expenses(expenses)
