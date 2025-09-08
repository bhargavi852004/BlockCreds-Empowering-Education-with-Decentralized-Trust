# BlockCreds – Empowering Education with Decentralized Trust
A Secure and Scalable Blockchain-Based Academic Credential Verification System

---

## Overview

BlockCreds is a decentralized academic credential verification platform that ensures trust, transparency, and security in the issuance and verification of academic certificates.

Built on **Polygon Amoy Testnet**, BlockCreds leverages:

- **IPFS (InterPlanetary File System)** for decentralized storage  
- **Smart Contracts** for on-chain validation  
- **Django Framework** for a secure and responsive web application  

This solution significantly reduces transaction costs, verification time, and eliminates fraudulent certificates.

---

## Tech Stack

- **Blockchain:** Polygon (Amoy Testnet)  
- **Storage:** IPFS via Pinata API  
- **Smart Contracts:** Solidity  
- **Backend:** Django, Web3.py  
- **Frontend:** Bootstrap, Tailwind CSS  
- **Database:** SQLite (can be extended to PostgreSQL/MySQL)  

---

## Key Features

✅ Decentralized & Tamper-Proof Certificates stored on IPFS  
✅ Smart Contract Integration on Polygon for on-chain trust  
✅ Bulk Certificate Issuance via CSV upload  
✅ Integrated Revocation Mechanism for invalidating certificates  
✅ Real-Time Verification via QR Code  
✅ Modern & Responsive UI (Bootstrap + Tailwind CSS)  

---

## System Workflow

1. Admin Issues Certificate(s) through dashboard  
2. Certificate file is uploaded to IPFS → IPFS returns a unique hash (CID)  
3. IPFS hash is stored on Polygon blockchain using a smart contract  
4. QR code & PDF are generated for the certificate  
5. Verification can be done via QR scanning → Fetches IPFS hash from blockchain  

---

## Project Folder Structure

```
blockcreds/
│
├── blockchain/
│   └── abi/
│       ├── Cert.abi.json
│       └── Cert.sol
│
├── blockcreds/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── core/
│   ├── management/
│   ├── migrations/
│   │   ├── 0001_initial.py
│   │   └── __init__.py
│   │
│   ├── static/core/
│   │   ├── css/
│   │   │   ├── forms.css
│   │   │   ├── styles.css
│   │   │   └── verify.css
│   │   ├── images/
│   │   │   ├── admin_login_images/
│   │   │   │   ├── 1.jpg
│   │   │   │   ├── 2.jpg
│   │   │   │   └── 3.jpg
│   │   │   ├── index_bg/
│   │   │   │   ├── 1.jpg
│   │   │   │   └── 2.jpg
│   │   │   ├── logo.png
│   │   │   └── signature.png
│   │   └── js/
│   │       ├── dashboard.js
│   │       ├── qr-scanner.js
│   │       ├── verifier.js
│   │       └── verify_admin.js
│   │
│   ├── templates/core/
│   │   ├── admin_login.html
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── email_template.html
│   │   ├── index.html
│   │   ├── issue_certificate.html
│   │   ├── revoke_certificate.html
│   │   ├── verifier_base.html
│   │   ├── verifier_dashboard.html
│   │   ├── verifier_result.html
│   │   ├── verify_certificate.html
│   │   └── verify_result.html
│   │
│   ├── utils/
│   │   ├── blockchain.py
│   │   ├── certificate_utils.py
│   │   ├── email_sender.py
│   │   ├── hashing.py
│   │   ├── ipfs.py
│   │   ├── pdf_generator.py
│   │   ├── pinata.py
│   │   └── qr_generator.py
│   │
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── sync_events.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── media/
│   ├── certificates/
│   └── qr/
│
├── scripts/
│   ├── pinata_upload_test.py
│   ├── test_chain_connect.py
│   ├── test_issue.py
│   └── test_verify.py
│
├── .env
├── .gitignore
├── db.sqlite3
├── manage.py
├── README.md
└── requirements.txt
```

---

## Smart Contract

**File:** `blockchain/abi/Cert.sol`  
**Language:** Solidity  

**Features:**  
✅ Issue Certificates  
✅ Verify Certificates  
✅ Revoke Certificates  

**Deployed on:** Polygon Amoy Testnet (using POL tokens)  

---

## Installation Guide

### 1. Create Virtual Environment & Install Dependencies
```bash
python -m venv venv
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows
pip install -r requirements.txt
```

### 2. Configure Environment Variables in `.env`
```
SECRET_KEY=your_django_secret_key
DEBUG=True
PINATA_API_KEY=your_pinata_api_key
PINATA_SECRET_KEY=your_pinata_secret_key
PINATA_JWT=your_pinata_jwt
POLYGON_PRIVATE_KEY=your_wallet_private_key
POLYGON_RPC_URL=https://rpc-amoy.polygon.technology
CONTRACT_ADDRESS=your_deployed_contract_address
# Email Settings (for student notifications)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your@gmail.com
EMAIL_HOST_PASSWORD=PASSWORD

```

### 3. Run Migrations & Start Server
```bash
python manage.py migrate
python manage.py runserver
```

Access the application at:  
👉 [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## Usage Guide

### Admin Login
- Navigate to the Admin Login page.  
- Enter your admin email and password.  
- Click **Login** to access the dashboard.
<img width="1919" height="1021" alt="Index" src="https://github.com/user-attachments/assets/ef0e9a18-23b2-4284-af89-1e3bd0b9aa72" />
<img width="1919" height="1033" alt="Admin" src="https://github.com/user-attachments/assets/354c8f31-2f87-4936-b28c-1ff314511ab1" />

---
### Admin Dashboard
- Get Info about issued, revoked certificates.
- Navigate to the issue certificate page.  
- Navigate to the Verify certificate page.
- Navigate to the Revoke certificate page.
<img width="1919" height="1024" alt="Dashboard" src="https://github.com/user-attachments/assets/0b563a40-d870-4415-8d50-319589b17cd4" />

### 1. Issue Certificate
- Go to **Issue Certificate** from the dashboard.  
- Fill in Student Details, Course Name, and other fields.  
- Click **Generate Certificate**.  
<img width="1596" height="990" alt="Issue_Certificate Dashboard" src="https://github.com/user-attachments/assets/66648b6c-f719-48da-9ee5-50a885483481" />

The system will:  
- Generate PDF & QR Code  
- Upload PDF to IPFS  
- Store IPFS Hash on Polygon Smart Contract  
- Send Email to student  
<img width="954" height="742" alt="Screenshot 2025-09-08 140534" src="https://github.com/user-attachments/assets/0de0839c-028a-4722-9256-a085ed6f4fe3" />



---

### 2. Verify Certificate
- Scan the QR Code or visit the **Verify Certificate** page.  
- Enter the Certificate Hash.  
- Click **Verify** to check authenticity.
<img width="1208" height="533" alt="Screenshot 2025-09-08 140919" src="https://github.com/user-attachments/assets/15ad0622-e667-456d-a1fb-344c9097d529" />
<img width="909" height="555" alt="Screenshot 2025-09-08 140944" src="https://github.com/user-attachments/assets/82a682e8-4405-4ae6-9850-836b1ad0a86b" />

<img width="1918" height="951" alt="Verify_Certificate Dashboard" src="https://github.com/user-attachments/assets/0e2abd47-c263-4496-822c-aee19dbb36a0" />
---

### 4. Revoke Certificate
- Navigate to **Revoke Certificate** page.  
- Select the certificate and click **Revoke**.  
- Blockchain updates status to Revoked.  
<img width="1592" height="977" alt="Revoke Dashboard" src="https://github.com/user-attachments/assets/0d6059d6-2fc5-4e68-adca-a2a2f007ee58" />


---

## Smart Contract Details

- **Language:** Solidity  
- **Deployed On:** Polygon Amoy Testnet  
- **Features:** Issue, Verify, and Revoke certificates  
- **Tools:** Remix for deployment  

---
## ✍️ Developed By

* **Nagulapally Bhargavi** - https://github.com/bhargavi852004



