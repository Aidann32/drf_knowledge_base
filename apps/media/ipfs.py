import requests

from config import settings


def upload_to_ipfs(file):
    ipfs_api_url = settings.IPFS_API_URL  # e.g., "http://127.0.0.1:5001/api/v0/add"
    files = {'file': file}
    response = requests.post(ipfs_api_url, files=files)

    if response.status_code == 200:
        return response.json().get('Hash')
    else:
        raise Exception(f"Failed to upload to IPFS: {response.text}")