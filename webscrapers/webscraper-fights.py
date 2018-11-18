from urllib.request import urlopen as uReq
from urllib.error import HTTPError
from bs4 import BeautifulSoup as soup
import string
import re

my_url = 'http://fightmetric.com/statistics/events/completed?page=all'
headers = ''

def fight_scraper(url, filename):
	file = open(filename, "w")
	events = page_soup.findAll('a', attrs={'href':re.compile("^http://fightmetric.com/event-details")})

	for link in events:
		current_event = link.get('href')
		page_soup = soup(uReq(current_event).read(), 'html.parser')
		