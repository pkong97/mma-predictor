from urllib.request import urlopen as uReq
from urllib.error import HTTPError
from bs4 import BeautifulSoup as soup
import string
import re
import numpy as np
import pandas as pd
from datetime import datetime
from datetime import date

next_event_name = ''
next_event_date = ''
next_event_date_name = ''
my_url = 'http://ufcstats.com/statistics/events/completed?page=all'
headers = 'event_id,event_name,f1_id,f1_name,f2_id,f2_name\n'

# collect data on next event

def scrape_next_event(url):

    global next_event_date, next_event_name, next_event_date_name

    page_soup = soup(uReq(url).read(), 'html.parser')
    events = page_soup.findAll('a', attrs={'href':re.compile("^http://ufcstats.com/event-details")})
    event = events[0].get('href')
    try:
        event_page = uReq(event).read()
        event_soup = soup(event_page, 'html.parser')
    except HTTPError as e:
        e.read()

    event_id = event.split('/')[-1]
    # get event name mutate to lowercase
    next_event_name = event_soup.findAll('span',{'class':'b-content__title-highlight'})[0].text.strip()
    next_event_name_clean = re.sub('[^A-Za-z0-9]+', '-', next_event_name).lower()
    # get event date in YYYY-MM-DD format
    next_event_date = event_soup.findAll("li", {"class":"b-list__box-list-item"})[0].text.strip("[Date:, \n]")
    next_event_date = str(datetime.strptime(next_event_date, '%B %d, %Y').date())
    fighters = event_soup.findAll('a', attrs={'href':re.compile("^http://ufcstats.com/fighter-details")})

    next_event_date_name = 'predictions/' + next_event_date + '-' + next_event_name_clean + '-predicitons.csv'

    file = open(next_event_date_name, "w")
    file.write(headers)

    for i in range(0, len(fighters), 2):
        f1_id = fighters[i].get('href').split("/")[-1]
        f1_name = fighters[i].text.strip()
        f2_id = fighters[i+1].get('href').split("/")[-1]
        f2_name = fighters[i+1].text.strip()

        file.write(event_id + ',' + next_event_name + ',' + f1_id + ',' + f1_name
            + ',' + f2_id + ',' + f2_name + '\n')

        print(f1_name + " vs. " + f2_name)

    file.close()

scrape_next_event(my_url)

# load training sets
fighters = pd.read_csv('data/' + str(date.today()) + '-fighter-data-clean.csv')
fights = pd.read_csv('raw-data/' + str(date.today()) + '-fight-data-raw.csv')
comp = pd.read_csv('data/' + str(date.today()) + '-all-fights-fighters-data.csv')
next_event = pd.read_csv(next_event_date_name)

# elo ranking formulas
def expected_score(ratingA, ratingB, player):
    '''player must be A or B'''
    if player == 'A':
        return 1/(1+10**((ratingB-ratingA)/400))
    else:
        return 1/(1+10**((ratingA-ratingB)/400))

def update_elo(ratingA, ratingB, player, outcome):
    '''outcome True for win, False otherwise'''
    if outcome:
        return ratingA + 60*(1 - expected_score(ratingA, ratingB, player))
    else:
        return ratingA + 60*(0 - expected_score(ratingA, ratingB, player))

# track differences in databases
f_ids = list(next_event['f1_id'].append(next_event['f2_id']))
missing = []
f_ids_fighters = list(fighters['id'])
for i in set(f_ids):
    if i not in f_ids_fighters:
        f_ids.remove(i)
        missing.append(i)

# remove fights w/ fighters not in database
for i in range(0, len(next_event)):
    if next_event.loc[i, 'f1_id'] in missing or next_event.loc[i, 'f2_id'] in missing:
        next_event = next_event.drop(index = i)
next_event = next_event.reset_index()

# create testing set
start_elo = 1000

headings = ['id','name','id_opp','name_opp','event_id','event_name','elo','elo_opp','height_diff','reach_diff','ss_min_diff','str_acc_diff', 
            'str_a_min_diff','str_def_diff','td_avg_diff','td_acc_diff','td_def_diff','sub_avg_diff', 
            'wins_diff','losses_diff','momentum_diff','wl_diff_diff']

n_event = pd.DataFrame.from_records([], columns = headings)


for i in range(0, len(next_event)):
    ID = next_event.loc[i, 'f1_id']
    name = next_event.loc[i, 'f1_name']
    id_opp = next_event.loc[i, 'f2_id']
    name_opp = next_event.loc[i, 'f2_name']
    event_id = next_event.loc[i, 'event_id']
    event_name = fights.loc[i, 'event_name']
    f1_data = fighters.loc[fighters['id'] == ID]
    f2_data = fighters.loc[fighters['id'] == id_opp]
    f1_comp_data = comp.loc[comp['id'] == ID]
    f2_comp_data = comp.loc[comp['id'] == id_opp]
    
    if ID not in list(comp['id'].append(comp['id_opp'])):
        elo = start_elo
    elif f1_comp_data['outcome'].values[-1] == 'W':
        f1_current_elo = f1_comp_data['elo'].values[-1]
        elo = update_elo(f1_current_elo, f1_comp_data['elo_opp'].values[-1], 'A', True)
    else:
        f1_current_elo = f1_comp_data['elo'].values[-1]
        elo = update_elo(f1_current_elo, f1_comp_data['elo_opp'].values[-1], 'A', False)
    
    if id_opp not in list(comp['id'].append(comp['id_opp'])):
        elo_opp = start_elo
    elif f2_comp_data['outcome'].values[-1] == 'W':
        f2_current_elo = f2_comp_data['elo'].values[-1]
        elo_opp = update_elo(f2_current_elo, f2_comp_data['elo_opp'].values[-1], 'A', True)
    else:
        f2_current_elo = f2_comp_data['elo'].values[-1]
        elo_opp = update_elo(f2_current_elo, f2_comp_data['elo_opp'].values[-1], 'A', False)
    
    height_diff = f1_data['height'].values[0] - f2_data['height'].values[0]
    reach_diff = f1_data['reach'].values[0] - f2_data['reach'].values[0]
    ss_min_diff = f1_data['ss_min'].values[0] - f2_data['ss_min'].values[0]
    str_acc_diff = f1_data['str_acc'].values[0] - f2_data['str_acc'].values[0]
    str_a_min_diff = f1_data['str_a_min'].values[0] - f2_data['str_a_min'].values[0]
    str_def_diff = f1_data['str_def'].values[0] - f2_data['str_def'].values[0]
    td_avg_diff = f1_data['td_avg'].values[0] - f2_data['td_avg'].values[0]
    td_acc_diff = f1_data['td_acc'].values[0] - f2_data['td_acc'].values[0]
    td_def_diff = f1_data['td_def'].values[0] - f2_data['td_def'].values[0]
    sub_avg_diff = f1_data['sub_avg'].values[0] - f2_data['sub_avg'].values[0]
    wins_diff = f1_data['wins'].values[0] - f2_data['wins'].values[0]
    losses_diff = f1_data['losses'].values[0] - f2_data['losses'].values[0]
    momentum_diff = f1_data['momentum'].values[0] - f2_data['momentum'].values[0]
    wl_diff_diff = f1_data['wl_diff'].values[0] - f2_data['wl_diff'].values[0]
    
    n_event = n_event.append([{'id':ID,'name':name,'id_opp':id_opp,'name_opp':name_opp,'event_id':event_id,'event_name':event_name,
                         'elo':elo,'elo_opp':elo_opp, 'height_diff':height_diff,'reach_diff':reach_diff,
                         'ss_min_diff':ss_min_diff,'str_acc_diff':str_acc_diff,'str_a_min_diff':str_a_min_diff,
                         'str_def_diff':str_def_diff,'td_avg_diff':td_avg_diff,'td_acc_diff':td_acc_diff,
                         'td_def_diff':td_def_diff,'sub_avg_diff':sub_avg_diff,'wins_diff':wins_diff,
                         'losses_diff':losses_diff,'momentum_diff':momentum_diff, 'wl_diff_diff':wl_diff_diff}], 
                       ignore_index = True)


#predictors = ['elo','elo_opp','height_diff','reach_diff','ss_min_diff','str_acc_diff', 
#            'str_a_min_diff','str_def_diff','td_avg_diff','td_acc_diff','td_def_diff','sub_avg_diff', 
#            'wins_diff','losses_diff','momentum_diff','wl_diff_diff']
#outcome = 'outcome'

# Logistic Regression
from sklearn.linear_model import LogisticRegression
# Random Forest
from sklearn.ensemble import RandomForestClassifier

predictors = ['elo','elo_opp','ss_min_diff','str_acc_diff', 
            'str_a_min_diff','str_def_diff','td_acc_diff','td_def_diff', 
            'momentum_diff','wl_diff_diff']
outcome = 'outcome'

model = LogisticRegression()

#model_selection = input('0 for LogisticRegression, 1 for RandomForestClassification')

#if model_selection == 0:
#	model = LogisticRegression()
#elif model_selection == 1:
#	model = RandomForestClassifier()

model.fit(comp[predictors],comp[outcome])
n_event[outcome] = model.predict(n_event[predictors])

n_event.to_csv(next_event_date_name)

