class Contact:
    def __init__(self, contactID: object, name: object, email: object, phoneNumber: object) -> None:
        self.contactID = contactID
        self.name = name
        self.email = email
        self.phoneNumber = phoneNumber

    def __str__(self):
        return (
            f"ID: {self.contactID}\n"
            f"Name: {self.name}\n"
            f"Email: {self.email}\n"
            f"Phone Number: {self.phoneNumber}"
        )

    def to_dict(self):
        return {
            'ID': self.contactID,
            'Name': self.name,
            'Email': self.email,
            'Phone': self.phoneNumber
        }

    @staticmethod
    def is_valid_email(email):
        if "@" not in email or "." not in email:
            return False
        at_index = email.index("@")
        dot_index = email.rindex(".")
        return at_index < dot_index and at_index > 0 and dot_index < len(email) - 1

    @staticmethod
    def is_valid_phone(phoneNumber):
        return len(phoneNumber) == 10 and phoneNumber.isdigit()