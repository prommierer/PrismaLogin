import sqlite3
import hashlib

db = sqlite3.connect("users.db")
cursor = db.cursor()

cursor.execute("""
CREATE TABLE users(
id INTEGER PRIMARY KEY,
email TEXT UNIQUE,
password TEXT,
verified INTEGER,
admin INTEGER
)
""")

# Erster Admin
admin_email = "admin@prisma.local"   # PLACEHOLDER: Email für ersten Admin
admin_password = hashlib.sha256("admin123".encode()).hexdigest()  # PLACEHOLDER: Passwort für ersten Admin

cursor.execute(
"INSERT INTO users(email,password,verified,admin) VALUES(?,?,1,1)",
(admin_email,admin_password)
)

db.commit()
db.close()

print("Database erstellt!")