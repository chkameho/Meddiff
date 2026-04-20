import streamlit as st
import pandas as pd
import requests
import json

import datetime
from utils.jsonbin import save_key, load_key, del_first_count, load_data
from utils.login import login
from utils.count_tool import count_tool
from utils.manipulate_session_state import transfer_count

jsonbin_secrets_1 = st.secrets["jsonbin_1"]
api_key_1 = jsonbin_secrets_1["api_key"]
bin_id_1 = jsonbin_secrets_1["bin_id"]

jsonbin_secrets_2 = st.secrets["jsonbin_2"]
api_key_2 = jsonbin_secrets_2["api_key"]
bin_id_2 = jsonbin_secrets_2["bin_id"]

hugging_face=st.secrets["hugging_face"]
token = hugging_face["token"]

login()

st.title("manuelle Differenzierung (Blutbilder)")
st.write(st.session_state)

tab1, tab2, tab3, tab4 = st.tabs(["Tastatur", "Beurteilung", "Resultat", " Zellen Identifizieren"])

first_count = count_tool("first_count")
first_count.initialize_session_state()

second_count = count_tool("second_count")
second_count.initialize_session_state()

with tab1:  
    st.header("Tastatur ⌨️")
    Identifikation = st.text_input("Identifikationsnummer")
    st.write("---")
    auf_oder_unter_zaehlen = st.radio("", ('addieren', 'subtrahieren'))
    
    if first_count.sum_of_leucocyte() < 100:
        first_count.HemaDiff_tool(auf_oder_unter_zaehlen)

        if first_count.sum_of_leucocyte() == 100:
            st.success("Bei der aktuellen Zählung 100 Zellen ausgezählt.")
            st.rerun() 

    elif second_count.sum_of_leucocyte() < 100:
        second_count.HemaDiff_tool(auf_oder_unter_zaehlen)

    else:
        st.success("Du hast 200 Zellen ausgezählt")

    with st.expander("A/B/C/D"):
        st.write('''Die Tasten A, B, C und D sind für spezielle Zellen wie Gumprecht'sche Kernschatten, Haarzellen und andere Auffälligkeiten während der hundert Zellen-Zählung vorgesehen. Während "C" und "D" nicht in die 100 Zellen gezählt werden, werden "A" und "B" in die Zählung einbezogen. Beachte bitte, dass der "Normoblast" nicht zu den Leukozyten gehört und daher nicht zu den hundert Zellen zählt.''')
    A_B_C_D= st.text_input('Spezifiziere Zelltypen für A, B, C, D Tasten im Textfeld.')
    st.write("---")  
    
    col1, col2, col3 = st.columns(3) # for compact key layout

    with col1:
        if st.button("Zählung beenden", use_container_width = True):
            if (first_count.sum_of_leucocyte() + second_count.sum_of_leucocyte()) >= 100:
                st.info('Du kannst im Tab "Beurteilung" das Blutbild beurteilen.')
            else:
                st.error("Zähle 100 Zellen aus")
                 
    with col2:
        if st.button("Erste Zählung Löschen", use_container_width = True): 
            transfer_count(first_count.count_times, second_count.count_times)
            second_count.reset()
            st.rerun()
            
    with col3: 
        if st.button('Zweite Zählung Löschen', use_container_width = True):
            second_count.reset() 
            st.rerun()
    df_all_counts = pd.DataFrame([first_count.Zählung_Dictionary(), second_count.Zählung_Dictionary()], index =["Erste Zählung", "Zweite Zählung"]).T
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

    if first_count.sum_of_leucocyte() != 100:
        st.error("Noch keine 100 Zellen gezählt.")
    else: 
        if first_count.sum_of_leucocyte():
            result = first_count.Zählung_Dictionary() 
            index = ["Erste Zählung"]
        if second_count.sum_of_leucocyte() == 100:
            result = (first_count.Zählung_Dictionary(), second_count.Zählung_Dictionary()) 
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
        #zeigt Beurteilung an. Und Überschrift mit dickere Schrift.
        st.write("<p style='font-weight: bold;'>Erythrozyten Beurteilung: </p>",Erythrozyten_Beurteilung, unsafe_allow_html=True)
        st.write("---")
        st.write("<p style='font-weight: bold;'>Leukozyten Beurteilung: </p>", Leukozyten_Beurteilung, unsafe_allow_html=True)
        st.write("---")
        st.write("<p style='font-weight: bold;'>Thrombozyten Beurteilung: </p>", Thrombozyten_Beurteilung, unsafe_allow_html=True)

    else:
        st.error("Beurteilung nicht vollständig ausgefüllt.")
    st.write("---")
    if st.button("Speicherung"):
        Patientenspeicherung = load_key(api_key_2,bin_id_2, st.session_state["username"])
        if "Mittelwert" in df_result: 
            Jetzt = datetime.datetime.now().strftime("%Y-%M-%d %H:%M:%S")
            neue_Patient=dict(df_result["Mittelwert"])
            neue_Patient["Specherzeit"]= Jetzt
            neue_Patient["Identifikationsnummer"]=Identifikation
            neue_Patient["Erythrozyten Beurteilung"]=Erythrozyten_Beurteilung
            neue_Patient["Leukozyten Beurteilung"]=Leukozyten_Beurteilung
            neue_Patient["Thrombozyten Beurteilung"]=Thrombozyten_Beurteilung
            neue_Patient["Legende"]=A_B_C_D
            Patientenspeicherung.append(neue_Patient) 
            save_key(api_key_2, bin_id_2, st.session_state["username"],Patientenspeicherung)
            st.success("Erfolgreich gespeichert")
        elif first_count.sum_of_leucocyte() != 100:
            st.error("Die Speicherung kann erst nach mindestens 100 Zellen zählen stattfinden.")
        elif first_count.sum_of_leucocyte() == 100:
            neue_Patient= first_count.Zählung_Dictionary()
            Jetzt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            neue_Patient["Speicherzeit"]= Jetzt
            neue_Patient["Identifikationsnummer"]=Identifikation
            neue_Patient["Erythrozyten Beurteilung"]=Erythrozyten_Beurteilung
            neue_Patient["Leukozyten Beurteilung"]=Leukozyten_Beurteilung
            neue_Patient["Thrombozyten Beurteilung"]=Thrombozyten_Beurteilung
            neue_Patient["Legende"]=A_B_C_D
            Patientenspeicherung.append(neue_Patient)
            save_key(api_key_2, bin_id_2, st.session_state["username"],Patientenspeicherung)
            st.success("Erfolgreich gespeichert")

    with tab4:
        # Define the API endpoint
        st.header("Zellen Identifizieren 📷")
        st.write("Wenn eine Zelle nicht erkannt wird, kannst du das untenstehende System zur Klassifizierung der Leukozyten verwenden. Beachte, dass das API nur die reifen Formen der eosinophilen, neutrophilen, basophilen, lymphozytären und monozytären Reihe erkennt. Die Score-Werte näher an Eins deuten auf eine höhere Sicherheit der API-Antwort hin.")
        API_URL = "https://api-inference.huggingface.co/models/polejowska/swin-tiny-patch4-window7-224-lcbsi-wbc"

        # Set your authorization header with your token
        headers = {"Authorization": "Bearer " + token}

        # Load the image
        image_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
        
        if image_file is not None:
            image_bytes = image_file.read()
            # Send a POST request to the API with the image data and headers
            response = requests.post(API_URL, headers=headers, data=image_bytes)
            # Get the predicted class from the response
            result = json.loads(response.content.decode())
            if "error" in result:
                st.error("Derzeit gibt es einen internen Serverfehler. Bitte versuchen Sie die Seite neu zu laden, um das Problem zu beheben. Beachten Sie jedoch, dass beim Neustart möglicherweise die Zählungen verloren gehen.")
            else:
                result = pd.DataFrame(result)
                st.write(result)
            st.image(image_file)

            

            
