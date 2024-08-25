"""
Contains the actions for authentication and execution of gmail api's
"""
import json
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from src.config.base_config import LOG as logger

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]


class GmailAuthenticator(object):
    """
    Class for authenticating gmail api's.
    """

    def __init__(self):
        self.service = build("gmail", "v1", credentials=self.__authenticate())

    def __authenticate(self):
        """
        Function to create authentication token using OAuth authentication.
        """
        creds = None
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                cur_dir = os.path.dirname(os.path.realpath(__file__))
                auth_flow = InstalledAppFlow.from_client_secrets_file("{0}/credentials.json".format(cur_dir), SCOPES)
                creds = auth_flow.run_local_server(port=8080)
            with open("token.json", "w") as token:
                token.write(creds.to_json())
        return creds


class GmailFetcher(GmailAuthenticator):
    """
    Class for fetching the gmail mails for the authenticated gmail account
    """

    def fetch(self, limit: int = 10):
        """
        Function to fetch all the mails from the gmail account
        """
        req_result = self.service.users().messages().list(userId="me", maxResults=limit).execute()
        messages = req_result.get('messages', [])
        if len(messages) == 0:
            logger.info("No message fetched from the account.")
            return []

        logger.info(f"Retrieved message count: {len(messages)}")
        batch_req = self.service.new_batch_http_request()
        for msg in messages:
            batch_req.add(self.service.users().messages().get(userId="me", id=msg["id"]))
        batch_req.execute()
        batch_response = list(batch_req._responses.values())
        email_list = [json.loads(resp[1].decode()) for resp in batch_response]
        logger.info(f"Emails count: {len(email_list)}")
        return email_list


class GmailActionExecutor(GmailAuthenticator):
    """
    Gmail action performer
    """
    def perform(self, payload):
        """
        Fetches all type of mails from the gmail
        """
        request = (self.service.users().messages().batchModify(userId="me", body=payload))
        request.execute()


if __name__ == '__main__':
    from pprint import pprint
    records = GmailFetcher().fetch(1)
    pprint(records[0])
