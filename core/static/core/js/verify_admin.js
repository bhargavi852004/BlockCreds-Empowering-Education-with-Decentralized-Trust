let scannedQR = null;

// Start QR Scan
function startQRScan() {
    const qrReader = new Html5Qrcode("qr-reader");

    qrReader.start(
        { facingMode: "environment" },
        { fps: 10, qrbox: 250 },
        qrCodeMessage => {
            scannedQR = qrCodeMessage;
            qrReader.stop().then(() => {
                redirectToResult(scannedQR);
            });
        },
        errorMessage => {
            console.log("Scan error:", errorMessage);
        }
    ).catch(err => {
        console.error("Unable to start scanning", err);
    });
}

// Upload QR image verification
function uploadQR() {
    const fileInput = document.getElementById("qrUpload");
    if (fileInput.files.length === 0) return alert("Please select a QR image.");

    const file = fileInput.files[0];
    const reader = new FileReader();

    reader.onload = function () {
        const img = new Image();
        img.onload = function () {
            const canvas = document.createElement("canvas");
            canvas.width = img.width;
            canvas.height = img.height;
            const ctx = canvas.getContext("2d");
            ctx.drawImage(img, 0, 0);
            const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);

            // Use jsQR to decode QR
            const code = jsQR(imageData.data, canvas.width, canvas.height);
            if (code) {
                redirectToResult(code.data);
            } else {
                alert("No QR code found in image.");
            }
        };
        img.src = reader.result;
    };

    reader.readAsDataURL(file);
}

// Redirect to result page
function redirectToResult(qrContent) {
    if (!qrContent) return;

    // Extract hash from QR URL
    let hash = qrContent.split("hash=")[1];
    if (!hash) return alert("Invalid QR code format.");

    window.location.href = `/verify-result/?hash=${hash}`;
}

// Tab switch
function showTab(tab) {
    document.querySelectorAll('.tab-content').forEach(tc => tc.classList.add('hidden'));
    document.getElementById(tab).classList.remove('hidden');

    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active', 'bg-primary', 'text-white'));
    const tabBtn = document.getElementById(`${tab}-tab`);
    tabBtn.classList.add('active', 'bg-primary', 'text-white');

    if (tab === 'scan') startQRScan();
}
