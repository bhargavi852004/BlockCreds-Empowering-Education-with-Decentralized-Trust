# core/sync_events.py

from django.utils.timezone import make_aware
from datetime import datetime
from core.models import Certificate, BlockchainSyncStatus, Student
from core.utils.blockchain import get_contract
from web3 import Web3
import uuid
import logging

logger = logging.getLogger(__name__)


def sync_blockchain_events():
    """
    Incrementally sync issued and revoked certificates from blockchain.
    Safe version: handles connection errors and avoids crashing the dashboard.
    """

    try:
        # ✅ Get Web3 instance and Contract
        web3, contract = get_contract()
    except Exception as e:
        logger.error(f"[Blockchain Sync] Unable to connect to blockchain: {e}")
        return None

    # Get last synced block from DB
    sync_status, _ = BlockchainSyncStatus.objects.get_or_create(id=1)
    last_synced_block = sync_status.last_synced_block or 0
    try:
        latest_block = web3.eth.block_number
    except Exception as e:
        logger.error(f"[Blockchain Sync] Failed to fetch latest block: {e}")
        return last_synced_block

    # Nothing new to sync
    if latest_block <= last_synced_block:
        return latest_block

    # -------------------------------
    # Fetch new Issued & Revoked events
    # -------------------------------
    try:
        issued_events = contract.events.Issued.create_filter(
            fromBlock=last_synced_block + 1, toBlock=latest_block
        ).get_all_entries()

        revoked_events = contract.events.Revoked.create_filter(
            fromBlock=last_synced_block + 1, toBlock=latest_block
        ).get_all_entries()
    except Exception as e:
        logger.error(f"[Blockchain Sync] Failed to fetch events: {e}")
        return last_synced_block

    # -------------------------------
    # Process Issued Certificates
    # -------------------------------
    for event in issued_events:
        try:
            cert_hash = event["args"]["hash"].hex()
            ipfs_cid = event["args"]["cid"]
            block_number = event["blockNumber"]
            issued_at = make_aware(datetime.fromtimestamp(event["args"]["issuedAt"]))
            tx_hash = event["transactionHash"].hex()

            # Create placeholder student if unknown
            student, _ = Student.objects.get_or_create(
                roll_no="Unknown",
                defaults={
                    "name": "Unknown",
                    "email": f"unknown_{uuid.uuid4()}@example.com"
                }
            )

            Certificate.objects.get_or_create(
                blockchain_hash=cert_hash,
                defaults={
                    "student": student,
                    "course_name": "Unknown",
                    "pdf_file": "",
                    "qr_code": "",
                    "ipfs_cid": ipfs_cid,
                    "transaction_hash": tx_hash,
                    "issued_block": block_number,
                    "issued_at": issued_at,
                    "revoked": False
                }
            )
        except Exception as e:
            logger.warning(f"[Blockchain Sync] Failed to process issued event: {e}")
            continue

    # -------------------------------
    # Process Revoked Certificates
    # -------------------------------
    for event in revoked_events:
        try:
            cert_hash = event["args"]["hash"].hex()
            block_number = event["blockNumber"]

            Certificate.objects.filter(blockchain_hash=cert_hash).update(
                revoked=True,
                revoked_block=block_number
            )
        except Exception as e:
            logger.warning(f"[Blockchain Sync] Failed to process revoked event: {e}")
            continue

    # -------------------------------
    # Update sync status
    # -------------------------------
    sync_status.last_synced_block = latest_block
    sync_status.save()

    logger.info(f"[Blockchain Sync] Synced blocks {last_synced_block+1} to {latest_block}")
    return latest_block
