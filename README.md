# Simple Flask Email Service
Simple email service in Python and Flask. A service with one route that will send an email via Sendgrid by default or send an email via Mailgun with an added configuration. Python and Flask was chosen just because it's light weight for a simple service. Python is also a popular language and clean and easy. No linting required. No other real library dependencies needed aside from Python requests library and Flask. 

As of currently, route only handles single email sends in plain text. Next step would be to be able to handle email sends to multiple recipients with the same email body. Then multiple recipients with different email bodies.  Additionally, a simple configuration and with light modification to code email should be able to handle html sends as well. Security and a authentication token in header should also be configured for safe measure for usage of endpoint. 

Time spent on exercise was a little over expected time range mainly due to running into some sendgrid/mailgun authentication issues and python virtualenv configuration issues. 

## Getting Started
- Install python
- Install pip
- Install virtualenv
- Create and source/activate virtualenv environment
- In command line, use workon virtualenv_enviornment_name
- Install necessary packages
```
pip install -r requirements.txt
```
- Sign up for Mailgun API key and Sendgrid API key. Note: mailgun API Key will be the Private API key.
- Replace MAILGUN_DOMAIN value in constants.py with registered a domain from Mailgun.
- Register a verified single sender domain in Sendgrid with the emails you'll be sending from. https://app.sendgrid.com/settings/sender_auth
- Create a .env file and add the two API key under the variables SENDGRID_KEY and MAILGUN_KEY

example .env file
```
SENDGRID_KEY="blahblahkey"
MAILGUN_KEY="blahblahkey"
```

- In commandline run app with: 
```
flask run
```
reload with code change and debug mode is:

```
flask --debug run
```
- App should say it is running on http://IP_ADDRESS:PORT_NUMBER

## Sending Email
When server is running you should be able to send an email via a POST request:

Route is:
```
POST request on  http://127.0.0.1:5000/email/
```
JSON request body schema in that POST request to be:
```
{
  "to": "fake@example.com", 
  "to_name": "Mr. Fake",
  "from": "no-reply@fake.com", // Domain of from email must be registered with Mailgun and or Sendgrid 
  "from_name":"Ms. Fake",
  "subject": "A message from The Fake Family",
  "body": "<h1>Your Bill</h1><p>$10</p>",
   "mailgun": true // optional boolean value to configure for email to be sent by Mailgun. Otherwise defaults to sendgrid.
}
```

All fields are required and in string format with the exception of "mailgun" only to be passed if intended to switch email sending service to Mailgun instead of Sendgrid. 

To leave to_name or from_name empty, send in empty strings, "".

## Running tests

- Run unit tests with:
```
python -m unittest test_helpers.py
```
- Run integration tests with Postman with the expected json schema as above. Or curl request. 
```
curl -X POST http://127.0.0.1:5000/email/ 
   -H "Content-Type: application/json"
   -d '{
    "to": "fake@example.com", 
    "to_name": "Mr. Fake",
    "from": "no-reply@fake.com",
    "from_name":"Ms. Fake",
    "subject": "A message from The Fake Family",
    "body": "<h1>Your Bill</h1><p>$10</p>"
    }' 
```

