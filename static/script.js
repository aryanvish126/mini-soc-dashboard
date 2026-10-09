
let loginChart = null;

async function loadDashboard() {
    try {
        const response = await fetch("/api/dashboard");

        if (!response.ok) {
            throw new Error("Dashboard API returned an error");
        }

        const data = await response.json();

        document.getElementById("total-events").textContent =
            data.total_events;

        document.getElementById("failed-logins").textContent =
            data.failed_logins;

        document.getElementById("successful-logins").textContent =
            data.successful_logins;

        document.getElementById("high-alerts").textContent =
            data.high_alerts;

        renderAlerts(data.alerts);
        renderEvents(data.events);
        renderChart(data.successful_logins, data.failed_logins);

    } catch (error) {
        console.error("Dashboard loading failed:", error);
    }
}

function renderAlerts(alerts) {
    const tbody = document.getElementById("alerts-body");
    tbody.replaceChildren();

    if (!alerts.length) {
        const row = tbody.insertRow();
        const cell = row.insertCell();
        cell.colSpan = 4;
        cell.textContent = "No alerts detected.";
        return;
    }

    alerts.forEach(alert => {
        const row = tbody.insertRow();

        const severity = row.insertCell();
        const badge = document.createElement("span");
        badge.className = "severity high";
        badge.textContent = alert.severity;
        severity.appendChild(badge);

        row.insertCell().textContent = alert.title;
        row.insertCell().textContent = alert.source_ip;
        row.insertCell().textContent = alert.description;
    });
}

function renderEvents(events) {
    const tbody = document.getElementById("events-body");
    tbody.replaceChildren();

    events.forEach(event => {
        const row = tbody.insertRow();

        row.insertCell().textContent =
            new Date(event.timestamp).toLocaleString();

        row.insertCell().textContent = event.source_ip;
        row.insertCell().textContent = event.username;
        row.insertCell().textContent = event.event_type;

        const statusCell = row.insertCell();
        const badge = document.createElement("span");

        badge.className = "status " +
            event.status.toLowerCase();

        badge.textContent = event.status;
        statusCell.appendChild(badge);
    });
}

function renderChart(successful, failed) {
    const canvas = document.getElementById("loginChart");

    if (!canvas || typeof Chart === "undefined") {
        console.error("Chart.js did not load.");
        return;
    }

    if (loginChart) {
        loginChart.destroy();
    }

    loginChart = new Chart(canvas, {
        type: "doughnut",
        data: {
            labels: ["Successful Logins", "Failed Logins"],
            datasets: [{
                data: [successful, failed],
                backgroundColor: ["#34d399", "#fb7185"],
                borderColor: "#111b2e",
                borderWidth: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: "bottom",
                    labels: {
                        color: "#e6edf7",
                        padding: 20
                    }
                }
            }
        }
    });
}

document.addEventListener("DOMContentLoaded", () => {
    loadDashboard();

    // Refresh dashboard data every 30 seconds.
    setInterval(loadDashboard, 30000);
});