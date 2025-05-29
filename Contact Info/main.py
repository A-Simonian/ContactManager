from contact import Contact
from db import initialize_database, add_contact, is_duplicate, get_all_contacts, delete_contact, update_contact
from search import search, search_by_id


def get_contact(next_id):
    name = input("Enter name: ").strip()
    while True:
        email = input("Enter email: ").strip()
        if Contact.is_valid_email(email):
            break
        print("Invalid email. Try again")
    while True:
        phoneNumber = input("Enter phone number: ").strip()
        if Contact.is_valid_phone(phoneNumber):
            break
        print("Invalid phone number. Try again")

    contactID = next_id

    contact = Contact(contactID, name, email, phoneNumber)

    return contact, next_id + 1

def update_contact_prompt():
    contact_id = input("Enter contact ID to update: ").strip()
    results = search_by_id(contact_id)

    if not results:
        print("Contact not found.")
        return

    contact = results[0]
    print("Current contact:")
    print(contact)

    while True:
        print("\nUpdate:")
        print("1. Name")
        print("2. Email")
        print("3. Phone")
        print("4. Done")
        choice = input("Enter choice: ")

        if choice == '1':
            contact.name = input("New name: ")
        elif choice == '2':
            contact.email = input("New email: ")
        elif choice == '3':
            contact.phoneNumber = input("New phone: ")
        elif choice == '4':
            break
        else:
            print("Invalid choice.")

    updated = update_contact(contact.contactID, contact.name, contact.email, contact.phoneNumber)
    if updated:
        print("Contact updated.")
    else:
        print("Update failed.")

# --- Main Driver ---
fileName = "contacts.db"
next_id = 1

initialize_database(fileName)


while True:
    print("Press 1 to add contact")
    print("Press 2 to search contact")
    print("Press 3 to delete contact")
    print("Press 4 to update contact")
    print("Press 5 to print all contacts")
    print("Press 6 to quit")
    choice = input("Enter choice: ")

    match choice:
        case '1':
            contact, next_id = get_contact(next_id)

            if not is_duplicate(contact):
                add_contact(contact)
            else:
                print("Contact already exists.")

        case '2':

            search()

        case '3':
            contact_id = input("Enter ID number to delete: ").strip()

            deleted = delete_contact(contact_id)

            if deleted:
                print("Contact deleted")
            else:
                print("Contact ID not found")

        case '4':
            update_contact_prompt()

        case '5':
            print("\nAll Contacts")
            print("------------")
            for contact in sorted(get_all_contacts(), key=lambda c: c.name.lower()):
                print(contact)

        case '6':
            break

        case _:
            print("Invalid choice")



