// Analytics page JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Sample data - in a real application, this would come from the server
    const documentTypes = {
        'PDF': 45,
        'DOCX': 30,
        'TXT': 15,
        'Image': 10
    };
    
    const readabilityScores = {
        'Simple (0-30)': 20,
        'Standard (31-70)': 50,
        'Complex (71-100)': 30
    };
    
    const commonKeywords = {
        'technology': 24,
        'report': 18,
        'analysis': 16,
        'data': 14,
        'research': 12,
        'project': 10,
        'results': 9,
        'development': 8,
        'system': 7,
        'implementation': 6
    };
    
    // Document Types Chart
    const documentTypesCtx = document.getElementById('documentTypesChart').getContext('2d');
    new Chart(documentTypesCtx, {
        type: 'pie',
        data: {
            labels: Object.keys(documentTypes),
            datasets: [{
                data: Object.values(documentTypes),
                backgroundColor: [
                    'rgba(255, 99, 132, 0.7)',
                    'rgba(54, 162, 235, 0.7)',
                    'rgba(255, 206, 86, 0.7)',
                    'rgba(75, 192, 192, 0.7)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                },
                title: {
                    display: true,
                    text: 'Document Type Distribution'
                }
            }
        }
    });
    
    // Readability Chart
    const readabilityCtx = document.getElementById('readabilityChart').getContext('2d');
    new Chart(readabilityCtx, {
        type: 'doughnut',
        data: {
            labels: Object.keys(readabilityScores),
            datasets: [{
                data: Object.values(readabilityScores),
                backgroundColor: [
                    'rgba(75, 192, 192, 0.7)',
                    'rgba(255, 206, 86, 0.7)',
                    'rgba(255, 99, 132, 0.7)'
                ],
                borderColor: [
                    'rgba(75, 192, 192, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(255, 99, 132, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                },
                title: {
                    display: true,
                    text: 'Document Readability Distribution'
                }
            }
        }
    });
    
    // Keywords Chart
    const keywordsCtx = document.getElementById('keywordsChart').getContext('2d');
    new Chart(keywordsCtx, {
        type: 'bar',
        data: {
            labels: Object.keys(commonKeywords),
            datasets: [{
                label: 'Frequency',
                data: Object.values(commonKeywords),
                backgroundColor: 'rgba(54, 162, 235, 0.7)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Frequency'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Keyword'
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: 'Most Common Keywords Across Documents'
                }
            }
        }
    });
});
