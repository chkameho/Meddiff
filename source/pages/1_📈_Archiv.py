import streamlit as st
import pandas as pd
from utils.jsonbin_client import load_data
from utils.data_formatter import DisplayFormatter
import base64

jsonbin_secrets = st.secrets["jsonbin"]
api_key = jsonbin_secrets["api_key"]
bin_id = jsonbin_secrets["bin_id"]        

st.title("Archiv")
dict_data = load_data(api_key, bin_id, st.session_state.username)

if len(dict_data) == 0:
    st.warning("Keine Daten vorhanden")
    
else:
    id = st.selectbox("Selektiere die Identifikationsnummer",(dict_data.keys()))
    dict_select_data = dict_data[id]
    formatter = DisplayFormatter(dict_select_data)
    df_count = formatter.to_dataframe()
    st.table(df_count)   
    legend, save_time = formatter.get_meta_info()
    st.write(f"""Legende: {legend}""")
    
    st.plotly_chart(formatter.to_pie_plot())
    
    dict_morph = formatter.get_morph_data()
      
    st.write("---")
    st.markdown("**Erythrozyten Beurteilung:**")
    st.write(dict_morph["Erythrozyten Beurteilung"] )
    st.write("---")
    st.markdown("**Leukozyten Beurteilung:**")
    st.write(dict_morph["Leukozyten Beurteilung"])
    st.write("---")
    st.markdown("**Thrombozyten Beurteilung:**")
    st.write(dict_morph["Thrombozyten Beurteilung"])
    st.write("---")
 
    # Add a download button
    csv = df_count.to_csv(index=False) # Convert the DataFrame to CSV
    b64 = base64.b64encode(csv.encode()).decode() # Encode to base64
    href = f'<a href="data:file/csv;base64,{b64}" download="my_file.csv">Download CSV file</a>'
    st.markdown(href, unsafe_allow_html=True)

