from django.urls import path
from core import views

urlpatterns = [
    # Landing Page
    path('', views.index_view, name='index'),

    # Admin Login / Logout
    path('admin-login/', views.admin_login_view, name='admin_login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # Admin Certificate Actions
    path('issue-certificate/', views.issue_certificate_view, name='issue_certificate'),
    path('revoke-certificate/', views.revoke_certificate_view, name='revoke_certificate'),
    path('verify/', views.verify_certificate_view, name='verify_certificate'),
    # Verifier Dashboard and Actions
    path('verifier-dashboard/', views.verifier_dashboard_view, name='verifier_dashboard'),
    path('verify-result/', views.verify_result, name='verify_result'),
    # Verifier-specific result page
    path('verifier-result/', views.verifier_result_view, name='verifier_result'),

    # API Endpoint (for QR code verification)
    path('verify-api/', views.verify_api_view, name='verify_api'),
]
