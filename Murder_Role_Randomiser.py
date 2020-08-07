import smtplib, re
from random import shuffle
from email.message import EmailMessage
import config

def decorate():
	print("\n" + "*"*10 + "\n")


def add_player(current_players):
	while True:
		add_player = input("Please enter player's email or press enter to return to main menu:  ")
		if add_player == '':
			return decorate()
		if validate(add_player):
			if not add_player in current_players:
				decorate()
				return current_players.append(add_player)
			else:
				print("This player is already in the game!")
		else:
			print("Email not valid!")
		decorate()


def remove_player(current_players):
	while True:
		remove_player = input("Please enter player's email to be removed or press enter to return to main menu:  ")
		if remove_player == '':
			return decorate()
		if remove_player in current_players:
			print(f"{remove_player} was removed.")
			decorate()
			return current_players.remove(remove_player)
		else:
			print("This player does not exist!")
			decorate()


def validate(email):
	pattern = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
	string = email
	return pattern.fullmatch(string)


def set_roles(current_players):
	roles = ['Detective', 'Murderer', 'Bystander', 'Bystander']
	if 4 < len(current_players) <= 9:
		for i in range(len(current_players) - 4):
			roles.append('Bystander')
	if len(current_players) >= 10:
		roles.append('Murderer')
		for i in range(len(current_players) - 5):
			roles.append('Bystander')
	return roles


def randomise(current_players, role_list):
    shuffle(current_players)
    shuffle(role_list)
    random_list = list(zip(current_players, role_list))
    return random_list


def send_email(randomised, email, server_host):
	try:
		with smtplib.SMTP(host=server_host, port=587) as smtp:
			smtp.ehlo()
			smtp.starttls()
			smtp.login(email, config.APP_PASSWORD)
			email = EmailMessage()
			email['from'] = email
			for i in randomised:
				email['to'] = f'{i[0]}'
				email['subject'] = f'{i[1]}'
				smtp.send_message(email)
		print("Emails Sent Successfully!")
	except smtplib.SMTPAuthenticationError as e:
		print("Email or Password was incorrect please check the config file\n\n" + str(e))


def log_in():
	while True:
		decorate()
		game_host = input("Please enter your email address: ")
		if validate(game_host):
			decorate()
			domains = {"smtp.gmail.com":['gmail', 'googlemail'], "smtp.office365.com":['hotmail', 'live', 'msn', 'passport', 'outlook'], "smtp.mail.yahoo.com":['yahoo', 'ymail'], "smtp.mail.me.com":['icloud']}
			domain_search = game_host.find('@') + 1
			domain = game_host[domain_search:game_host.find('.',domain_search)]
			for k,v in domains.items():
				for i in v:
					if i == domain:
						return game_host, k
			print("Email domain not supported. Gmail Recommended.")
		else:
			decorate()
			print("That email is not valid. Try again.")


if __name__ == '__main__':
	game_host, server_host = log_in()
	current_players = [game_host]
	while True:
		if current_players == []:
			choice = input(f"There are currently no players, you need at least 4.\n\nWhat would you like to do?\n1) Add a Player\n2) Remove Player\n3) Send Email\n4) Exit\n\n" + "*"*10 + "\n\n")
		elif len(current_players) == 1:
			choice = input(f"There is currently 1 player, you need at least 4: {str(current_players)[1:-1]}\n\nWhat would you like to do?\n1) Add a Player\n2) Remove Player\n3) Send Email\n4) Exit\n\n" + "*"*10 + "\n\n")
		else:
			choice = input(f"There are currently {len(current_players)} players, you need at least 4: {str(current_players)[1:-1]}\n\nWhat would you like to do?\n1) Add a Player\n2) Remove Player\n3) Send Email\n4) Exit\n\n" + "*"*10 + "\n\n")
		if choice != '1' and choice != '2' and choice != '3' and choice != '4':
			print("You did not select an option.\n")
		decorate()
		if choice == '1':
			add_player(current_players)
		if choice == '2':
			remove_player(current_players)
		if choice == '3':
			if current_players == []:
				print("There is no-one to email!")
			else:
				role_list = set_roles(current_players)
				randomised = randomise(current_players, role_list)
				send_email(randomised, game_host, server_host)
		if choice == '4':
			break