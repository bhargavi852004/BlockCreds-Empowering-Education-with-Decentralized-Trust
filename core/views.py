import os
from datetime import timedelta
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
from django.contrib import messages
from django.utils.timezone import now

from .models import Student, Certificate, RevokedCertificate
from .forms import CertificateIssueForm
from .utils.blockchain import (
    issue_certificate_on_chain,
    revoke_certificate_on_chain,
    get_certificate_from_chain
)
from .utils.pinata import upload_to_pinata
from .utils.certificate_utils import generate_certificate_pdf
from .utils.email_sender import send_certificate_email

User = get_user_model()
QR_CODE_BASE_URL = os.getenv("QR_CODE_BASE_URL", "http://127.0.0.1:8000/verify/?hash=")


# ----------------------------
# Landing Page
# ----------------------------
def index_view(request):
    return render(request, "core/index.html")


# ----------------------------
# Admin Login
# ----------------------------
def admin_login_view(request):
    if request.method == "POST":
        identifier = request.POST.get("email_or_username")
        password = request.POST.get("password")
        user = None
        try:
            user_obj = User.objects.get(email=identifier)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = authenticate(request, username=identifier, password=password)

        if user and user.is_staff:
            login(request, user)
            return redirect("dashboard")

        return render(request, "core/admin_login.html", {"error": "Invalid credentials"})

    return render(request, "core/admin_login.html")


# ----------------------------
# Logout
# ----------------------------
def logout_view(request):
    logout(request)
    return redirect("index")


# ----------------------------
# Admin Dashboard
# ----------------------------
@login_required(login_url="admin_login")
def dashboard_view(request):
    total_certificates = Certificate.objects.count()
    active_certificates = Certificate.objects.filter(revoked=False).count()
    revoked_certificates = Certificate.objects.filter(revoked=True).count()

    issued_labels, issued_data = [], []
    for i in range(6, -1, -1):
        day = now().date() - timedelta(days=i)
        count = Certificate.objects.filter(issued_at__date=day).count()
        issued_labels.append(day.strftime("%b %d"))
        issued_data.append(count)

    return render(request, "core/dashboard.html", {
        "total_certificates": total_certificates,
        "active_certificates": active_certificates,
        "revoked_certificates": revoked_certificates,
        "issued_labels": issued_labels,
        "issued_data": issued_data,
    })


# ----------------------------
# Issue Certificate
# ----------------------------
@login_required(login_url="admin_login")
def issue_certificate_view(request):
    if request.method == "POST":
        form = CertificateIssueForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            roll_no = form.cleaned_data["roll_no"]
            course_name = form.cleaned_data["course_name"]
            percentage = form.cleaned_data["percentage"]

            student, _ = Student.objects.get_or_create(
                email=email,
                defaults={"name": name, "roll_no": roll_no}
            )

            # Generate unique hash
            cert_hash = os.urandom(32).hex()
            verify_url = f"{QR_CODE_BASE_URL}{cert_hash}"

            # Generate PDF & QR code
            pdf_path, qr_path = generate_certificate_pdf(
                student_name=name,
                course_name=course_name,
                hash_value=cert_hash,
                verify_url=verify_url,
                logo_path=os.path.join(settings.BASE_DIR, "core/static/core/images/logo.png"),
                cgpa=percentage
            )

            try:
                # Upload to IPFS
                ipfs_cid = upload_to_pinata(pdf_path)

                # Issue on blockchain (waits for confirmation)
                tx_hash = issue_certificate_on_chain(bytes.fromhex(cert_hash), ipfs_cid)
                if not tx_hash:
                    messages.error(request, "Failed to issue certificate on blockchain.")
                    return redirect("issue_certificate")

                # Save to DB
                certificate = Certificate.objects.create(
                    student=student,
                    course_name=course_name,
                    pdf_file=f"certificates/{os.path.basename(pdf_path)}",
                    qr_code=f"qr/{cert_hash}.png",
                    blockchain_hash=cert_hash,
                    transaction_hash=tx_hash,
                    ipfs_cid=ipfs_cid,
                    revoked=False
                )

                # Send email
                try:
                    send_certificate_email(email, name, pdf_path, qr_path)
                except Exception as e:
                    messages.warning(request, f"Certificate issued but email failed: {str(e)}")

                messages.success(request, "Certificate issued successfully!")
                return redirect("dashboard")

            except Exception as e:
                messages.error(request, f"Error issuing certificate: {str(e)}")
                return redirect("issue_certificate")
    else:
        form = CertificateIssueForm()

    return render(request, "core/issue_certificate.html", {"form": form})


# ----------------------------
# Revoke Certificate
# ----------------------------
@login_required(login_url="admin_login")
def revoke_certificate_view(request):
    certificates = Certificate.objects.select_related('student').all()

    if request.method == "POST":
        cert_hash = request.POST.get("hash")
        try:
            tx_hash = revoke_certificate_on_chain(bytes.fromhex(cert_hash))
            if tx_hash:
                cert_obj = Certificate.objects.get(blockchain_hash=cert_hash)
                cert_obj.revoked = True
                cert_obj.save()
                RevokedCertificate.objects.create(certificate=cert_obj)
                messages.success(request, "Certificate revoked successfully!")
            else:
                messages.error(request, "Blockchain transaction failed for revocation.")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")

    return render(request, "core/revoke_certificate.html", {"certificates": certificates})


# ----------------------------
# Verifier Dashboard
# ----------------------------
@login_required(login_url="admin_login")
def verifier_dashboard_view(request):
    return render(request, "core/verifier_dashboard.html")


# ----------------------------
# Verify Certificate Page
# ----------------------------
def verify_certificate_view(request):
    return render(request, "core/verify_certificate.html")


# ----------------------------
# API Verification Endpoint
# ----------------------------
def verify_api_view(request):
    hash_value = request.GET.get("hash")
    if not hash_value:
        return JsonResponse({"status": "error", "message": "No hash provided."})

    try:
        cert = Certificate.objects.get(blockchain_hash=hash_value)
        response = {
            "status": "success",
            "cid": cert.ipfs_cid,
            "issuedAt": int(cert.issued_at.timestamp()),
            "revoked": cert.revoked,
            "studentName": cert.student.name,
            "courseName": cert.course_name,
        }
    except Certificate.DoesNotExist:
        response = {"status": "error", "message": "Certificate not found."}

    return JsonResponse(response)


# ----------------------------
# Verify Result Page
# ----------------------------
def verify_result(request):
    cert_hash = request.GET.get('hash')
    context = {
        "status": None,
        "message": None,
        "student_name": None,
        "course_name": None,
        "issued_at": None,
        "cid": None,
        "hash": cert_hash
    }

    if cert_hash:
        try:
            cid, issued_at, revoked = get_certificate_from_chain(bytes.fromhex(cert_hash))
            cert_obj = Certificate.objects.filter(blockchain_hash=cert_hash).first()

            if revoked:
                context["status"] = "revoked"
                context["message"] = "This certificate has been revoked."
            else:
                context["status"] = "valid"
                context["message"] = "This certificate is valid."

            context.update({
                "cid": cid,
                "issued_at": issued_at,
                "student_name": cert_obj.student.name if cert_obj else "Unknown",
                "course_name": cert_obj.course_name if cert_obj else "Unknown"
            })

        except Exception:
            context["status"] = "tampered"
            context["message"] = "Certificate is invalid or tampered."
    else:
        context["status"] = "error"
        context["message"] = "No hash provided."

    return render(request, "core/verify_result.html", context)
# ----------------------------
# Verifier Result Page
# ----------------------------
def verifier_result_view(request):
    cert_hash = request.GET.get('hash')
    context = {
        "status": None,
        "message": None,
        "student_name": None,
        "course_name": None,
        "issued_at": None,
        "cid": None,
        "hash": cert_hash
    }

    if cert_hash:
        try:
            cert = Certificate.objects.filter(blockchain_hash=cert_hash).first()
            if cert:
                context["status"] = "revoked" if cert.revoked else "valid"
                context["message"] = "This certificate has been revoked." if cert.revoked else "This certificate is valid."
                context["student_name"] = cert.student.name
                context["course_name"] = cert.course_name
                context["issued_at"] = cert.issued_at
                context["cid"] = cert.ipfs_cid
            else:
                context["status"] = "tampered"
                context["message"] = "Certificate not found."
        except Exception:
            context["status"] = "tampered"
            context["message"] = "Certificate is invalid or tampered."
    else:
        context["status"] = "error"
        context["message"] = "No hash provided."

    return render(request, "core/verifier_result.html", context)
