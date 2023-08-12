import os
import requests
from flask import Flask
from flask import request
from html.parser import HTMLParser
import json
from constants import MAILGUN_DOMAIN, CONTENT_TYPE
from helpers import MassageDataToJSONSchema

app = Flask(__name__)

    
"""
email post route expect the following schema as a reponse body with currently all the dictionary values expected to be strings:

{
  "to": "fake@example.com",
  "to_name": "Mr. Fake",
  "from": "no-reply@fake.com",
  "from_name":"Ms. Fake",
  "subject": "A message from The Fake Family",
  "body": "<h1>Your Bill</h1><p>$10</p>"
}

All fields required with the to_name and from_name can be left as empty strings "" if desired to be left blank. 
The following route at the moment handles plain text email but can be easily converted to handle html emails. 
Also at the moment only take one recipient but can be easily altered to take multiple recipient.
"""

@app.route('/email/', methods = ['POST'])
def email():
    data = request.json
    massage_data = MassageDataToJSONSchema()
    
    if data.get("mailgun"):
        try:
            data = massage_data.handle_Mailgun_data(data)
  
            # Mailgun domain must be registered with mailgun and verified to work. 
            # Domain must also match from email domain. 
            url = f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages"
            auth = ("api", os.getenv("MAILGUN_KEY"))
            response = requests.post(url, auth=auth, data=data)
            if response.ok:
                return 'OK'
            else: 
                print(response)
                return 'Error'
        except requests.exceptions.HTTPError as e:
            return e.response.text

    else:
        try:
            # Sendgrid from email must be a registered sender with Sendgrid. 
            SENDGRID_KEY = os.getenv("SENDGRID_KEY")
            headers = {"Authorization":f"Bearer {SENDGRID_KEY}", "Content-Type": CONTENT_TYPE}
            url = "https://api.sendgrid.com/v3/mail/send"
            data = massage_data.handle_Sendgrid_data(data)
            response = requests.post(url, headers=headers, data=data)
            if response.ok:
                return 'OK'
            else: 
                print(response)
                return 'Error'
        except requests.exceptions.HTTPError as e:
            return e.response.message


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)