import pandas as pd
from datetime import datetime

def kpi7_rupture_pe(df_arrivees):
    df = df_arrivees.copy()

    def parse_date(date_str):
        try:
            return pd.to_datetime(date_str, dayfirst=True)
        except:
            return pd.NaT

    df["Date d'arrivée"] = df["Date d'arrivée"].apply(parse_date)
    df["Date de fin (si applicable)"] = df["Date de fin (si applicable)"].apply(parse_date)

    # CDI uniquement
    df = df[df["Type de contrat"].str.lower() == "cdi"]

    # Filtrer ceux qui sont partis
    df = df[~df["Date de fin (si applicable)"].isna()]
    df["Durée en mois"] = (df["Date de fin (si applicable)"] - df["Date d'arrivée"]) / pd.Timedelta(days=30)

    df = df[~df["Durée en mois"].isna()]
    df["Année de départ"] = df["Date de fin (si applicable)"].dt.year

    grouped = df.groupby("Année de départ").agg(
        total_departs=("Nom", "count"),
        ruptures_pe=("Durée en mois", lambda x: (x < 8).sum())
    ).reset_index()

    grouped["% Ruptures PE"] = (grouped["ruptures_pe"] / grouped["total_departs"] * 100).round(1)

    return grouped.rename(columns={"Année de départ": "Année"})
