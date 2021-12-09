from oauth2client.service_account import ServiceAccountCredentials
import gspread

scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('oplon.json', scope)
client = gspread.authorize(creds)

oplon_soloq = client.open("OPL").sheet1
# kc_soloq = client.open("KC").sheet1
# mirage_soloq = client.open("MIRAGE").sheet1
# vit_soloq = client.open("VITBEE").sheet1
# ldlc_soloq = client.open("LDLCOL").sheet1
# bds_soloq = client.open("BDS").sheet1
# sly_soloq = client.open("SOLARY").sheet1
# gw_soloq = client.open("GAMEWARD").sheet1
# msf_soloq = client.open("MISFITS").sheet1
# go_soloq = client.open("GO").sheet1


oplon_soloq.update_cell(2,10, "Hello World")
