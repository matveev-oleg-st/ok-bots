from ok.browser import OkBrowser
from ok.group import OkGroupBot
from ok.data import accounts

def test_login(name, hide=False):
	browser = OkBrowser(hide=hide)
	if browser.login(accounts[name]) != 'Error':
		print(name, ' ok')
	else:
		print(name, ' error')
	browser.end_work()

def test_action_group(url, name='nastya', hide=True):
	group   = 'Дискурс'
	browser = OkGroupBot(hide=hide)
	account = accounts[name]
	if browser.login(account) != 'Error':
		if browser.get_page(url) != 'Error':
			if browser.action_group(group) != 'Error':
				update = "UPDATE users SET action_group = 'ok' WHERE url = '{}'".format(url)
				if browser.execute_custom_query(update) != 'Error':
					print('Пользователь {} приглашен в группу'.format(url))
			else:
				print('Ошибка добавления пользователя в группу')
	browser.end_work()