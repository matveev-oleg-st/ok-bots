from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from ok.functions import *
from ok.database import OkDatabase

class OkBrowser(webdriver.Chrome):
	def __init__(self, hide=True):
		self.ok_url   = 'https://www.ok.ru'
		self.fopen    = open('logs/parser.log', 'a')
		self.database = OkDatabase()
		options		  = webdriver.ChromeOptions()
		if hide == True:
			options.add_argument('headless')
		options.add_argument("start-maximized")

		super().__init__(options=options)

		print('Браузер готов к работе...')

	def get_page(self, url):
		try:
			self.get(url)
		except Exception as e:
			error_message = 'Error: get {}|{}'.format(url, e)
			self.write_log(error_message)
			return 'Error'
		return None

	def login(self, account):
		if self.get_page(self.ok_url) != 'Error':
			try:
				self.find_element_by_xpath("//*[contains(text(), 'Вход')]").click()
				print('Найден блок входа ...')
			except:
				print('Ошибка поиска блока входа')
				return 'Error enter'

			try:
				self.find_element_by_xpath('//input[@name="st.email"]').send_keys(account['login'])
				print('Найден элемент st.email и введен логин... ', account['login'])
			except:
				print('Ошибка элемента st.email')
				return 'Error'

			try:
				element = self.find_element_by_xpath('//input[@name="st.password"]')
				element.send_keys(account['pass'])
				element.send_keys(Keys.TAB)
				element.send_keys(Keys.ENTER)

				print('Найден элемент st.password и введен пароль...')
			except Exception as e:
				print('Ошибка элемента st.password', e)
				return 'Error'

			print("Вошли...")
			return None
		else:
			return 'Error'

	def get_search_url(self, online=True,country=None,location=None,gender=None,single=None,age_min=None,age_max=None):
		if gender == None:
			url = "https://ok.ru/dk?st.cmd=searchResult&st.mode=Users&st.grmode=Groups"
		else:
			url = "https://ok.ru/dk?st.cmd=searchResult&st.mode=Users&st.gender=" + gender + "&st.grmode=Groups"
			
		if online == True:
			url += "&st.onSite=on"

		if country != None:
			url += "&st.country=" + country

		if location != None:
			url += "&st.location=" + location

		if age_min != None:
			url += "&st.fromAge=" + str(age_min)

		if age_max != None:
			url += "&st.tillAge=" + str(age_max)

		if single == True:
			url += "&st.single=on"

		return url

	def search(self,gender=None,location=None,online=None,single=None,age_min=None,age_max=None,scroll=None):

		url = self.get_search_url(gender=gender,location=location,online=online,single=single,age_min=age_min)
		self.get(url)
		print('Поиск: Получили страницу ' + url)

		new_height  = 0
		last_height = 0
		i = 0
		while True:
			self.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			set_pause(1)
			new_height = self.execute_script("return document.body.scrollHeight")
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
			links = self.find_elements_by_xpath('//a[@class="link__91azp title-link__79ad9"]')
		except:
			print('Поиск: Ошибка при получении необработанных ссылок')
			return 'Error'

		urls = []
		for link in links:
			urls.append(link.get_attribute("href"))

		return urls

	def create_list_urls(self, urls, step):
		n_urls = []
		i_urls = []
		i = 0
		for url in urls:
			i = i + 1
			i_urls.append(url)
			if i == step:
				n_urls.append(i_urls)
				i_urls = []
				i = 0

		return n_urls

	def execute_custom_query(self, query):
		return self.database.execute_custom_query(query)

	def execute_custom_query_select(self, query):
		return self.database.execute_custom_query_select(query)

	def write_log(self, in_data):
		out_data = datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S") + ' - ' + in_data + '\n'
		self.fopen.write(out_data)
		print(out_data)

	def end_work(self):
		self.fopen.close()
		self.database.db_close()
		self.quit()