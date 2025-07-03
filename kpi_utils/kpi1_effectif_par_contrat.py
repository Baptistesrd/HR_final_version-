import pandas as pd

def kpi1_effectif_par_contrat(df):
    df = df.copy()
    df = df[df["Date d'arrivée"].str.contains(r"\d{2}/\d{2}/\d{4}", na=False)]
    df["Date d'arrivée"] = pd.to_datetime(df["Date d'arrivée"], dayfirst=True, errors="coerce")
    df["Année"] = df["Date d'arrivée"].dt.year
    df = df[df["Année"].notna()]
    df["Année"] = df["Année"].astype(int)
    
    df["Date de fin (si applicable)"] = pd.to_datetime(df["Date de fin (si applicable)"], dayfirst=True, errors="coerce")
    
    result = []
    for year in sorted(df["Année"].unique()):
        snapshot = df[(df["Date d'arrivée"].dt.year <= year) & (
            df["Date de fin (si applicable)"].isna() | (df["Date de fin (si applicable)"].dt.year >= year)
        )]
        counts = snapshot["Type de contrat"].value_counts().to_dict()
        counts["Année"] = year
        result.append(counts)

    df_result = pd.DataFrame(result).fillna(0)
    df_result["Année"] = df_result["Année"].astype(int)
    cols = ["Année"] + [col for col in df_result.columns if col != "Année"]
    return df_result[cols]
