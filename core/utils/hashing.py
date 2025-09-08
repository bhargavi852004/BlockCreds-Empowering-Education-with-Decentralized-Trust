from web3 import Web3


def generate_hash_from_file(file_path: str) -> bytes:
    """Generate keccak256 hash from a file"""
    with open(file_path, "rb") as f:
        return Web3.keccak(f.read())


def generate_hash_from_text(text: str) -> bytes:
    """Generate keccak256 hash from text"""
    return Web3.keccak(text.encode())
