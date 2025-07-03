import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

def load_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)

    SPREADSHEET_ID = "1s0lgJ_JX5Zt2UvFAqrU_GPeO_Zibx0mX3zwuSm4--jc"
    spreadsheet = client.open_by_key(SPREADSHEET_ID)

    sheet_arrivees = spreadsheet.worksheet("Arrivées")
    sheet_sorties = spreadsheet.worksheet("Sorties")

    # Arrivées (lignes 5 à 153)
    records_arr = sheet_arrivees.get_all_values()[4:153]
    headers_arr = sheet_arrivees.row_values(5)
    data_arrivees = pd.DataFrame(records_arr, columns=headers_arr)

    # Sorties (lignes 4 à 27)
    records_sort = sheet_sorties.get_all_values()[3:27]
    headers_sort = sheet_sorties.row_values(4)
    data_sorties = pd.DataFrame(records_sort, columns=headers_sort)

    return data_arrivees, data_sorties
