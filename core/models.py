from django.db import models
from django.utils import timezone


class Student(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    roll_no = models.CharField(max_length=100, unique=True)  # ✅ Roll number for uniqueness

    def __str__(self):
        return f"{self.name} ({self.roll_no})"


class Certificate(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="certificates")
    course_name = models.CharField(max_length=255)

    pdf_file = models.FileField(upload_to="certificates/")
    qr_code = models.ImageField(upload_to="qr/")

    ipfs_cid = models.CharField(max_length=255, blank=True, null=True)  # ✅ IPFS storage
    blockchain_hash = models.CharField(max_length=255, unique=True)     # ✅ Unique blockchain hash
    transaction_hash = models.CharField(max_length=255, unique=True)    # ✅ Blockchain TX reference
    issued_block = models.IntegerField(null=True, blank=True, default=None)
    revoked_block = models.IntegerField(null=True, blank=True)

    issued_at = models.DateTimeField(auto_now_add=True)
    revoked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.name} - {self.course_name} ({'Revoked' if self.revoked else 'Active'})"


class BlockchainSyncStatus(models.Model):
    """Tracks the last synced block for incremental updates."""
    last_synced_block = models.BigIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Last Synced Block: {self.last_synced_block}"
class RevokedCertificate(models.Model):
    certificate = models.OneToOneField(Certificate, on_delete=models.CASCADE, related_name="revocation")
    revoked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Revoked: {self.certificate.student.name} - {self.certificate.course_name}"
