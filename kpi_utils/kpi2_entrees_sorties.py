import pandas as pd
from datetime import datetime

def kpi2_entrees_sorties(arrivees_df):
    df = arrivees_df.copy()

    def parse_date(date_str):
        try:
            return pd.to_datetime(date_str, dayfirst=True)
        except:
            return pd.NaT

    df["Date d'arrivée"] = df["Date d'arrivée"].apply(parse_date)
    df["Date de fin (si applicable)"] = df["Date de fin (si applicable)"].apply(parse_date)

    # Exclure les stagiaires
    df = df[df["Type de contrat"].str.lower() != "stage"]

    # Préparer les entrées
    entrees = df[~df["Date d'arrivée"].isna()].copy()
    entrees["Année"] = entrees["Date d'arrivée"].dt.year
    entrees["Mois"] = entrees["Date d'arrivée"].dt.strftime("%b")
    entrees["Entrées"] = 1

    # Préparer les sorties
    sorties = df[~df["Date de fin (si applicable)"].isna()].copy()
    sorties["Année"] = sorties["Date de fin (si applicable)"].dt.year
    sorties["Mois"] = sorties["Date de fin (si applicable)"].dt.strftime("%b")
    sorties["Sorties"] = 1

    # Colonnes communes pour le groupby
    group_cols = ["Année", "Mois", "Type de contrat", "Pôle associé"]

    entrees_grouped = entrees.groupby(group_cols)["Entrées"].sum().reset_index()
    sorties_grouped = sorties.groupby(group_cols)["Sorties"].sum().reset_index()

    # Merge pour avoir entrées & sorties dans le même tableau
    merged = pd.merge(entrees_grouped, sorties_grouped, how="outer", on=group_cols).fillna(0)
    merged["Entrées"] = merged["Entrées"].astype(int)
    merged["Sorties"] = merged["Sorties"].astype(int)

    # Trie les mois dans l’ordre réel
    mois_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    merged["Mois"] = pd.Categorical(merged["Mois"], categories=mois_order, ordered=True)

    merged = merged.sort_values(by=["Année", "Mois", "Pôle associé", "Type de contrat"])

    return merged
