import streamlit as st
import pandas as pd
import yaml
from yaml.loader import SafeLoader
from jsonbin import load_key
import streamlit_authenticator as stauth
import plotly.express as px
import base64

#####################secrets#####################################################
#Jsonbin_2
jsonbin_secrets = st.secrets["jsonbin_2"]
api_key = jsonbin_secrets["api_key"]
bin_id = jsonbin_secrets["bin_id"]
#####user login#################################################################
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
###############################################################################
#Funktionen 

def load_data():
    #Aus der Jsonbin loaden
    load =load_key(api_key, bin_id, username)
    if load == None:
        load=[]
    return load

def Identifikation_sortieren(Identifikationsnummer):
    # Dublikate der Identifikationnummer wird gelöscht.
    lenght = []
    for key in Identifikationsnummer:
        if key not in lenght:
            lenght.append(key)
        else:
            None
    return lenght            

##################################################################################

st.title("Archiv")
Datei = load_data()
DataFrame= pd.DataFrame(Datei)
if len(Datei) == 0:
    st.warning("Keine Daten vorhanden")
else:
    Identifikationsnummer=DataFrame["Identifikationsnummer"]
    Identifikationsnummer=Identifikation_sortieren(Identifikationsnummer)
    Patienten_Identifikation_Auswahl=st.selectbox("Selektiere die Identifikationsnummer",(Identifikationsnummer))
    gewählte_Patienten_Daten=DataFrame[DataFrame["Identifikationsnummer"]== Patienten_Identifikation_Auswahl]
    if len(gewählte_Patienten_Daten)>1:
        Speicherzeit=gewählte_Patienten_Daten["Speicherzeit"]
        Nach_Speicherzeit_selektieren=st.selectbox("Selektiere die Identifikationsnummer",(Speicherzeit))
        gewählte_Patienten_Daten=DataFrame[DataFrame["Speicherzeit"]== Nach_Speicherzeit_selektieren]
    Leukozyten_Wert = st.number_input("Leukozyten mit dem Einheit G/L")
    gewählte_Patienten_Daten_gedreht= gewählte_Patienten_Daten.T
    zugeschnittene_Patienten_Daten = gewählte_Patienten_Daten_gedreht.iloc[:16]
    zugeschnittene_Patienten_Daten.columns = ["Einheit: %"]
    if Leukozyten_Wert != 0:
         zugeschnittene_Patienten_Daten["Einheit: G/L"]= (Leukozyten_Wert / 100.00) * zugeschnittene_Patienten_Daten["Einheit: %"]
    st.table(zugeschnittene_Patienten_Daten)
    if len(gewählte_Patienten_Daten["Legende"]) != 0:
        st.write(gewählte_Patienten_Daten["Legende"].T)

    # Extrahiere den Namen
    name = zugeschnittene_Patienten_Daten.index

    # Erstelle ein Pie-Chart
    fig = px.pie(zugeschnittene_Patienten_Daten, values='Einheit: %', names=name, title=f"Leukozytenverteilung")

    # Zeige das Pie-Chart in Streamlit
    st.plotly_chart(fig)
    
    #Zeigt die Bewertung der Zellen an
    Bewertungen = gewählte_Patienten_Daten_gedreht.iloc[18:21]
    Bewertung =dict(Bewertung)
    st.table(Bewertungen)

    # Add a download button
    csv = gewählte_Patienten_Daten.to_csv(index=False) # Convert the DataFrame to CSV
    b64 = base64.b64encode(csv.encode()).decode() # Encode to base64
    href = f'<a href="data:file/csv;base64,{b64}" download="my_file.csv">Download CSV file</a>'
    st.markdown(href, unsafe_allow_html=True)

