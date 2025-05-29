import os
import csv
from contact import Contact

def open_file(fileName, fieldNames):
    contacts = []
    max_id = 0

    if not os.path.exists(fileName):
        print("File not found. Creating file with header.")
        with open(fileName, 'w') as csvFile:
            writer = csv.DictWriter(csvFile, fieldnames=fieldNames)
            writer.writeheader()
    else:
        with open(fileName, 'r') as csvFile:
            csvReader = csv.DictReader(csvFile)
            for row in csvReader:
                contactID = int(row['ID'])
                name = row['Name']
                email = row['Email']
                phone = row['Phone']

                if contactID > max_id:
                    max_id = contactID

                contact = Contact(contactID, name, email, phone)
                contacts.append(contact)

    return contacts, max_id

def writeContacts(fileName, fieldNames, contacts):
    with open(fileName, 'w', newline='') as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=fieldNames)
        writer.writeheader()
        for contact in contacts:
            writer.writerow(contact.to_dict())