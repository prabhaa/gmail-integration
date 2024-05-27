# Fetching all the emails from Gmail through Oauth 2.0 with the Google client API library.

# Prerequisites for running the app:

    - Download the credenetial file from the GCP and rename it to client.json. keep this file into the main folder.
    - Any python version above 3.8 is ok.
    - Install the requirements.txt

# This repository has three files:

    - Oauth_integration.py : This file is responsible for getting the OAuth token writing it to the JSON file and authenticating it to the Auth server.
    - email_gathering.py : This file will gather the list of mail from the Inbox and store it in the DB.
    - filtering_email.py : Based on the rules provided by the user, this file will apply rules to the email by parsing the data from DB and gathering the ID of the email. The ID will be applied to a Gmail Rest API to change the status of it.

# Run the App:

```
pip install -r requirements.txt
python email_gathering.py -> This file will gather the emails from Gmail inbox.
python filtering_email.py -> will parse the email and apply the rules on the email with API.

```

# Task Pending:

- [x] Authenticate to Google’s Gmail API using OAuth (use Google’s official Python client) and fetch a list of emails from your Inbox. Do NOT use IMAP.
- [x] Come up with a database table representation and store these emails there. Use any relational database for this (Postgres / MySQL / SQLite3).
- [x] Now that you can fetch emails, write another script that can process emails (in Python code, not using Gmail’s Search) based on some rules and take some actions on them using the REST API.
- [x] These rules can be stored in a JSON file. The file should have a list of rules. Each rule has a set of conditions with an overall predicate and a set of actions.
- Actions
  - [x] Mark as read/mark as unread
  - [x] Move Message.
