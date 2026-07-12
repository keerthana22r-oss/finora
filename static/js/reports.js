document.addEventListener('DOMContentLoaded', function () {
    const yearlyRows = JSON.parse(document.getElementById('yearly-rows-data').textContent);
    const categoryTotals = JSON.parse(document.getElementById('category-totals-data').textContent);

    // ---- Yearly Income vs Expense Bar Chart ----
    const trendCtx = document.getElementById('yearlyTrendChart');
    if (trendCtx) {
        new Chart(trendCtx, {
            type: 'bar',
            data: {
                labels: yearlyRows.map(r => r.month_name),
                datasets: [
                    {
                        label: 'Income',
                        // Values arrive as strings (Decimal serialized via DjangoJSONEncoder), so parseFloat them.
                        data: yearlyRows.map(r => parseFloat(r.income)),
                        backgroundColor: '#2f9e44',
                        borderRadius: 4,
                    },
                    {
                        label: 'Expense',
                        data: yearlyRows.map(r => parseFloat(r.expense)),
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

    // ---- Full-Year Category Breakdown Doughnut Chart ----
    const categoryCtx = document.getElementById('categoryYearChart');
    if (categoryCtx && categoryTotals.labels.length > 0) {
        const palette = [
            '#2f80ed', '#e03131', '#2f9e44', '#f59f00', '#9c36b5',
            '#1098ad', '#e8590c', '#495057', '#c2255c', '#5f3dc4',
            '#0ca678', '#f08c00', '#7048e8', '#1971c2', '#d6336c', '#37b24d',
        ];
        new Chart(categoryCtx, {
            type: 'doughnut',
            data: {
                labels: categoryTotals.labels,
                datasets: [{
                    data: categoryTotals.values,
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
});
