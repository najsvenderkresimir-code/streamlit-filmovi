import streamlit as st
import pandas as pd
from ucitaj import ucitaj_podatke

SHEET_URL = st.secrets["sheet_url"]
SHEET_NAME = "filmovi"
df, worksheet = ucitaj_podatke(SHEET_URL, SHEET_NAME)

df["GODINA"] = pd.to_numeric(df["GODINA"])
df["OCJENA"] = pd.to_numeric(df["OCJENA"])

st.title("Moji omiljeni filmovi")

st.subheader("Trenutni popis filmova")
st.dataframe(df)

st.subheader("Dodaj novi film")
naslov = st.text_input("NASLOV")
godina = st.number_input("GODINA", step=1, format="%d")
žanr = st.text_input("ŽANR")
ocjena = st.slider("OCJENA", 1,10)

if st.button("DOdaj film"):
    novi_red = [naslov, int(godina), žanr, ocjena]
    worksheet.append_row(novi_red)
    st.success("Film je dodan uspješno")
    st.rerun()

st.subheader("Pretraži filmove")
filtrirani = df.copy()

žanr_filt = st.text_input("Pretraži po žanru")
godina_filt = st.number_input("Pretraži po godini", step=1 , format="%d")

if žanr_filt:
    filtrirani = filtrirani[filtrirani["ŽANR"].str.contains(žanr_filt, case=False) ]

if godina_filt:
    filtrirani = filtrirani[filtrirani["GODINA"]== int(godina_filt)]

st.dataframe(filtrirani)

st.subheader("Brisanje filmova")

filmovi_opcije = df.apply(lambda row: f"{row["NASLOV"]} ({row["GODINA"]})" , axis=1).tolist()
film_za_brisanje = st.selectbox("Odaberi film za brisanje", options=filmovi_opcije)

if st.button("Izbriši film"):
    for idx, row in df.iterrows():
        if f"{row["NASLOV"]} ({row["GODINA"]})" == film_za_brisanje:
            worksheet.delete_rows(idx + 2)
            st.success("Film je uspješno obrisan")
            st.rerun

st.subheader("TOP TRI FILMA(Po ocjeni)")

top3 = df.sort_values(by= "OCJENA", ascending=False).head(3)
st.table(top3)


