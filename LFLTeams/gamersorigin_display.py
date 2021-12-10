#IMPORTS
from riotwatcher import LolWatcher, ApiError
import pandas as pd
import csv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from df2gspread import df2gspread as d2g

#GOOGLE SHEETS
scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('oplon.json', scope)
client = gspread.authorize(creds)
go_soloq = client.open("GAMERSORIGIN").sheet1

#VARIABLES
api_key = 'RGAPI-39f24dbd-8310-40d0-82a9-c58d7f3ccc54'
watcher = LolWatcher(api_key)
my_region = 'euw1'
region = 'europe'


#PUUIDS
vizicaci_id = '_ckb4SIYiIXBOsluBtlpHuIEm-6mlVy5el6oDPBxVnTja1AQBtTF4YIVVq5qJ9afwJ3_nfZORoHZPg'
karimkt_id = 'QQI0OndcLWeNYZ3H2lPhfPBSIemykok5fXfpS6Co_0tX1orc81a-4TNtsSFt3tU4uZ0fA2HPhIURoA'
ronaldo_id = '6We5vKAt5RHm5dN-c5A7U18eh8E-xvTbNMcyW-6DhJSWTYynGSpXKNJPgIzeFzWIX2B2CAsEZYPybw'
smiley_id = 'PFVBOMpcmw8obZR4ISRmNZUlxaNFdcOOSSceMkLzJr4umu9Y608Uxo6E-vDSABWLmaJdQ9H7k54q7Q'
enjawe_id = 'bLZVaQcBI8DNcF-NfxfXya6Nz-kIniFDD1Y3CORZ-d0Xr_R6fnouILhdEO8OYq8k8NLOVrT2Ahsx9A'
go = [vizicaci_id, karimkt_id, ronaldo_id, smiley_id, enjawe_id]

c = 0
#get data
for p in go:
    compte = []
    newfinal = []
    champions = []
    final = []
    # mh = list(watcher.match.matchlist_by_puuid(region, peng_id, type="ranked", start_time=1637809200, end_time=1639082241, count=100))
    mh = list(watcher.match.matchlist_by_puuid(region, p, type="ranked", count=25))
    for i in mh:
        data = watcher.match.by_id(region, i)
        for j in range(10):
            if data['info']['participants'][j]['puuid'] == p:
                champ_name = data['info']['participants'][j]['championName']
                url1 = '=IMAGE("https://ddragon.leagueoflegends.com/cdn/11.24.1/img/champion/{}.png")'.format(champ_name)
                champions.append(url1)
    for i in champions:
        compte.append(champions.count(i))

    for i in range(len(champions)):
        final.append([champions[i], compte[i]])

    for i in final:
        if i not in newfinal:
            newfinal.append(i)
    #DATAFRAMES
    if c == 0:
        print_loc = 'A:B'
    if c == 1:
        print_loc = 'C:D'
    if c == 2:
        print_loc = 'E:F'
    if c == 3:
        print_loc = 'G:H'
    if c == 4:
        print_loc = 'I:J'
    df = pd.DataFrame(newfinal, columns=['Champion', 'Games'])
    sorted_df = df.sort_values(by=['Games'], ascending=False)
    #df.to_csv(r'matches.csv',sep=';',encoding="utf-8", index=False)
    print(sorted_df)
    go_soloq.update("{}".format(print_loc), [sorted_df.columns.values.tolist()] + sorted_df.values.tolist(), value_input_option='USER_ENTERED') #PRINT MIDLANE
    # d2g.upload(df, spreadsheet_key, wks_name, credentials=credentials, row_names=True)
    c = c + 1
