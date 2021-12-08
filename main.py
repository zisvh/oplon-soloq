from riotwatcher import LolWatcher, ApiError
import pandas as pd
import csv
import gspread

#variables
api_key = 'RGAPI-1768d1af-bf89-40ff-923d-45f37445b8ad'
watcher = LolWatcher(api_key)
my_region = 'euw1'
region = 'europe'
peng_id = 'IDlMIxG2hN-fB3vUg4KuwpLKEZ73cMQhhoXyQf_mrdKYRHuAKgwq3wp8h3h8ny-peDTE6y_wS9omNg'

#functions
mh = list(watcher.match.matchlist_by_puuid(region, peng_id, type="ranked", count=5))
last = mh[0]
match_stats = watcher.match.by_id(region, last)
champions = []
compte = []
final = []
newfinal = []



#get data
for i in mh:
    data = watcher.match.by_id(region, i)
    for j in range(10):
        if data['info']['participants'][j]['puuid'] == peng_id:
            champions.append(data['info']['participants'][j]['championName'])


for i in champions:
    compte.append(champions.count(i))

for i in range(len(champions)):
    final.append([champions[i], compte[i]])

for i in final:
    if i not in newfinal:
        newfinal.append(i)

print(newfinal)

