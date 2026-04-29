import streamlit as st
import pandas as pd

import datetime
from utils.jsonbin import save_key, load_key
from utils.login import login
from utils.hematology_differential import HematologyDifferential
from utils.manipulate_session_state import copy_default_count_categories

jsonbin_secrets = st.secrets["jsonbin"]
api_key = jsonbin_secrets["api_key"]
bin_id = jsonbin_secrets["bin_id"]

login()

st.title("manuelle Differenzierung (Blutbilder)")

tab1, tab2, tab3 = st.tabs(["Tastatur", "Beurteilung", "Resultat"])

first_count = HematologyDifferential("first_count")
first_count.initialize_session_state()

second_count = HematologyDifferential("second_count")
second_count.initialize_session_state()

with tab1:  
    st.header("Tastatur ⌨️")
    Identifikation = st.text_input("Identifikationsnummer")

    st.write("---")
    auf_oder_unter_zaehlen = st.radio("", ('addieren', 'subtrahieren'))
    
    if first_count.get_total_leukocytes() < 100:
        first_count.render_differential_counter(auf_oder_unter_zaehlen)

        if first_count.get_total_leukocytes() == 100:
            st.success("Bei der aktuellen Zählung 100 Zellen ausgezählt.")
            st.rerun() 

    elif second_count.get_total_leukocytes() < 100:
        second_count.render_differential_counter(auf_oder_unter_zaehlen)

    else:
        st.success("Du hast 200 Zellen ausgezählt")

    with st.expander("A/B/C/D"):
        st.write('''Die Tasten A, B, C und D sind für spezielle Zellen wie Gumprecht'sche Kernschatten, Haarzellen und andere Auffälligkeiten während der hundert Zellen-Zählung vorgesehen. Während "C" und "D" nicht in die 100 Zellen gezählt werden, werden "A" und "B" in die Zählung einbezogen. Beachte bitte, dass der "Normoblast" nicht zu den Leukozyten gehört und daher nicht zu den hundert Zellen zählt.''')
    A_B_C_D= st.text_input('Spezifiziere Zelltypen für A, B, C, D Tasten im Textfeld.')
    st.write("---")  
    
    col1, col2, col3 = st.columns(3) # for compact key layout

    with col1:
        if st.button("Zählung beenden", use_container_width = True):
            if (first_count.get_total_leukocytes() + second_count.get_total_leukocytes()) >= 100:
                st.info('Du kannst im Tab "Beurteilung" das Blutbild beurteilen.')
            else:
                st.error("Zähle 100 Zellen aus")
                 
    with col2:
        if st.button("Erste Zählung Löschen", use_container_width = True): 
            copy_default_count_categories(first_count.count_times, second_count.count_times)
            second_count.reset_all_counts()
            st.rerun()
            
    with col3: 
        if st.button('Zweite Zählung Löschen', use_container_width = True):
            second_count.reset_all_counts() 
            st.rerun()
    df_all_counts = pd.DataFrame([first_count.get_combined_counts(), second_count.get_combined_counts()], index =["Erste Zählung", "Zweite Zählung"]).T
    st.table(df_all_counts)

with tab2:
    st.header("Beurteilung ✒️")
    st.caption("In den dafür vorgesehenen Feldern kannst du die Beurteilungen der Blutbilder eintragen. Achte darauf, dass die Mengenangaben sowohl in Worten als auch durch Kreuze angegeben werden können.")
    
    Erythrozyten_Beurteilung = st.text_area("Erythrozyten Beurteilung")
    Leukozyten_Beurteilung = st.text_area("Leukozyten Beurteilung")
    Thrombozyten_Beurteilung = st.text_area("Thrombozyten Beurteilung")
    
    st.write("Im Tab 'Resultate' findest du eine Übersicht und Bewertung deiner eingetragenen Daten, wo du sie überprüfen und auswerten kannst.")

with tab3:
    st.header('Resultate 📄') 
    st.write("In diesem Tab hast du die Möglichkeit, die Zählungen zu löschen oder zu speichern. Die Zählung kann hier manuell vorgenommen werden.")
    st.subheader(Identifikation)
    st.subheader("Zählung")

    if first_count.get_total_leukocytes() != 100:
        st.error("Noch keine 100 Zellen gezählt.")
    else: 
        if first_count.get_total_leukocytes():
            result = first_count.get_combined_counts() 
            index = ["Erste Zählung"]
        if second_count.get_total_leukocytes() == 100:
            result = (first_count.get_combined_counts(), second_count.get_combined_counts()) 
            index = ["Erste Zählung", "Zweite Zählung"]
        df_result = pd.DataFrame(result, index = index).T
        df_result["Mittelwert"]= df_result.mean(axis=1,)
        df_result["Einheit"] = "%"
        st.table(df_result)
    st.subheader("Beurteilung")
    st.write('Änderungen können nur im Tab "Beurteilung" durchgeführt werden.')
    if len(Erythrozyten_Beurteilung) == 0 and len(Leukozyten_Beurteilung) == 0 and len(Thrombozyten_Beurteilung) == 0:
        st.error("Noch keine Beurteilung vorhanden.")
    elif len(Erythrozyten_Beurteilung) != 0 and len(Leukozyten_Beurteilung) != 0 and len(Thrombozyten_Beurteilung) != 0:
        
        st.write("<p style='font-weight: bold;'>Erythrozyten Beurteilung: </p>",Erythrozyten_Beurteilung, unsafe_allow_html=True)
        st.write("---")
        st.write("<p style='font-weight: bold;'>Leukozyten Beurteilung: </p>", Leukozyten_Beurteilung, unsafe_allow_html=True)
        st.write("---")
        st.write("<p style='font-weight: bold;'>Thrombozyten Beurteilung: </p>", Thrombozyten_Beurteilung, unsafe_allow_html=True)

    else:
        st.error("Beurteilung nicht vollständig ausgefüllt.")
    st.write("---")

    
    if st.button("Speicherung"):
        Patientenspeicherung = load_key(api_key, bin_id, st.session_state["username"])
        if Identifikation == "":
            st.error("Die Identifikationsnummer ist leer")
        elif (Erythrozyten_Beurteilung == "" ) or (Leukozyten_Beurteilung == "") or (Thrombozyten_Beurteilung == ""):
            st.error("Beurteilung nicht vollständig oder nicht ausgefüllt.")
        
        elif "Mittelwert" in df_result: 
            neue_Patient = df_result.to_dict()
            neue_Patient["Specherzeit"]= datetime.datetime.now().strftime("%Y-%M-%d %H:%M:%S")
            neue_Patient["Identifikationsnummer"] = Identifikation
            neue_Patient["Erythrozyten Beurteilung"] = Erythrozyten_Beurteilung
            neue_Patient["Leukozyten Beurteilung"] = Leukozyten_Beurteilung
            neue_Patient["Thrombozyten Beurteilung"] = Thrombozyten_Beurteilung
            neue_Patient["Legende"] = A_B_C_D
            Patientenspeicherung.append(neue_Patient) 

            save_key(api_key, bin_id, st.session_state["username"], Patientenspeicherung)
            st.success("Erfolgreich gespeichert")
        elif first_count.get_total_leukocytes() != 100:
            st.error("Die Speicherung kann erst nach mindestens 100 Zellen zählen stattfinden.")

            

            
