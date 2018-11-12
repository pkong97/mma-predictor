from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import string

my_url = 'http://fightmetric.com/statistics/fighters?char='

def fightmetric_scraper(url, filename):
	for i in string.ascii_lowercase:
		uClient = uReq(url) + i
		page_html = uClient.read()

		page_soup = soup(page_html, 'html.parser')

		for link in page_soup.findAll('a', attrs={'href':re.compile("^http://fightmetric.com/fighter-details")}):
			current_fighter = link.get('href')
			fighter_page = uReq(url).read()
			fighter_soup = soup(fighter_page, 'html.parser')

			#Variables
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

