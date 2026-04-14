import streamlit as st
import pandas as pd
import requests
import json

import datetime
from utils.jsonbin import save_key, load_key, del_first_count, load_data
from utils.login import login
from utils.count_tool import count_tool

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
        first_count.HemaDiff_tool(auf_oder_unter_zaehlen) # new class?
        zaehler = first_count.sum_of_leucocyte()
        st.write( zaehler ,"/100 Zellen") # after resetting the counting, this resets with delay.
    elif first_count.sum_of_leucocyte() == 100:
        st.success("Bei der aktuellen Zählung 100 Zellen ausgezählt.")

    elif second_count.sum_of_leucocyte() < 100: ## does not reach yet
        second_count.HemaDiff_tool(auf_oder_unter_zaehlen) # new class?
        zaehler = second_count.sum_of_leucocyte() 
        st.write( zaehler ,"/100 Zellen") # after resetting the counting, this resets with delay.
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
            first_count.reset()
            
    with col3: 
        if st.button('Zweite Zählung Löschen', use_container_width = True):
            second_count.reset() 

    if second_count.sum_of_leucocyte() > 0: # better would be to create one table with two counts
        st.table(second_count.Zählung_Dictionary())
    else:
        st.table(first_count.Zählung_Dictionary())

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
    zaehler = first_count.sum_of_leucocyte()
    #Laden der Speicher um Dataframe zu generieren 
    Speicherplatz = load_data(api_key_1, bin_id_1, st.session_state["username"])
    if len(Speicherplatz) == 0 and zaehler != 100:
        #Kann nicht bewertet werden, da noch keine 100 Zellen Zählung vorhanden ist.
        st.error("Noch keine 100 Zellen gezählt.")
    elif len(Speicherplatz) != 0 and zaehler == 100:
        #Wird mit weiteren if-Statement verschachtelt, da wir mit session_state zu tun haben.
        if len(Speicherplatz) == 1:
            #Wenn die Differenzierung mit 200 Zellen duchgeführt wurde. 
            Zählung_2 = second_count.Zählung_Dictionary() 
            Speicherplatz.append(Zählung_2)
            #die erste 100 Zellen Zählung mit den zweiten 100 Zellen Zählung zusammenfügen.
            del_first_count(api_key_1, bin_id_1,st.session_state["username"])
            #Session_State löschen.
            save_key(api_key_1, bin_id_1, st.session_state["username"],Speicherplatz)
            #erste und zweite Zählung speichern und somit vom session_state lösen.
            Speicherplatz= load_data(api_key_1, bin_id_1, st.session_state["username"])
            Speicherplatz= pd.DataFrame(Speicherplatz, index=["erste Zählung","zweite Zählung"]).T
            Speicherplatz=Speicherplatz["Mittelwert"]= (Speicherplatz["erste Zählung"]+Speicherplatz["zweite Zählung"])/2 
            Speicherplatz["Einheit"]="%"
            st.table(Speicherplatz)
        else:
            #Wenn else nicht definiert wird, wird die Speicherung wiederholen oder nur die erste Zählung anzeigen.
            Speicherplatz = load_data(api_key_1, bin_id_1, st.session_state["username"])
            Speicherplatz= pd.DataFrame(Speicherplatz, index=["erste Zählung","zweite Zählung"]).T
            Speicherplatz["Mittelwert"]= (Speicherplatz["erste Zählung"]+Speicherplatz["zweite Zählung"])/2 
            Speicherplatz["Einheit"]="%"            
            st.table(Speicherplatz)
    elif len(Speicherplatz) == 1:
        #Damit beim zweiten Zählung die erste Zählung noch ersichtlich ist.
        Zählung_1 = pd.DataFrame(Speicherplatz, index=["erste Zählung"]).T
        Zählung_1["Einheit"]= "%"
        st.table(Zählung_1)
    else:
    #Nicht gespeicherte Daten in Dataframe darstellen.        
        Zählung_1 = first_count.Zählung_Dictionary()
        Zählung_1 = pd.DataFrame(Zählung_1, index=["erste Zählung"]).T
        Zählung_1["Einheit"]="%"
        st.table(Zählung_1)
    st.write("Legende: ",A_B_C_D)

    if st.button("Alle Zählungen löschen"):
        first_count.reset()
        second_count.reset()


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
        if "Mittelwert" in Speicherplatz: 
            Jetzt = datetime.datetime.now().strftime("%Y-%M-%d %H:%M:%S")
            neue_Patient=dict(Speicherplatz["Mittelwert"])
            neue_Patient["Specherzeit"]= Jetzt
            neue_Patient["Identifikationsnummer"]=Identifikation
            neue_Patient["Erythrozyten Beurteilung"]=Erythrozyten_Beurteilung
            neue_Patient["Leukozyten Beurteilung"]=Leukozyten_Beurteilung
            neue_Patient["Thrombozyten Beurteilung"]=Thrombozyten_Beurteilung
            neue_Patient["Legende"]=A_B_C_D
            Patientenspeicherung.append(neue_Patient) 
            save_key(api_key_2, bin_id_2, st.session_state["username"],Patientenspeicherung)
            st.success("Erfolgreich gespeichert")
        elif zaehler != 100 and len(Speicherplatz) == 0:
            st.error("Die Speicherung kann erst nach mindestens 100 Zellen zählen stattfinden.")
        elif zaehler == 100 and len(Speicherplatz)== 0:
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
####################################################################################################################
#tab 4 
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

            

            
