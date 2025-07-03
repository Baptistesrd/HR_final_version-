import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st

def load_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    # ✅ On utilise directement le secret en tant que dictionnaire
    service_account_info = st.secrets["gcp_service_account"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)

    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(st.secrets["spreadsheet_id"])

    sheet_arrivees = spreadsheet.worksheet("Arrivées")
    sheet_sorties = spreadsheet.worksheet("Sorties")

    data_arrivees = pd.DataFrame(sheet_arrivees.get_all_records(head=4))
    data_sorties = pd.DataFrame(sheet_sorties.get_all_records(head=4))

    return data_arrivees, data_sorties
