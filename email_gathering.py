from os import path
import yaml
import base64
from email import message_from_string
import pandas as pd
import sqlite3
# google oauth lib's
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
# other modules
from Oauth_integration import OAuth_Token


class Fetching_Inbox:

    def __init__(self):
        # getting the scopes from the constant file
        with open("constants.yaml","r") as data:
            constants = yaml.full_load(data.read())
        # checking credential
        self.creds = OAuth_Token().validating_credentials()

    def fetching_email(self):
        try:
            service = build('gmail', 'v1', credentials=self.creds)
            message_data = service.users().messages().list(userId='me', labelIds=['INBOX'],maxResults=10).execute()
            messages = message_data.get('messages', [])
            inbox_data = []
            for ind_messages in messages:
                content_data = {}
                message_data = service.users().messages().get(userId='me',id = ind_messages["id"],format = "raw").execute()
                parsed_data = message_from_string(base64.urlsafe_b64decode(message_data.get("raw")).decode("UTF-8"))
                if isinstance(parsed_data.get_payload(),list):
                    # currently skipping this part as some of the emails has more numbers of object into it.
                    pass
                else:
                    content_data = {
                        "from" : parsed_data.get("From"),
                        "to" : parsed_data.get("To"),
                        "date" : parsed_data.get("Date"),
                        "message_id" : message_data.get("id"),
                        "content_type" : parsed_data.get("Content-Type"),
                        "content" : parsed_data.get_payload(),
                        "subject" : parsed_data.get("Subject"),
                        "labels" : ",".join(message_data.get("labelIds"))
                    }
                    inbox_data.append(content_data)
            # preparing the connection for sqlite
            connection_sqlite = sqlite3.connect("DB/email_db")
            # converting the json to dataframe
            email_df = pd.DataFrame.from_records(inbox_data, index = None)
            email_df.to_sql("inbox",con = connection_sqlite,if_exists='append',index=False)
        except BaseException as error:
            print(f"email fetching - {error}")
        finally:
            connection_sqlite.close()
            del email_df, content_data, message_data

Fetching_Inbox().fetching_email()


