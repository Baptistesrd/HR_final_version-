import pandas as pd
from datetime import datetime

def kpi4_effectif_cdi_moyen(df_arrivees):
    df = df_arrivees.copy()

    def parse_date(date_str):
        try:
            return pd.to_datetime(date_str, dayfirst=True)
        except:
            return pd.NaT

    df["Date d'arrivée"] = df["Date d'arrivée"].apply(parse_date)
    df["Date de fin (si applicable)"] = df["Date de fin (si applicable)"].apply(parse_date)

    # Ne garder que les CDI hors stagiaires
    df = df[df["Type de contrat"].str.lower() == "cdi"]
    df = df[~df["Date d'arrivée"].isna()]

    annee_min = df["Date d'arrivée"].dt.year.min()
    annee_max = datetime.today().year
    annees = range(annee_min, annee_max + 1)

    result = []

    for annee in annees:
        mois_total = 0
        for _, row in df.iterrows():
            start = row["Date d'arrivée"]
            end = row["Date de fin (si applicable)"]

            if pd.isna(end) or end.year > annee:
                end = pd.Timestamp(f"{annee}-12-31")
            elif end.year < annee:
                continue
            else:
                end = min(end, pd.Timestamp(f"{annee}-12-31"))

            start_effective = max(start, pd.Timestamp(f"{annee}-01-01"))
            if start_effective > end:
                continue

            months = (end.year - start_effective.year) * 12 + (end.month - start_effective.month + 1)
            mois_total += months

        effectif_moyen = mois_total / 12
        result.append({"Année": annee, "Effectif moyen CDI (hors stages)": round(effectif_moyen, 2)})

    return pd.DataFrame(result)
