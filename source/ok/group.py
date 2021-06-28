from ok.functions import *
from ok.browser import OkBrowser
from ok.data import accounts

class OkGroupBot(OkBrowser):
	def __init__(self, hide=True):
		super().__init__(hide=hide)

	def print_group_info(self, location=None):
		if location != None:
			query = "SELECT COUNT(*) FROM users WHERE location = '{}' AND action_group != 'ok' ".format(location)
		else:
			query = "SELECT COUNT(*) FROM users WHERE action_group != 'ok' "

		count = self.execute_custom_query_select("SELECT COUNT(*) FROM users WHERE action_group = 'ok'")[0][0]
		last  = self.execute_custom_query_select(query)[0][0]

		print("Всего отправлено приглашений: ", count, ", осталось: ", last)

	def search_group_users(self, url, page='group', scroll=None):
		self.get(url)
			
		print('Поиск в группе: Получили страницу группы ' + url)

		new_height  = 0
		last_height = 0
		i = 0
		while True:
			self.execute_script("window.scrollTo(0, document.body.scrollHeight);")

			set_pause(1)

			new_height = self.execute_script("return document.body.scrollHeight")

			if i == scroll:
				break

			if new_height == last_height:
				try:
					self.find_element_by_xpath('//a[@class="js-show-more link-show-more"]').click()
				except:
					print('\nПоиск: Ошибка при поиске more...')
					break

			last_height = new_height

			print('Поиск в группе... прокрутили страницу [{}]'.format(i), end ="\r")

			i = i + 1

		print('Поиск в группе... прокрутили страницу [{}]'.format(i))

		links = []
		l	  = 0
		i	  = 0
		ii	  = 0

		try:
			if page == 'group':
				links = self.find_elements_by_xpath('//a[@class="bold n-t"]')
				l	  = len(links)
			elif page == 'user':
				links = self.find_elements_by_xpath('//a[@class="o"]')
				l	  = len(links)
		except:
			print('Поиск: Ошибка при получении необработанных ссылок')
			return 'Error'

		urls = []
		for link in links:
			urls.append(link.get_attribute("href"))

		urls = random_shuffle(urls)

		return urls
		
	def action_group(self, group_name):
		try:
			self.find_element_by_xpath("//li[@class='u-menu_li expand-action-item']").click()
		except Exception as e:
			print('Ошибка при нажатии меню...', e)
			return 'Error'

		try:
			self.find_element_by_xpath("//*[contains(text(), 'Пригласить в группу')]").click()
		except:
			return 'ok'
			#print('Ошибка при нажатии кнопки "Пригласить в группу"...', e)
			#return 'Error'

		links = self.find_element_by_id("hook_Block_PopLayer").find_elements_by_tag_name('a')
		for link in links:
			try:
				request = "//*[contains(text(), '" + group_name + "')]"
				if link.find_element_by_xpath(request):
					link.click()
			except:
				pass

		return 'ok'

def start_action_group(login=None, location=None, group='Дискурс', records=None, n=None, hide=True):
	select   = "SELECT * FROM 'users' WHERE location = '{}' AND action_group != 'ok' ORDER BY RANDOM() LIMIT {}".format(location,records)
	browser = OkGroupBot(hide=hide)
	account = accounts[login]
	if browser.login(account) != 'Error':
		users = browser.execute_custom_query_select(select)
		l	 = len(users);
		i	 = 1

		if l == 0:
			print('Никого не найдено для приглашения в группу')
			browser.end_work()
			return None

		for user in users:
			if browser.get_page(user[0]) != 'Error':
				if browser.action_group(group) != 'Error':
					update = "UPDATE users SET action_group = 'ok' WHERE url = '{}'".format(user[0])
					if browser.execute_custom_query(update) != 'Error':
						print('{}. {}: [{}/{}] Пользователь {} приглашен в группу'.format(n,login,i,l,user[1]), end='\r')
						set_pause(2)
				else:
					print('Ошибка. Пользователь: ', user[0])
					return 'Error'
			set_pause(5)
			i = i + 1

	else:
		browser.end_work()
		return 'Error'

	browser.end_work()
	set_pause(10)
	return 'ok'

def start_actions_group(logins=['evola','valya','natali','ilia','olga','alex'], location=None, group=None, loops=None, records=20, hide=True):
	print('loops:', loops, '| records:', records)
	
	if loops == None:
		i  = 1
		while True:
			login  = random_choice(logins)
			result = start_action_group(login=login,location=location,records=records,n=i,hide=hide)

			set_pause(10)

			if result == 'Error':
				return 'Error'
			elif result == None:
				return None
			else:
				clear_terminal()
		return 'ok'

	elif type(loops) == int:
		for i in range(loops):
			login  = random_choice(logins)
			action = start_action_group(login=login,location=location,records=records,n=i,hide=hide)
			if action == 'Error':
				return 'Error'
			elif action == None:
				return None
		return 'ok'

	return None

def start_actions_group_online(logins=['nastya', 'natali', 'valya'], group='Дискурс', location=None, hide=True, step=5, scroll=None):
	browser = OkGroupBot(hide=hide)

	if browser.login(accounts[random_choice(logins)]) != 'Error':
		for gender in ['m','f']:
			urls = browser.search(gender=gender, location=location, online=True, scroll=scroll)

			l = len(urls)
			i = 0

			print('Получено ссылок: {}'.format(l))

			urls = browser.create_list_urls(urls, step)

			browser.end_work()

			for i_urls in urls:
				browser = OkGroupBot(hide=hide)
				if browser.login(accounts[random_choice(logins)]) != 'Error':
					for url in i_urls:
						if url[-7:] == '/photos':
							url = url[:-7]
						record = browser.database.profile_exist(url)
						if record == None or record == False:
							if browser.get_page(url) != 'Error':
								if browser.action_group(group) != 'Error':
									if record == False:
										update = "UPDATE users SET action_group = 'ok' WHERE url = '{}'".format(url)
										if browser.database.execute_custom_query(update) != 'Error':
											play_signal_tact()
											print('[{}/{}] Пользователь [{}] приглашен в группу'.format(i,l,url), end='\r')
										else:
											break
										browser.database.profile_exist(url)
									elif record == None:
										username = browser.find_element_by_xpath("//h1").text
										if browser.database.insert_user(url, user_name=None, location=location, gender=gender) != 'Error':
											play_signal_tact()
											print('[{}/{}] Пользователь [{}] приглашен в группу и добавлен в базу'.format(i,l,username), end='\r')
										else:
											break
							set_pause(5)

						i = i + 1

				clear_terminal()
				browser.print_group_info(location)
				browser.end_work()
				set_pause(20)

	else:
		browser.end_work()
			
	play_signal_end()

def start_actions_group_from_page(first_url, logins=['nastya', 'natali', 'valya'], page='group', group='Дискурс', location=None, hide=True, step=5, scroll=None):
	browser   = OkGroupBot(hide=hide)

	if browser.login(accounts[random_choice(logins)]) != 'Error':
		urls  = browser.search_group_users(first_url, page=page, scroll=scroll)
		l = len(urls)
		i = 0
		print('Получено ссылок: {}'.format(l))

		urls = browser.create_list_urls(urls, step)

		browser.end_work()

		for i_urls in urls:
			browser = OkGroupBot(hide=hide)
			if browser.login(accounts[random_choice(logins)]) != 'Error':
				for url in i_urls:
					if url[-7:] == '/photos':
						url = url[:-7]
					record = browser.database.profile_exist(url)
					if record == None or record == False:
						if browser.get_page(url) != 'Error':
							if browser.action_group(group) != 'Error':
								if record == False:
									update = "UPDATE users SET action_group = 'ok' WHERE url = '{}'".format(url)
									if browser.database.execute_custom_query(update) != 'Error':
										play_signal_tact()
										print('[{}/{}] Пользователь [{}] приглашен в группу'.format(i,l,url), end='\r')
									else:
										break
									browser.database.profile_exist(url)
								elif record == None:
									username = browser.find_element_by_xpath("//h1").text
									if browser.database.insert_user(url, user_name=None, location=location) != 'Error':
										play_signal_tact()
										print('[{}/{}] Пользователь [{}] приглашен в группу и добавлен в базу'.format(i,l,username), end='\r')
									else:

										break
						set_pause(5)

					i = i + 1
					if i == 5:
						break

			clear_terminal()
			
			print("Обработано: ", i)

			browser.print_group_info(location)
			browser.end_work()
			set_pause(15)

	else:
		browser.end_work()

	play_signal_end()