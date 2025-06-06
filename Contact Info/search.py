from contact import Contact
from db import run_query

def search_by_name(query):
    sql = "SELECT id, name, email, phone FROM contacts WHERE LOWER(name) LIKE ?"
    params = (f"%{query.lower()}%",)
    rows = run_query(sql, params)
    return [Contact(*row) for row in rows]

def search_by_email(query):
    sql = "SELECT id, name, email, phone FROM contacts WHERE LOWER(email) LIKE ?"
    params = (f"%{query.lower()}%",)
    rows = run_query(sql, params)
    return [Contact(*row) for row in rows]

def search_by_phone(query):
    sql = "SELECT id, name, email, phone FROM contacts WHERE phone = ?"
    params = (query,)
    rows = run_query(sql, params)
    return [Contact(*row) for row in rows]

def search_by_id(query):
    sql = "SELECT id, name, email, phone FROM contacts WHERE id = ?"
    params = (query,)
    rows = run_query(sql, params)
    return [Contact(*row) for row in rows]

def search_all_fields(query):
    sql = """
        SELECT id, name, email, phone FROM contacts
        WHERE LOWER(name) LIKE ?
           OR LOWER(email) LIKE ?
           OR phone LIKE ?
           OR CAST(id AS TEXT) = ?
    """
    query_like = f"%{query.lower()}%"
    params = (query_like, query_like, f"%{query}%", query)
    rows = run_query(sql, params)
    return [Contact(*row) for row in rows]


def search():
    print("Search by:")
    print("1. Name")
    print("2. Email")
    print("3. Phone")
    print("4. ID")
    print("5. Back")
    search_choice = input("Enter choice: ")

    if search_choice == '1':
        query = input("Enter name to find: ").strip()
        results = search_by_name(query)
    elif search_choice == '2':
        query = input("Enter email to find: ").strip()
        results = search_by_email(query)
    elif search_choice == '3':
        query = input("Enter phone number to find: ").strip()
        results = search_by_phone(query)
    elif search_choice == '4':
        query = input("Enter contact ID to find: ").strip()
        results = search_by_id(query)
    elif search_choice == '5':
        return
    else:
        print("Invalid choice.")
        return

    if results:
        for contact in results:
            print(contact)
    else:
        print("Contact not found.")
