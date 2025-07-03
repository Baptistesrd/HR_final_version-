import sys
import os
sys.path.append(os.path.dirname(__file__))

import streamlit as st
from data_loader import load_google_sheets
from kpi_utils.kpi1_effectif_par_contrat import kpi1_effectif_par_contrat
from kpi_utils.kpi3_turnover import kpi3_turnover_par_pole_par_an
from kpi_utils.kpi4_effectif_cdi_moyen import kpi4_effectif_cdi_moyen
from kpi_utils.kpi5_effectif_cdi_avec_stages import kpi5_effectif_cdi_avec_stages
from kpi_utils.kpi6_taux_depart import kpi6_taux_depart
from kpi_utils.kpi7_rupture_pe import kpi7_rupture_pe

# 🎨 UI Config
st.set_page_config(page_title="Dashboard RH", layout="wide")
st.title("📊 Dashboard RH – Suivi Dynamique des Effectifs et Départs")

try:
    # 🔁 Chargement des données
    arrivees_df, sorties_df = load_google_sheets()
    st.success("Connexion à Google Sheets réussie")

    # 🧹 Nettoyage rapide des données pour les filtres
    arrivees_df["Date d'arrivée"] = arrivees_df["Date d'arrivée"].astype(str)
    arrivees_df["Année arrivée"] = arrivees_df["Date d'arrivée"].str[-4:]
    arrivees_df = arrivees_df[arrivees_df["Année arrivée"].str.isnumeric()]

    # 📌 Filtres latéraux
    st.sidebar.header("Filtres")
    annees = sorted(arrivees_df["Année arrivée"].dropna().unique())
    types_contrats = sorted(arrivees_df["Type de contrat"].dropna().unique())
    poles = sorted(arrivees_df["Pôle associé"].dropna().unique())

    selected_years = st.sidebar.multiselect("Année d'arrivée", annees, default=annees)
    selected_contrats = st.sidebar.multiselect("Type de contrat", types_contrats, default=types_contrats)
    selected_poles = st.sidebar.multiselect("Pôle associé", poles, default=poles)

    # 🔎 Application des filtres
    arrivees_filtered = arrivees_df[
        arrivees_df["Année arrivée"].isin(selected_years) &
        arrivees_df["Type de contrat"].isin(selected_contrats) &
        arrivees_df["Pôle associé"].isin(selected_poles)
    ]

    # 📁 Deux onglets bien distincts
    onglet_effectifs, onglet_depart = st.tabs(["Effectifs", "Départs"])

    # --- ONGLET EFFECTIFS ---
    with onglet_effectifs:
        st.subheader("Effectif par type de contrat et par an")
        df_kpi1 = kpi1_effectif_par_contrat(arrivees_filtered)
        st.dataframe(df_kpi1, use_container_width=True, hide_index=True)

        st.markdown("---")
        st.subheader("Effectif CDI moyen annuel (hors stagiaires)")
        df_kpi4 = kpi4_effectif_cdi_moyen(arrivees_filtered)
        st.dataframe(df_kpi4, use_container_width=True, hide_index=True)

        st.markdown("---")
        st.subheader("Effectif total moyen annuel (CDI + stages)")
        df_kpi5 = kpi5_effectif_cdi_avec_stages(arrivees_filtered)
        st.dataframe(df_kpi5, use_container_width=True, hide_index=True)

    # --- ONGLET DÉPARTS ---
    with onglet_depart:
        st.subheader("Turnover par pôle et par an")
        df_kpi3 = kpi3_turnover_par_pole_par_an(arrivees_filtered)
        st.dataframe(df_kpi3, use_container_width=True, hide_index=True)

        st.markdown("---")
        st.subheader("Taux de départ CDI par type de sortie")
        df_kpi6 = kpi6_taux_depart(arrivees_df, sorties_df)
        st.dataframe(df_kpi6, use_container_width=True, hide_index=True)

        st.markdown("---")
        st.subheader("Ruptures de période d’essai (< 8 mois)")
        df_kpi7 = kpi7_rupture_pe(arrivees_filtered)
        st.dataframe(df_kpi7, use_container_width=True, hide_index=True)

except Exception as e:
    st.error("Erreur de chargement des données.")
    st.exception(e)
