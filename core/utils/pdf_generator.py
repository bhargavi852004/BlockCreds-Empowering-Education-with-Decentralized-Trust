from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
import io, os

def generate_certificate_pdf(student_name, roll_no, course_name, percentage, status,
                             verify_url, qr_path, signature_path, logo_path, institute_name,
                             cert_title="Certificate of Completion"):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # =====================
    # Border
    # =====================
    margin = 40
    c.setStrokeColor(colors.darkblue)
    c.setLineWidth(4)
    c.rect(margin, margin, width - 2*margin, height - 2*margin)

    # Inner border
    c.setStrokeColor(colors.lightblue)
    c.setLineWidth(1)
    c.rect(margin+10, margin+10, width - 2*(margin+10), height - 2*(margin+10))

    # =====================
    # Logo + Institute Name
    # =====================
    if logo_path and os.path.exists(logo_path):
        logo = ImageReader(logo_path)
        c.drawImage(logo, width/2 - 40, height - 140, width=80, height=80, preserveAspectRatio=True)

    c.setFont("Helvetica-Bold", 26)
    c.setFillColor(colors.darkblue)
    c.drawCentredString(width / 2, height - 170, institute_name)

    # =====================
    # Certificate Title
    # =====================
    c.setFont("Times-BoldItalic", 30)
    c.setFillColor(colors.black)
    c.drawCentredString(width / 2, height - 230, cert_title)

    # =====================
    # Certificate Body
    # =====================
    c.setFont("Helvetica", 14)
    c.setFillColor(colors.black)
    c.drawCentredString(width / 2, height - 280, "This is to certify that")

    c.setFont("Times-BoldItalic", 22)
    c.setFillColor(colors.darkred)
    c.drawCentredString(width / 2, height - 320, student_name)

    c.setFont("Helvetica", 14)
    c.setFillColor(colors.black)
    c.drawCentredString(width / 2, height - 350, f"Roll No: {roll_no}")
    c.drawCentredString(width / 2, height - 380, "has successfully completed the course:")

    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(colors.darkblue)
    c.drawCentredString(width / 2, height - 410, course_name)

    c.setFont("Helvetica", 14)
    c.setFillColor(colors.black)
    c.drawCentredString(width / 2, height - 440, f"Percentage/CGPA: {percentage}")
    c.drawCentredString(width / 2, height - 460, f"Status: {status}")

    # =====================
    # QR Code + Verification URL
    # =====================
    if qr_path and os.path.exists(qr_path):
        qr_img = ImageReader(qr_path)
        c.drawImage(qr_img, 100, 80, width=80, height=80)

    c.setFont("Helvetica", 10)
    c.setFillColor(colors.black)
    c.drawString(100, 70, f"Verify at: {verify_url}")

    # =====================
    # Principal Signature
    # =====================
    if signature_path and os.path.exists(signature_path):
        sign_img = ImageReader(signature_path)
        c.drawImage(sign_img, width - 220, 90, width=120, height=50, mask="auto")
        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(colors.black)
        c.drawCentredString(width - 160, 70, "Principal")

    # =====================
    # Watermark (Optional)
    # =====================
    c.saveState()
    c.setFont("Helvetica-Bold", 50)
    c.setFillColorRGB(0.9, 0.9, 0.9, alpha=0.3)
    c.translate(width/2, height/2)
    c.rotate(30)
    c.drawCentredString(0, 0, institute_name.upper())
    c.restoreState()

    # Finalize PDF
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer
