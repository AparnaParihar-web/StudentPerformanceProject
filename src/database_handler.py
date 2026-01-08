import sqlite3
import os

DB_PATH = 'Data/student_performance.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS Students (
        Roll_No INTEGER PRIMARY KEY,
        Name TEXT
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS Subjects (
        Subject_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Subject_Name TEXT
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS Results (
        Result_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Roll_No INTEGER,
        Subject_ID INTEGER,
        Marks REAL,
        Grade TEXT
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS Attendance (
        Attendance_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Roll_No INTEGER,
        Percentage REAL
    )""")

    conn.commit()
    conn.close()

def insert_processed_dataframe(df):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    for _, row in df.iterrows():
        cur.execute("INSERT OR IGNORE INTO Students(Roll_No, Name) VALUES(?,?)",
                    (int(row['Roll_No']), row['Name']))

    subjects = [c for c in df.columns if c not in ('Roll_No','Name','Total','Percentage','Grade','Attendance(%)')]
    for s in subjects:
        cur.execute("INSERT OR IGNORE INTO Subjects(Subject_Name) VALUES(?)", (s,))

    conn.commit()

    cur.execute("SELECT Subject_ID, Subject_Name FROM Subjects")
    subj_map = {name: sid for sid, name in cur.fetchall()}

    for _, row in df.iterrows():
        roll = int(row['Roll_No'])
        for s in subjects:
            cur.execute("INSERT INTO Results(Roll_No, Subject_ID, Marks, Grade) VALUES(?,?,?,?)",
                        (roll, subj_map[s], float(row[s]), row['Grade']))
        cur.execute("INSERT INTO Attendance(Roll_No, Percentage) VALUES(?,?)",
                    (roll, float(row['Attendance(%)'])))

    conn.commit()
    conn.close()