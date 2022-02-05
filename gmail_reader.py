import json
import base64
import dateutil.parser as parser

from httplib2 import Http
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from oauth2client import client, file, tools
from oauth2client.clientsecrets import InvalidClientSecretsError


class GMAIL:

    _SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

    def __init__(self, credentials_file="credentials.json", token_file="token.json", _creds=None):
        try:
            # The file token.json stores the user's access and refresh
            # tokens, and is created automatically when the authorization flow
            # completes for the first time.
            self.credentials_file = credentials_file
            self.token_file = token_file
            if _creds:
                self.creds = _creds
            else:
                store = file.Storage(self.token_file)
                self.creds = store.get()

            if not self.creds or self.creds.invalid:
                # Will ask you to authenticate an account in your browser.
                flow = client.flow_from_clientsecrets(
                    self.credentials_file, self._SCOPES
                )
                self.creds = tools.run_flow(flow, store)

            self._service = build('gmail', 'v1', http=self.creds.authorize(
                Http()), cache_discovery=False)

        except InvalidClientSecretsError:
            raise FileNotFoundError(
                "Your 'credentials.json' file is nonexistent. Make sure "
                "the file is in the root directory of your application. If "
                "you don't have a client secrets file, go to https://"
                "developers.google.com/gmail/api/quickstart/python, and "
                "follow the instructions listed there."
            )

    @property
    def service(self):
        # Since the token is only used through calls to the service object,
        # this ensure that the token is always refreshed before use.
        if self.creds.access_token_expired:
            self.creds.refresh(Http())

        return self._service

    def search_inbox_messages(self, query=""):
        """
            Get inbox messages objects using search query if present
        """
        result = self.service.users().messages().list(
            userId='me', q=query, labelIds=["INBOX"]).execute()
        messages = []
        if 'messages' in result:
            messages.extend(result['messages'])
        while 'nextPageToken' in result:
            page_token = result['nextPageToken']
            result = self.service.users().messages().list(
                userId='me', q=query, pageToken=page_token).execute()
            if 'messages' in result:
                messages.extend(result['messages'])
        return messages

    def get_message_content(self, payload):
        """
            Parse email payload to get content of the email
        """
        # Get body of email
        if payload['mimeType'] == 'text/html':
            data = payload['body']['data']
            data = base64.urlsafe_b64decode(data)
            body = BeautifulSoup(data, 'lxml', from_encoding='utf-8').body
            return [{"type": "html", "content": str(body)}]

        elif payload['mimeType'] == 'text/plain':
            data = payload['body']['data']
            data = base64.urlsafe_b64decode(data)
            body = data.decode('UTF-8')
            return [{"type": "plain", "content": body}]

        elif payload['mimeType'].startswith('multipart'):
            ret = []
            if 'parts' in payload:
                for part in payload['parts']:
                    ret.extend(self.get_message_content(part,))
            return ret

        return []

    def read_message(self, message_object={}):
        """
            Get Message data including content
        """
        if not message_object:
            raise Exception("Message object missing")

        message = self.service.users().messages().get(
            userId="me", id=message_object["id"], format="full").execute()
        payload = message['payload']
        headers = payload.get("headers")
        # Get header fields (date, from, to, subject)
        message_data = {}
        for hdr in headers:
            if hdr['name'].lower() == 'date':
                try:
                    message_data["date"] = str(
                        parser.parse(hdr['value']).astimezone())
                except Exception:
                    message_data["date"] = hdr['value']
            elif hdr['name'].lower() == 'from':
                message_data["from"] = hdr['value']
            elif hdr['name'].lower() == 'to':
                message_data["to"] = hdr['value']
            elif hdr['name'].lower() == 'subject':
                message_data["subject"] = hdr['value']

        # Get body of email
        message_content = self.get_message_content(payload)
        message_data["data"] = message_content

        return message_data


if __name__ == '__main__':
    QUERY = "barnesandnoble"

    gmail = GMAIL()
    print(f"Search query: {QUERY}")

    messages = gmail.search_inbox_messages(query=QUERY)
    print(f"Messages Found: {len(messages)}")

    # Get data of each email
    for message in messages:
        message_data = gmail.read_message(message)
        print(json.dumps(message_data, indent=4))
