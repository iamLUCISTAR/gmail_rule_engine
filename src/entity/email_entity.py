"""
Entity object to process data received from Gmail Api for storing in the db.
"""
import base64
from datetime import datetime


class EmailMasterEntity(object):
    """
    Class for defining the getters and setters of email parameters
    """
    def __init__(self, raw_data):
        self._data = raw_data
        self._payload = raw_data['payload']
        self._headers = self._payload['headers']
        self._parts = self._payload.get('parts', [])
        self._body = self._payload.get('body', None)

    def _fetch_header_data(self, key):
        for header in self._headers:
            if header['name'] == key:
                return header['value']
        return None

    def get_id(self):
        return self._data['id']

    def get_thread_id(self):
        return self._data['threadId']

    def get_history_id(self):
        return self._data['historyId']

    def get_to_mail(self):
        return self._fetch_header_data('To')

    def get_from_mail(self):
        return self._fetch_header_data('From')

    def get_subject(self):
        return self._fetch_header_data('Subject')

    def get_body(self):
        if self._parts:
            text_body = None
            html_body = None
            parts_data = self._parts
            for part in self._parts:
                if part['mimeType'] == 'multipart/alternative':
                    parts_data = part['parts']
                    break

            for part in parts_data:
                if part['mimeType'] == 'text/plain':
                    text_body = base64.urlsafe_b64decode(part['body']['data'])
                if part['mimeType'] == 'text/html':
                    html_body = base64.urlsafe_b64decode(part['body']['data'])
            return text_body or html_body

        return None

    def get_received_date(self):
        internal_date = self._data['internalDate']
        datetime_obj = datetime.fromtimestamp(int(internal_date) / 1000)
        return datetime_obj.strftime("%Y-%m-%d %H:%M:%S")

    def get_msg_size(self):
        return self._data['sizeEstimate']
