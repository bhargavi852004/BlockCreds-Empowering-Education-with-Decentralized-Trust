from django.contrib import admin
from .models import Student, Certificate, RevokedCertificate


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "roll_no")  # ✅ Show roll number too
    search_fields = ("name", "email", "roll_no")


from django.utils.html import format_html
@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = (
        "id", "student", "course_name", "issued_at",
        "revoked", "ipfs_cid", "blockchain_hash", "pdf_link", "qr_link"
    )
    list_filter = ("revoked", "issued_at")
    search_fields = (
        "student__name", "student__email",
        "student__roll_no", "course_name", "ipfs_cid", "blockchain_hash"
    )
    readonly_fields = ("issued_at", "transaction_hash")

    def pdf_link(self, obj):
        if obj.pdf_file:
            return format_html('<a href="{}" target="_blank">Download PDF</a>', obj.pdf_file.url)
        return "-"
    pdf_link.short_description = "PDF"

    def qr_link(self, obj):
        if obj.qr_code:
            return format_html('<a href="{}" target="_blank">View QR</a>', obj.qr_code.url)
        return "-"
    qr_link.short_description = "QR Code"



@admin.register(RevokedCertificate)
class RevokedCertificateAdmin(admin.ModelAdmin):
    list_display = ("id", "certificate", "revoked_at")
    readonly_fields = ("revoked_at",)
