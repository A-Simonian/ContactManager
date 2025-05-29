import unittest
from ..search import search_name, search_email, search_phone, search_id, search
from ..contact import Contact

class TestSearchFunctions(unittest.TestCase):

    def setUp(self):
        self.alice = Contact(1, "Alice Johnson", "alice@example.com", "3105551234")
        self.bob = Contact(2, "Bob Smith", "bob@workmail.com", "5555555555")
        self.contacts = [self.alice, self.bob]

    def test_search_name_found(self):
        results = search_name(self.contacts, "Alice")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "Alice Johnson")

    def test_search_name_not_found(self):
        results = search_name(self.contacts, "NotHere@example.com")
        self.assertEqual(results, [])

    def test_search_email_found(self):
        results = search_email(self.contacts, "Alice")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].email, "alice@example.com")

    def test_search_email_not_found(self):
        results = search_email(self.contacts, "NotHere@example.com")
        self.assertEqual(results, [])

    def test_search_phone_found(self):
        results = search_phone(self.contacts, "3105551234")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].phoneNumber, "3105551234")

    def test_search_phone_not_found(self):
        results = search_phone(self.contacts, "1111111111")
        self.assertEqual(results, [])

    def test_search_id_found(self):
        results = search_id(self.contacts, '1')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].contactID, 1)

    def test_search_id_invalid_id(self):
        results = search_id(self.contacts, 'B')
        self.assertEqual(results, [])




if __name__ == '__main__':
    unittest.main()
