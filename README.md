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

### 1. Admin Login
- Navigate to the Admin Login page.  
- Enter your admin email and password.  
- Click **Login** to access the dashboard.  

📌 Screenshot Placeholder:  
![Admin Login](static/core/images/screenshots/admin_login.png)

---

### 2. Issue Certificate
- Go to **Issue Certificate** from the dashboard.  
- Fill in Student Details, Course Name, and other fields.  
- Click **Generate Certificate**.  

The system will:  
- Generate PDF & QR Code  
- Upload PDF to IPFS  
- Store IPFS Hash on Polygon Smart Contract  
- Send Email to student  

📌 Screenshot Placeholder:  
![Issue Certificate](static/core/images/screenshots/issue_certificate.png)

---

### 3. Verify Certificate
- Scan the QR Code or visit the **Verify Certificate** page.  
- Enter the Certificate Hash.  
- Click **Verify** to check authenticity.  

📌 Screenshot Placeholder:  
![Verify Certificate](static/core/images/screenshots/verify_certificate.png)

---

### 4. Revoke Certificate
- Navigate to **Revoke Certificate** page.  
- Select the certificate and click **Revoke**.  
- Blockchain updates status to Revoked.  

📌 Screenshot Placeholder:  
![Revoke Certificate](static/core/images/screenshots/revoke_certificate.png)

---

## Smart Contract Details

- **Language:** Solidity  
- **Deployed On:** Polygon Amoy Testnet  
- **Features:** Issue, Verify, and Revoke certificates  
- **Tools:** Remix for deployment  

---

