import psycopg2
import streamlit as st
import pandas as pd
import numpy as np
import psycopg2.extras


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
    with conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cur:
        cur.execute(query)
        return cur.fetchall()

navigate = st.sidebar.radio("Contents", ["Main", "Database", "Retrieval", "Queries", "ER diagram"], index=0)

if navigate=="Main":
    st.subheader("ATP Analysis")
    st.caption("Association of Tennis Professionals")
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
                #results = pd.DataFrame(results, columns=['Player_ID', 'Player_Name', 'Player_Location', 'Player_Height','Player_Hand'])
                results = pd.DataFrame(results)
                st.dataframe(results)
            elif table=="Tournament":
                sql = "SELECT * from tournament;"
                results = run_query(sql)
                #results = pd.DataFrame(results, columns=['Tournament_ID', 'Tournament_Name', 'Surface', 'Year'])
                results = pd.DataFrame(results)
                st.dataframe(results)
            elif table=='Match Stats':
                sql = "SELECT * from match_stats;"
                results = run_query(sql)
                #results = pd.DataFrame(results, columns=['Tournament_ID', 'Winner_ID', 'Loser_ID', 'Date', 'Score', 'Winner_Points', 'Loser_Points'])
                results = pd.DataFrame(results)
                st.dataframe(results)
            elif table=='Tournament Stats':
                sql = "SELECT * from tournament_stats;"
                results = run_query(sql)
                #results = pd.DataFrame(results, columns=['tournament_id', 'w_ace', 'w_df', 'w_svpt', 'w_SvGms', 'w_bpSaved',
                #                                       'w_bpFaced', 'l_ace', 'l_df', 'l_svpt', 'l_SvGms', 'l_bpSaved','l_bpFaced'])
                results = pd.DataFrame(results)
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
            results = pd.DataFrame(results)
            if len(results) > 0:
                st.dataframe(results)
    else:
        st.error("Database not connected!")
        st.info("Please connect to the database.")

elif navigate=="Queries":
    st.subheader("SQL queries and analysis.")
    st.write("\n")
    st.info("Number of Matches won by a Player")
    col1, col2 = st.columns(2)
    q1 = """select player.player_id, player.name, count(match_stats.winner_points) AS matches_won
from match_stats left join player ON player.Player_ID = match_stats.Winner_ID
GROUP BY player.player_id, player.name
ORDER BY matches_won DESC"""
    col1.code(q1)
    r1 = run_query(q1)
    r1 = pd.DataFrame(r1)
    col2.dataframe(r1)
    st.write("\n\n\n\n\n\n")

    st.info("Number of Matches lost by a Player")
    col1, col2 = st.columns(2)
    q2 = """select player.player_id, player.name, count(match_stats.loser_points) AS matches_lost 
from match_stats inner join player ON player.Player_ID = match_stats.loser_ID
GROUP BY player.player_id, player.name
ORDER BY matches_lost DESC"""
    col1.code(q2)
    r2 = run_query(q2)
    r2 = pd.DataFrame(r2)
    col2.dataframe(r2)
    st.write("\n\n\n\n\n\n")

    st.info("Number of Matches won by a Player on a particular surface")
    col1, col2 = st.columns(2)
    q3 = """select player.Player_ID, player.name, a.Surface, 
count(a.Surface) AS surface_count
from (tournament INNER JOIN match_stats ON tournament.Tournament_ID = match_stats.Tournament_ID) A 
LEFT JOIN player ON A.Winner_ID = player.player_id
where player.Player_ID in (SELECT DISTINCT match_stats.Winner_ID from match_stats) 
group by a.Surface, player.Player_ID, player.name
order by player.Player_ID, player.Name, surface_count DESC"""
    col1.code(q3)
    r3 = run_query(q3)
    r3 = pd.DataFrame(r3)
    col2.dataframe(r3)
    st.write("\n\n\n\n\n\n")

    st.info("Insert rows to the player table")
    col1, col2 = st.columns(2)
    iq4 = """INSERT INTO player 
VALUES (111111,'Prajval Nataraj','IND','170','R');
VALUES (222222,'Sachin BS','IND','183','R');"""
    q4 = "select * from player where player_id in (111111,222222)"
    col1.code(iq4)
    r4 = run_query(q4)
    r4 = pd.DataFrame(r4)
    col2.dataframe(r4)
    st.write("\n\n\n\n\n\n")

    st.info("Add a column 'player_type_winner' in match_stats table")
    col1, col2 = st.columns(2)
    iq5 = """ALTER TABLE match_stats
ADD player_type_winner VARCHAR(50);"""
    #q5 = "select * from match_stats"
    col1.code(iq5)
    #r5 = run_query(q5)
    #r5 = pd.DataFrame(r5)
    #col2.dataframe(r5)
    st.write("\n\n\n\n\n\n")
    
    st.info("Delete a column 'player_type_winner' from match_stats table")
    col1, col2 = st.columns(2)
    q6 = """ALTER TABLE match_stats
DROP COLUMN player_type_winner;"""
    col1.code(q6)
    #r6 = run_query(q6)
    #r6 = pd.DataFrame(r6)
    #col2.dataframe(r6)
    st.write("\n\n\n\n\n\n")
    
    st.info("Add values to the player_type_winner. If the Player is the 'USA'  he will be assigned as Local else International")
    col1, col2 = st.columns(2)
    iq7 = """UPDATE match_stats
SET player_type_winner = 'local'
WHERE winner_id IN (select distinct match_stats.winner_id 
					from match_stats INNER JOIN player ON match_stats.Winner_ID = player.player_id 
					WHERE player.location = 'USA')
                    
UPDATE match_stats
SET player_type_winner = 'international'
WHERE winner_id IN (select distinct match_stats.winner_id 
					from match_stats INNER JOIN player ON match_stats.Winner_ID = player.player_id 
					WHERE player.location != 'USA')
"""
    q7 = """select * from match_stats"""
    col1.code(iq7)
    r7 = run_query(q7)
    r7 = pd.DataFrame(r7)
    col2.dataframe(r7)
    st.write("\n\n\n\n\n\n")


    st.info("Find how many points each player has won per year.")
    col1, col2 = st.columns(2)
    q8 = """select match_stats.winner_id ,tournament.year, sum(match_stats.winner_points) as total_winning_points
from match_stats inner join tournament on tournament.Tournament_ID = match_stats.Tournament_ID
group by match_stats.winner_id ,tournament.year
order by match_stats.winner_id, tournament.year, total_winning_points DESC"""
    col1.code(q8)
    r8 = run_query(q8)
    r8 = pd.DataFrame(r8)
    col2.dataframe(r8)
    st.write("\n\n\n\n\n\n")
    

    st.info("Highest scorer of that particular year.")
    col1, col2 = st.columns(2)
    q11 = """select e.year, e.highest_point, player.name from 
(select c.year, c.highest_point, d.winner_id from
(select b.year, max(b.total_winning_points) as highest_point from 
(select match_stats.winner_id ,tournament.year, sum(match_stats.winner_points) as total_winning_points
from match_stats inner join tournament on tournament.Tournament_ID = match_stats.Tournament_ID
group by match_stats.winner_id ,tournament.year
order by match_stats.winner_id, tournament.year, total_winning_points DESC) b
group by b.year) c INNER JOIN (select match_stats.winner_id ,tournament.year, sum(match_stats.winner_points) as total_winning_points
from match_stats inner join tournament on tournament.Tournament_ID = match_stats.Tournament_ID
group by match_stats.winner_id ,tournament.year
order by match_stats.winner_id, tournament.year, total_winning_points DESC) d ON c.year = d.year AND c.highest_point = d.total_winning_points
order by c.year) e INNER JOIN player on e.winner_id = player.player_id 
order by e.year DESC;"""
    col1.code(q11)
    r11 = run_query(q11)
    r11 = pd.DataFrame(r11)
    col2.dataframe(r11)
    col1.metric("Execution time", "79 ms")
    st.write("\n\n\n\n\n\n")


    st.info("Introducing indexing")
    q12 = """CREATE INDEX idx_player ON player (name, location, height, hand);
CREATE INDEX idx_tournament ON tournament (tournament_id, name, surface, year);
CREATE INDEX idx_matchstats ON match_stats (tournament_id, winner_id, loser_id, date, score, winner_points, loser_points);"""
    st.code(q12)
    st.write("\n\n\n\n\n\n")

    st.info("After indexing, Highest scorer of that particular year.")
    q13 = """select e.year, e.highest_point, player.name from 
(select c.year, c.highest_point, d.winner_id from
(select b.year, max(b.total_winning_points) as highest_point from 
(select match_stats.winner_id ,tournament.year, sum(match_stats.winner_points) as total_winning_points
from match_stats inner join tournament on tournament.Tournament_ID = match_stats.Tournament_ID
group by match_stats.winner_id ,tournament.year
order by match_stats.winner_id, tournament.year, total_winning_points DESC) b
group by b.year) c INNER JOIN (select match_stats.winner_id ,tournament.year, sum(match_stats.winner_points) as total_winning_points
from match_stats inner join tournament on tournament.Tournament_ID = match_stats.Tournament_ID
group by match_stats.winner_id ,tournament.year
order by match_stats.winner_id, tournament.year, total_winning_points DESC) d ON c.year = d.year AND c.highest_point = d.total_winning_points
order by c.year) e INNER JOIN player on e.winner_id = player.player_id 
order by e.year DESC;"""
    col1, col2 = st.columns(2)
    col1.code(q13)
    r13 = run_query(q13)
    r13 = pd.DataFrame(r13)
    col2.dataframe(r13)
    col1.metric("Execution time", "64 ms", "-15 ms")
    st.write("\n\n\n\n\n\n")


    st.info("Delete all the player_id from player table which are in the loser_id of match_stats")
    q14 = """DELETE FROM player
WHERE player_id IN (SELECT DISTINCT loser_id FROM match_stats)"""
    st.code(q14)
    st.write("\n\n\n\n\n\n")


    st.info("Delete all rows from tournament_stats where w_ace =< 5")
    q15 = """DELETE FROM tournament_stats
WHERE w_ace =< 5"""
    st.code(q15)
    st.write("\n\n\n\n\n\n")


    



    