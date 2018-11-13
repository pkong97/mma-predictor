from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import string
import re

my_url = 'http://fightmetric.com/statistics/fighters?char='

major_promotions = ["UFC", "Bellator", "Pride", "Strikeforce", "WEC"]

def major_promotion_record():
	counter = 2
	for i in range(0, len(pros)):
		if i <= len(pros)-3:
			print(pros[counter].text.strip())
			counter+=3

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
	return momentum

def fightmetric_scraper(url, filename):
	file = open(filename, "W")
	headers = ''
	file.write(headers)
	for i in string.ascii_lowercase:
		uClient = uReq(url) + i
		page_html = uClient.read()

		page_soup = soup(page_html, 'html.parser')

		for link in page_soup.findAll('a', attrs={'href':re.compile("^http://fightmetric.com/fighter-details")}):
			current_fighter = link.get('href')
			fighter_page = uReq(url).read()
			fighter_soup = soup(fighter_page, 'html.parser')

			# Variables
			name = page_soup.findAll("span", {"class":"b-content__title-highlight"})[0].text.strip()
			nickname = page_soup.findAll("p",{"class":"b-content__Nickname"})[0].text.strip()
			stats = (page_soup.findAll("li", {'class':'b-list__box-list-item b-list__box-list-item_type_block'}))
			height = stats[0].text.strip()
			weight = stats[1].text.strip()
			reach = stats[2].text.strip()
			stance = stats[3].text.strip()
			dob = stats[4].text.strip()
			ss_min = stats[5].text.strip()
			str_acc = stats[6].text.strip()
			ss_a_min = stats[7].text.strip()
			str_def = stats[8].text.strip()
			td_avg = stats[9].text.strip()
			td_acc = stats[10].text.strip()
			td_def = stats[11].text.strip()
			sub_avg = stats[12].text.strip()
			record_list = []

			record = page_soup.findAll("i",{"class":"b-flag__text"})
			for i in record:
				record_list.append(i.text.strip())

			# only counts fights from major promotions
			win_loss_diff = record_list.count('win') - record_list.count('loss')


