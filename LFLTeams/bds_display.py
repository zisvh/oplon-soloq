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
bds_soloq = client.open("BDS").sheet1

#VARIABLES
api_key = 'RGAPI-39f24dbd-8310-40d0-82a9-c58d7f3ccc54'
watcher = LolWatcher(api_key)
my_region = 'euw1'
region = 'europe'


#PUUIDS
agressivo_id = 'mGZh_Bz29334fOhBuAOWJ9O_qowVBhLMiEUjSyrXVul8bbIgdk7-m7L4B_9wzW7JLk8QfyreaaI78Q'
sheo_id = 'jGQ_E6phyVljpkq_neCqhUErCeAIj7-E76v_WwGIkz_TYaRtj9PTpmG63FFP3QY_E5Lmae7Q61txPQ'
xico_id = 'NujDUF0MVLd4lD1lrwz3sodZMCBlMrAs1LananRrnbozX9npzMQaoh2RgC1bfKFTwHfVdtNCBWHAzg'
crownshot_id = '8u3bQjr1v8ndXOh3KPPCwD_fDM0KgAjvcC8vBjfIRhfb4dQDYZFzEiVBYZn4WTHiB_XRlxeQbwT6cw'
erdote_id = 'jxgM7z509FV1hTlojjAI90dkzt50PUnmuCT2gHZP2kiAm2qW-tpjWiHiGwNNDmAdacbsycHVajvDbw'
bds = [agressivo_id, sheo_id, xico_id, crownshot_id, erdote_id]

c = 0
#get data
for p in bds:
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
    bds_soloq.update("{}".format(print_loc), [sorted_df.columns.values.tolist()] + sorted_df.values.tolist(), value_input_option='USER_ENTERED') #PRINT MIDLANE
    # d2g.upload(df, spreadsheet_key, wks_name, credentials=credentials, row_names=True)
    c = c + 1
