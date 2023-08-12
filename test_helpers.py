import unittest
import json
from constants import EMAIL_TYPE_PLAIN
from helpers import TextStrip, MassageDataToJSONSchema

class TestStringMethods(unittest.TestCase):
    def test_html_strip(self):
        t =  TextStrip()
        html_str = "<h1>Hello, World!</h1><div><div> More complex content.</div></div>"
        t.feed(html_str)
        result = t.get_data()
        expected = "Hello, World! More complex content."
        self.assertEqual(result, expected)

    def test_plaintext_string(self):
        t =  TextStrip()
        str = "Testing content. String = String."
        t.feed(str)
        result = t.get_data()
        expected = "Testing content. String = String."
        print(result, expected)
        self.assertEqual(result, expected)

class TestMassageDataToJSONSchema(unittest.TestCase):
    m = MassageDataToJSONSchema()
    def test_handle_Mailgun_data(self):
        data = {
            "from": "fake@fake.org",
            "from_name": "Testing Smith",
            "to_name": "Tester Brown",
            "to": "yas123@gmail.com",
            "subject": "test mailgun",
            "body": "<div>Hello, World!<div>",
            "mailgun": True
        }
        result = self.m.handle_Mailgun_data(data)
        expected = {
            "from": "Testing Smith <fake@fake.org>",
            "to": ["Tester Brown <yas123@gmail.com>"],
            "subject": "test mailgun",
            "text": "Hello, World!"
        }
        self.assertDictEqual(result, expected)
    def test_handle_Sendgrid_data(self):
        data = {
            "from": "fake@fake.org",
            "from_name": "Testing Smith",
            "to_name": "Tester Brown",
            "to": "stillfake@gmail.com",
            "subject": "test sendgrid",
            "body": "<div>Hello, World!<div>"
        }
        jsonStr = self.m.handle_Sendgrid_data(data)
        result = json.loads(jsonStr)
        expected = {
                "from": {
                    "email": "fake@fake.org",
                    "name": "Testing Smith"
                    },
                "personalizations": [{
                    "to": [{
                        "email": "stillfake@gmail.com",
                        "name": "Tester Brown"
                        }]
                    }],
                "subject": "test sendgrid",
                "content": [{
                    "type": EMAIL_TYPE_PLAIN,
                    "value": "Hello, World!"
                    }]
                }
        self.assertDictEqual(result, expected)
        

if __name__ == '__main__':
    unittest.main()