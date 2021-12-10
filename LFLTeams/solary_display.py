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
solary_soloq = client.open("SOLARY").sheet1

#VARIABLES
api_key = 'RGAPI-39f24dbd-8310-40d0-82a9-c58d7f3ccc54'
watcher = LolWatcher(api_key)
my_region = 'euw1'
region = 'europe'


#PUUIDS
kio_id = 'UNvaIyvlwP7WYSgcLgK3xK8AZmauunquBOawBx0muFGEyKY_x-hIwtMbW-eRzb3gTexwX6q63-A-YQ'
djoko_id = 'GHvYVU3vW7NH-NA-M-XuPlzqPHZFIvJEB16cRLtyderZhKS9V_uFT_hWIILp4zKxm1F4Zd4zBjPncw'
scarlet_id = 'g5zakEv_epiVxxWWRbt3z5IHW0epE2NSA-zThAa7Ux2vJrYDk0ky8JMdAeOMQBj0uC6dlxuVrFynCg'
asza_id = '0Y0HmC7kBqp63rUPoJOjKsLr8uZhLKYEc6DyHjdzmqGl0tUxSEFCODUnNj6h1y4R-XgkkKqMLFP5zA'
steelback_id = '9d0w3h7qjw5dGmkd2EfglqKu_AxBx5S0h40RF7IRDrx06snEgYl5BiLRjn5rICIKanA4phWFRTqfQA'
solary = [kio_id, djoko_id, scarlet_id, asza_id, steelback_id]


c = 0
#get data
for p in solary:
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
    solary_soloq.update("{}".format(print_loc), [sorted_df.columns.values.tolist()] + sorted_df.values.tolist(), value_input_option='USER_ENTERED') #PRINT MIDLANE
    # d2g.upload(df, spreadsheet_key, wks_name, credentials=credentials, row_names=True)
    c = c + 1
