from ok.group import start_actions_group_online, start_actions_group_from_page
from ok.friends import start_actions_friends_online_spy

if __name__ == "__main__":
	i = 0
	while i < 5:
		start_actions_friends_online_spy(hide=False,scroll=100)

		i = i + 1

		set_pause(25)
