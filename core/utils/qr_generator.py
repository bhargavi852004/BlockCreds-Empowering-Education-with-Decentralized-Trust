import qrcode
import os


def generate_qr_code(verification_url, output_path):
    """
    Generate a QR code image for certificate verification URL.
    """
    img = qrcode.make(verification_url)
    img.save(output_path)
