
import pymysql
import streamlit as st


# Function to create and return a database connection and cursor
def get_db_connection():
    mydb = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="forensics"
    )
    cursor = mydb.cursor()
    return mydb, cursor

# Function to close the connection and cursor
def close_db_connection(mydb, cursor):
    cursor.close()
    mydb.close()

# Function to view all rows from a table
def viewTables(tableName):
    mydb, cursor = get_db_connection()
    command = f'SELECT * FROM {tableName};'
    cursor.execute(command)
    data = cursor.fetchall()
    close_db_connection(mydb, cursor)
    return data

def viewQueryResult(choice):
    mydb, cursor = get_db_connection()
    command=""
    if choice==1:
        command = 'select NameOfCase, model, Manufacturer from (AUTOMOBILE JOIN CASES ON AUTOMOBILE.CaseID=CASES.CaseID);'
    elif choice==2:
        command = 'select NameOfCase, dname,narcotic from (DRUGS JOIN CASES ON DRUGS.CaseID=CASES.CaseID);'
    elif choice==3:
        command = 'SELECT CASES.NameOfCase, BALLISTICS.model, BALLISTICS.manufacturer, BALLISTICS.year, BALLISTICS.typeofgun, BALLISTICS.gauge, BALLISTICS.caliber FROM BALLISTICS JOIN CASES ON BALLISTICS.CaseID = CASES.CaseID;'
    elif choice==4:
        command = 'select CName, NameOfCase  from (CriminalCase JOIN Criminal ON CriminalCase.CriminalID=Criminal.CID) JOIN CASES ON CASES.CaseID=CriminalCase.CrimeID;'
    elif choice==5:
        command = 'select DISTINCT CName, TypeOfCase  from (CriminalCase JOIN Criminal ON CriminalCase.CriminalID=Criminal.CID) JOIN CASES ON CASES.CaseID=CriminalCase.CrimeID;'
    elif choice==6:
        command = 'select DISTINCT CName, LeadingOfficer from (CASES JOIN (CRIMINALCASE JOIN CRIMINAL ON CRIMINALCASE.CriminalID=CRIMINAL.CID) ON Cases.CaseID=CriminalCase.CrimeID) UNION select DISTINCT CName, AsstOfficer from (CASES JOIN (CRIMINALCASE JOIN CRIMINAL ON CRIMINALCASE.CriminalID=CRIMINAL.CID) ON Cases.CaseID=CriminalCase.CrimeID);'
    elif choice==7:
        command = 'select NameOfCase, count(*) from (DRUGS NATURAL JOIN CASES) group by CaseID;'
    elif choice==8:
        command = 'select Solvent, count(*) from Paint group by Solvent;'
    elif choice==9:
        command = 'select narcotic, count(*) from DRUGS group by narcotic;'
    elif choice==10:
        command = 'select Loc, count(*) from CASES group by Loc;'
    elif choice==11:
        command = 'select DISTINCT NameOfCase, LeadingOfficer from CASES;'
    elif choice==12:
        command = 'select number_of_cases("ongoing");'
    elif choice==13:
        command='select number_of_criminals("Active");'
    elif choice==14:
        command='select dname from DRUGS where narcotic="yes" INTERSECT select dname from DRUGS where color="blue";' 
    elif choice==15:
        command='select number_of_cases_lead("Jake Peralta");'
    elif choice==16:
        command='select DISTINCT CName, LeadingOfficer from (CASES JOIN (CRIMINALCASE JOIN CRIMINAL ON CRIMINALCASE.CriminalID=CRIMINAL.CID) ON Cases.CaseID=CriminalCase.CrimeID) UNION select DISTINCT CName, AsstOfficer from (CASES JOIN (CRIMINALCASE JOIN CRIMINAL ON CRIMINALCASE.CriminalID=CRIMINAL.CID) ON Cases.CaseID=CriminalCase.CrimeID)'     
    elif choice==17:
        command='select DISTINCT CName, LeadingOfficer from (CASES JOIN (CRIMINALCASE JOIN CRIMINAL ON CRIMINALCASE.CriminalID=CRIMINAL.CID) ON Cases.CaseID=CriminalCase.CrimeID);'
   
    
    cursor.execute(command)
    data = cursor.fetchall()
    close_db_connection(mydb, cursor)
    return data


# Function to update status in specified table
def updateStatus(id, status, choice):
    mydb, cursor = get_db_connection()
    if choice == "Criminal":
        command = 'UPDATE CRIMINAL SET CurrentStatus = %s WHERE CID = %s'
    elif choice == "Cases":
        command = 'UPDATE CASES SET StatusOfCase = %s WHERE CaseID = %s'
    cursor.execute(command, (status, id))
    mydb.commit()
    close_db_connection(mydb, cursor)
    

# Function to execute a custom query
def execQuery(command):
    try:
        mydb, cursor = get_db_connection()
        cursor.execute(command)
        data = cursor.fetchall()  # Only valid for SELECT queries
        return data
    finally:
        close_db_connection(mydb, cursor)

# Function to get case numbers
def get_case_no():
    mydb, cursor = get_db_connection()
    cursor.execute('SELECT CaseID FROM CASES')
    case_ids = cursor.fetchall()
    close_db_connection(mydb, cursor)
    return case_ids

# Functions to get IDs for other tables
def get_criminal_no():
    mydb, cursor = get_db_connection()
    cursor.execute('SELECT CID FROM CRIMINAL')
    data = cursor.fetchall()
    close_db_connection(mydb, cursor)
    return data
def get_criminalbackup_no():
    mydb, cursor = get_db_connection()
    cursor.execute('SELECT ID FROM CRIMINALBACKUP')
    data = cursor.fetchall()
    close_db_connection(mydb, cursor)
    return data

def get_drug_no():
    mydb, cursor = get_db_connection()
    cursor.execute('SELECT NDC_No FROM DRUGS')
    data = cursor.fetchall()
    close_db_connection(mydb, cursor)
    return data

def get_automobile_no():
    mydb, cursor = get_db_connection()
    cursor.execute('SELECT AID FROM AUTOMOBILE')
    data = cursor.fetchall()
    close_db_connection(mydb, cursor)
    return data

def get_username():
    mydb, cursor = get_db_connection()
    cursor.execute('SELECT Username FROM user_credentials')
    data = cursor.fetchall()
    close_db_connection(mydb, cursor)
    return data

def get_ballistics_no():
    mydb, cursor = get_db_connection()
    cursor.execute('SELECT B_ID FROM BALLISTICS')
    data = cursor.fetchall()
    close_db_connection(mydb, cursor)
    return data

def get_paint_no():
    mydb, cursor = get_db_connection()
    cursor.execute('SELECT PID FROM PAINT')
    data = cursor.fetchall()
    close_db_connection(mydb, cursor)
    return data

def get_criminalcase_no():
    mydb, cursor = get_db_connection()
    cursor.execute('SELECT CID FROM CRIMINALCASE')
    data = cursor.fetchall()
    close_db_connection(mydb, cursor)
    return data

# Function to delete records from tables based on choice
import streamlit as st

def delRec(id, choice):
    mydb, cursor = get_db_connection()

    # Prevent deletion of admin username directly in the query
    if choice == "User_Credentials" and id.lower() == "admin":
        raise ValueError("Admin username cannot be deleted.")

    # Define deletion commands
    command = None
    if choice == "Automobile":
        command = 'DELETE FROM AUTOMOBILE WHERE AID = %s'
    elif choice == "Ballistics":
        command = 'DELETE FROM BALLISTICS WHERE B_ID = %s'
    elif choice == "Drugs":
        command = 'DELETE FROM DRUGS WHERE NDC_NO = %s'
    elif choice == "Paint":
        command = 'DELETE FROM PAINT WHERE PID = %s'
    elif choice == "Cases":
        command = 'DELETE FROM CASES WHERE CaseID = %s'
    elif choice == "Criminal":
        command = 'DELETE FROM CRIMINAL WHERE CID = %s'
    elif choice == "CriminalBackup":
        command = 'DELETE FROM CRIMINALBACKUP WHERE ID = %s'
    elif choice == "User_Credentials":
        command = 'DELETE FROM user_credentials WHERE USERNAME = %s'

    # Ensure the command is valid
    if command is None:
        raise ValueError(f"Invalid choice: {choice}")

    # Execute the command
    try:
        cursor.execute(command, (id,))
        mydb.commit()  # Commit the deletion

        # Display success message before closing the connection
        st.success("Successfully deleted the record")

    except Exception as e:
        st.error(f"An error occurred: {e}")
    
    finally:
        # Close the connection only after all operations are done
        close_db_connection(mydb, cursor)


# Functions to add records to each table
def add_automobile(cid, id, name, year, mfd, type):
    mydb, cursor = get_db_connection()
    command = 'INSERT INTO AUTOMOBILE VALUES(%s, %s, %s, %s, %s, %s)'
    cursor.execute(command, (cid, id, name, year, mfd, type))
    mydb.commit()
    close_db_connection(mydb, cursor)

def add_ballistics(cid, id, name, mfd, year, type, gauge, caliber, orig):
    mydb, cursor = get_db_connection()
    command = 'INSERT INTO BALLISTICS VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)'
    cursor.execute(command, (cid, id, name, mfd, year, type, gauge, caliber, orig))
    mydb.commit()
    close_db_connection(mydb, cursor)

def add_case(id, type, name, lo, ao, loc, stat):
    mydb, cursor = get_db_connection()
    command = 'INSERT INTO CASES VALUES(%s, %s, %s, %s, %s, NOW(), %s, %s)'
    cursor.execute(command, (id, type, name, lo, ao, loc, stat))
    mydb.commit()
    close_db_connection(mydb, cursor)

def add_criminal(id, name, alias, age, n, h, stat, dna, f, nationality):
    mydb, cursor = get_db_connection()
    command = 'INSERT INTO CRIMINAL VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    cursor.execute(command, (id, name, alias, age, n, h, stat, dna, f, nationality))
    mydb.commit()
    close_db_connection(mydb, cursor)

def add_drug(cid, code, name, color, dclass, narc):
    mydb, cursor = get_db_connection()
    command = 'INSERT INTO DRUGS VALUES(%s, %s, %s, %s, %s, %s)'
    cursor.execute(command, (cid, code, name, color, dclass, narc))
    mydb.commit()
    close_db_connection(mydb, cursor)

def add_paint(cid, id, col, sol, bind, pigment, add):
    mydb, cursor = get_db_connection()
    command = 'INSERT INTO PAINT VALUES(%s, %s, %s, %s, %s, %s, %s)'
    cursor.execute(command, (cid, id, col, sol, bind, pigment, add))
    mydb.commit()
    close_db_connection(mydb, cursor)

def add_criminalcase(cid, id):
    mydb, cursor = get_db_connection()
    command = 'INSERT INTO CriminalCase VALUES(%s, %s)'
    cursor.execute(command, (cid, id))
    mydb.commit()
    close_db_connection(mydb, cursor)

def add_user(nm, ps, rl):
    try:
        mydb, cursor = get_db_connection()
        command = 'INSERT INTO user_credentials VALUES(%s, %s, %s)'
        cursor.execute(command, (nm, ps, rl))
        mydb.commit()
    except Exception as e:
        if "Duplicate entry" in str(e) or "UNIQUE constraint failed" in str(e):  # Match error message for your DB
            raise ValueError("Username already exists")
        else:
            raise ValueError("An unexpected error occurred: {}".format(e))
    finally:
        close_db_connection(mydb, cursor)
