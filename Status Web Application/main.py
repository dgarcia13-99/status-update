#Daniela Garcia
#MCS 275 Spring 2023
#Final Project 4
#I have followed the rules for this assignment
#and declare this code is solely my own

"What are you working on?"

import flask
import sqlite3
import os
import time #for time information
from datetime import date #for date information
import status_database
from status_database import database


#THIS IS THE MAIN PAGE THAT HANDLES FORM REQUESTS AND UPDATES INFORMATION INTO THE DATABASE

app=flask.Flask("Status")

#HOMEPAGE
@app.route("/")
def homepage():
    "Showcase the home page"
    return flask.render_template("home.html")

#SUBMIT NEW STATUS PAGE
@app.route("/newstatus/")
def new_status():
    "Show the status submission page"
    return flask.render_template("submitstatus.html")

#NEW STATUS SUBMISSION
@app.route("/newstatus/submit",methods = ["POST", "GET"])
def submit_newstatus():
    "Handle the form submission from the 'new_status' route"

    #From form submission, get post information and insert into database
    username=flask.request.values.get("username")
    description=flask.request.values.get("description")
    date_=date.today()
    time_=time.time()
    
    #Add the username, description, and post id into the database
    con = sqlite3.connect(database)
    res=con.execute("""INSERT INTO status (username, description, date, time) VALUES (?,?,?,?);""",(username,description,date_,time_))
    con.commit()
    con.close()

    return flask.render_template("submission_success.html",username=username, description=description,date=date_,time=time_)

#USER STATUS PAGE
@app.route("/current_status/<username>")
def current_status(username):
    "Show user's current status page"
     
    #Access user's newest post description
    con = sqlite3.connect(database)
    res = con.execute("SELECT description FROM status WHERE username=? ORDER BY date DESC,time DESC LIMIT 1 ;",[username])
    post_description = res.fetchone()[0]
    con.commit() 
    con.close()
   
    return flask.render_template("currentstatus.html",username=username, post_description=post_description)

#HISTORY PAGE
@app.route("/history/<username>")
def history(username):
    "Show user's current status page"
     
    #Access user's newest post description
    con = sqlite3.connect(database)
    res = con.execute("SELECT username, description, date, time FROM status WHERE username=? ORDER BY date DESC,time DESC;",[username])
    history_info = res.fetchall()
    con.commit() 
    con.close()
   
    return flask.render_template("history.html",username=username, history_info=history_info)

#USERS PAGE
@app.route("/users/current/")
def users_current():
    "Create and display distinct users who have posted a status"
    con = sqlite3.connect(database)
    res=con.execute("SELECT DISTINCT username FROM status ORDER BY username ASC;")
    all_users=res.fetchall()
    con.commit() 
    con.close()
    return flask.render_template("users_current.html",all_users=all_users)

#USERS PAGE
@app.route("/users/history/")
def users_history():
    "Create and display distinct users who have posted a status"
    con = sqlite3.connect(database)
    res=con.execute("SELECT DISTINCT username FROM status ORDER BY username ASC;")
    all_users=res.fetchall()
    con.commit() 
    con.close()
    return flask.render_template("users_history.html",all_users=all_users)

#USER SEARCH FORM SUBMISSION/ CURRENT STATUS
@app.route("/search/current/", methods = ["POST", "GET"])
def user_search_current():
    "From search, redirect to user's current status page"
    username=flask.request.values.get("username")
    return flask.render_template("currentstatus.html",username=username)

#USER SEARCH FORM SUBMISSION/ HISTORY
@app.route("/search/history/", methods = ["POST", "GET"])
def user_search_history():
    "From search, redirect to user's status history page"
    username=flask.request.values.get("username")
    return flask.render_template("history.html",username=username)



# Check that database exists
#This code is directly taken from Professor Dumas' ordernova.py script
add_sample_data = False
if not os.path.exists(database):
    print("The database '{}' was not found.  Creating it.".format(database))
    add_sample_data = True

con = sqlite3.connect(database)

print("Making sure the DB contains the necessary tables...", end="")
status_database.create_table(con)
print("Done")

if add_sample_data:
    print("Populating DB with sample data, since it was empty...", end="")
    status_database.status_samples(con)
    print("Done")

con.commit()
con.close()

#run the application
app.run()
