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
mirage_soloq = client.open("MIRAGE").sheet1

#VARIABLES
api_key = 'RGAPI-39f24dbd-8310-40d0-82a9-c58d7f3ccc54'
watcher = LolWatcher(api_key)
my_region = 'euw1'
region = 'europe'


#PUUIDS
badlulu_id = 'I4eGiizycCCoKveoGkwlNiqdNOHSaYcUkrD7f4VnQAuQQfLozN3FsTcIjY-_BBuQ6VcQ8hNuC_U3Zw'
memento_id = 'wzjJTTTy6y8dinNHAWVCsMsGhDlmP2xX-oiRGEzLzKl_pLOWix-tw_f7oKuztU8A_efINSlIrPwZCQ'
rangjun_id = 'LCuOswQ1ObRdGVKKX2GuMUwc-8IlIYW0wN6hbQJOJ9hHD2S2K-Elok_mYi_xKS9Ny_zy8zHbBDS-Eg'
codysun_id = 'LCuOswQ1ObRdGVKKX2GuMUwc-8IlIYW0wN6hbQJOJ9hHD2S2K-Elok_mYi_xKS9Ny_zy8zHbBDS-Eg'
raxxo_id = 'ZvZLcUp15T8cydr34ess6u2Kh13vwdEvOuQDtJS6uTUbPYFzn3CE9Mot2rndj_43KkogPsBwyOYOKQ'
mirage = [badlulu_id, memento_id, rangjun_id, codysun_id, raxxo_id]

c = 0
#get data
for p in mirage:
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
    mirage_soloq.update("{}".format(print_loc), [sorted_df.columns.values.tolist()] + sorted_df.values.tolist(), value_input_option='USER_ENTERED') #PRINT MIDLANE
    # d2g.upload(df, spreadsheet_key, wks_name, credentials=credentials, row_names=True)
    c = c + 1
