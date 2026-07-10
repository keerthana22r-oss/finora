// Reads chart data safely injected by Django's {{ data|json_script:"..." }} tag
// (this avoids XSS risks that come from dumping raw JSON into a <script> tag directly)

document.addEventListener('DOMContentLoaded', function () {
    const barData = JSON.parse(document.getElementById('bar-chart-data').textContent);
    const doughnutData = JSON.parse(document.getElementById('doughnut-chart-data').textContent);
    const trendData = JSON.parse(document.getElementById('trend-chart-data').textContent);

    // ---- Income vs Expense Bar Chart ----
    const barCtx = document.getElementById('barChart');
    if (barCtx) {
        new Chart(barCtx, {
            type: 'bar',
            data: {
                labels: barData.labels,
                datasets: [
                    {
                        label: 'Income',
                        data: barData.income,
                        backgroundColor: '#2f9e44',
                        borderRadius: 4,
                    },
                    {
                        label: 'Expense',
                        data: barData.expense,
                        backgroundColor: '#e03131',
                        borderRadius: 4,
                    },
                ],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { position: 'bottom' } },
                scales: { y: { beginAtZero: true } },
            },
        });
    }

    // ---- Expense by Category Doughnut Chart ----
    const doughnutCtx = document.getElementById('doughnutChart');
    if (doughnutCtx && doughnutData.labels.length > 0) {
        const palette = [
            '#2f80ed', '#e03131', '#2f9e44', '#f59f00', '#9c36b5',
            '#1098ad', '#e8590c', '#495057', '#c2255c', '#5f3dc4',
            '#0ca678', '#f08c00', '#7048e8', '#1971c2', '#d6336c', '#37b24d',
        ];
        new Chart(doughnutCtx, {
            type: 'doughnut',
            data: {
                labels: doughnutData.labels,
                datasets: [{
                    data: doughnutData.values,
                    backgroundColor: palette,
                }],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { position: 'right', labels: { boxWidth: 12 } } },
            },
        });
    }

    // ---- Monthly Spending Trend Line Chart ----
    const trendCtx = document.getElementById('trendChart');
    if (trendCtx) {
        new Chart(trendCtx, {
            type: 'line',
            data: {
                labels: trendData.labels,
                datasets: [{
                    label: 'Total Expenses',
                    data: trendData.values,
                    borderColor: '#2f80ed',
                    backgroundColor: 'rgba(47, 128, 237, 0.1)',
                    fill: true,
                    tension: 0.3,
                    pointRadius: 4,
                }],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: { y: { beginAtZero: true } },
            },
        });
    }
});
