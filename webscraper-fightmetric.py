from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import string
import re

my_url = 'http://fightmetric.com/statistics/fighters?char='

def calc_momentum(record):
	momentum = 0
	streak = record[0]
	for i in record:
		if i == streak:
			momentum += 1
		else:
			break
	if streak == "loss":
		momentum *= -1
	elif streak == "draw":
		momentum = 0
	return momentum

def fightmetric_scraper(url, filename):
	file = open(filename, "w")
	headers = 'id, name, nickname, height, weight, reach, dob, ss_min, str_acc, str_a_min, str_def, td_avg, td_acc, td_def, sub_avg, wins, losses, wl_diff, momentum\n'
	file.write(headers)
	f_id = 0
	for i in string.ascii_lowercase:
		url = url + i + '&page=all'
		print('Starting on ' + i)
		uClient = uReq(url)
		page_html = uClient.read()

		page_soup = soup(page_html, 'html.parser')

		fighter_links = []

		for link in page_soup.findAll('a', attrs={'href':re.compile("^http://fightmetric.com/fighter-details")}):
			fighter_links.append(link.get('href'))

		fighter_links = set(fighter_links)
		print(len(fighter_links))

		for current_fighter in fighter_links:
			fighter_page = uReq(current_fighter).read()
			fighter_soup = soup(fighter_page, 'html.parser')

			# Variables
			f_id += 1
			name = fighter_soup.findAll("span", {"class":"b-content__title-highlight"})[0].text.strip()
			print(name)
			nickname = fighter_soup.findAll("p",{"class":"b-content__Nickname"})[0].text.strip()
			stats = fighter_soup.findAll("li", {'class':'b-list__box-list-item b-list__box-list-item_type_block'})
			height = re.sub("[^0-9\'\"]", "", stats[0].text.strip()) #filter out unnecessary headings
			weight = re.sub("[^0-9]", "", stats[1].text.strip())
			reach = re.sub("[^0-9\^.]", "", stats[2].text.strip())
			dob = stats[4].text.strip()[-4:]
			ss_min = re.sub("[^0-9\^.]", "", stats[5].text.strip())
			str_acc = re.sub("[^0-9]", "", stats[6].text.strip())
			ss_a_min = re.sub("[^0-9\^.]", "", stats[7].text.strip())
			str_def =  re.sub("[^0-9]", "", stats[8].text.strip())
			td_avg = re.sub("[^0-9\^.]", "", stats[10].text.strip())
			td_acc = re.sub("[^0-9]", "", stats[11].text.strip())
			td_def = re.sub("[^0-9]", "", stats[12].text.strip())
			sub_avg = re.sub("[^0-9\^.]", "",stats[13].text.strip())
			record_list = []

			record = fighter_soup.findAll("i",{"class":"b-flag__text"})
			for i in record:
				record_list.append(i.text.strip())

			wins = record_list.count('win')
			losses = record_list.count('loss')
			win_loss_diff = wins - losses
			if len(record) != 0:
				momentum = calc_momentum(record_list)
			else:
				momentum = 0
			file.write(str(f_id) + "," + name + "," + nickname + "," + height + "," + weight + "," + reach + "," + dob + "," + ss_min + "," 
				+ str_acc + "," + ss_a_min + "," + str_def + "," + td_avg + "," + td_acc + "," + td_def + "," + sub_avg + "," + str(wins) + 
				"," + str(losses) + "," + str(win_loss_diff) + "," + str(momentum) + "\n")

	file.close()

fightmetric_scraper(my_url, 'fighter-database.csv')

