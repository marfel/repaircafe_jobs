import os
import pickle

import streamlit as st
from defs import STATUS_INFO

PICKLE_DATEI = "jobs.pkl"


def lade_jobs():
    if os.path.exists(PICKLE_DATEI):
        with open(PICKLE_DATEI, "rb") as f:
            return pickle.load(f)
    else:
        return [{"id": i, "status": "IDLE", "device": "?"} for i in range(1, 51)]


def speichere_jobs(jobs):
    with open(PICKLE_DATEI, "wb") as f:
        pickle.dump(jobs, f)


st.set_page_config(page_title="Auftragsmanager", layout="wide")

# Jobs laden
jobs = lade_jobs()

# Finde den Index des ersten Jobs, der NICHT "FINISHED" oder "CANCELED" ist
start_index = 0
while start_index < len(jobs):
    if jobs[start_index]["status"] not in ("FINISHED", "CANCELED"):
        break
    start_index += 1

# Prüfen, ob noch aktive Jobs vorhanden sind
if start_index >= len(jobs):
    st.write("Keine aktiven (offenen) Jobs vorhanden.")
else:
    # Zeige von start_index bis start_index + 19 (max. 20 Jobs)
    cols = st.columns(2)
    end_index = min(start_index + 20, len(jobs))
    zu_zeigende_jobs = jobs[start_index:end_index]

    for i, job in enumerate(zu_zeigende_jobs):
        job_id = job["id"]
        status = job["status"]
        device = job["device"]

        farbe = STATUS_INFO[status]["bg_color"]
        textfarbe = STATUS_INFO[status]["text_color"]
        status_de = STATUS_INFO[status]["label"]

        # HTML für ein kleines farbiges Kästchen
        box_html = f"""
        <div style="
            background-color: {farbe};
            color: white;
            text-align: center;
            padding: 5px;
            margin-bottom: 5px;
            border-radius: 8px;
            font-size: 20px;
            color: {textfarbe};">
            <strong>{job_id:02d}</strong>
        </div>
        """
        col_index = i % 2
        with cols[col_index].container(border=True):
            colA, colB = st.columns([2, 2], vertical_alignment="center")
            colA.markdown(box_html, unsafe_allow_html=True)
            job["device"] = colB.text_input(
                label="Gerät", value=device, key=f"device_{job_id}"
            )
            col1, col2, col3, col4, col5 = st.columns(5)

            # Button für jeden möglichen Status
            if col1.button("Leerlauf", key=f"idle_{job_id}"):
                job["status"] = "IDLE"
                speichere_jobs(jobs)
                st.rerun()

            if col2.button("Wartend", key=f"waiting_{job_id}"):
                job["status"] = "WAITING"
                speichere_jobs(jobs)
                st.rerun()

            if col3.button("Läuft", key=f"inprogress_{job_id}"):
                job["status"] = "IN_PROGRESS"
                speichere_jobs(jobs)
                st.rerun()

            if col4.button("Fertig", key=f"finished_{job_id}"):
                job["status"] = "FINISHED"
                speichere_jobs(jobs)
                st.rerun()

            if col5.button("Abbruch", key=f"canceled_{job_id}"):
                job["status"] = "CANCELED"
                speichere_jobs(jobs)
                st.rerun()

# Button zum Zurücksetzen aller Jobs
if st.sidebar.button("Alle Jobs zurücksetzen", type="primary"):
    for job in jobs:
        job["status"] = "IDLE"
        job["device"] = "?"
    speichere_jobs(jobs)
    st.rerun()
