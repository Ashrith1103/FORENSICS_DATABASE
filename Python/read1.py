import streamlit as st
import pandas as pd
from database import viewTables

def read1():
    menu = ["Drugs", "Ballistics", "Paint", "Automobile", "Cases", "Criminal","CriminalCase"]
    choice = st.sidebar.selectbox("Menu", menu)
    result = viewTables(choice)
    #print(result)
    if choice==menu[0]:
        df = pd.DataFrame(result, columns=("Case ID", "NDC Code", "Name","Color", "Class", "Narcotic")) 
    elif choice==menu[1]:
        df = pd.DataFrame(result, columns=("Case ID", "ID", "Make", "Manufacturer", "Year of Manufacture", "Type", "Caliber", "Gauge", "Country of Origin"))
    elif choice==menu[2]:
        df = pd.DataFrame(result, columns=("Case ID", "ID", "Color", "Solvent", "Binder", "Pigment", "Additive"))
    elif choice==menu[3]:
        df = pd.DataFrame(result, columns=("Case ID", "ID", "Model", "Year of Manufacture", "Manufacturer", "Type"))
    elif choice==menu[4]:
        df = pd.DataFrame(result, columns=("Case ID", "Type", "Name", "Leading Officer", "Assissting Officer", "Time of Report", "Location", "Status"))
    elif choice==menu[5]:
        df = pd.DataFrame(result, columns=("Criminal ID", "Name", "Alias", "Age", "Number of Cases", "Dominant Hand", "Status", "DNA", "Fingerprint", "Nationality"))
    elif choice==menu[6]:
        df = pd.DataFrame(result, columns=("Criminal ID", "Case ID"))
        with st.expander("View Criminals"):
            result = viewTables("Criminal")
            df1 = pd.DataFrame(result, columns=("Criminal ID", "Name", "Alias", "Age", "Number of Cases", "Dominant Hand", "Status", "DNA", "Fingerprint", "Nationality")) 
            st.dataframe(df1)
        with st.expander("View Cases"):
            r1 = viewTables("Cases")
            df2 = pd.DataFrame(r1,columns=("Case ID", "Type", "Name", "Leading Officer", "Assissting Officer", "Time of Report", "Location", "Status"))
            st.dataframe(df2)
    
    st.dataframe(df)
