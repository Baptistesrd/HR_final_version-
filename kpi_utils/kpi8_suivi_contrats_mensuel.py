import pandas as pd
from datetime import datetime

def kpi8_suivi_contrats_mensuel(df_arrivees):
    df = df_arrivees.copy()

    def parse_date(date_str):
        try:
            return pd.to_datetime(date_str, dayfirst=True)
        except:
            return pd.NaT

    df["Date d'arrivée"] = df["Date d'arrivée"].apply(parse_date)
    df["Date de fin (si applicable)"] = df["Date de fin (si applicable)"].apply(parse_date)

    df = df[~df["Date d'arrivée"].isna()]

    min_date = df["Date d'arrivée"].min().replace(day=1)
    max_date = datetime.today().replace(day=1)
    mois = pd.date_range(min_date, max_date, freq="MS")

    result = []

    for date in mois:
        snapshot = df[
            (df["Date d'arrivée"] <= date) &
            (
                df["Date de fin (si applicable)"].isna() |
                (df["Date de fin (si applicable)"] >= date)
            )
        ]
        counts = snapshot["Type de contrat"].value_counts().to_dict()
        counts["Mois"] = date.strftime("%Y-%m")
        result.append(counts)

    df_result = pd.DataFrame(result).fillna(0)
    cols = ["Mois"] + sorted([col for col in df_result.columns if col != "Mois"])
    return df_result[cols].astype({col: int for col in df_result.columns if col != "Mois"})
