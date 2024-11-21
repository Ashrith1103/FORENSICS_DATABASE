import streamlit as st
import pandas as pd
import plotly.express as px
from database import viewQueryResult
from database import viewTables
from database import execQuery

def predef_queries():
    q = [   "Cars associated with Cases", 
            "Durgs associated with Cases",
            "Ballistics associated with cases",
            "Criminals and the cases they are associated with", 
            "Criminals and the type of cases they are associated with",
            "Crimnals being Investigated by each officer",
            "Cases Associated with drugs",
            "Colors grouped by solvent",
            "Narcotic vs non narcotic drugs",
            "Cases grouped by Location",
            "Lead by each officer",
            "Number of Ongoing cases",
            "Number of active criminal",
            "Drugs that are narcotic and blue",
            "Number of cases lead by Jake Peralta",
            "Criminal and their investigating officer",
            "Cases by Location",
            "Cases by Type"
            ]
    choice = st.selectbox("Choose a Query: ", q)
    if(choice!=q[16] and choice!=q[17]):
        print(choice)
        result = viewQueryResult(q.index(choice)+1)
    #print(result)
    if(choice==q[0]):
        df = pd.DataFrame(result, columns=("Case", "Model", "Manufacturer"))
        st.dataframe(df)
    elif(choice==q[1]):
        df = pd.DataFrame(result, columns=("Name of the case", "Drugs", "Narcotic"))
        st.dataframe(df)
    elif(choice==q[2]):
        df = pd.DataFrame(result, columns=("Name of the case", "Model", "Manufacturer","Year","Type of Gun","Guage","Caliber"))
        st.dataframe(df)
    elif(choice==q[3]):
        df = pd.DataFrame(result, columns=("Criminal", "Case Name"))
        st.dataframe(df)
    elif(choice==q[4]):
        df = pd.DataFrame(result, columns=("Criminal", "Type of Case"))
        st.dataframe(df)
    elif(choice==q[5]):
        df = pd.DataFrame(result, columns=("Criminal", "Investigating Officer"))
        st.dataframe(df)
    elif(choice==q[6]):
        df = pd.DataFrame(result, columns=("Case Name", "Drug Name"))
        st.dataframe(df)
    elif(choice==q[7]):
        df = pd.DataFrame(result, columns=("Paint Solvent", "Count"))
        st.dataframe(df)
    elif(choice==q[8]):
        df = pd.DataFrame(result, columns=("Narcotic", "Count"))
        st.dataframe(df)
    elif(choice==q[9]):
        df = pd.DataFrame(result, columns=("Location", "No of Cases"))
        st.dataframe(df)
    elif(choice==q[10]):
        df = pd.DataFrame(result, columns=("Case", "Officer"))
        st.dataframe(df)
    elif(choice==q[11]):
        df = pd.DataFrame(result, columns=("Count",))
        st.dataframe(df)
    elif(choice==q[12]):
        df = pd.DataFrame(result, columns=("Count",))
        st.dataframe(df)
    elif(choice==q[13]):
        df = pd.DataFrame(result, columns=("NAME",))
        st.dataframe(df)
    elif(choice==q[14]):
        df = pd.DataFrame(result, columns=("Number of cases",))
        st.dataframe(df)
    elif(choice==q[15]):
        df = pd.DataFrame(result, columns=("criminal","leading officer"))
        st.dataframe(df)
    elif(choice==q[16]):
        df = pd.DataFrame(viewTables("Cases"), columns=("Case ID", "Type", "Name", "Leading Officer", "Assissting Officer", "Time of Report", "Location", "Status"))
        task_df = df['Location'].value_counts().to_frame()
        task_df = task_df.reset_index()
        p1 = px.pie(task_df, names='Location', values='count' )
        st.plotly_chart(p1)
    elif(choice==q[17]):
        df = pd.DataFrame(viewTables("Cases"), columns=("Case ID", "Type", "Name", "Leading Officer", "Assissting Officer", "Time of Report", "Location", "Status"))
        task_df = df['Type'].value_counts().to_frame()
        task_df = task_df.reset_index()
        p1 = px.pie(task_df, names='Type', values='count')
        st.plotly_chart(p1)
    

def query_cmd():
    command = st.text_input("Enter Query")
    if command:
        # Validate the query type
        if not command.strip().upper().startswith("SELECT"):
            st.error("Only SELECT queries are allowed. Please try again.")
            return
        
        # Restrict access to specific tables
        restricted_tables = ["user_credentials", "criminalbackup"]
        if any(table in command.lower() for table in restricted_tables):
            st.error("Access to restricted tables ('user_credentials' or 'criminalbackup') is not allowed.")
            return
        
        try:
            result = execQuery(command)
            if result:
                df = pd.DataFrame(result)
                st.dataframe(df)
            else:
                st.info("Query executed successfully, but no data to display.")
        except Exception as e:
            st.error(f"An error occurred: {e}")