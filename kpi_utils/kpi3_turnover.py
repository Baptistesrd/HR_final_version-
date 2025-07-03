import pandas as pd
from datetime import datetime

def kpi3_turnover_par_pole_par_an(df_arrivees):
    df = df_arrivees.copy()

    def parse_date(date_str):
        try:
            return pd.to_datetime(date_str, dayfirst=True)
        except:
            return pd.NaT

    df["Date d'arrivée"] = df["Date d'arrivée"].apply(parse_date)
    df["Date de fin (si applicable)"] = df["Date de fin (si applicable)"].apply(parse_date)

    # Ne garder que les CDI
    df = df[df["Type de contrat"].str.lower() == "cdi"]
    df = df[~df["Date d'arrivée"].isna()]

    annee_min = df["Date d'arrivée"].dt.year.min()
    annee_max = datetime.today().year
    annees = range(annee_min, annee_max + 1)

    result = []

    for annee in annees:
        for pole in df["Pôle associé"].dropna().unique():
            df_pole = df[df["Pôle associé"] == pole]

            # Effectif moyen CDI pour l’année = nombre de mois de présence cumulés / 12
            mois_presence_total = 0
            for _, row in df_pole.iterrows():
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
                mois_presence_total += months

            effectif_moyen = mois_presence_total / 12

            # Départs cette année
            nb_departs = df_pole[
                df_pole["Date de fin (si applicable)"].dt.year == annee
            ].shape[0]

            turnover = (nb_departs / effectif_moyen) if effectif_moyen > 0 else 0

            result.append({
                "Année": annee,
                "Pôle associé": pole,
                "Départs CDI": nb_departs,
                "Effectif moyen CDI": round(effectif_moyen, 2),
                "Turnover (%)": round(turnover * 100, 1)
            })

    return pd.DataFrame(result)

