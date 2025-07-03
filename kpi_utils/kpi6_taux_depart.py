import pandas as pd
from datetime import datetime

def kpi6_taux_depart(df_arrivees, df_sorties):
    df_a = df_arrivees.copy()
    df_s = df_sorties.copy()

    def parse_date(date_str):
        try:
            return pd.to_datetime(date_str, dayfirst=True)
        except:
            return pd.NaT

    df_a["Date d'arrivée"] = df_a["Date d'arrivée"].apply(parse_date)
    df_a["Date de fin (si applicable)"] = df_a["Date de fin (si applicable)"].apply(parse_date)
    df_s["Date de départ prévue"] = df_s["Date de départ prévue"].apply(parse_date)

    # Ne garder que les CDI
    df_a = df_a[df_a["Type de contrat"].str.lower() == "cdi"]
    df_s = df_s[df_s["Type de contrat"].str.lower() == "cdi"]

    # Filtrer les lignes avec dates valides
    df_s = df_s[~df_s["Date de départ prévue"].isna()]
    df_s = df_s[~df_s["Type de départ"].isna()]

    annee_min = df_s["Date de départ prévue"].dt.year.min()
    annee_max = datetime.today().year
    annees = range(annee_min, annee_max + 1)

    result = []

    for annee in annees:
        # Calcul de l'effectif moyen CDI cette année-là
        mois_total = 0
        for _, row in df_a.iterrows():
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

        effectif_moyen = mois_total / 12 if mois_total > 0 else 0

        # Comptage des départs CDI de chaque type cette année-là
        df_annee = df_s[df_s["Date de départ prévue"].dt.year == annee]
        depart_counts = df_annee["Type de départ"].value_counts()

        for type_depart, nb in depart_counts.items():
            taux = (nb / effectif_moyen) * 100 if effectif_moyen > 0 else 0
            result.append({
                "Année": annee,
                "Type de départ": type_depart,
                "Départs CDI": nb,
                "Effectif moyen CDI": round(effectif_moyen, 2),
                "Taux de départ (%)": round(taux, 1)
            })

    return pd.DataFrame(result)
