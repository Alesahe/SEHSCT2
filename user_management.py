from filelock import FileLock
import sqlite3 as sql
import time
import random
import html
import bcrypt

def hash(password):
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode('utf-8'), salt)

def insertUser(username, password, DoB):
    password = hash(password)
    html.escape(username, quote=True)
    # html.escape(password, quote=True)
    html.escape(DoB, quote=True)
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    cur.execute(
        "INSERT INTO users (username,password,dateOfBirth) VALUES (?,?,?)",
        (username, password, DoB),
    )
    con.commit()
    con.close()


def retrieveUsers(username, password):
    password = hash(password)
    html.escape(username, quote=True)
    # html.escape(password, quote=True)
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    cur.execute(
        "SELECT * FROM users WHERE username = ?", 
        (username,),
    )
    if cur.fetchone() == None:
        con.close()
        return False
    else:
        cur.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?", 
            (username, password,),
        )
        
        #call update visitor count
        updateVisitorCount()
        
        # Simulate response time of heavy app for testing purposes
        time.sleep(random.randint(80, 90) / 1000)
        if cur.fetchone() == None:
            con.close()
            return False
        else:
            con.close()
            return True

def updateVisitorCount():
    # Plain text log of visitor count as requested by Unsecure PWA management
    lockedFile = "visitor_log.txt.lock"
    with FileLock("visitor_log.txt.lock"):
        with open("visitor_log.txt", "r") as file:
            number = int(file.read().strip())
            number += 1
        with open("visitor_log.txt", "w") as file:
            file.write(str(number))

def insertFeedback(feedback):
    html.escape(feedback)
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    cur.execute(
        "INSERT INTO feedback (feedback) VALUES (?)",
        (feedback,),
    )
    con.commit()
    con.close()


def listFeedback():
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    data = cur.execute("SELECT * FROM feedback").fetchall()
    con.close()
    f = open("templates/partials/success_feedback.html", "w")
    for row in data:
        f.write("<p>\n")
        f.write(f"{row[1]}\n")
        f.write("</p>\n")
    f.close()
