import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

fighters = pd.read_csv("C:/Users/patri/OneDrive/Projects/mma-predictor/data/fighter-database.csv")
fights = pd.read_csv("C:/Users/patri/OneDrive/Projects/mma-predictor/data/fight-database.csv")

# track differences in databases
f_ids = list(fights['f1_id'].append(fights['f2_id']))
missing = []
f_ids_fighters = list(fighters['id'])
for i in set(f_ids):
    if i not in f_ids_fighters:
        f_ids.remove(i)
        missing.append(i)
print(len(f_ids))
print(len(missing))

# remove fights w/ fighters not in database
for i in range(0, len(fights)):
    if fights.loc[i, 'f1_id'] in missing or fights.loc[i, 'f2_id'] in missing:
        fights = fights.drop(index = i)
fights = fights.reset_index()
len(fights)

def expected_score(ratingA, ratingB, player):
    '''player must be A or B'''
    if player == 'A':
        return 1/(1+10**((ratingB-ratingA)/400))
    else:
        return 1/(1+10**((ratingA-ratingB)/400))

def update_elo(ratingA, ratingB, player, outcome):
    '''outcome True for win, False otherwise'''
    if outcome:
        return ratingA + 32*(1 - expected_score(ratingA, ratingB, player))
    else:
        return ratingA + 32*(0 - expected_score(ratingA, ratingB, player))

# create composite database
headings = ['id','name','id_opp','name_opp','event_id','event_name','elo','elo_opp','height_diff','reach_diff','ss_min_diff','str_acc_diff', 
            'str_a_min_diff','str_def_diff','td_avg_diff','td_acc_diff','td_def_diff','sub_avg_diff', 
            'wins_diff','losses_diff','momentum_diff','wl_diff_diff','outcome']
comp = pd.DataFrame.from_records([], columns = headings)

# fill composite database
start_elo = 750
elos = {}

for i in range(len(fights)-1, 0, -1):
    ID = fights.loc[i, 'f1_id']
    name = fights.loc[i, 'f1_name']
    id_opp = fights.loc[i, 'f2_id']
    name_opp = fights.loc[i, 'f2_name']
    event_id = fights.loc[i, 'event_id']
    event_name = fights.loc[i, 'event_name']
    f1_data = fighters.loc[fighters['id'] == ID]
    f2_data = fighters.loc[fighters['id'] == id_opp]
    
    # determine current elo rating
    if ID not in list(comp['id'].append(comp['id_opp'])):
        elo = start_elo
    elif ID in elos.keys():
        elo = elos[ID]
    if id_opp not in list(comp['id'].append(comp['id_opp'])):
        elo_opp = start_elo
    elif id_opp in elos.keys():
        elo_opp = elos[id_opp]
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
    
    outcome = 'W'
    elos[ID] = update_elo(elo, elo_opp, 'A', True)
    elos[id_opp] = update_elo(elo_opp, elo, 'A', False)

    comp = comp.append([{'id':ID,'name':name,'id_opp':id_opp,'name_opp':name_opp,'event_id':event_id,'event_name':event_name,
                         'elo':elo,'elo_opp':elo_opp, 'height_diff':height_diff,'reach_diff':reach_diff,
                         'ss_min_diff':ss_min_diff,'str_acc_diff':str_acc_diff,'str_a_min_diff':str_a_min_diff,
                         'str_def_diff':str_def_diff,'td_avg_diff':td_avg_diff,'td_acc_diff':td_acc_diff,
                         'td_def_diff':td_def_diff,'sub_avg_diff':sub_avg_diff,'wins_diff':wins_diff,
                         'losses_diff':losses_diff,'momentum_diff':momentum_diff, 'wl_diff_diff':wl_diff_diff,'outcome':outcome}], 
                       ignore_index = True)
    comp = comp.append([{'id':id_opp,'name':name_opp,'id_opp':ID,'name_opp':name,'event_id':event_id,'event_name':event_name,
                         'elo':elo_opp,'elo_opp':elo, 'height_diff':-height_diff,'reach_diff':-reach_diff,
                         'ss_min_diff':-ss_min_diff,'str_acc_diff':-str_acc_diff,'str_a_min_diff':-str_a_min_diff,
                         'str_def_diff':-str_def_diff,'td_avg_diff':-td_avg_diff,'td_acc_diff':-td_acc_diff,
                         'td_def_diff':-td_def_diff,'sub_avg_diff':-sub_avg_diff,'wins_diff':-wins_diff,
                         'losses_diff':-losses_diff,'momentum_diff':-momentum_diff, 'wl_diff_diff':-wl_diff_diff,'outcome':'W' if outcome == 'L' else 'L'}],
                      ignore_index = True)

# convert to all values to numerics
comp['elo'] = comp.elo.astype(float)
comp['elo_opp'] = comp.elo_opp.astype(float)
comp['height_diff'] = comp.height_diff.astype(float)
comp['str_acc_diff'] = comp.str_acc_diff.astype(float)
comp['str_def_diff'] = comp.str_def_diff.astype(float)
comp['td_acc_diff'] = comp.td_acc_diff.astype(float)
comp['td_def_diff'] = comp.td_def_diff.astype(float)
comp['wins_diff'] = comp.wins_diff.astype(float)
comp['losses_diff'] = comp.losses_diff.astype(float)
comp['momentum_diff'] = comp.momentum_diff.astype(float)
comp['wl_diff_diff'] = comp.wl_diff_diff.astype(float)

comp.to_csv('C:/Users/patri/OneDrive/Projects/mma-predictor/data/composite-database.csv')