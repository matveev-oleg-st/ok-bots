from ok.functions import *
from ok.browser import OkBrowser
from ok.data import accounts
from selenium.webdriver.common.keys import Keys

class OkFriendBot(OkBrowser):
	def __init__(self, hide=True):
		super().__init__(hide=hide)

	def action_friend(self):
		try:
			friends = int(self.find_element_by_xpath('//span[@class="portlet_h_count"]').text)
			if friends > 900:
				self.find_element_by_xpath("//*[contains(text(), 'Добавить в друзья')]").click()
				return 'ok'
			else:
				return 'Error'
		except:
			return 'Error'

def start_actions_friends_online_spy(hide=True, scroll=None):
	browser = OkFriendBot(hide=hide)
	if browser.login(accounts['evola']) != 'Error':		
		url = browser.get_search_url(online=True)
		browser.get(url)

		print('Поиск: Получили страницу ' + url)

		new_height  = 0
		last_height = 0
		i = 0

		browser.find_element_by_tag_name('body').send_keys(Keys.ESCAPE)

		while True:
			browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			set_pause(0.5)
			new_height = browser.execute_script("return document.body.scrollHeight")
			if new_height == last_height:
				break

			last_height = new_height

			print('Поиск... прокрутили страницу [{}]'.format(i), end ="\r")
			
			if scroll != None:
				if i == scroll:
					break

			i = i + 1

		print('Поиск... прокрутили страницу [{}]'.format(i))

		try:
			links = browser.find_elements_by_xpath('//a[@class="link__91azp title-link__79ad9"]')
		except:
			print('Поиск: Ошибка при получении необработанных ссылок')
			return 'Error'

		urls = []
		for link in links:
			url = link.get_attribute("href")
			if url[-7:] == '/photos':
				url = url[:-7]
			urls.append(url)

		i = 0
		while(len(urls) > 0):
			url = urls.pop(0)
			
			record = browser.database.profile_exist(url)
			if record == None or record == False:
				if browser.get_page(url) != 'Error':
					if browser.action_friend() != 'Error':
						if record == False:
							update = "UPDATE users SET action_friend = 'ok' WHERE url = '{}'".format(url)
							if browser.database.execute_custom_query(update) != 'Error':
								play_signal_tact()
								print('{}. Пользователь [{}] добавлен в друзья'.format(i,url))
							else:
								break

						elif record == None:
							username = browser.find_element_by_xpath("//h1").text
							if browser.database.insert_user(url, user_name=username, action_friend='ok') != 'Error':
								play_signal_tact()
								print('{}. Пользователь [{}] добавлен в друзья и базу'.format(i,username))
							else:
								break

						set_pause(1)
			i = i + 1

	#clear_terminal()
	browser.end_work()

def start_actions_friends_online(location=None, hide=True, step=5, scroll=None):
	browser = OkFriendBot(hide=hide)
	if browser.login(accounts['evola']) != 'Error':
		urls = browser.search(gender=None, location=location, online=True, scroll=scroll)
		l = len(urls)
		i = 0
		print('Получено ссылок: {}'.format(l))
		for url in urls:
			if url[-7:] == '/photos':
				url = url[:-7]
			record = browser.database.profile_exist(url)
			if record == None or record == False:
				if browser.get_page(url) != 'Error':
					if browser.action_friend() != 'Error':
						if record == False:
							update = "UPDATE users SET action_friend = 'ok' WHERE url = '{}'".format(url)
							if browser.database.execute_custom_query(update) != 'Error':
								play_signal_tact()
								print('[{}/{}] Пользователь [{}] добавлен в друзья'.format(i,l,url), end='\r')
							else:
								break
							browser.database.profile_exist(url)
						elif record == None:
							username = browser.find_element_by_xpath("//h1").text
							if browser.database.insert_user(url, user_name=username, location=location, gender=gender, action_friend='ok') != 'Error':
								play_signal_tact()
								print('[{}/{}] Пользователь [{}] добавлен в друзья и в базу'.format(i,l,username), end='\r')
							else:
								break

			set_pause(1)
			i = i + 1

		clear_terminal()
		browser.print_group_info(location)
		browser.end_work()