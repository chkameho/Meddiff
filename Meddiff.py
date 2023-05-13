import streamlit as st
import pandas as pd
import yaml
from yaml.loader import SafeLoader
import datetime
from jsonbin import save_key, load_key, del_erste_Zählung_
import streamlit_authenticator as stauth
################################################################################################################################################################
#secrets
#Jsonbin_1
jsonbin_secrets_1 = st.secrets["jsonbin_1"]
api_key_1 = jsonbin_secrets_1["api_key"]
bin_id_1 = jsonbin_secrets_1["bin_id"]

#Jsonbin_2
jsonbin_secrets_2 = st.secrets["jsonbin_2"]
api_key_2 = jsonbin_secrets_2["api_key"]
bin_id_2 = jsonbin_secrets_2["bin_id"]
# -------- user login --------
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
)

fullname, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status == True:   # login successful
    authenticator.logout('Logout', 'main')   # show logout button
elif authentication_status == False:
    st.error('Username/password is incorrect')
    st.stop()
elif authentication_status == None:
    st.warning('Please enter your username and password')
    st.stop()

#############################################################################################################
#Neu
# Laden des aktuellen Session State
current_session_state = st.session_state

# Kopieren des aktuellen Session State in einen neuen Session State mit einem neuen Namen
logged_in_session_state = current_session_state

# Ändern des Session State-Namens
logged_in_session_state["Einloggen"] = "logged_in_session_state"
    
    
    ###########################################################################################################
##################################################################################################################################################################
# Funktion zum Laden aus einer Jsonbin-Datei

def load_data():
    load_key(api_key_1, bin_id_1, username)




# Funktion zum Speichern in einer JSON-Datei

def save_data(data):
    return save_key(api_key_1, bin_id_1, username, address_list)

def load_data_1():
    return load_key(api_key_2,bin_id_2, username)

# Funktion zum Speichern in einer JSON-Datei
def save_data_1(data):
    return save_key(api_key_2, bin_id_2, username, address_list)

def del_erste_Zählung():
    return del_erste_Zählung_(api_key_1, bin_id_1)  

def Tastatur_Blutbild_Differenzierung():  
    # Generiert ein Tastatur für die Blutbiddifferenzierung 
    #st.session_state wird gebraucht,damit die Zählung gelingt.
       
    # ein neues Dictionary erstellen, um die Variablen zu gruppieren
    my_group = {
        'Basophilen': 0,
        'Monozyten': 0,
        'Blasten': 0,
        'A': 0,
        'Eosinophilen': 0,
        'Lymphozyten': 0,
        'Promyelozyten': 0,
        'B': 0,
        'Normoblast': 0,
        'Segmentierten': 0,
        'Myelozyten': 0,
        'C': 0,
        'Plasmazellen': 0,
        'Stabkernigen': 0,
        'Metamyelozyten': 0,
        'D': 0
    }

    # neue Gruppe im session_state erstellen und ihr das Dictionary zuweisen
    if 'meine_gruppe' not in st.session_state:
         st.session_state.meine_gruppe = my_group


    #Um Tastatur, wie im Realität zu imitieren, werden die Tastatur in 4 Reihen aufgeteilt. 
    col1, col2, col3, col4 = st.columns(4)
    if zaehler <= 99:
       with col1:
           if st.button('Basophile')!= 0:
               st.session_state.meine_gruppe.Basophilen += 1


           if st.button('Monozyt') != 0:
               st.session_state.meine_gruppe.Monozyten += 1


           if  st.button('Blast')!= 0:
               st.session_state.meine_gruppe.Blasten += 1


           if st.button('A'):
               st.session_state.meine_gruppe.A += 1


       with col2:
           if st.button('Eosinophil') != 0:
               st.session_state.meine_gruppe.Eosinophilen += 1


           if st.button('Lymphozyt') != 0:
               st.session_state.meine_gruppe.Lymphozyten += 1


           if st.button('Promyelozyt') != 0:
               st.session_state.meine_gruppe.Promyelozyten += 1
           if st.button('B'):
               st.session_state.meine_gruppe.B += 1



       with col3:
           if st.button('Normoblast') != 0:
               st.session_state.meine_gruppe.Normoblast += 1

           if st.button('Segmentiert') != 0:
               st.session_state.meine_gruppe.Segmentierten += 1


           if st.button('Myelozyt') != 0:
               st.session_state.meine_gruppe.Myelozyten += 1
           if st.button('C'):
               st.session_state.meine_gruppe.C += 1

 
       with col4:
           if st.button('Plasmazelle') != 0:
               st.session_state.meine_gruppe.Plasmazellen += 1


           if st.button('Stabkernige') != 0:
               st.session_state.Stabkernigen += 1
   

           if st.button('Metamyelozyt') != 0:
               st.session_state.Metamyelozyten += 1
           if st.button('D'):
               st.session_state.D += 1

    elif zaehler == 100:
        return st.session_state.meine_gruppe
    
    return st.write( zaehler ,"/100 Zellen")       

def Zählung_Dictionary():
    #Regeneriert die Zählung in session_state zu Dictionary
    Dictionary = {}
    for key in st.session_state.keys():
        Dictionary[key]=st.session_state.meine_gruppe[key]
    return Dictionary

def clear_session_state():
    #löscht den session_state
    for key in st.session_state.meine_gruppe.keys():
        del st.session_state.meine_gruppe[key]
        if key in globals():
            del globals()[key]

def clear_all():
    for key in st.session_state.meine_gruppe.keys():
            del st.session_state.meine_gruppe[key]
            if key in globals():
                del globals()[key]
    return del_erste_Zählung_(api_key_1, bin_id_1)
    
    
###################################################################################
st.title("manuelle Differenzierung (Blutbilder)")

tab1, tab2, tab3 = st.tabs(["Tastatur", "Beurteilung", "Resultat"])


###################################################################################
#TAB1
st.write(st.session_state)

with tab1:   
    st.header("Tastatur")
    #Um die Zählung einer Probennummer einzuordnen zu können.
    Identifikation=st.text_input("Identifikationsnummer")

    
    zaehler = sum(st.session_state.meine_gruppe.values())

    #Damit die Tastatur gut dargestellt werden kann.
    st.write("---")
    Tastatur_Blutbild_Differenzierung()
    Speicherplatz=load_data()
    if zaehler == 100 and len(Speicherplatz)==0:
        st.success("Bei der aktuellen Zählung 100 Zellen ausgezählt.")
    elif zaehler == 100 and len(Speicherplatz)!=0:
        st.success("Sie haben 200 Zellen gezählt")
        if len(Speicherplatz) > 1:
            if st.button("Zählung neu anfangen") != 0:
                clear_all()
    st.caption('''Tasten "Normoblast", "C" und "D" werden nicht in den 100 Zellen gezählt. Diese Tasten sind für Zählungen von Gumprecht'sche Kernschatten, Haarzellen und andere Auffälligkeit gedacht. Tasten "A" und "B" sind für die Speziellen Zellen gedacht und werden mit in den 100 Zellen gezählt.''')  
    A_B_C_D= st.text_input("A|B|C|D gebraucht? Schreibe die Variablen an")
    st.write("---")  
    
    col1, col2, col3, col4 = st.columns(4)
    #Tasten kompakter darstellen.
    with col1:
        if st.button('Auf 200 Zählen'):
            #Gibt die Möglichkeit, auf 200 Zellen zu zählen.
            if len(Speicherplatz) != 0:
                #Bei Blutbilder differenzieren, sollte man in der Regel nur 200 Zellen zählen.
                st.error("Kann nur auf 200 gezählt werden.")
            elif zaehler != 100:
                #Ein Error sollte angezeigt werden, wenn kein 100 Zellen gezählt wurde.
                st.error("Noch nicht auf 100 gezählt.")
            else:
                #Damit die neue Zählung die Session_State wiederverwenden kann, muss die Session_State für die vorherige Zählung aufgehoben werden. 
                Zählung_1=Zählung_Dictionary()
                Speicherplatz.append(Zählung_1)
                save_data(Speicherplatz)
                #Die st.session_state wird nach der Speicherung gelöscht, damit die Session_State von vorne angefangen werden kann.
                clear_session_state()
    with col2:
        if st.button("Zählung beenden") != 0:
            if Speicherplatz != 0 and zaehler == 100:
                #Wie eine Anleitung, damit die Nutzer instruktiv nach der Zählung weiter machen können.
                st.info('Sie können im Tab "Beurteilung" das Blutbild beurteilen.')
            elif Speicherplatz == 0 and zaehler == 100:
                #Wie eine Anleitung, damit die Nutzer instruktiv nach der Zählung weiter machen können.
                st.info('Sie können im Tab "Beurteilung" das Blutbild beurteilen.')
            else:
                st.error("Zählen Sie noch auf 100.")
                
        
    with col3:
        if st.button("erste Zählung Löschen") != 0:
            del_erste_Zählung()
            
    with col4: 
        if st.button('Aktuelle Zählung Löschen') != 0:
            # Delete all the items in Session state
            
            clear_session_state()

    with st.expander("Aktuelle Zählung"):
        st.dataframe(Zählung_Dictionary())

##################################################################################
#TAB2

with tab2:
    st.header("Beurteilung")
    st.caption("In diesen Feldern kannst du die Beurteilung des Blutbildes hinschreiben. Achte darauf, dass die Mengen Angaben in Worten oder in Kreuze angegeben werden kann.")
    Erythrozyten_Beurteilung = st.text_area("Erythrozyten Beurteilung")
    Leukozyten_Beurteilung = st.text_area("Leukozyten Beurteilung")
    Thrombozyten_Beurteilung = st.text_area("Thrombozyten Beurteilung")
    st.write('Im nächsten Tab "Resultate" können Sie Ihre gesamte Eingabe überprüfen.')
######################################################################################
#TAB3
with tab3:
    st.header('Resultate') 
    st.write("Hier können Sie nichts ändern. Sie können nur die Zählung vollständig löschen oder speichern.")
    st.subheader(Identifikation)
    Speicherplatz = load_data()
    st.subheader("Zählung")
    zaehler= sum(st.session_state.meine_gruppe.values())

    if len(Speicherplatz) == 0 and zaehler != 100:
        #Kann nicht bewertet werden, da noch keine 100 Zellen Zählung vorhanden ist.
        st.error("Noch keine 100 Zählung vorhanden.")
    elif len(Speicherplatz) != 0 and zaehler == 100:
        #Wird mit weiteren if-Statement verschachtelt, da wir mit session_state zu tun haben.
        if len(Speicherplatz) == 1:
            #Wenn die Differenzierung mit 200 Zellen duchgeführt wurde. 
            Zählung_2 = Zählung_Dictionary()
            Speicherplatz.append(Zählung_2)
            #die erste 100 Zellen Zählung mit den zweiten 100 Zellen Zählung zusammenfügen.
            del_erste_Zählung()
            #Session_State löschen.
            save_data(Speicherplatz)
            #erste und zweite Zählung speichern und somit vom session_state lösen.
            Speicherplatz=load_data()
            Speicherplatz= pd.DataFrame(Speicherplatz, index=["erste Zählung","zweite Zählung"]).T
            Speicherplatz=Speicherplatz["Mittelwert"]= (Speicherplatz["erste Zählung"]+Speicherplatz["zweite Zählung"])/2 
            Speicherplatz["Einheit"]="%"
            st.dataframe(Speicherplatz)
        else:
            #Wenn else nicht definiert wird, wird die Speicherung wiederholen oder nur die erste Zählung anzeigen.
            Speicherplatz = load_data()
            Speicherplatz= pd.DataFrame(Speicherplatz, index=["erste Zählung","zweite Zählung"]).T
            Speicherplatz["Mittelwert"]= (Speicherplatz["erste Zählung"]+Speicherplatz["zweite Zählung"])/2 
            Speicherplatz["Einheit"]="%"            
            st.dataframe(Speicherplatz)
    elif len(Speicherplatz) == 1:
        #Damit beim zweiten Zählung die erste Zählung noch ersichtlich ist.
        Zählung_1 = pd.DataFrame(Speicherplatz, index=["erste Zählung"]).T
        Zählung_1["Einheit"]= "%"
        st.dataframe(Zählung_1)
    else:
    #Nicht gespeicherte Daten in Dataframe darstellen.        
        Zählung_1 = Zählung_Dictionary()
        Zählung_1 = pd.DataFrame(Zählung_1, index=["erste Zählung"]).T
        Zählung_1["Einheit"]="%"
        st.dataframe(Zählung_1)
    st.write("Legende: ",A_B_C_D)

    if st.button("Alle Zählungen löschen")!=0:
        clear_all()

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
    if st.button("Speicherung")!=0:
        Patientenspeicherung = load_data_1()
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
            save_data_1(Patientenspeicherung)
            st.success("Erfolgreich gespeichert")
        elif zaehler != 100 and len(Speicherplatz) == 0:
            st.error("Die Speicherung kann erst nach mindestens 100 Zellen zählen stattfinden.")
        elif zaehler == 100 and len(Speicherplatz)== 0:
            neue_Patient=Zählung_Dictionary()
            Jetzt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            neue_Patient["Specherzeit"]= Jetzt
            neue_Patient["Identifikationsnummer"]=Identifikation
            neue_Patient["Erythrozyten Beurteilung"]=Erythrozyten_Beurteilung
            neue_Patient["Leukozyten Beurteilung"]=Leukozyten_Beurteilung
            neue_Patient["Thrombozyten Beurteilung"]=Thrombozyten_Beurteilung
            neue_Patient["Legende"]=A_B_C_D
            Patientenspeicherung.append(neue_Patient)
            save_data_1(Patientenspeicherung)
            st.success("Erfolgreich gespeichert")

            
