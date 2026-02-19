"""
File download/upload operations against the Creatio EntityFileService.
"""
import uuid

from services.integration.creatio_client import CreatioClient


class CreatioFileService:
    def __init__(self, client: CreatioClient):
        self.client = client

    def download_file(self, doc_id: str) -> bytes:
        """Download a file from Creatio by its document ID.

        Endpoint: GET {baseUrl}/0/ServiceModel/EntityFileService.svc/GetFile?id={doc_id}
        Returns raw file bytes.
        """
        url = f"{self.client.base_url}/0/ServiceModel/EntityFileService.svc/GetFile?id={doc_id}"
        response = self.client.get(url)
        return response.content

    def upload_file(self, record_id: str, file_name: str, file_bytes: bytes) -> dict:
        """Upload a file to Creatio and attach it to a record.

        Endpoint: POST {baseUrl}/0/ServiceModel/EntityFileService.svc/UploadFile
        Posts multipart form with file bytes and metadata.
        Returns the parsed JSON response.
        """
        url = f"{self.client.base_url}/0/ServiceModel/EntityFileService.svc/UploadFile"
        file_id = str(uuid.uuid4())

        files = {
            'file': (file_name, file_bytes, 'application/octet-stream'),
        }
        data = {
            'recordId': record_id,
            'fileName': file_name,
            'fileId': file_id,
        }

        response = self.client.post_multipart(url, files=files, data=data)
        return response.json()
