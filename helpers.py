import json
from io import StringIO
from html.parser import HTMLParser
from constants import EMAIL_TYPE_PLAIN

# class to help strip html tags for email body to become plain text
class TextStrip(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

# class that helps massage data to its rightful shape expected by each email service   
class MassageDataToJSONSchema():
    def handle_Mailgun_data(self, data):
        s = TextStrip()
        s.feed(data["body"])
        parsed = s.get_data()
        sender = data.get("from")
        sender_name = data.get("from_name")
        recipient = data.get("to")
        recipient_name = data.get("to_name")
        return {
            "to": [f"{recipient_name} <{recipient}>"],
            "from": f"{sender_name} <{sender}>",
            "subject": data.get("subject"),
            "text": parsed
        }
    def handle_Sendgrid_data(self, data):
        s = TextStrip()
        s.feed(data["body"])
        parsed = s.get_data()
        data = {
                "from": {
                    "email": data["from"],
                    "name": data["from_name"]
                    },
                "personalizations": [{
                    "to": [{
                        "email": data["to"],
                        "name": data["to_name"]
                        }]
                    }],
                "subject": data["subject"],
                "content": [{
                    "type": EMAIL_TYPE_PLAIN,
                    "value": parsed
                    }]
                }
        return json.dumps(data)



   