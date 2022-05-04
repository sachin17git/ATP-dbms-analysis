import psycopg2
import streamlit as st
import pandas as pd
import numpy as np


def connect():
    conn = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(host = "localhost",
                                database = 'TennisATP',
                                port = 5432,
                                user = 'postgres',
                                password = 'sachin@123')
    
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    return conn

conn = connect()

@st.cache(allow_output_mutation=True,
          hash_funcs={psycopg2.extensions.connection: conn},
          suppress_st_warning=True)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

navigate = st.sidebar.radio("Contents", ["Main", "Database", "Retrieval", "ER diagram", "Queries"], index=1)

if navigate=="Main":
    st.subheader("ATP Analysis")
    st.markdown("Statistical Analysis of tennis professionals for the past 3 years with the help of a database management system.")
    st.image('front1.jpg', caption=""" "Tennis is a fine balance between determination and tiredness." """, width=700)
    
elif navigate=="Database":
    st.subheader("Database connectivity")
    container = st.container()
    if conn:
        st.info("Database Connected!")
        db_dict = { "host" : "localhost", 
                    "database" : 'TennisATP',
                    "port" : 5432,
                    "user" : 'postgres'}
        st.write(" ")
        st.write("Db details")
        st.json(db_dict)
    
        with st.expander("Tables", expanded=True):
            table = st.selectbox('Select table to extract from the db', ['Player', 'Tournament', 'Match Stats', 'Tournament Stats'])
            if table=='Player':
                sql = "SELECT * from player;"
                results = run_query(sql)
                results = pd.DataFrame(results, columns=['Player_ID', 'Player_Name', 'Player_Location', 'Player_Height','Player_Hand'])
                st.dataframe(results)
            elif table=="Tournament":
                sql = "SELECT * from tournament;"
                results = run_query(sql)
                results = pd.DataFrame(results, columns=['Tournament_ID', 'Tournament_Name', 'Surface', 'Year'])
                st.dataframe(results)
            elif table=='Match Stats':
                sql = "SELECT * from match_stats;"
                results = run_query(sql)
                results = pd.DataFrame(results, columns=['Tournament_ID', 'Winner_ID', 'Loser_ID', 'Date', 'Score', 'Winner_Points', 'Loser_Points'])
                st.dataframe(results)
            elif table=='Tournament Stats':
                sql = "SELECT * from tournament_stats;"
                results = run_query(sql)
                results = pd.DataFrame(results, columns=['tournament_id', 'w_ace', 'w_df', 'w_svpt', 'w_SvGms', 'w_bpSaved',
                                                        'w_bpFaced', 'l_ace', 'l_df', 'l_svpt', 'l_SvGms', 'l_bpSaved','l_bpFaced'])
                st.dataframe(results)
    else:
        st.error("Database connection failed")
        st.info("Please try again")

elif navigate=="ER diagram":
    st.image("new_ER.png")
elif navigate=="Retrieval":
    st.subheader("Retrieval")
    st.write(" ")
    st.write(" ")
    if conn:
        query = st.text_input("Please enter a valid query.")
        if query:
            results = run_query(query)
            if results:
                st.dataframe(results)
    else:
        st.error("Database not connected!")
        st.info("Please connect to the database.")
