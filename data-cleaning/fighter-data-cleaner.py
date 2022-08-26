import numpy as np
import pandas as pd
from datetime import date

fighters = pd.read_csv("../raw-data/" + str(date.today()) + "-fighter-data-raw.csv")

#drop all rows with missing weight and height
for i in range(0, len(fighters)):
    if fighters['weight'].isnull()[i]:
        fighters = fighters.drop(index = i)
fighters = fighters.reset_index()
for i in range(0, len(fighters)):
    if fighters['height'].isnull()[i]:
        fighters = fighters.drop(index = i)
fighters = fighters.reset_index()

#replace missing reach values based on weight
avg_reach = fighters.pivot_table(values = 'reach', index ='weight')
for i in range(0, len(fighters)):
    if fighters['reach'].isnull()[i]:
        if fighters.loc[i, 'weight'] in range(0,116):
            fighters.loc[i, 'reach'] = avg_reach['reach'][115]
        if fighters.loc[i, 'weight'] in range(116,126):
            fighters.loc[i, 'reach'] = avg_reach['reach'][125]
        if fighters.loc[i, 'weight'] in range(126,136):
            fighters.loc[i, 'reach'] = avg_reach['reach'][135]
        if fighters.loc[i, 'weight'] in range(136,146):
            fighters.loc[i, 'reach'] = avg_reach['reach'][145]
        if fighters.loc[i, 'weight'] in range(146,156):
            fighters.loc[i, 'reach'] = avg_reach['reach'][155]
        if fighters.loc[i, 'weight'] in range(156,171):
            fighters.loc[i, 'reach'] = avg_reach['reach'][170]
        if fighters.loc[i, 'weight'] in range(171,186):
            fighters.loc[i, 'reach'] = avg_reach['reach'][185]
        if fighters.loc[i, 'weight'] in range(186,206):
            fighters.loc[i, 'reach'] = avg_reach['reach'][205]
        else:
            fighters.loc[i, 'reach'] = avg_reach['reach'][225]

#change heights into inches
import re
for i in range(0, len(fighters['height'])):
    if fighters['height'].isnull()[i] != True:
        fighters.loc[i, 'height'] = re.sub("[\'\"]", "", str(fighters.loc[i, 'height']))
for i in range(0, len(fighters['height'])):
    if fighters['height'].isnull()[i] != True:
        height1 = int(str(fighters.loc[i, 'height'])[0])*12
        height2 = int(str(fighters.loc[i, 'height'])[1:])
        total = height1 + height2
        fighters.loc[i, 'height'] = total

last_name = [x.split(' ')[-1] for x in fighters['name']]
fighters['last_name'] = last_name
fighters = fighters.sort_values('last_name')
fighters = fighters.drop(columns = ["last_name", "level_0", "index"])

#fix td_avg and sub_avg values
fighters['td_avg'] = fighters['td_avg'].apply(lambda x: float(x[1:]))
fighters['sub_avg'] = fighters['sub_avg'].apply(lambda x: float(x[2:]))

#remove outliers
for i in range(0, len(fighters)):
    if any(fighters.loc[i, 'ss_min'] == x for x in [0, 30]):
        fighters = fighters.drop(index = i)
fighters = fighters.reset_index()
for i in range(0, len(fighters)):
    if any(fighters.loc[i, 'str_acc'] == x for x in [0, 100]):
        fighters = fighters.drop(index = i)
fighters = fighters.reset_index()
for i in range(0, len(fighters)):
    if any(fighters.loc[i, 'str_a_min'] == x for x in [0, 49.41]):
        fighters = fighters.drop(index = i)
fighters = fighters.reset_index(drop = True)
for i in range(0, len(fighters)):
    if any(fighters.loc[i, 'str_def'] == x for x in [0, 100]):
        fighters = fighters.drop(index = i)
fighters = fighters.reset_index(drop = True)

fighters = fighters.drop(columns = ['level_0', 'index', 'dob'])

fighters.to_csv("../data/" + str(date.today()) + "-fighter-data-clean.csv")
