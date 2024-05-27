from os import path
import base64
import re
from datetime import datetime
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
        # checking credential
        self.creds = OAuth_Token().validating_credentials()

    def fetching_email(self):
        try:
            service = build('gmail', 'v1', credentials=self.creds)
            # Getting the list of emails from the inbox with a set limit of the first 100 records.
            message_data = service.users().messages().list(userId='me', labelIds=['INBOX'],maxResults=100).execute()
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
                    print(re.findall(r",(.*)\+",parsed_data.get("Date"))[0].strip())
                    content_data = {
                        "e_from" : parsed_data.get("From"),
                        "e_to" : parsed_data.get("To"),
                        "e_date" : datetime.strptime(re.findall(r",(.*)\+",parsed_data.get("Date"))[0].strip(),"%d %b %Y %H:%M:%S").strftime("%Y-%m-%d %H:%M"),
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
            del email_df, content_data, message_data, parsed_data

Fetching_Inbox().fetching_email()


