from db import get_all_contacts, initialize_database
import tkinter.messagebox
from tkinter import messagebox
import tkinter as tk
from contact import Contact

def view_contacts():
    window = tk.Toplevel()
    window.title("All Contacts")
    window.geometry("400x300")

    contacts = get_all_contacts()

    if not contacts:
        label = tk.Label(window, text="No contacts found.")
        label.pack(pady=10)
        return

    for contact in contacts:
        contact_label = tk.Label(window, text=str(contact), anchor='w', justify='left')
        contact_label.pack(padx=10, pady=2, anchor='w')

def add_contact_gui():
    window = tk.Toplevel()
    window.title("Add Contact")
    window.geometry("400x300")

    name_var = tk.StringVar()
    email_var = tk.StringVar()
    phone_var = tk.StringVar()

    # creating a label for
    # name using widget Label
    name_label = tk.Label(window, text='Name', font=('calibre', 10, 'bold'))

    # creating a entry for input
    # name using widget Entry
    name_entry = tk.Entry(window, textvariable=name_var, font=('calibre', 10, 'normal'))

    # creating a label for
    # email using widget Label
    email_label = tk.Label(window, text='Email', font=('calibre', 10, 'bold'))

    # creating a entry for input
    # email using widget Entry
    email_entry = tk.Entry(window, textvariable=email_var, font=('calibre', 10, 'normal'))

    # creating a label for
    # phone number using widget Label
    phone_label = tk.Label(window, text='Phone Number', font=('calibre', 10, 'bold'))

    # creating a entry for input
    # phone using widget Entry
    phone_entry = tk.Entry(window, textvariable=phone_var, font=('calibre', 10, 'normal'))

    def submit_contact():
        name = name_var.get().strip()
        email = email_var.get().strip()
        phone = phone_var.get().strip()

        # Validate fields
        if not name:
            tk.messagebox.showerror("Error", "Name cannot be empty.")
            return
        if not Contact.is_valid_email(email):
            tk.messagebox.showerror("Error", "Invalid email format.")
            return
        if not Contact.is_valid_phone(phone):
            tk.messagebox.showerror("Error", "Invalid phone number.")
            return

        # Create and save the contact
        contact = Contact(None,name, email, phone)  # ID will be set by DB
        from db import add_contact  # import locally to avoid circular issues
        add_contact(contact)

        tk.messagebox.showinfo("Success", "Contact added successfully.")
        window.destroy()

    name_label.pack()
    name_entry.pack()
    email_label.pack()
    email_entry.pack()
    phone_label.pack()
    phone_entry.pack()

    submit_button = tk.Button(window, text='Submit', command=submit_contact)
    submit_button.pack(pady=10)


def start_gui():
    window = tk.Tk()
    window.title("Contact Manager")
    window.geometry("300x200")
    view_button = tk.Button(window, text="View Contacts", width=25, command=view_contacts)
    add_button = tk.Button(window, text="Add Contact", width=25, command=add_contact_gui)
    quit_button = tk.Button(window, text="Quit", width=25, command=window.quit)

    view_button.pack(pady=5)
    add_button.pack(pady=5)
    quit_button.pack(pady=5)


    window.mainloop()

if __name__ == "__main__":
    initialize_database("contacts.db")
    start_gui()

