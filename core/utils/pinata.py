import os
import requests
from dotenv import load_dotenv

load_dotenv()

PINATA_JWT = os.getenv("PINATA_JWT")
PINATA_BASE_URL = "https://api.pinata.cloud/pinning/pinFileToIPFS"


def upload_to_pinata(file_path: str) -> str:
    """
    Upload a file to Pinata (IPFS).
    :param file_path: Local path of the file
    :return: IPFS hash (CID)
    """
    if not PINATA_JWT:
        raise ValueError("❌ Missing PINATA_JWT in .env")

    headers = {"Authorization": f"Bearer {PINATA_JWT}"}

    with open(file_path, "rb") as file:
        files = {"file": (os.path.basename(file_path), file)}
        response = requests.post(PINATA_BASE_URL, files=files, headers=headers)

    if response.status_code == 200:
        return response.json().get("IpfsHash")
    raise Exception(f"❌ Pinata upload failed: {response.text}")
