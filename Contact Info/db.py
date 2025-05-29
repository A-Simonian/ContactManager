import sqlite3
import contact

def initialize_database(file_name='contacts.db'):
    with sqlite3.connect(file_name) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL
            )
        ''')
        conn.commit()

def add_contact(contact):
    with sqlite3.connect("contacts.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO contacts (id, name, email, phone)
            VALUES (?, ?, ?, ?)
        """, (contact.contactID, contact.name, contact.email, contact.phoneNumber))

def is_duplicate(contact):
    with sqlite3.connect("contacts.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contacts WHERE name = ? and email = ?",
                       (contact.name, contact.email)
                       )
        result = cursor.fetchone()
        return result is not None

def get_all_contacts():
    with sqlite3.connect("contacts.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email, phone FROM contacts")
        rows = cursor.fetchall()

        return[contact.Contact(row[0], row[1], row[2], row[3]) for row in rows]

def run_query(sql, params=()):
    with sqlite3.connect("contacts.db") as conn:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        return cursor.fetchall()

def delete_contact(contact_id):
    with sqlite3.connect("contacts.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
        conn.commit()
        return cursor.rowcount

def update_contact(contact_id, name, email, phone):
    with sqlite3.connect("contacts.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE contacts
            SET name = ?, email = ?, phone = ?
            WHERE id = ?
        """, (name, email, phone, contact_id))
        conn.commit()
        return cursor.rowcount




