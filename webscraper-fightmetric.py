from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

my_url = 'http://www.fightmetric.com/fighter-details/634bb0de2eb043b4'

my_url2 = 'http://www.ufc.com/event/UFC-222'

uClient = uReq(my_url)
page_html = uClient.read()

page_soup = soup(page_html, "html.parser")

career_stats = page_soup.findAll("div", {"class":"b-list__info-box-left"}) 