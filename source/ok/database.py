import sqlite3

class OkDatabase:
	def __init__(self):
		self.__path		  = "data/ok.db"
		self.__connection = sqlite3.connect(self.__path)
		self.__cursor	  = self.__connection.cursor()

	def __db_create(self):
		self.__cursor.execute("CREATE TABLE IF NOT EXISTS users (url TEXT UNIQUE, name TEXT, photo TEXT, action_like TEXT, action_friend TEXT, action_group TEXT, location TEXT, interests TEXT, gender TEXT, single TEXT, age INT)")
		self.__connection.commit()

	def profile_exist(self, url):
		self.__cursor.execute("SELECT * FROM users WHERE url=?", [url])
		result = self.__cursor.fetchone()
		if result == None:
			return result
		elif result[5] != 'ok':
			return False
		else:
			return True

	def insert_user(self,
			user_url,
			user_name=None,
			user_photo=None,
			action_like=None,
			action_friend=None,
			action_group=None,
			location=None,
			interests=None,
			gender=None,
			single=None,
			age=None):

		if single == True:
			single = 'single'

		if action_like == None:
			action_like = 'unknown'
		if action_friend == None:
			action_friend = 'unknown'
		if action_group == None:
			action_group = 'unknown'

		user = [
			user_url,
			user_name,
			user_photo,
			action_like,
			action_friend,
			action_group,
			location,
			interests,
			gender,
			single,
			age
		]

		query = "INSERT OR IGNORE INTO users (url, name, photo, action_like, action_friend, action_group, location, interests, gender, single, age) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
		try:
			self.__cursor.execute(query, user)
			self.__connection.commit()
		except sqlite3.IntegrityError as e:
			print('sqlite error: ', e.args[0])
			return 'Error'
		return None

	def execute_custom_query(self, query):
		try:
			self.__cursor.execute(query)
			self.__connection.commit()
		except sqlite3.IntegrityError as e:
			print('sqlite error: ', e.args[0])
			return 'Error'

	def execute_custom_query_select(self, query):
		try:
			self.__cursor.execute(query)
			return self.__cursor.fetchall()
		except sqlite3.IntegrityError as e:
			print('sqlite error: ', e.args[0])
			return 'Error'

	def db_close(self):
		self.__cursor.close()