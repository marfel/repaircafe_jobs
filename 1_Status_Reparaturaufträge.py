import os
import pickle

import streamlit as st
from streamlit_autorefresh import st_autorefresh
from defs import STATUS_INFO

PICKLE_DATEI = "jobs.pkl"
MAX_JOBS = 50

def lade_jobs():
    if os.path.exists(PICKLE_DATEI):
        with open(PICKLE_DATEI, "rb") as f:
            return pickle.load(f)
    else:
        return [{"id": i, "status": "IDLE"} for i in range(1, 51)]

st.set_page_config(page_title="Übersicht", layout="wide")

# Titel
st.title("Status Reparaturaufträge")


# Run the autorefresh about every 10000 milliseconds (10 seconds)
st_autorefresh(interval=10000, key="my_refresh_key")

# Jobs laden
jobs = lade_jobs()

# Zeige die ersten 10 Jobs in 5 Spalten (je 2 Jobs pro Spalte)
cols = st.columns(5)

for i in range(MAX_JOBS):
    job = jobs[i]
    job_id = job["id"]
    status = job["status"]
    farbe = STATUS_INFO[status]["bg_color"]
    textfarbe = STATUS_INFO[status]["text_color"]
    status_de = STATUS_INFO[status]["label"]
    # HTML für ein kleines farbiges Kästchen
    box_html = f"""
    <div style="
        background-color: {farbe};
        color: white;
        text-align: left;
        padding: 10px;
        margin-bottom: 10px;
        border-radius: 8px;
        color: {textfarbe};
        font-size: 24px;">
        <strong>{job_id:02d}</strong>
        – {status_de}
    </div>
    """
    # Verteile sie auf die 5 Spalten
    col_index = i % 5
    with cols[col_index]:
        st.markdown(box_html, unsafe_allow_html=True)
