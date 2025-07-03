import pandas as pd

def kpi3_turnover_par_pole_par_an(df):
    df = df.copy()
    df = df[df["Type de contrat"].str.lower() == "cdi"]
    df["Date d'arrivée"] = pd.to_datetime(df["Date d'arrivée"], dayfirst=True, errors="coerce")
    df["Date de fin (si applicable)"] = pd.to_datetime(df["Date de fin (si applicable)"], dayfirst=True, errors="coerce")
    
    df["Année d'arrivée"] = df["Date d'arrivée"].dt.year
    df["Année de fin"] = df["Date de fin (si applicable)"].dt.year

    turnover_data = []
    min_year = int(df["Année d'arrivée"].min())
    max_year = pd.Timestamp.today().year

    for year in range(min_year, max_year + 1):
        for pole in df["Pôle associé"].dropna().unique():
            en_poste = df[(df["Année d'arrivée"] <= year) & 
                          ((df["Année de fin"].isna()) | (df["Année de fin"] >= year)) &
                          (df["Pôle associé"] == pole)]
            partis = df[(df["Année de fin"] == year) & (df["Pôle associé"] == pole)]
            total = len(en_poste)
            if total == 0: continue
            taux = len(partis) / total * 100
            turnover_data.append({
                "Année": year,
                "Pôle": pole,
                "Effectif en poste": total,
                "Départs": len(partis),
                "Turnover (%)": round(taux, 1)
            })

    df_turnover = pd.DataFrame(turnover_data)
    df_turnover["Année"] = df_turnover["Année"].astype(int)
    return df_turnover
