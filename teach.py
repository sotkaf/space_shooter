import sqlite3
from datetime import datetime

# Δημιουργία σύνδεσης με SQLite βάση
conn = sqlite3.connect("teacheranytime_erp.db")
cursor = conn.cursor()

# Δημιουργία πινάκων
cursor.execute('''
CREATE TABLE IF NOT EXISTS Teachers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    subject TEXT,
    email TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Lessons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    teacher_id INTEGER,
    student_id INTEGER,
    datetime TEXT,
    duration INTEGER,
    price REAL,
    FOREIGN KEY (teacher_id) REFERENCES Teachers(id),
    FOREIGN KEY (student_id) REFERENCES Students(id)
)
''')

conn.commit()

# -------- Εισαγωγή δεδομένων ----------
def add_teacher(name, subject, email):
    cursor.execute("INSERT INTO Teachers (name, subject, email) VALUES (?, ?, ?)", (name, subject, email))
    conn.commit()

def add_student(name, email):
    cursor.execute("INSERT INTO Students (name, email) VALUES (?, ?)", (name, email))
    conn.commit()

def schedule_lesson(teacher_id, student_id, date_str, duration, price):
    cursor.execute('''
        INSERT INTO Lessons (teacher_id, student_id, datetime, duration, price)
        VALUES (?, ?, ?, ?, ?)''',
        (teacher_id, student_id, date_str, duration, price))
    conn.commit()

# -------- Ερωτήματα ----------
def list_lessons():
    cursor.execute('''
        SELECT L.id, T.name, S.name, L.datetime, L.duration, L.price
        FROM Lessons L
        JOIN Teachers T ON L.teacher_id = T.id
        JOIN Students S ON L.student_id = S.id
    ''')
    for row in cursor.fetchall():
        print(f"Lesson ID: {row[0]} | Teacher: {row[1]} | Student: {row[2]} | Date: {row[3]} | Duration: {row[4]} min | Price: €{row[5]}")

# -------- Δοκιμή ----------
if __name__ == "__main__":
    add_teacher("Γιώργος Παπαδόπουλος", "Μαθηματικά", "g.pap@example.com")
    add_student("Ελένη Νικολάου", "eleni@example.com")
    schedule_lesson(1, 1, "2025-07-10 18:00", 60, 20.0)

    print("📚 Προγραμματισμένα Μαθήματα:")
    list_lessons()
