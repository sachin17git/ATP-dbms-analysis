import sys
import psycopg2
import pandas as pd

_, host, dbname, username, password = sys.argv

def connect(h, db, user, p):
    conn = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(host = h,
                                database = db,
                                port = 5432,
                                user = user,
                                password = p)
    
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    return conn


match_stats_df = pd.read_csv("./csv files/Match Stats.csv")
player_details_df = pd.read_csv("./csv files/Player Details.csv")
tournament_stats_df = pd.read_csv("./csv files/Tournament Stats.csv")
tournament_details_df = pd.read_csv("./csv files/Tournament_Details.csv")

sql_create_table = ["create table player (player_id integer primary key not null, name varchar(50), location varchar(5), height float(5), hand char(2));",
                    "create table tournament (tournament_id varchar(50) primary key not null, name varchar(50), surface varchar(10), year integer);",
                    "create table match_stats (tournament_id varchar(50), winner_id integer, loser_id integer, date varchar(20), score varchar(50), winner_points float(10), loser_points float(10), foreign key (tournament_id) references tournament(tournament_id), foreign key (winner_id) references player(player_id), foreign key (loser_id) references player(player_id));",
                    "create table tournament_stats (tournament_id varchar(50), w_ace float(10), w_df float(10), w_svpt float(10), w_SvGms float(10), w_bpSaved float(10), w_bpFaced float(10), l_ace float(10), l_df float(10), l_svpt float(10), l_SvGms float(10), l_bpSaved float(10), l_bpFaced float(10), foreign key (tournament_id) references tournament(tournament_id));"]

def create_table(conn, sql_q):
    cur = conn.cursor()

    for sql in sql_q:
        cur.execute(sql)

    conn.commit()
    cur.close()
    conn.close()
    print("Tables created")

conn = connect(host, dbname, username, password)
create_table(conn, sql_create_table)

sql_insert_table = ["insert into player values (%s, %s, %s, %s, %s)",
                    "insert into tournament values (%s, %s, %s, %s)",
                    "insert into match_stats values (%s, %s, %s, %s, %s, %s, %s)",
                    "insert into tournament_stats values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"]
conn = connect(host, dbname, username, password)
cur = conn.cursor()

# Insert into player table.
player_records = player_details_df.to_numpy().tolist()
player_result = [tuple(r) for r in player_records]
cur.executemany(sql_insert_table[0], player_result)

# insert into tournament table.
tournament_records = tournament_details_df.to_numpy().tolist()
tournament_result = [tuple(r) for r in tournament_records]
cur.executemany(sql_insert_table[1], tournament_result)

# insert into match_stats table.
matchstats_records = match_stats_df.to_numpy().tolist()
matchstats_result = [tuple(r) for r in matchstats_records]
cur.executemany(sql_insert_table[2], matchstats_result)

# insert into tournament_stats table.
tstats_records = tournament_stats_df.to_numpy().tolist()
tstats_result = [tuple(r) for r in tstats_records]
cur.executemany(sql_insert_table[3], tstats_result)

conn.commit()
cur.close()
conn.close()
print("Data ingestion complete.")




