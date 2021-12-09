from riotwatcher import LolWatcher, ApiError
import pandas as pd
import csv

#variables
api_key = 'RGAPI-f5c34ea0-ea09-4c17-9042-7e06e972b7f9'
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

df = pd.DataFrame(newfinal, columns=['Champion', 'Games'])
icons = ['1', '2', '3', '4', '5']
df['icons'] = icons

df.to_csv('matches.csv')
print(df)
