let scannedQR = null;
let qrScannerStarted = false;

// Tab switch
function showTab(tab) {
    document.querySelectorAll('.tab-content').forEach(tc => tc.classList.add('hidden'));
    document.getElementById(tab).classList.remove('hidden');

    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active', 'bg-primary', 'text-white'));
    document.getElementById(`${tab}-tab`).classList.add('active', 'bg-primary', 'text-white');

    if (tab === 'scan') startQRScan();
}

// Manual verify handled by form submission

// Upload QR
function uploadQR() {
    const fileInput = document.getElementById('qrUpload');
    if(fileInput.files.length === 0) { alert('Please upload a QR code image.'); return; }

    const reader = new FileReader();
    reader.onload = function() {
        const img = new Image();
        img.src = reader.result;
        img.onload = function() {
            const canvas = document.createElement('canvas');
            canvas.width = img.width; canvas.height = img.height;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(img, 0, 0);
            const code = jsQR(ctx.getImageData(0, 0, img.width, img.height).data, img.width, img.height);
            if(code) redirectToResult(code.data);
            else alert("No QR code found in the image.");
        }
    }
    reader.readAsDataURL(fileInput.files[0]);
}

// Start QR scanning from camera
function startQRScan() {
    if(qrScannerStarted) return;
    qrScannerStarted = true;

    const qrReader = new Html5Qrcode("qr-reader");

    Html5Qrcode.getCameras().then(cameras => {
        if(cameras && cameras.length) {
            qrReader.start(
                { facingMode: "environment" },
                { fps: 10, qrbox: { width: 250, height: 250 } },
                qrCodeMessage => {
                    scannedQR = qrCodeMessage;
                    qrReader.stop().then(() => redirectToResult(scannedQR));
                },
                errorMessage => {}
            ).catch(err => console.error("Unable to start scanning", err));
        }
    }).catch(err => console.error("No cameras found", err));
}

// Redirect to verifier_result page
function redirectToResult(qrContent) {
    if (!qrContent) return;

    let hash = qrContent.split("hash=")[1];
    if (!hash) return alert("Invalid QR code format.");

    window.location.href = `/verifier-result/?hash=${hash}`;
}
