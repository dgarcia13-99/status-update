import sqlite3
import time
import datetime

database="status.sqlite"

create_database="""
CREATE TABLE IF NOT EXISTS status(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    description TEXT NOT NULL,
    date INT,
    time INT,
    CHECK ((username IS NOT NULL AND description IS NOT NULL) OR (username IS NULL AND description IS NULL))
    );
"""

def create_table(con):
    con.execute(create_database)
    
    
def delete_statuses(con):
    con.execute("""DELETE FROM status;""")
    

def status_samples(con):
    samples= [

        ("dgarc","Working on project 4", datetime.date.today(),datetime.time(9,45,0)),
        ("bwilliams","On my way to the zoo", datetime.date(2023, 4, 7),datetime.time(13,7,0)),
        ("mjackson","Learning a new dance",datetime.datetime(2022, 6, 13),datetime.time(10,11,0))
     
    ]

    for s in samples:
        con.execute("""INSERT INTO status (username, description, date, time) VALUES (?,?,?,?);""",s)


if __name__ == "__main__":
    con = sqlite3.connect(database)
    create_table(con)
    delete_statuses(con)
    status_samples(con)

    con.commit()
    con.close()