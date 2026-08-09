const API_URL = "http://localhost:8000";

// Tab Switching Logic
function switchTab(tabId) {
    document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
    document.querySelector(`#${tabId}`).classList.add('active');

    document.querySelectorAll('.nav-links li').forEach(nav => nav.classList.remove('active'));
    event.currentTarget.classList.add('active');

    if (tabId === 'dashboard') loadDashboard();
    if (tabId === 'monitoring') loadMonitoring();
    if (tabId === 'mlflow') loadMLflow();
}

// Prediction Logic
async function submitPrediction() {
    const data = {
        gender: document.getElementById('gender').value,
        SeniorCitizen: parseInt(document.getElementById('SeniorCitizen').value),
        Partner: document.getElementById('Partner').value,
        Dependents: document.getElementById('Dependents').value,
        tenure: parseInt(document.getElementById('tenure').value),
        PhoneService: document.getElementById('PhoneService').value,
        MultipleLines: document.getElementById('MultipleLines').value,
        InternetService: document.getElementById('InternetService').value,
        OnlineSecurity: document.getElementById('OnlineSecurity').value,
        OnlineBackup: document.getElementById('OnlineBackup').value,
        DeviceProtection: document.getElementById('DeviceProtection').value,
        TechSupport: document.getElementById('TechSupport').value,
        StreamingTV: document.getElementById('StreamingTV').value,
        StreamingMovies: document.getElementById('StreamingMovies').value,
        Contract: document.getElementById('Contract').value,
        PaperlessBilling: document.getElementById('PaperlessBilling').value,
        PaymentMethod: document.getElementById('PaymentMethod').value,
        MonthlyCharges: parseFloat(document.getElementById('MonthlyCharges').value),
        TotalCharges: parseFloat(document.getElementById('TotalCharges').value)
    };

    const btn = document.querySelector('.btn.primary');
    btn.innerHTML = 'Predicting...';
    btn.disabled = true;

    try {
        const response = await fetch(`${API_URL}/predict/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        document.getElementById('res-risk').innerText = result.churn_risk;
        document.getElementById('res-prob').innerText = (result.probability * 100).toFixed(2) + '%';
        document.getElementById('res-drift').innerText = result.drift_score;

        const resBox = document.getElementById('result-box');
        resBox.style.display = 'block';
        resBox.setAttribute('data-risk', result.churn_risk);

    } catch (e) {
        alert('Error: ' + e.message + '. Ensure backend is running.');
    } finally {
        btn.innerHTML = 'Predict Churn';
        btn.disabled = false;
    }
}

async function submitBatchPrediction() {
    const fileInput = document.getElementById('batch-file');
    if (!fileInput.files.length) {
        alert("Please select a CSV file first.");
        return;
    }

    const btn = document.getElementById('batch-btn');
    btn.innerHTML = 'Processing...';
    btn.disabled = true;

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    try {
        const response = await fetch(`${API_URL}/predict/batch`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || 'Batch prediction failed');
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = "batch_predictions.csv";
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);

        alert("Batch prediction completed successfully! The file has been downloaded.");
    } catch (e) {
        alert('Error: ' + e.message);
    } finally {
        btn.innerHTML = 'Run Bulk Inference';
        btn.disabled = false;
        fileInput.value = '';
        updateFileName();
    }
}

function updateFileName() {
    const fileInput = document.getElementById('batch-file');
    const display = document.getElementById('file-name-display');
    if (fileInput.files.length > 0) {
        display.innerText = fileInput.files[0].name;
        display.style.color = 'var(--accent-glow)';
    } else {
        display.innerText = 'Click or Drag & Drop CSV Here';
        display.style.color = 'var(--text-primary)';
    }
}

// Dashboard Logic
let chartInstance = null;

async function loadDashboard() {
    try {
        const res = await fetch(`${API_URL}/dashboard/stats`);
        const stats = await res.json();

        document.getElementById('total-preds').innerText = stats.total_predictions;
        document.getElementById('high-risk-preds').innerText = stats.high_risk_predictions;

        // Also update Medium and Low risk elements if they exist
        const medEl = document.getElementById('medium-risk-preds');
        if (medEl) medEl.innerText = stats.medium_risk_predictions;

        const lowEl = document.getElementById('low-risk-preds');
        if (lowEl) lowEl.innerText = stats.low_risk_predictions;

        document.getElementById('anomalies-count').innerText = stats.anomalies_detected;

        // Render Chart
        if (chartInstance) chartInstance.destroy();
        const ctx = document.getElementById('riskDistributionChart').getContext('2d');

        chartInstance = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['High Risk', 'Medium Risk', 'Low Risk'],
                datasets: [{
                    data: [stats.high_risk_predictions, stats.medium_risk_predictions, stats.low_risk_predictions],
                    backgroundColor: [
                        'rgba(239, 68, 68, 0.8)',
                        'rgba(251, 191, 36, 0.8)',
                        'rgba(34, 197, 94, 0.8)'
                    ],
                    borderWidth: 0,
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { labels: { color: '#f8fafc' } }
                }
            }
        });
    } catch (e) { console.error('Dashboard load failed:', e); }
}

// Monitoring Logic
async function loadMonitoring() {
    try {
        const res = await fetch(`${API_URL}/dashboard/recent-logs?limit=15`);
        const logs = await res.json();

        const tbody = document.getElementById('logs-table-body');
        tbody.innerHTML = '';

        logs.forEach(log => {
            const tr = document.createElement('tr');

            const time = new Date(log.timestamp).toLocaleString();
            tr.innerHTML = `
                <td>${time}</td>
                <td><span class="tag ${log.churn_risk}">${log.churn_risk}</span></td>
                <td>${(log.probability * 100).toFixed(1)}%</td>
                <td>${log.drift_score}</td>
                <td><span class="tag ${log.is_anomaly ? 'True' : 'Low'}">${log.is_anomaly ? 'Yes' : 'No'}</span></td>
            `;
            tbody.appendChild(tr);
        });
    } catch (e) { console.error('Monitoring load failed:', e); }
}

// MLflow Logic
let mlflowChartInstance = null;

async function loadMLflow() {
    try {
        const res = await fetch(`${API_URL}/dashboard/mlflow-metrics`);
        const data = await res.json();

        if (data.error) {
            document.getElementById('mlflow-content').innerHTML = `<p style="color:red">Error: ${data.error}</p>`;
            return;
        }

        const metrics = data.metrics || {};

        // Build readable metrics
        let htmlStr = '<div class="stats-grid">';
        for (const [key, value] of Object.entries(metrics)) {
            htmlStr += `
                <div class="stat-card glass">
                    <h3 style="text-transform: capitalize;">${key.replace('_', ' ')}</h3>
                    <h2>${parseFloat(value).toFixed(4)}</h2>
                </div>
            `;
        }
        htmlStr += '</div>';
        document.getElementById('mlflow-content').innerHTML = htmlStr;

        // Optionally, render chart for metrics
        if (mlflowChartInstance) mlflowChartInstance.destroy();
        const ctx = document.getElementById('mlflowMetricsChart').getContext('2d');

        const labels = Object.keys(metrics).map(k => k.replace('_', ' ').toUpperCase());
        const values = Object.values(metrics);

        mlflowChartInstance = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Model Metrics',
                    data: values,
                    backgroundColor: 'rgba(56, 189, 248, 0.8)',
                    borderColor: 'rgba(56, 189, 248, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 1.0,
                        ticks: { color: '#94a3b8' }
                    },
                    x: {
                        ticks: { color: '#94a3b8' }
                    }
                },
                plugins: {
                    legend: { display: false }
                }
            }
        });

    } catch (e) { console.error('MLflow load failed:', e); }
}

// Initial Load
document.addEventListener('DOMContentLoaded', () => {
    // Start on Prediction Tab explicitly to set correct nav active state
    switchTab('predict');
});
