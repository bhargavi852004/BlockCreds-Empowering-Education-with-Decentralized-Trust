import os
import qrcode
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from django.conf import settings


def generate_qr_code(hash_value: str, verify_url: str) -> str:
    """Generate QR code and return file path."""
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(f"{verify_url}?hash={hash_value}")
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_path = os.path.join(settings.MEDIA_ROOT, "qr", f"{hash_value}.png")
    os.makedirs(os.path.dirname(qr_path), exist_ok=True)
    qr_img.save(qr_path)
    return qr_path


def generate_certificate_pdf(student_name, course_name, hash_value, verify_url,
                             cgpa="", logo_path=None, signatory="Dr.P.Radhika",
                             institute_name="Vignan's Nirula Institute of Technology and Science for Women") -> tuple:
    """
    Generate PDF certificate identical to original final_certificate.pdf.
    Returns: (pdf_path, qr_path)
    """

    cert_dir = os.path.join(settings.MEDIA_ROOT, "certificates")
    os.makedirs(cert_dir, exist_ok=True)
    pdf_path = os.path.join(cert_dir, f"{hash_value}.pdf")

    c = canvas.Canvas(pdf_path, pagesize=landscape(A4))
    width, height = landscape(A4)
    margin = 40

    # Border
    c.setStrokeColor(HexColor("#1E3A8A"))
    c.setLineWidth(4)
    c.rect(margin, margin, width - 2 * margin, height - 2 * margin)

    # Logo + Institute Name at Top-Left
    if logo_path and os.path.exists(logo_path):
        logo_img = ImageReader(logo_path)
        logo_width = 120
        logo_height = 120
        logo_x = margin + 10
        logo_y = height - margin - logo_height
        c.drawImage(logo_img, logo_x, logo_y, width=logo_width, height=logo_height, preserveAspectRatio=True)

        # College Name beside logo in two lines
        c.setFont("Helvetica-Bold", 25)
        c.setFillColor(HexColor("#1E3A8A"))
        line1 = "Vignan's Nirula Institute of Technology and "
        line2 = " Science for Women"
        c.drawString(logo_x + logo_width + 40, logo_y + logo_height - 55, line1)
        c.drawString(logo_x + logo_width + 170, logo_y + logo_height - 95, line2)

    # Certificate Body
    c.setFont("Helvetica", 14)
    c.drawCentredString(width / 2 + 30, height - 160, "Pedapalakaluru, Guntur")

    # Certificate Title
    c.setFont("Helvetica-Bold", 25)
    c.drawCentredString(width / 2 + 20, height - 240, "Certificate of Achievement")

    # Certificate Body
    c.setFont("Helvetica", 14)
    c.drawCentredString(width / 2 + 20, height - 270, "This is to certify that")

    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(width / 2 + 20, height - 300, student_name)

    c.setFont("Helvetica", 14)
    c.drawCentredString(width / 2 + 20, height - 330, "has successfully completed the course")

    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2 + 20, height - 360, f"'{course_name}'")

    # CGPA / Percentage
    if cgpa:
        c.setFont("Helvetica", 14)
        c.drawCentredString(width / 2 + 20, height - 390, f"with a CGPA/percentage of {cgpa}")

    # Footer: Issued Date, Signature, QR Code
    issued_date = datetime.now().strftime("%d-%m-%Y")
    c.setFont("Helvetica", 12)
    c.drawString(margin + 10, margin + 70, signatory)
    c.drawString(margin + 10, margin + 55, "Principal")

    c.setFont("Helvetica", 10)
    c.drawString(margin + 10, margin + 30, f"Issued on: {issued_date}")

    # QR Code
    qr_path = generate_qr_code(hash_value, verify_url)
    c.drawImage(ImageReader(qr_path), width - margin - 80, margin + 40, width=60, height=60)

    # Verification URL and Certificate ID
    c.setFont("Helvetica-Oblique", 9)
    c.drawCentredString(width / 2, margin + 30, f"Verify at: {verify_url}?hash= hashvalue")
    c.setFont("Helvetica", 8)
    c.drawCentredString(width / 2, margin + 20, f"Certificate ID: {hash_value}")

    c.save()
    return pdf_path, qr_path
