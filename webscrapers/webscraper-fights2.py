from urllib.request import urlopen as uReq
from urllib.error import HTTPError
from bs4 import BeautifulSoup as soup
import string
import re

f_name = input('Specify the file path and name: ')

my_url = 'http://fightmetric.com/statistics/events/completed?page=all'
headers = 'event_id,method\n'
movs = ['KO', 'SUB', 'DEC', 'Overturned','CNC','DQ','Other']

def fight_scraper(url, filename):
	file = open(filename, "w")
	file.write(headers)
	page_soup = soup(uReq(url).read(), 'html.parser')
	events = page_soup.findAll('a', attrs={'href':re.compile("^http://fightmetric.com/event-details")})

	for i in range(1, len(events)):
		current_event = events[i].get('href')
		event_id = current_event.split('/')[-1]
		try:
			event_page = uReq(current_event).read()
			event_soup = soup(event_page, 'html.parser')
		except HTTPError as e:
				e.read()
		
		methods = event_soup.findAll("p", {"class":"b-fight-details__table-text"})

		for i in range(0, len(methods)):
			if any(x in methods[i].text.strip() for x in movs):
				method = methods[i].text.strip()
				file.write(event_id + ',' + method + '\n')
				print(method)
	
	file.close()

fight_scraper(my_url, f_name)