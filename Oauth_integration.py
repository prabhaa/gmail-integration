from os import path
import yaml
# google oauth lib's
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow



class OAuth_Token:

    def __init__(self):
        # opening the constants from the yaml
        with open("constants.yaml","r") as data:
            self.constants = yaml.full_load(data.read())
    
    def writing_token(self):
        try:
            flow = InstalledAppFlow.from_client_secrets_file("client.json", self.constants["SCOPE"])
            creds = flow.run_local_server(port=0)
            with open("token_keys.json", "w") as token:
                token.write(creds.to_json())
            return True
        except BaseException as error:
            return False
    
    def checking_token_expire(self):
        pass

    def validating_credentials(self):
        if not path.exists("token_keys.json"):
            status_token = self.writing_token()
        else:
            creds = Credentials.from_authorized_user_file("token_keys.json", self.constants["SCOPE"])
            return creds
        raise RuntimeError("Connection issues with Oauth server")

