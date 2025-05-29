import unittest
from ..contact import Contact

class TestContactEmailValidation(unittest.TestCase):
    def test_valid_email(self):
        self.assertTrue(Contact.is_valid_email("test@example.com"))

    def test_invalid_email_missing_at(self):
        self.assertFalse(Contact.is_valid_email("testexample.com"))

    def test_invalid_email_ends_with_dot(self):
        self.assertFalse(Contact.is_valid_email("test@example."))

class TestContactPhoneValidation(unittest.TestCase):
    def test_valid_phone(self):
        self.assertTrue(Contact.is_valid_phone("3105555555"))

    def test_phone_number_short(self):
        self.assertFalse(Contact.is_valid_phone("234"))

    def test_phone_number_long(self):
        self.assertFalse(Contact.is_valid_phone("12345678902"))

    def test_phone_number_letters(self):
        self.assertFalse(Contact.is_valid_phone("1234aba3b2"))

class TestContactToDict(unittest.TestCase):

    def setUp(self):
        self.contact = Contact(1, "Alice","alice@example.com", "2215553535")

    def test_to_dict(self):
        expected = {
            'ID': 1,
            'Name': "Alice",
            'Email': "alice@example.com",
            'Phone': "2215553535"
        }
        self.assertEqual(self.contact.to_dict(), expected)


if __name__ == '__main__':
    unittest.main()
