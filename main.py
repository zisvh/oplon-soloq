from riotwatcher import LolWatcher, ApiError
import pandas as pd
import csv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from df2gspread import df2gspread as d2g

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'oplon.json', scope)
gc = gspread.authorize(credentials)
spreadsheet_key = '1EnZGfwWdwEH95sG84snaUfO5TVX3_L93POUVsoKWLrI'
wks_name = 'soloq'
# #GOOGLE SHEETS HANDLER
# scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
# creds = ServiceAccountCredentials.from_json_keyfile_name('oplon.json', scope)
# client = gspread.authorize(creds)

# oplon_soloq = client.open("OPL").sheet1
# # kc_soloq = client.open("KC").sheet1
# # mirage_soloq = client.open("MIRAGE").sheet1
# # vit_soloq = client.open("VITBEE").sheet1
# # ldlc_soloq = client.open("LDLCOL").sheet1
# # bds_soloq = client.open("BDS").sheet1
# # sly_soloq = client.open("SOLARY").sheet1
# # gw_soloq = client.open("GAMEWARD").sheet1
# # msf_soloq = client.open("MISFITS").sheet1
# # go_soloq = client.open("GO").sheet1

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
d2g.upload(df, spreadsheet_key, wks_name, credentials=credentials, row_names=True)
# oplon_soloq.update_cell(2,10, newfinal)

