import pandas as pd
from datetime import datetime

def kpi1_effectif_par_contrat(df_arrivees):
    df = df_arrivees.copy()

    # Nettoyage des dates
    def parse_date(date_str):
        try:
            return pd.to_datetime(date_str, dayfirst=True)
        except:
            return pd.NaT

    df["Date d'arrivée"] = df["Date d'arrivée"].apply(parse_date)
    df["Date de fin (si applicable)"] = df["Date de fin (si applicable)"].apply(parse_date)

    # Supprimer les lignes sans Date d'arrivée
    df = df[~df["Date d'arrivée"].isna()]

    # Extraire les années utiles
    annee_min = df["Date d'arrivée"].dt.year.min()
    annee_max = datetime.today().year + 1
    annees = range(annee_min, annee_max + 1)

    # Initialiser le résultat
    result = []

    for annee in annees:
        df_present = df[
            (df["Date d'arrivée"].dt.year <= annee) &
            (
                df["Date de fin (si applicable)"].isna() |
                (df["Date de fin (si applicable)"].dt.year >= annee)
            )
        ]

        counts = df_present["Type de contrat"].value_counts()
        row = {"Année": annee}
        row.update(counts.to_dict())
        result.append(row)

    df_result = pd.DataFrame(result).fillna(0).sort_values(by="Année")
    df_result = df_result.set_index("Année")

    return df_result.astype(int)
