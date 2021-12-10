from riotwatcher import LolWatcher, ApiError
import pandas as pd
import csv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from df2gspread import df2gspread as d2g

#GS HANDLES
scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('oplon.json', scope)
client = gspread.authorize(creds)
oplon_soloq = client.open("OPL").sheet1

#variables
api_key = 'RGAPI-f5c34ea0-ea09-4c17-9042-7e06e972b7f9'
watcher = LolWatcher(api_key)
my_region = 'euw1'
region = 'europe'
peng_id = 'IDlMIxG2hN-fB3vUg4KuwpLKEZ73cMQhhoXyQf_mrdKYRHuAKgwq3wp8h3h8ny-peDTE6y_wS9omNg'
darlik_id = 'fQwRacUndeCleiOeQi4qm4WTFuoqSZg7SXnQWeAepWZPZ6teQ7Aytl5wAoAG3ltsM_ZcNT904BbIUg'
brunes_id = '7ZYtr9dWdugLIH0u9vvQNAHqSreCq0mRzmbezoZzvGHivl5DN4HoJRBKXpGOKn0wEM4iIO3zMeV2iw'
adc_id = 'R9G6ILHKjrhY56vUAN-KAdAVx1Dn8J2kdPzpZq6hfF0q2gDRAMc7JywT5RVpVzrIGv15E1qtdVTIeQ'
sup_id = 'IQYpa2gn6ocPcdte-LHXNk8VTVSrcFY6EzfJqux4Nw33wonDXugp6bChZm3bY5-hC2d-2g_17HfMGg'

#functions
# mh = list(watcher.match.matchlist_by_puuid(region, peng_id, type="ranked", start_time=1637809200, end_time=1639082241, count=100))
mh = list(watcher.match.matchlist_by_puuid(region, brunes_id, type="ranked", count=15))
last = mh[0]
match_stats = watcher.match.by_id(region, last)
champions = []
compte = []
final = []
newfinal = []
# puuids = ['fQwRacUndeCleiOeQi4qm4WTFuoqSZg7SXnQWeAepWZPZ6teQ7Aytl5wAoAG3ltsM_ZcNT904BbIUg', 'IDlMIxG2hN-fB3vUg4KuwpLKEZ73cMQhhoXyQf_mrdKYRHuAKgwq3wp8h3h8ny-peDTE6y_wS9omNg', '7ZYtr9dWdugLIH0u9vvQNAHqSreCq0mRzmbezoZzvGHivl5DN4HoJRBKXpGOKn0wEM4iIO3zMeV2iw'
#           , 'R9G6ILHKjrhY56vUAN-KAdAVx1Dn8J2kdPzpZq6hfF0q2gDRAMc7JywT5RVpVzrIGv15E1qtdVTIeQ', 'IQYpa2gn6ocPcdte-LHXNk8VTVSrcFY6EzfJqux4Nw33wonDXugp6bChZm3bY5-hC2d-2g_17HfMGg']


#get data
for i in mh:
    data = watcher.match.by_id(region, i)
    for j in range(10):
        if data['info']['participants'][j]['puuid'] == brunes_id or data['info']['participants'][j]['puuid'] == darlik_id:
            champ_name = data['info']['participants'][j]['championName']
            url1 = '=IMAGE("https://ddragon.leagueoflegends.com/cdn/11.8.1/img/champion/{}.png")'.format(champ_name)
            champions.append(url1)


for i in champions:
    compte.append(champions.count(i))

for i in range(len(champions)):
    final.append([champions[i], compte[i]])

for i in final:
    if i not in newfinal:
        newfinal.append(i)

#DATAFRAMES
df = pd.DataFrame(newfinal, columns=['Champion', 'Games'])
sorted_df = df.sort_values(by=['Games'], ascending=False)
# df.to_csv(r'matches.csv',sep=';',encoding="utf-8", index=False)
oplon_soloq.update('G1:H30', [sorted_df.columns.values.tolist()] + sorted_df.values.tolist()) #PRINT MIDLANE
# d2g.upload(df, spreadsheet_key, wks_name, credentials=credentials, row_names=True)
