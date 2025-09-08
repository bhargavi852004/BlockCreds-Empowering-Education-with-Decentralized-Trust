document.addEventListener("DOMContentLoaded", () => {
    const data = window.dashboardData;

    const issuedCtx = document.getElementById('issuedChart').getContext('2d');
    new Chart(issuedCtx, {
        type: 'line',
        data: {
            labels: data.issuedLabels,
            datasets: [{
                label: 'Issued Certificates',
                data: data.issuedData,
                borderColor: '#4F46E5',
                backgroundColor: 'rgba(79, 70, 229, 0.2)',
                fill: true,
                tension: 0.4
            }]
        },
        options: { responsive: true, maintainAspectRatio: false }
    });

    const revokedCtx = document.getElementById('revokedChart').getContext('2d');
    new Chart(revokedCtx, {
        type: 'doughnut',
        data: {
            labels: ['Active', 'Revoked'],
            datasets: [{
                data: [data.activeCertificates, data.revokedCertificates],
                backgroundColor: ['#22c55e', '#ef4444']
            }]
        },
        options: { responsive: true, maintainAspectRatio: false }
    });
});
