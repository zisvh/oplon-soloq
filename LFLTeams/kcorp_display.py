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
kcorp_soloq = client.open("KCORP").sheet1

#VARIABLES
api_key = 'RGAPI-39f24dbd-8310-40d0-82a9-c58d7f3ccc54'
watcher = LolWatcher(api_key)
my_region = 'euw1'
region = 'europe'


#PUUIDS
cabochard_id = 'ZMpXJRiDk9P80o0Zw2DcjDp1Gz_4BO2r0lAVJXlrHvBDScjQufceAbKS7GkBu0dvzHYwdoeMYfVqPA'
oot_id = '9NJ0NCAv3Fv5p5QUtcT7OtTU553bPtQCkH3G9wbH_kshEDWgnLe5vmIammDIrBri_k6E1QHI_9rqbQ'
saken_id = 'NEggEroC7Sq--QawFv2eI7WPDhhDiUmqRMM6S5e7vnmYHkzsq5rw8CdRQXOoy8z406Sdt3UyucIgnQ'
rekkles_id = 'yQ6TPrc7de4RRy-pC0KfyGPfXjdXYKHeUmksJ7JJXDbQE-rHZDQNejulN2t_OHRqyJp3-SWx1WfiVg'
hantera_id = 'aDNGiNZRWYMkFiCUVr55xX4N4TtCyxsz1NEhfPHrYJ9l4agbUQVw5dey3j0yvLCwi2QJ4z8k-KFb2w'
kcorp = [cabochard_id, oot_id, saken_id, rekkles_id, hantera_id]

c = 0
#get data
for p in kcorp:
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
    kcorp_soloq.update("{}".format(print_loc), [sorted_df.columns.values.tolist()] + sorted_df.values.tolist(), value_input_option='USER_ENTERED') #PRINT MIDLANE
    # d2g.upload(df, spreadsheet_key, wks_name, credentials=credentials, row_names=True)
    c = c + 1
