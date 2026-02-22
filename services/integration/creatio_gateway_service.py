import requests

from config.config import creatio_base_url, creatio_auth_secret
from services.integration.request_retry_decorator import retry_on_failure


class CreatioGatewayService:
    def __init__(self):
        self.base_url = creatio_base_url.rstrip('/')
        self.session = requests.Session()
        self.headers = {
            'AuthSecret': creatio_auth_secret,
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }

    @retry_on_failure(max_retries=3, delay=2)
    def execute_get(self, url):
        response = self.session.get(url, headers=self.headers)
        response.raise_for_status()
        json_response = response.json()
        if "value" in json_response:
            return json_response["value"]
        else:
            return json_response

    @retry_on_failure(max_retries=3, delay=2)
    def execute_get_bytes(self, url):
        """Fetch raw binary content (e.g. file downloads). Skips JSON parsing."""
        headers = {k: v for k, v in self.headers.items() if k != 'Content-Type'}
        response = self.session.get(url, headers=headers)
        response.raise_for_status()
        return response.content

    @retry_on_failure(max_retries=3, delay=2)
    def execute_post(self, url, data):
        if data is not None:
            response = self.session.post(url, json=data, headers=self.headers)
        else:
            response = self.session.post(url, headers=self.headers)
        response.raise_for_status()
        json_response = response.json()
        if "value" in json_response:
            return json_response["value"]
        else:
            return json_response

    @retry_on_failure(max_retries=3, delay=2)
    def execute_post_multipart(self, url, files=None, data=None):
        """Post multipart form data (e.g. file uploads). Omits Content-Type so requests sets the boundary."""
        headers = {'AuthSecret': creatio_auth_secret}
        response = self.session.post(url, files=files, data=data, headers=headers)
        response.raise_for_status()
        return response.json()

    @retry_on_failure(max_retries=3, delay=2)
    def execute_put(self, url, data):
        if data is not None:
            response = self.session.put(url, json=data, headers=self.headers)
        else:
            response = self.session.put(url, headers=self.headers)
        response.raise_for_status()
        json_response = response.json()
        if "value" in json_response:
            return json_response["value"]
        else:
            return json_response

    @retry_on_failure(max_retries=3, delay=2)
    def execute_patch(self, url, data):
        response = self.session.patch(url, json=data, headers=self.headers)
        response.raise_for_status()
        if response.status_code in [200, 204]:
            return True
        else:
            return response.json()

    @retry_on_failure(max_retries=3, delay=2)
    def execute_delete(self, url):
        response = self.session.delete(url, headers=self.headers)
        response.raise_for_status()
        if response.status_code in [200, 204]:
            return True
        else:
            return response.json()
