from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

my_url = 'http://fightmetric.com/statistics/fighters?char='

uClient = uReq(my_url)
page_html = uClient.read()

page_soup = soup(page_html, "html.parser")

for link in page_soup.findAll('a', attrs={'href':re.compile("^http://fightmetric.com/fighter-details")}):
	current_fighter = link.get('href')
	