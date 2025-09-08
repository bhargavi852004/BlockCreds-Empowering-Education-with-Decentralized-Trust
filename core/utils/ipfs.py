import os
import requests
from dotenv import load_dotenv

load_dotenv()

PINATA_JWT = os.getenv("PINATA_JWT")
PINATA_BASE_URL = "https://api.pinata.cloud/pinning/pinFileToIPFS"


def upload_to_ipfs(file_path: str) -> str:
    """
    Upload file to IPFS via Pinata.
    """
    if not PINATA_JWT:
        raise ValueError("❌ Missing PINATA_JWT in .env")

    headers = {"Authorization": f"Bearer {PINATA_JWT}"}

    with open(file_path, "rb") as file:
        response = requests.post(PINATA_BASE_URL, headers=headers, files={"file": file})

    if response.status_code == 200:
        return response.json().get("IpfsHash")
    raise Exception(f"❌ Failed to upload to IPFS: {response.text}")
