import os
import json
import time
from web3 import Web3
from dotenv import load_dotenv

# ----------------------------
# Environment & RPC Setup
# ----------------------------
load_dotenv()

POLYGON_RPC_URL = os.getenv("POLYGON_RPC_URL")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
PUBLIC_ADDRESS = os.getenv("PUBLIC_ADDRESS")

w3 = Web3(Web3.HTTPProvider(POLYGON_RPC_URL))
if not w3.is_connected():
    raise Exception(f"❌ Failed to connect to Polygon RPC at {POLYGON_RPC_URL}")

# Change this if contract deployed at a different block
CONTRACT_DEPLOYMENT_BLOCK = 25470407

# ----------------------------
# Load ABI
# ----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ABI_PATH = os.path.join(BASE_DIR, "blockchain", "abi", "Cert.abi.json")

if not os.path.exists(ABI_PATH):
    raise FileNotFoundError(f"❌ ABI file not found at {ABI_PATH}")

with open(ABI_PATH, "r") as f:
    contract_abi = json.load(f)

contract = w3.eth.contract(
    address=Web3.to_checksum_address(CONTRACT_ADDRESS),
    abi=contract_abi
)

# ----------------------------
# Helper Functions
# ----------------------------
def get_safe_nonce():
    """Get nonce safely accounting for pending transactions."""
    pending = w3.eth.get_transaction_count(PUBLIC_ADDRESS, "pending")
    latest = w3.eth.get_transaction_count(PUBLIC_ADDRESS, "latest")
    return max(pending, latest)

def get_dynamic_gas():
    """Fetch dynamic gas price and add buffer for congestion."""
    base_fee = w3.eth.gas_price
    max_fee = int(base_fee * 2)
    priority_fee = w3.to_wei("30", "gwei")
    return max_fee, priority_fee

def bump_gas(transaction):
    """Increase gas fees to replace a stuck transaction."""
    transaction["maxFeePerGas"] = int(transaction["maxFeePerGas"] * 1.5)
    transaction["maxPriorityFeePerGas"] = int(transaction["maxPriorityFeePerGas"] * 1.5)
    print(f"🔄 Bumping gas: maxFee={transaction['maxFeePerGas']}, priorityFee={transaction['maxPriorityFeePerGas']}")
    return transaction

def is_tx_pending(tx_hash):
    """Check if a transaction is still pending."""
    try:
        w3.eth.get_transaction_receipt(tx_hash)
        return False  # mined
    except:
        return True  # pending or unknown

def build_and_send_txn(transaction, retries=5):
    """
    Sign, send, and confirm a transaction with retries and gas bumping.
    Returns the last transaction hash even if not confirmed.
    """
    last_tx_hash = None
    transaction["nonce"] = get_safe_nonce()

    for attempt in range(1, retries + 1):
        try:
            signed_txn = w3.eth.account.sign_transaction(transaction, private_key=PRIVATE_KEY)
            last_tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            print(f"✅ Transaction sent: {w3.to_hex(last_tx_hash)}")

            receipt = w3.eth.wait_for_transaction_receipt(last_tx_hash, timeout=120)
            if receipt.status == 1:
                print(f"✅ Transaction confirmed in block {receipt.blockNumber}")
                return w3.to_hex(last_tx_hash)
            else:
                print("❌ Transaction failed on-chain")
                return w3.to_hex(last_tx_hash)

        except Exception as e:
            print(f"⚠ Error (Attempt {attempt}): {e}")

            if "already known" in str(e) or "replacement transaction" in str(e):
                transaction = bump_gas(transaction)
                time.sleep(5)
            else:
                time.sleep(3)

    print("⚠ All retries failed. Returning last pending transaction hash.")
    return w3.to_hex(last_tx_hash) if last_tx_hash else None

# ----------------------------
# Core Blockchain Functions
# ----------------------------
def issue_certificate_on_chain(cert_hash: bytes, cid: str) -> str:
    """Store certificate on blockchain."""
    max_fee, priority_fee = get_dynamic_gas()
    txn = contract.functions.issueCertificate(cert_hash, cid).build_transaction({
        "from": PUBLIC_ADDRESS,
        "nonce": get_safe_nonce(),
        "gas": 3000000,
        "maxFeePerGas": max_fee,
        "maxPriorityFeePerGas": priority_fee,
    })
    return build_and_send_txn(txn)

def revoke_certificate_on_chain(cert_hash: bytes) -> str:
    """Revoke certificate on blockchain."""
    max_fee, priority_fee = get_dynamic_gas()
    txn = contract.functions.revokeCertificate(cert_hash).build_transaction({
        "from": PUBLIC_ADDRESS,
        "nonce": get_safe_nonce(),
        "gas": 3000000,
        "maxFeePerGas": max_fee,
        "maxPriorityFeePerGas": priority_fee,
    })
    return build_and_send_txn(txn)

def get_certificate_from_chain(cert_hash: bytes):
    """Fetch certificate details from blockchain."""
    return contract.functions.getCertificate(cert_hash).call()

# ----------------------------
# Event Fetching Functions
# ----------------------------
def get_all_issued_certificates():
    """Fetch all issued certificates since deployment."""
    event_filter = contract.events.Issued.create_filter(
        fromBlock=CONTRACT_DEPLOYMENT_BLOCK,
        toBlock="latest"
    )
    return event_filter.get_all_entries()

def get_all_revoked_certificates():
    """Fetch all revoked certificates since deployment."""
    event_filter = contract.events.Revoked.create_filter(
        fromBlock=CONTRACT_DEPLOYMENT_BLOCK,
        toBlock="latest"
    )
    return event_filter.get_all_entries()

def get_contract():
    return contract
