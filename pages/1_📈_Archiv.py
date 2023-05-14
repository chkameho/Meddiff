import streamlit as st
import pandas as pd
import yaml
from yaml.loader import SafeLoader
from jsonbin import load_key
import streamlit_authenticator as stauth
import plotly.express as px


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
    load =load_key(api_key, bin_id, username)
    if load == None:
        load=[]
    return load

st.title("Archiv")
Datei = load_data()
DataFrame= pd.DataFrame(Datei)
Identifikationsnummer=DataFrame["Identifikationsnummer"]
Patienten_Identifikation_Auswahl=st.selectbox("Selektiere die Identifikationsnummer",(Identifikationsnummer))
gewählte_Patienten_Daten=DataFrame[DataFrame["Identifikationsnummer"]== Patienten_Identifikation_Auswahl]
if len(gewählte_Patienten_Daten)>1:
    #Speicherzeit später korregieren
    Speicherzeit=gewählte_Patienten_Daten["Specherzeit"]
    Nach_Speicherzeit_selektieren=st.selectbox("Selektiere die Identifikationsnummer",(Speicherzeit))
    gewählte_Patienten_Daten=DataFrame[DataFrame["Specherzeit"]== Nach_Speicherzeit_selektieren]
Leukozyten_Wert = st.number_input("Leukozyten mit dem Einheit G/L")
gewählte_Patienten_Daten_gedreht= gewählte_Patienten_Daten.T
zugeschnittene_Patienten_Daten = gewählte_Patienten_Daten_gedreht.iloc[:16]
zugeschnittene_Patienten_Daten.columns = ["Einheit: %"]
if Leukozyten_Wert != 0:
      zugeschnittene_Patienten_Daten["Einheit: G/L"]= (Leukozyten_Wert / 100.00) * zugeschnittene_Patienten_Daten["Einheit: %"]
zugeschnittene_Patienten_Daten.rename(columns={zugeschnittene_Patienten_Daten.columns[0]: 'Parameter'}, inplace=True)
st.write(zugeschnittene_Patienten_Daten)


# Extrahiere den Namen
name = zugeschnittene_Patienten_Daten.index[]

# Erstelle ein Pie-Chart
fig = px.pie(zugeschnittene_Patienten_Daten, values='Einheit: %', names=name, title=f"Leukozytenverteilung")

# Zeige das Pie-Chart in Streamlit
st.plotly_chart(fig)

