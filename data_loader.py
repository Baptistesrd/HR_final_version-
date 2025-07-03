import streamlit as st
import gspread
import pandas as pd
import json
from oauth2client.service_account import ServiceAccountCredentials

def load_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    # 🔐 Lecture du credentials depuis les secrets
    service_account_info = json.loads(st.secrets["gcp_service_account"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)

    client = gspread.authorize(creds)

    SPREADSHEET_ID = "1s0lgJ_JX5Zt2UvFAqrU_GPeO_Zibx0mX3zwuSm4--jc"
    sheet_arrivees = client.open_by_key(SPREADSHEET_ID).worksheet("Arrivées")
    sheet_sorties = client.open_by_key(SPREADSHEET_ID).worksheet("Sorties")

    data_arrivees = pd.DataFrame(sheet_arrivees.get_all_records(head=4))
    data_sorties = pd.DataFrame(sheet_sorties.get_all_records(head=3))

    return data_arrivees, data_sorties
