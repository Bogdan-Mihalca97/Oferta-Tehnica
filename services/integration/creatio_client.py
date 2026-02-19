"""
HTTP client for Creatio API calls.
Uses a requests.Session with a static AuthSecret header.
"""
import requests

from config.config import creatio_base_url, creatio_auth_secret


class CreatioClient:
    def __init__(self):
        self.base_url = creatio_base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({'AuthSecret': creatio_auth_secret})

    def get(self, url: str) -> requests.Response:
        response = self.session.get(url)
        response.raise_for_status()
        return response

    def post(self, url: str, data=None, json=None) -> requests.Response:
        response = self.session.post(url, data=data, json=json)
        response.raise_for_status()
        return response

    def post_multipart(self, url: str, files=None, data=None) -> requests.Response:
        response = self.session.post(url, files=files, data=data)
        response.raise_for_status()
        return response
