import sqlite3
import json
from config import *

class DB():

	def __init__(self):
		self.dbpath = DBPATH
		with sqlite3.connect(self.dbpath) as con:
			cur = con.cursor()
			# Create table
			cur.execute('''CREATE TABLE IF NOT EXISTS dictionary
                  		(key TEXT PRIMARY KEY, value TEXT)''')
				
	
	# Convert dictionary to JSON for storage
	def dict_to_json(self, dictionary):
		return json.dumps(dictionary)

	# Convert JSON back to dictionary
	def json_to_dict(self, json_str):
		return json.loads(json_str)
	
	# Function to save/update a dictionary
	def save_or_update_dict(self, dictionary, key):
		existing_dict = self.load_dict(key)
		existing_dict.update(dictionary)  # Update with new data
		json_data = self.dict_to_json(existing_dict)
		with sqlite3.connect(self.dbpath) as con:
			cur = con.cursor()
			cur.execute("INSERT OR REPLACE INTO dictionary (key, value) VALUES (?, ?)", (key, json_data))

	# Function to load a dictionary
	def load_dict(self, key):
		with sqlite3.connect(self.dbpath) as con:
			cur = con.cursor()
			cur.execute("SELECT value FROM dictionary WHERE key=?", (key,))
			data = cur.fetchone()
			if data:
				return self.json_to_dict(data[0])
			return {}


sqlitedb = DB()
