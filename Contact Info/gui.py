from db import get_all_contacts, initialize_database
import tkinter.messagebox
from tkinter import messagebox
import tkinter as tk
from contact import Contact
import csv
from tkinter import filedialog

contact_window = None

def export_contacts_to_csv():
    contacts = get_all_contacts()

    if not contacts:
        messagebox.showinfo("No Contacts", "There are no contacts to export")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv")],
        title="Save Contacts As"
    )

    if not file_path:
        return #User cancelled save process

    try:
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Name", "Email", "Phone"]) #header

            for contact in contacts:
                writer.writerow([contact.contactID, contact.name, contact.email, contact.phoneNumber])

        messagebox.showinfo("Export Successful", f"Contacts exported to:\n{file_path}")

    except Exception as e:
        messagebox.showerror("Export Failed", f"An error occurred: \n{str(e)}")

def import_contacts_from_csv():
    file_path = filedialog.askopenfilename(
        filetypes=[("CSV Files", "*.csv")],
        title="Select CSV File to Import"
    )

    if not file_path:
        return #user cancels opening file

    imported = 0
    skipped = 0
    errors = []

    from db import add_contact
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        expected_headers = {"Name", "Email", "Phone"}

        if not expected_headers.issubset(set(reader.fieldnames)):
            messagebox.showerror("Invalid File", "CSV File must contain Name, Email, and Phone columns")
            return

            for i, row in enumerate(reader, start=2):  # line 2 is first row after header
                name = row.get("Name", "").strip()
                email = row.get("Email", "").strip()
                phone = row.get("Phone", "").strip()

                if not name or not Contact.is_valid_email(email) or not Contact.is_valid_phone(phone):
                    skipped += 1
                    errors.append(f"Line {i}: Invalid data")
                    continue

                contact = Contact(None, name, email, phone)
                add_contact(contact)
                imported += 1

        message = f"Imported: {imported} contact(s).\nSkipped: {skipped} invalid row(s)."
        if skipped > 0:
            message += "\n\nDetails:\n" + "\n".join(errors[:5])
            if skipped > 5:
                message += "\n... (more skipped entries not shown)"

        messagebox.showinfo("Import Completed", message)

        if contact_window and contact_window.winfo_exists():
            refresh_contact_list()

def delete_contact_gui():
    window =  tk.Toplevel()
    window.title("Delete Contact")
    window.geometry("400x300")

    contacts = get_all_contacts()

    if not contacts:
        tk.Label(window, text="No Contacts to delete.").pack(pady=10)
        return

        # Frame to hold both the listbox and the scrollbar
    list_frame = tk.Frame(window)
    list_frame.pack(pady=10)

    scrollbar = tk.Scrollbar(list_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox = tk.Listbox(list_frame, width=50, height=10, yscrollcommand=scrollbar.set)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH)

    scrollbar.config(command=listbox.yview)

    contact_map = {}

    for contact in contacts:
        display_text = f"{contact.contactID}: {contact.name} ({contact.email})"
        contact_map[display_text] = contact.contactID
        listbox.insert(tk.END, display_text)


    def delete_selected():
        selection = listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "No contact selected.")
            return

        selected_text = listbox.get(selection[0])
        contact_id = contact_map[selected_text]

        from db import delete_contact

        success = delete_contact(contact_id)

        if success:
            messagebox.showinfo("Success", "Contact Deleted.")
            window.destroy()
            if contact_window and contact_window.winfo_exists():
                refresh_contact_list()
        else:
            messagebox.showerror("Error", "Failed to delete contact.")

    delete_button = tk.Button(window, text="Delete Selected", command=delete_selected)
    delete_button.pack()


def view_contacts():
    global contact_window

    if contact_window is not None and contact_window.winfo_exists():
        contact_window.lift()
        refresh_contact_list()
        return

    contact_window = tk.Toplevel()
    contact_window.title("All Contacts")
    contact_window.geometry("400x300")


    refresh_contact_list()


def refresh_contact_list():
    global contact_window

    if contact_window is None or not contact_window.winfo_exists():
        return  # If the window isn't open, do nothing

    for widget in contact_window.winfo_children():
        widget.destroy()

    from db import get_all_contacts
    contacts = get_all_contacts()

    if not contacts:
        label = tk.Label(contact_window, text="No contacts found.")
        label.pack(pady=10)
        return

    for contact in contacts:
        label = tk.Label(contact_window, text=str(contact), anchor='w', justify='left')
        label.pack(padx=10, pady=2, anchor='w')


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
        contact = Contact(None, name, email, phone)
        from db import add_contact
        add_contact(contact)

        if contact_window and contact_window.winfo_exists():
            refresh_contact_list()
        else:
            view_contacts()

        messagebox.showinfo("Success", "Contact added successfully.")
        window.destroy()

    name_label.pack()
    name_entry.pack()
    email_label.pack()
    email_entry.pack()
    phone_label.pack()
    phone_entry.pack()

    submit_button = tk.Button(window, text='Submit', command=submit_contact)
    submit_button.pack(pady=10)

def update_contact_gui():
    window = tk.Toplevel()
    window.title("Update Contact")
    window.geometry("400x400")

    contacts = get_all_contacts()

    if not contacts:
        tk.Label(window, text="No contacts to update.").pack(pady=10)
        return

    tk.Label(window, text="Select a contact to update:").pack()

    # Frame to hold both the listbox and the scrollbar
    list_frame = tk.Frame(window)
    list_frame.pack(pady=10)

    scrollbar = tk.Scrollbar(list_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox = tk.Listbox(list_frame, width=50, height=10, yscrollcommand=scrollbar.set)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH)

    scrollbar.config(command=listbox.yview)

    contact_map = {}

    for contact in contacts:
        display_text = f"{contact.contactID}: {contact.name} ({contact.email})"
        contact_map[display_text] = contact
        listbox.insert(tk.END, display_text)

    name_var = tk.StringVar()
    email_var = tk.StringVar()
    phone_var = tk.StringVar()

    def on_select(event):
        selected = listbox.curselection()
        if not selected:
            return

        selected_text = listbox.get(selected[0])
        contact = contact_map[selected_text]
        print(f"Selected contact: {contact}")

        name_var.set(contact.name)
        email_var.set(contact.email)
        phone_var.set(contact.phoneNumber)

    listbox.bind("<<ListboxSelect>>", on_select)

    tk.Label(window, text="Name:").pack()
    name_entry = tk.Entry(window, textvariable=name_var)
    name_entry.pack()

    tk.Label(window, text="Email:").pack()
    email_entry = tk.Entry(window, textvariable=email_var)
    email_entry.pack()

    tk.Label(window, text="Phone:").pack()
    phone_entry = tk.Entry(window, textvariable=phone_var)
    phone_entry.pack()

    def save_changes():
        selected = listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "No contact selected.")
            return

        contact = contact_map[listbox.get(selected[0])]

        name = name_var.get().strip()
        email = email_var.get().strip()
        phone = phone_var.get().strip()

        if not name:
            messagebox.showerror("Error", "Name cannot be empty.")
            return
        if not Contact.is_valid_email(email):
            messagebox.showerror("Error", "Invalid email format.")
            return
        if not Contact.is_valid_phone(phone):
            messagebox.showerror("Error", "Invalid phone number.")
            return

        from db import update_contact
        success = update_contact(contact.contactID, name, email, phone)
        if success:
            messagebox.showinfo("Success", "Contact updated.")
            window.destroy()
            if contact_window and contact_window.winfo_exists():
                refresh_contact_list()
        else:
            messagebox.showerror("Error", "Update failed.")

    save_button = tk.Button(window, text="Save Changes", command=save_changes)
    save_button.pack(pady=10)


def search_contact_gui():
    window = tk.Toplevel()
    window.title("Search Contact")
    window.geometry("450x350")

    tk.Label(window, text="Enter name or part of name:").pack(pady=5)
    search_var = tk.StringVar()
    search_entry = tk.Entry(window, textvariable=search_var, width=40)
    search_entry.pack(pady=5)

    # Frame to hold Listbox and Scrollbar
    result_frame = tk.Frame(window)
    result_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(result_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox = tk.Listbox(result_frame, width=60, height=10, yscrollcommand=scrollbar.set)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar.config(command=listbox.yview)

    contact_map = {}

    def perform_search():
        query = search_var.get().strip()
        listbox.delete(0, tk.END)

        if not query:
            messagebox.showwarning("Warning", "Search query cannot be empty.")
            return

        from search import search_all_fields
        results = search_all_fields(query)

        if not results:
            listbox.insert(tk.END, "No results found.")
            return

        for contact in results:
            display_text = f"{contact.contactID}: {contact.name} ({contact.email})"
            contact_map[display_text] = contact
            listbox.insert(tk.END, display_text)

    search_button = tk.Button(window, text="Search", command=perform_search)
    search_button.pack(pady=5)

    def on_select(event):
        selection = listbox.curselection()
        if not selection:
            return
        selected_text = listbox.get(selection[0])
        contact = contact_map.get(selected_text)
        if contact:
            open_update_window_with_contact(contact)

    listbox.bind("<<ListboxSelect>>", on_select)

def open_update_window_with_contact(contact):
    window = tk.Toplevel()
    window.title("Update Contact")
    window.geometry("400x300")

    name_var = tk.StringVar(value=contact.name)
    email_var = tk.StringVar(value=contact.email)
    phone_var = tk.StringVar(value=contact.phoneNumber)

    tk.Label(window, text="Name:").pack()
    name_entry = tk.Entry(window, textvariable=name_var)
    name_entry.pack()

    tk.Label(window, text="Email:").pack()
    email_entry = tk.Entry(window, textvariable=email_var)
    email_entry.pack()

    tk.Label(window, text="Phone:").pack()
    phone_entry = tk.Entry(window, textvariable=phone_var)
    phone_entry.pack()

    def save_changes():
        name = name_var.get().strip()
        email = email_var.get().strip()
        phone = phone_var.get().strip()

        if not name:
            messagebox.showerror("Error", "Name cannot be empty.")
            return
        if not Contact.is_valid_email(email):
            messagebox.showerror("Error", "Invalid email format.")
            return
        if not Contact.is_valid_phone(phone):
            messagebox.showerror("Error", "Invalid phone number.")
            return

        from db import update_contact
        success = update_contact(contact.contactID, name, email, phone)
        if success:
            messagebox.showinfo("Success", "Contact updated.")
            window.destroy()
            if contact_window and contact_window.winfo_exists():
                refresh_contact_list()
        else:
            messagebox.showerror("Error", "Update failed.")

    save_button = tk.Button(window, text="Save Changes", command=save_changes)
    save_button.pack(pady=10)


def start_gui():
    window = tk.Tk()
    window.title("Contact Manager")
    window.resizable(True, False)  # Let it grow vertically as needed

    button_frame = tk.Frame(window)
    button_frame.pack(padx=10, pady=10)

    buttons = [
        ("View Contacts", view_contacts),
        ("Add Contact", add_contact_gui),
        ("Search Contact", search_contact_gui),
        ("Update Contact", update_contact_gui),
        ("Delete Contact", delete_contact_gui),
        ("Export Contact", export_contacts_to_csv),
        ("Import Contact", import_contacts_from_csv),
        ("Quit", window.quit),
    ]

    for text, command in buttons:
        tk.Button(button_frame, text=text, width=25, command=command).pack(pady=5)

    window.mainloop()


if __name__ == "__main__":
    initialize_database("contacts.db")
    start_gui()

