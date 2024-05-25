from os import path
import yaml
# google oauth lib's
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError



class OAuth_Token:

    def __init__(self):
        # opening the constants from the yaml
        with open("constants.yaml","r") as data:
            self.constants = yaml.full_load(data.read())
    
    def writing_token(self):
        flow = InstalledAppFlow.from_client_secrets_file("client.json", self.constants["SCOPE"])
        creds = flow.run_local_server(port=0)
        with open("token_keys.json", "w") as token:
            token.write(creds.to_json())
    
    def checking_token_expire(self):
        pass

    def validating_credentials(self):
        if path.exists("token_keys.json"):
            creds = Credentials.from_authorized_user_file("token_keys.json", self.constants["SCOPE"])
        return creds
