import streamlit as st
from utils.jsonbin import save_key, load_key, del_erste_Zählung_

@st.cache_data(ttl=10)

def load_data(api_key_1, bin_id_1, username):
    load =load_key(api_key_1, bin_id_1, username)
    #Falls keine Daten gespeichert wurde, wird die Daten als eine leere Liste definiert.
    if load == None:
        load=[]
    return load
        
# Funktion zum Speichern in einer Jsonbin-Datei
def save_data(data, api_key_1, bin_id_1, username):
    return save_key(api_key_1, bin_id_1, username, data)

#Funktion zum Laden aus einer Jsonbin-Datei
def load_data_1(api_key_2,bin_id_2, username):
    return load_key(api_key_2,bin_id_2, username)

# Funktion zum Speichern in einer JSON-Datei
def save_data_1(data, api_key_2, bin_id_2, username):
    return save_key(api_key_2, bin_id_2, username, data)

def del_erste_Zählung(api_key_1, bin_id_1,username):
    return del_erste_Zählung_(api_key_1, bin_id_1,username)  


def Tastatur_Blutbild_Differenzierung(auf_oder_unter_zählen):     
    # sum up all cells 
    zaehler = sum([st.session_state.Basophilen,st.session_state.Monozyten,st.session_state.Blasten, st.session_state.A, st.session_state.Eosinophilen,st.session_state.Lymphozyten,st.session_state.Promyelozyten,st.session_state.B,st.session_state.Segmentierten,st.session_state.Myelozyten,st.session_state.Plasmazellen,st.session_state.Stabkernigen,st.session_state.Metamyelozyten])

    # Um Tastatur, wie im Realität zu imitieren, werden die Tastatur in 4 Reihen aufgeteilt. Die Tastaturen zählen auf und runter.
    # auf_oder_unter_zählen verschlüsselt addieren oder subthrahieren. Damit je nach st.radio die Nutzer die Option hat die Zählung auf oder rückwärts zu zählen.
       
    col1, col2, col3, col4 = st.columns(4, gap="small")
    if zaehler <= 99:
       with col1:
           if st.button('Basophil', use_container_width = True):
               if auf_oder_unter_zählen == 'addieren':
                    st.session_state.Basophilen += 1
               elif auf_oder_unter_zählen == 'subtrahieren':
                    st.session_state.Basophilen -= 1

           if st.button('Monozyt', use_container_width = True):
               if auf_oder_unter_zählen == 'addieren':
                    st.session_state.Monozyten += 1
               elif auf_oder_unter_zählen == 'subtrahieren':
                    st.session_state.Monozyten -= 1

           if  st.button('Blast', use_container_width = True):
               if auf_oder_unter_zählen == 'addieren':
                    st.session_state.Blasten += 1
               elif auf_oder_unter_zählen == 'subtrahieren':
                    st.session_state.Blasten -= 1


           if st.button('A', use_container_width = True):
               if auf_oder_unter_zählen == 'addieren':
                    st.session_state.A += 1
               elif auf_oder_unter_zählen == 'subtrahieren':
                    st.session_state.A -= 1


       with col2:
           if st.button('Eosinophil', use_container_width = True):
               if auf_oder_unter_zählen == 'addieren':
                    st.session_state.Eosinophilen += 1
               elif auf_oder_unter_zählen == 'subtrahieren':
                    st.session_state.Eosinophilen -= 1

           if st.button('Lymphozyt', use_container_width = True):
               if auf_oder_unter_zählen == 'addieren':
                    st.session_state.Lymphozyten += 1
               elif auf_oder_unter_zählen == 'subtrahieren':
                    st.session_state.Lymphozyten -= 1

           if st.button('Promyelozyt', use_container_width = True):
               if auf_oder_unter_zählen == 'addieren':
                    st.session_state.Promyelozyten += 1
               elif auf_oder_unter_zählen == 'subtrahieren':
                    st.session_state.Promyelozyten -= 1
                    
           if st.button('B', use_container_width = True):
               if auf_oder_unter_zählen == 'addieren':
                    st.session_state.B += 1
               elif auf_oder_unter_zählen == 'subtrahieren':
                    st.session_state.B -= 1
                    
       with col3:
           if st.button('Normoblast', use_container_width = True):
               if auf_oder_unter_zählen == 'addieren':
                    st.session_state.Normoblast += 1
               elif auf_oder_unter_zählen == 'subtrahieren':
                    st.session_state.Normoblast -= 1
                    
           if st.button('Segmentierte', use_container_width = True):
               if auf_oder_unter_zählen == 'addieren':
                    st.session_state.Segmentierten += 1
               elif auf_oder_unter_zählen == 'subtrahieren':
                    st.session_state.Segmentierten -= 1

           if st.button('Myelozyt', use_container_width = True) != 0:
               if auf_oder_unter_zählen == 'addieren':
                    st.session_state.Myelozyten += 1
               elif auf_oder_unter_zählen == 'subtrahieren':
                    st.session_state.Myelozyten -= 1
                    
           if st.button('C', use_container_width = True):
               if auf_oder_unter_zählen == 'addieren':
                    st.session_state.C += 1
               elif auf_oder_unter_zählen == 'subtrahieren':
                    st.session_state.C -= 1
 
       with col4:
           if st.button('Plasmazelle', use_container_width = True):
               if auf_oder_unter_zählen == 'addieren':
                    st.session_state.Plasmazellen += 1
               elif auf_oder_unter_zählen == 'subtrahieren':
                    st.session_state.Plasmazellen -= 1

           if st.button('Stabkernige', use_container_width = True):
               if auf_oder_unter_zählen == 'addieren':
                    st.session_state.Stabkernigen += 1
               elif auf_oder_unter_zählen == 'subtrahieren':
                    st.session_state.Stabkernigen -= 1   

           if st.button('Metamyelozyt', use_container_width = True):
               if auf_oder_unter_zählen == 'addieren':
                    st.session_state.Metamyelozyten += 1
               elif auf_oder_unter_zählen == 'subtrahieren':
                    st.session_state.Metamyelozyten -= 1
                    
           if st.button('D', use_container_width = True):
               if auf_oder_unter_zählen == 'addieren':
                    st.session_state.D += 1
               elif auf_oder_unter_zählen == 'subtrahieren':
                    st.session_state.D -= 1
                    
    elif zaehler == 100:
        return st.session_state
    
def Zählung_Dictionary():
    #Regeneriert die Zählung in session_state zu Dictionary
    Dictionary = {}
    zaehler = ['Basophilen', 'Monozyten', 'Blasten','A','Eosinophilen','Lymphozyten','Promyelozyten','B','Normoblast','Segmentierten','Myelozyten','C','Plasmazellen','Stabkernigen','Metamyelozyten','D'] 
    for key in zaehler:
        Dictionary[key]=st.session_state[key]
    return Dictionary

def clear_session_state():
    # Löscht die Zählung komplet.
    zaehler = ['Basophilen', 'Monozyten', 'Blasten','A','Eosinophilen','Lymphozyten','Promyelozyten','B','Normoblast','Segmentierten','Myelozyten','C','Plasmazellen','Stabkernigen','Metamyelozyten','D'] 
    for key in zaehler:
        del st.session_state[key]
        if key in globals():
            del globals()[key]

def clear_all(key,api_key_1,bin_id_1, username):
    #löscht alle Zählung
    zaehler = ['Basophilen', 'Monozyten', 'Blasten','A','Eosinophilen','Lymphozyten','Promyelozyten','B','Normoblast','Segmentierten','Myelozyten','C','Plasmazellen','Stabkernigen','Metamyelozyten','D'] 
    for key in zaehler:
        del st.session_state[key]
        if key in globals():
            del globals()[key]
    return del_erste_Zählung_(api_key_1, bin_id_1,username)


def session_state_initialisieren():
    #Damit die session_state intialisiert wird
    if 'Basophilen' not in st.session_state:
        st.session_state.Basophilen=0

    if 'Monozyten' not in st.session_state:
        st.session_state.Monozyten=0

    if 'Blasten' not in st.session_state:
        st.session_state.Blasten=0

    if 'A' not in st.session_state:
        st.session_state.A=0

    if 'Eosinophilen' not in st.session_state:
        st.session_state.Eosinophilen=0

    if 'Lymphozyten' not in st.session_state:
        st.session_state.Lymphozyten=0

    if 'Promyelozyten' not in st.session_state:
        st.session_state.Promyelozyten=0

    if 'B' not in st.session_state:
        st.session_state.B=0

    if 'Normoblast' not in st.session_state:
        st.session_state.Normoblast=0

    if 'Segmentierten' not in st.session_state:
        st.session_state.Segmentierten=0

    if 'Myelozyten' not in st.session_state:
        st.session_state.Myelozyten=0

    if 'C' not in st.session_state:
        st.session_state.C=0

    if 'Plasmazellen' not in st.session_state:
        st.session_state.Plasmazellen=0

    if 'Stabkernigen' not in st.session_state:
        st.session_state.Stabkernigen=0

    if 'Metamyelozyten' not in st.session_state:
        st.session_state.Metamyelozyten=0

    if 'D' not in st.session_state:
       st.session_state.D=0