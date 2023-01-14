from kivy.metrics import dp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.screen import MDScreen
from random import randint
import sqlite3


class MyDatabase:
	# SQLite3
	def build(self):
		# Create Database Or Connect To One
		conn = sqlite3.connect('first_db.db')

		# Create A Cursor
		c = conn.cursor()

		# Create A Table
		c.execute("""CREATE TABLE if not exists customers(
			product text,
			quantity int(100), 
			order_number text)
		 """)

		# Commit our changes
		conn.commit()

		# Close our connection
		conn.close()

	
	def submit(self, product_name, quantity):
		# Create Database Or Connect To One
		conn = sqlite3.connect('first_db.db')

		# Create A Cursor
		c = conn.cursor()

		# Add values
		order_number = 'R'
		for i in range(4):
			order_number += str(randint(0, 9))

		# Add A Record
		values = (product_name, quantity, order_number)
		c.execute("INSERT INTO customers VALUES (:first, :second, :third)",
			{
				'first': product_name,
				'second': quantity,
				'third': order_number,
			})

		# Commit our changes
		conn.commit()

		# Close our connection
		conn.close()
		
	def show_records(self):
		# Create Database Or Connect To One
		conn = sqlite3.connect('first_db.db')

		# Create A Cursor
		c = conn.cursor()

		# Grab records from database
		c.execute("SELECT * FROM customers")
		records = c.fetchall()

		word = ''
		# Loop thru records
		for record in records:
			word = f'{word}\n{record}'

		# Commit our changes
		conn.commit()

		# Close our connection
		conn.close()
		return word

	def delete_records(self):
		# Create Database Or Connect To One
		conn = sqlite3.connect('first_db.db')

		# Create A Cursor
		c = conn.cursor()

		# Grab records from database
		c.execute("DELETE FROM customers")

		# Commit our changes
		conn.commit()

		# Close our connection
		conn.close()