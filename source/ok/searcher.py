	def search_all_st(self):
		logins = ['evola','ilia','nastya','valya']
		if self.login(accounts[random.choice(logins)]) != 'Error':
			self.search_all_genders(location='Стаханов')
		print("Поиск по Стаханову завершен...")
		self.end_work()

	def search_all_locations(self, location=None):
		for account in accounts:
			for location in accounts[account]['locations']:
				if location != 'Стаханов':
					if self.login(accounts[account]) != 'Error':
						self.search_all_genders(location=location)
						print("Поиск {} в {} завершен...".format(accounts[account], location))
		print("Поиск всех локаций завершен...")
		self.end_work()

	def search_all_ok(self, location=None):
		logins = ['evola', 'alex', 'olga', 'natali', 'ilia', 'nastya', 'valya']
		if self.login(accounts[random.choice(logins)]) != 'Error':
			self.search_all_genders(location=None)
			self.end_work()
		print("Поиск по Одноклассникам завершен...")
		self.end_work()

	def search_f(self, location=None):
		for online in [True, False]:
			for single in [True, False]:
				self.search(gender='f', location=location, online=online, single=single)

	def search_m(self, location=None):
		for online in [True, False]:
			self.search(gender='m', location=location, online=online)

	def search_all_genders(self, location=None):
		self.search_f(location)
		self.search_m(location)

	def search_all_offline(self, location=None):
		if self.login(accounts[random.choice(logins)]) != 'Error':
			self.search(gender='f', location=location, online=False)
			self.search(gender='m', location=location, online=False)
		self.end_work()

	def search_lera(self):
		browser.search(gender='f', location='Украина', online=False, age_min='40', age_max='40')
		self.end_work()

def start_search():
	browser = OkBrowser()
	browser.search_all_st()

	browser = OkBrowser()
	browser.search_all_locations()

	browser = OkBrowser()
	browser.search_all_ok()#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!