from urllib.request import urlopen as uReq
from urllib.error import HTTPError
from bs4 import BeautifulSoup as soup
import string
import re

my_url = 'http://fightmetric.com/statistics/events/completed?page=all'
headers = 'event_id, method,\n'
movs = ['KO', 'SUB', 'DEC', 'Overturned']

def fight_scraper(url, filename):
	file = open(filename, "w")
	file.write(headers)
	page_soup = soup(uReq(url).read(), 'html.parser')
	events = page_soup.findAll('a', attrs={'href':re.compile("^http://fightmetric.com/event-details")})

	for link in events:
		current_event = link.get('href')
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
			elif ":" in methods[i].text.strip():
				time = methods[i].text.strip()

			file.write(event_id + ',' + method + '\n')
			print(method)
	
	file.close()

fight_scraper(my_url, "fight-database2.csv")