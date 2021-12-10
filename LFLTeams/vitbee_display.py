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
vitbee_soloq = client.open("VITBEE").sheet1

#VARIABLES
api_key = 'RGAPI-39f24dbd-8310-40d0-82a9-c58d7f3ccc54'
watcher = LolWatcher(api_key)
my_region = 'euw1'
region = 'europe'


#PUUIDS
szygenda_id = 'lS3ZNocWRHnwfmkgfNKpL7OAQfyjB1XR8vTxAEdtAF32OXldQje_ekEpeDk225PDl9e1nBQhS_KArQ'
skeanz_id = 'OdAfgss9YvAkPY22dOfhR_mNUOkdsYuCWN4QtxK4uaoDjy5mX6Wo-QqS34hL1L2_RIcCSxT886EnpQ'
diplex_id = 'o54DZQyqdpNuY82LsIJoPfJ_2Nn7wR3VwcaGeeXi-bMx4rD8lkJVaJ4aw7_RUiRqMFSfQ3LdV0mFgw'
jeskla_id = 'wC-FTrnZ-zG-z4WneNSu7PO-wn7obxgfxolwE245QGKWokA4V4A5g-e5BTqBEagDOL8N6n49Os7eQg'
jactroll_id = '0FBP13KJ7SPWYj532cIqeJAyuZzbPXklu8LRNwSBYpR61Sdj68W8C04C6HxU6h4SjuVYy1E5WgRrXQ'
vitbee = [szygenda_id, skeanz_id, diplex_id, jeskla_id, jactroll_id]

c = 0
#get data
for p in vitbee:
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
    vitbee_soloq.update("{}".format(print_loc), [sorted_df.columns.values.tolist()] + sorted_df.values.tolist(), value_input_option='USER_ENTERED') #PRINT MIDLANE
    # d2g.upload(df, spreadsheet_key, wks_name, credentials=credentials, row_names=True)
    c = c + 1
