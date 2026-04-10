import streamlit as st
import pandas as pd
import yaml
from yaml.loader import SafeLoader
import datetime
from utils.jsonbin import save_key, load_key, del_first_count
import streamlit_authenticator as stauth
import requests
import json
import copy
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

#huggning_face
hugging_face=st.secrets["hugging_face"]
token = hugging_face["token"]

#####user login###################################################################################################################################################
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
)

try: 
    username = authenticator.login('main','Login')

except Exception as e:
    st.error(e)

if st.session_state.get("authentication_status") == True:   # login successful
    authenticator.logout('Logout', 'main')   # show logout button
elif st.session_state.get("authentication_status") == False:
    st.error('Username/password is incorrect')
    st.stop()
elif st.session_state.get("authentication_status") == None:
    st.warning('Please enter your username and password')
    st.stop()

##################################################################################################################################################################
# Funktion zum Laden aus einer Jsonbin-Datei, Mit st.cache soll 10 Sekunden reloaden.
@st.cache_data(ttl=10)

def load_data():
    load = load_key(api_key_1, bin_id_1, st.session_state["username"])
    #Falls keine Daten gespeichert wurde, wird die Daten als eine leere Liste definiert.
    if load == None:
        load=[]
    return load
        
# Funktion zum Speichern in einer Jsonbin-Datei
def save_data(data):
    return save_key(api_key_1, bin_id_1, st.session_state["username"], data)

#Funktion zum Laden aus einer Jsonbin-Datei
def load_data_1():
    return load_key(api_key_2,bin_id_2, st.session_state["username"])

# Funktion zum Speichern in einer JSON-Datei
def save_data_1(data):
    return save_key(api_key_2, bin_id_2, st.session_state["username"], data)

def count_of_leucocyte():
    return sum(st.session_state["leucocyte_count"].values())

def Tastatur_Blutbild_Differenzierung(add_or_sub_count):  
    """
    Displays the counter for leucocytes, including Normoblast and some non-leucocyte types as C and D.
    
    Args:
        add_or_sub_count (str): The string can either be "addieren" or "subtrahieren".
    """   
    count = count_of_leucocyte()

    col1, col2, col3, col4 = st.columns(4, gap="small")

    if add_or_sub_count == "addieren":
        variable = +1
    elif add_or_sub_count == "subtrahieren":
        variable = -1
    else:
        raise TypeError("Input can either be 'addieren' or 'subtrahieren'") 

    if count <= 99:
       with col1:
           if st.button('Basophil', use_container_width = True):
                st.session_state.leucocyte_count["Basophilen"] += variable

           if st.button('Monozyt', use_container_width = True):
                st.session_state.leucocyte_count["Monozyten"] += variable

           if  st.button('Blast', use_container_width = True):
                st.session_state.leucocyte_count["Blasten"] += variable

           if st.button('A', use_container_width = True):
                st.session_state.leucocyte_count["A"] += variable

       with col2:
           if st.button('Eosinophil', use_container_width = True):
                st.session_state.leucocyte_count["Eosinophilen"] += variable

           if st.button('Lymphozyt', use_container_width = True):
                st.session_state.leucocyte_count["Lymphozyten"] += variable

           if st.button('Promyelozyt', use_container_width = True):
                st.session_state.leucocyte_count["Promyelozyten"] += variable
                    
           if st.button('B', use_container_width = True):
                st.session_state.leucocyte_count["B"] += variable

       with col3:
           if st.button('Normoblast', use_container_width = True):
                st.session_state.diverse_count["Normoblast"] += variable
                    
           if st.button('Segmentierte', use_container_width = True):
                st.session_state.leucocyte_count["Segmentierten"] += variable

           if st.button('Myelozyt', use_container_width = True) != 0:
                st.session_state.leucocyte_count["Myelozyten"] += variable
                    
           if st.button('C', use_container_width = True):
                st.session_state.diverse_count["C"] += variable
 
       with col4:
           if st.button('Plasmazelle', use_container_width = True):
                st.session_state.leucocyte_count["Plasmazellen"] += variable

           if st.button('Stabkernige', use_container_width = True):
                st.session_state.leucocyte_count["Stabkernigen"] += variable

           if st.button('Metamyelozyt', use_container_width = True):
                st.session_state.leucocyte_count["Metamyelozyten"] += variable
                    
           if st.button('D', use_container_width = True):
                st.session_state.diverse_count["D"] += variable


def Zählung_Dictionary(): 
    Dict = copy.deepcopy(st.session_state.leucocyte_count)
    for cell in st.session_state.diverse_count:
        Dict[cell] = st.session_state.diverse_count[cell]
    return Dict

def clear_session_state():
    # Löscht die Zählung komplet. 
    del st.session_state.leucocyte_count
    del st.session_state.diverse_count
    if "leucocyte_count" in globals():
        del globals()["leucocygte_count"]
    if "diverse_count" in globals():
        del globals()["diverse_count"]

def clear_all():
    #löscht alle Zählung
    clear_session_state()
    return del_first_count(api_key_1, bin_id_1,st.session_state["username"])

def session_state_initialisieren(): 
    """Initialize streamlit.session_state to add 'leucocyte_count' and 'diverse_count' into the  """
    leucocyte_count_dict = {'Basophilen': 0, 'Monozyten':0, 'Blasten':0,'A':0,'Eosinophilen':0,'Lymphozyten':0,'Promyelozyten':0,'B':0,'Segmentierten':0,'Myelozyten':0,'Plasmazellen':0,'Stabkernigen':0,'Metamyelozyten':0}
    diverse_count_dict = {'Normoblast':0, 'C':0, 'D':0}
    if "leucocyte_count" not in st.session_state:
        st.session_state.leucocyte_count = leucocyte_count_dict
    if "diverse_count" not in st.session_state:
        st.session_state.diverse_count = diverse_count_dict

    
###################################################################################
st.title("manuelle Differenzierung (Blutbilder)")

tab1, tab2, tab3, tab4 = st.tabs(["Tastatur", "Beurteilung", "Resultat", " Zellen Identifizieren"])

###################################################################################
#TAB1
with tab1:   
    st.header("Tastatur ⌨️")
    session_state_initialisieren()
    #Um die Zählung einer Probennummer einzuordnen zu können.
    Identifikation=st.text_input("Identifikationsnummer")
    Speicherplatz_erste_Zählung = load_data() #<-------------------------------a problem that hinders fast clicking
    st.write("---")
    # ermöglicht die Zählung zu korregieren in dem man addieren oder subtrahieren kann.
    auf_oder_unter_zaehlen = st.radio(
    "",
    ('addieren', 'subtrahieren'))
    
    #Damit die Tastatur gut dargestellt werden kann.
    if len(Speicherplatz_erste_Zählung)>1:
        if st.button("Differenzierung starten"):
            del_first_count(api_key_1, bin_id_1,st.session_state["username"])
            Tastatur_Blutbild_Differenzierung(auf_oder_unter_zaehlen)
            #zaehler ist der Counter
            zaehler = sum(st.session_state.leucocyte_count.values())    
            st.write( zaehler ,"/100 Zellen")
    else:
        Tastatur_Blutbild_Differenzierung(auf_oder_unter_zaehlen)
        #Da Login auch mit session_state arbeitet, muss ich genau definieren, welchen Parameter in session_state zusammen gezählt wird.
        zaehler = sum(st.session_state.leucocyte_count.values())    
        st.write( zaehler ,"/100 Zellen")
    session_state_initialisieren()
    if zaehler == 100 and len(Speicherplatz_erste_Zählung)==0:
        st.success("Bei der aktuellen Zählung 100 Zellen ausgezählt.")
    elif zaehler > 100:
        st.error("Ops, du bist über 100 Zellen. Klicke nicht so schnell. Lösche einige Zellen von der Zählung.")
    elif zaehler == 100 and len(Speicherplatz_erste_Zählung)!=0:
        st.success("Du hast 200 Zellen ausgezählt")
        if len(Speicherplatz_erste_Zählung) > 1:
            if st.button("Zählung ganz neu anfangen"):
                clear_all()
    session_state_initialisieren()
    with st.expander("A/B/C/D"):
        st.write('''Die Tasten A, B, C und D sind für spezielle Zellen wie Gumprecht'sche Kernschatten, Haarzellen und andere Auffälligkeiten während der hundert Zellen-Zählung vorgesehen. Während "C" und "D" nicht in die 100 Zellen gezählt werden, werden "A" und "B" in die Zählung einbezogen. Beachte bitte, dass der "Normoblast" nicht zu den Leukozyten gehört und daher nicht zu den hundert Zellen zählt.''')
    A_B_C_D= st.text_input('Spezifiziere Zelltypen für A, B, C, D Tasten im Textfeld.')
    st.write("---")  
    
    col1, col2, col3, col4 = st.columns(4)
    #Tasten kompakter darstellen.
    with col1:
        if st.button('Auf 200 Zählen', use_container_width = True):
            if len(Identifikation) != 0:
                #Gibt die Möglichkeit, auf 200 Zellen zu zählen.
                if len(Speicherplatz_erste_Zählung) != 0:
                    #Bei Blutbilder differenzieren, sollte man in der Regel nur 200 Zellen zählen.
                    st.error("Kann nur auf 200 gezählt werden.")
                elif zaehler != 100:
                    #Ein Error sollte angezeigt werden, wenn kein 100 Zellen gezählt wurde.
                 st.error("Noch nicht auf 100 gezählt.")
                else:
                    #Damit die neue Zählung die Session_State wiederverwenden kann, muss die Session_State für die vorherige Zählung aufgehoben werden. 
                    Zählung_1=Zählung_Dictionary()
                    Speicherplatz_erste_Zählung.append(Zählung_1)
                    save_data(Speicherplatz_erste_Zählung)
                    #Die st.session_state wird nach der Speicherung gelöscht, damit die Session_State von vorne angefangen werden kann.
                    clear_session_state()
                    session_state_initialisieren()
            if len(Identifikation) == 0:
                st.error("Schreibe die ein Identifikationsnummer")
    with col2:
        if st.button("Zählung beenden", use_container_width = True):
            if Speicherplatz_erste_Zählung != 0 and zaehler == 100:
                #Wie eine Anleitung, damit die Nutzer instruktiv nach der Zählung weiter machen können.
                st.info('Du kannst im Tab "Beurteilung" das Blutbild beurteilen.')
            elif Speicherplatz_erste_Zählung == 0 and zaehler == 100:
                #Wie eine Anleitung, damit die Nutzer instruktiv nach der Zählung weiter machen können.
                st.info('Sie können im Tab "Beurteilung" das Blutbild beurteilen.')
            else:
                st.error("Zähle 100 Zellen aus")
                
        
    with col3:
        if st.button("erste Zählung Löschen", use_container_width = True):
            del_first_count(api_key_1, bin_id_1,st.session_state["username"])
            session_state_initialisieren()
            
    with col4: 
        if st.button('Aktuelle Zählung Löschen', use_container_width = True):
            # Delete all the items in Session state            
            clear_session_state()
            session_state_initialisieren()

    Aktuelle_Zählung=pd.DataFrame(Zählung_Dictionary(),index=["Aktuelle Zählung"]).T
    st.table(Aktuelle_Zählung)
        
##################################################################################
#TAB2
with tab2:
    st.header("Beurteilung ✒️")
    st.caption("In den dafür vorgesehenen Feldern kannst du die Beurteilungen der Blutbilder eintragen. Achte darauf, dass die Mengenangaben sowohl in Worten als auch durch Kreuze angegeben werden können.")
    Erythrozyten_Beurteilung = st.text_area("Erythrozyten Beurteilung")
    Leukozyten_Beurteilung = st.text_area("Leukozyten Beurteilung")
    Thrombozyten_Beurteilung = st.text_area("Thrombozyten Beurteilung")
    st.write("Im Tab 'Resultate' findest du eine Übersicht und Bewertung deiner eingetragenen Daten, wo du sie überprüfen und auswerten kannst.")
######################################################################################
#TAB3
with tab3:
    st.header('Resultate 📄') 
    st.write("In diesem Tab hast du die Möglichkeit, die Zählungen zu löschen oder zu speichern. Die Zählung kann hier manuell vorgenommen werden.")
    st.subheader(Identifikation)
    st.subheader("Zählung")
    zaehler = sum(st.session_state.leucocyte_count.values())
    #Laden der Speicher um Dataframe zu generieren 
    Speicherplatz = load_data()
    if len(Speicherplatz) == 0 and zaehler != 100:
        #Kann nicht bewertet werden, da noch keine 100 Zellen Zählung vorhanden ist.
        st.error("Noch keine 100 Zellen gezählt.")
    elif len(Speicherplatz) != 0 and zaehler == 100:
        #Wird mit weiteren if-Statement verschachtelt, da wir mit session_state zu tun haben.
        if len(Speicherplatz) == 1:
            #Wenn die Differenzierung mit 200 Zellen duchgeführt wurde. 
            Zählung_2 = Zählung_Dictionary() 
            Speicherplatz.append(Zählung_2)
            #die erste 100 Zellen Zählung mit den zweiten 100 Zellen Zählung zusammenfügen.
            del_first_count(api_key_1, bin_id_1,st.session_state["username"])
            #Session_State löschen.
            save_data(Speicherplatz)
            #erste und zweite Zählung speichern und somit vom session_state lösen.
            Speicherplatz=load_data()
            Speicherplatz= pd.DataFrame(Speicherplatz, index=["erste Zählung","zweite Zählung"]).T
            Speicherplatz=Speicherplatz["Mittelwert"]= (Speicherplatz["erste Zählung"]+Speicherplatz["zweite Zählung"])/2 
            Speicherplatz["Einheit"]="%"
            st.table(Speicherplatz)
        else:
            #Wenn else nicht definiert wird, wird die Speicherung wiederholen oder nur die erste Zählung anzeigen.
            Speicherplatz = load_data()
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
        Zählung_1 = Zählung_Dictionary()
        Zählung_1 = pd.DataFrame(Zählung_1, index=["erste Zählung"]).T
        Zählung_1["Einheit"]="%"
        st.table(Zählung_1)
    st.write("Legende: ",A_B_C_D)

    if st.button("Alle Zählungen löschen"):
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
    if st.button("Speicherung"):
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
            neue_Patient["Speicherzeit"]= Jetzt
            neue_Patient["Identifikationsnummer"]=Identifikation
            neue_Patient["Erythrozyten Beurteilung"]=Erythrozyten_Beurteilung
            neue_Patient["Leukozyten Beurteilung"]=Leukozyten_Beurteilung
            neue_Patient["Thrombozyten Beurteilung"]=Thrombozyten_Beurteilung
            neue_Patient["Legende"]=A_B_C_D
            Patientenspeicherung.append(neue_Patient)
            save_data_1(Patientenspeicherung)
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

            

            
