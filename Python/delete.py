import streamlit as st
from database import delRec, viewTables, get_automobile_no, get_ballistics_no, get_drug_no, get_paint_no, get_case_no, get_criminal_no, get_criminalbackup_no, get_username
import pandas as pd

def delete():
    menu = ["Automobile", "Ballistics", "Cases", "Criminal", "Drugs", "Paint", "CriminalBackup", "User_Credentials"]
    choice = st.sidebar.selectbox("Menu", menu)
    result = viewTables(choice)
    
    # Display the correct DataFrame based on the selected menu
    if choice == "Drugs":
        df = pd.DataFrame(result, columns=("Case ID", "NDC Code", "Name", "Color", "Class", "Narcotic"))
    elif choice == "Ballistics":
        df = pd.DataFrame(result, columns=("Case ID", "ID", "Make", "Manufacturer", "Year of Manufacture", "Type", "Caliber", "Gauge", "Country of Origin"))
    elif choice == "Paint":
        df = pd.DataFrame(result, columns=("Case ID", "ID", "Color", "Solvent", "Binder", "Pigment", "Additive"))
    elif choice == "Automobile":
        df = pd.DataFrame(result, columns=("Case ID", "ID", "Model", "Year of Manufacture", "Manufacturer", "Type"))
    elif choice == "Cases":
        df = pd.DataFrame(result, columns=("Case ID", "Type", "Name", "Leading Officer", "Assisting Officer", "Time of Report", "Location", "Status"))
    elif choice == "Criminal":
        df = pd.DataFrame(result, columns=("Criminal ID", "Name", "Alias", "Age", "Number of Cases", "Dominant Hand", "Status", "DNA", "Fingerprint", "Nationality"))
    elif choice == "CriminalBackup":
        df = pd.DataFrame(result, columns=("Criminal ID", "Name", "Alias", "Number of Cases", "Dominant Hand", "Nationality"))
    elif choice == "User_Credentials":
        df = pd.DataFrame(result, columns=("Username", "Password", "Role"))
    
    st.dataframe(df)
    
    # Retrieve available IDs for deletion
    list_of_id = []
    if choice == "Drugs":
        list_of_id = [i[0] for i in get_drug_no()]
    elif choice == "Automobile":
        list_of_id = [i[0] for i in get_automobile_no()]
    elif choice == "Paint":
        list_of_id = [i[0] for i in get_paint_no()]
    elif choice == "Ballistics":
        list_of_id = [i[0] for i in get_ballistics_no()]
    elif choice == "Cases":
        list_of_id = [i[0] for i in get_case_no()]
    elif choice == "Criminal":
        list_of_id = [i[0] for i in get_criminal_no()]
    elif choice == "CriminalBackup":
        list_of_id = [i[0] for i in get_criminalbackup_no()]
    elif choice == "User_Credentials":
        list_of_id = [i[0] for i in get_username()]
    
    # Check if the list of IDs is empty
    if not list_of_id:
        st.warning("No records available to delete.")
        return
    
    # Select ID to delete
    id = st.selectbox("Enter ID", list_of_id)
    
    # Delete record directly without confirmation
    if st.button("Delete Record"):
        try:
        # Ensure delRec function is called with proper arguments
            if choice == "User_Credentials":
                if id.lower() == "admin":  # Prevent deletion of admin user
                    st.error("admin username cannot be deleted.")
                    return

        # Call the delRec function and handle the deletion
            delRec(id, choice)  

        except Exception as e:
            st.error(f"An error occurred: {e}")  # Display error if any exception occurs

