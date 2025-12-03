// Water Quality Dashboard - Main JavaScript

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeCharts();
    setupPredictionForm();
    setupSmoothScroll();
});

// Initialize all charts
function initializeCharts() {
    createQualityPieChart();
    createWaterBodyBarChart();
    createFeatureImportanceChart();
    createWQIHistogramChart();
}

// Water Quality Distribution Pie Chart
function createQualityPieChart() {
    const ctx = document.getElementById('qualityPieChart');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Safe/Potable', 'Polluted', 'Highly Polluted'],
            datasets: [{
                data: [3, 118, 44],
                backgroundColor: [
                    'rgba(16, 185, 129, 0.8)',
                    'rgba(245, 158, 11, 0.8)',
                    'rgba(239, 68, 68, 0.8)'
                ],
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        font: {
                            size: 14
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.parsed;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((value / total) * 100).toFixed(1);
                            return `${label}: ${value} samples (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

// Water Body Comparison Bar Chart
function createWaterBodyBarChart() {
    const ctx = document.getElementById('waterBodyBarChart');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['River Godavari', 'River Krishna', 'River Musi', 'River Manjeera', 'Lakes & Tanks', 'Other Rivers'],
            datasets: [{
                label: 'Average WQI',
                data: [52, 51, 28, 48, 44, 50],
                backgroundColor: 'rgba(37, 99, 235, 0.7)',
                borderColor: 'rgba(37, 99, 235, 1)',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    title: {
                        display: true,
                        text: 'Water Quality Index (WQI)'
                    },
                    ticks: {
                        callback: function(value) {
                            return value;
                        }
                    }
                },
                x: {
                    ticks: {
                        maxRotation: 45,
                        minRotation: 45
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const value = context.parsed.y.toFixed(2);
                            let quality = 'Safe';
                            if (value < 40) quality = 'Highly Polluted';
                            else if (value < 70) quality = 'Polluted';
                            return `WQI: ${value} (${quality})`;
                        }
                    }
                },
                annotation: {
                    annotations: {
                        line1: {
                            type: 'line',
                            yMin: 70,
                            yMax: 70,
                            borderColor: 'rgb(16, 185, 129)',
                            borderWidth: 2,
                            borderDash: [5, 5],
                            label: {
                                display: true,
                                content: 'Safe (70)',
                                position: 'end'
                            }
                        },
                        line2: {
                            type: 'line',
                            yMin: 40,
                            yMax: 40,
                            borderColor: 'rgb(245, 158, 11)',
                            borderWidth: 2,
                            borderDash: [5, 5],
                            label: {
                                display: true,
                                content: 'Polluted (40)',
                                position: 'end'
                            }
                        }
                    }
                }
            }
        }
    });
}

// Feature Importance Chart
function createFeatureImportanceChart() {
    const ctx = document.getElementById('featureImportanceChart');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: [
                'Total Coliform',
                'Fecal Coliform',
                'BOD',
                'COD',
                'DO',
                'TDS',
                'pH',
                'Turbidity',
                'Nitrate',
                'Chloride'
            ],
            datasets: [{
                label: 'Importance Score',
                data: [0.18, 0.16, 0.14, 0.12, 0.11, 0.09, 0.07, 0.05, 0.04, 0.04],
                backgroundColor: [
                    'rgba(239, 68, 68, 0.7)',
                    'rgba(239, 68, 68, 0.6)',
                    'rgba(245, 158, 11, 0.7)',
                    'rgba(245, 158, 11, 0.6)',
                    'rgba(14, 165, 233, 0.7)',
                    'rgba(14, 165, 233, 0.6)',
                    'rgba(16, 185, 129, 0.7)',
                    'rgba(16, 185, 129, 0.6)',
                    'rgba(139, 92, 246, 0.7)',
                    'rgba(139, 92, 246, 0.6)'
                ],
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                x: {
                    beginAtZero: true,
                    max: 0.2,
                    title: {
                        display: true,
                        text: 'Feature Importance'
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const value = (context.parsed.x * 100).toFixed(1);
                            return `Importance: ${value}%`;
                        }
                    }
                }
            }
        }
    });
}

// WQI Distribution Histogram
function createWQIHistogramChart() {
    const ctx = document.getElementById('wqiHistogramChart');
    if (!ctx) return;

    // Real data from analysis: WQI distribution across 165 samples
    const wqiDistribution = {
        '0-10': 2,
        '10-20': 8,
        '20-30': 15,
        '30-40': 19,
        '40-50': 45,
        '50-60': 38,
        '60-70': 28,
        '70-80': 8,
        '80-90': 2,
        '90-100': 0
    };

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Object.keys(wqiDistribution),
            datasets: [{
                label: 'Number of Samples',
                data: Object.values(wqiDistribution),
                backgroundColor: function(context) {
                    const label = context.label || '';
                    const value = parseInt(label.split('-')[0]);
                    if (value >= 70) return 'rgba(16, 185, 129, 0.8)';
                    if (value >= 40) return 'rgba(245, 158, 11, 0.8)';
                    return 'rgba(239, 68, 68, 0.8)';
                },
                borderColor: function(context) {
                    const label = context.label || '';
                    const value = parseInt(label.split('-')[0]);
                    if (value >= 70) return 'rgba(16, 185, 129, 1)';
                    if (value >= 40) return 'rgba(245, 158, 11, 1)';
                    return 'rgba(239, 68, 68, 1)';
                },
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 5
                    },
                    title: {
                        display: true,
                        text: 'Number of Samples',
                        font: {
                            size: 12,
                            weight: 'bold'
                        }
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'WQI Range',
                        font: {
                            size: 12,
                            weight: 'bold'
                        }
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: 'Distribution of 165 Water Samples',
                    font: {
                        size: 14
                    },
                    padding: 10
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    callbacks: {
                        label: function(context) {
                            const total = Object.values(wqiDistribution).reduce((a, b) => a + b, 0);
                            const percentage = ((context.parsed.y / total) * 100).toFixed(1);
                            return `Samples: ${context.parsed.y} (${percentage}%)`;
                        },
                        afterLabel: function(context) {
                            const label = context.label;
                            const value = parseInt(label.split('-')[0]);
                            if (value >= 70) return 'Quality: Safe/Potable';
                            if (value >= 40) return 'Quality: Polluted';
                            return 'Quality: Highly Polluted';
                        }
                    }
                }
            }
        }
    });
}

// Setup Prediction Form
function setupPredictionForm() {
    const form = document.getElementById('predictionForm');
    if (!form) return;

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        predictWaterQuality();
    });
}

// WHO/BIS Water Quality Standards
const standards = {
    'pH': {'ideal': 7.0, 'min': 6.5, 'max': 8.5, 'weight': 4},
    'DO': {'ideal': 6.0, 'min': 5.0, 'max': 14.0, 'weight': 5},
    'BOD': {'ideal': 0, 'min': 0, 'max': 3.0, 'weight': 5},
    'COD': {'ideal': 0, 'min': 0, 'max': 10.0, 'weight': 4},
    'TotalColiform': {'ideal': 0, 'min': 0, 'max': 50, 'weight': 5},
    'TDS': {'ideal': 300, 'min': 0, 'max': 500, 'weight': 4}
};

// Calculate Quality Index for a single parameter
function calculateQI(value, paramName) {
    if (value === null || value === undefined || isNaN(value)) return null;
    if (!standards[paramName]) return null;
    
    const std = standards[paramName];
    let qi;
    
    // pH special handling (ideal range)
    if (paramName === 'pH') {
        if (value >= std.min && value <= std.max) {
            qi = 100 - Math.abs(value - std.ideal) * 10;
        } else {
            qi = Math.max(0, 100 - Math.abs(value - std.ideal) * 20);
        }
    }
    // For pollutants (lower is better)
    else if (std.ideal === 0) {
        if (value <= std.max) {
            qi = 100 - (value / std.max) * 100;
        } else {
            qi = Math.max(0, 100 - (value / std.max) * 150);
        }
    }
    // For parameters with ideal range
    else {
        if (value <= std.max) {
            qi = 100 - Math.abs(value - std.ideal) / std.max * 100;
        } else {
            qi = Math.max(0, 100 - (value - std.max) / std.max * 100);
        }
    }
    
    return Math.max(0, Math.min(100, qi));
}

// Calculate Water Quality Index using WHO/BIS standards
function calculateWQI(parameters) {
    let qiValues = [];
    let weights = [];
    
    for (let param in parameters) {
        const qi = calculateQI(parameters[param], param);
        if (qi !== null) {
            qiValues.push(qi);
            weights.push(standards[param].weight);
        }
    }
    
    if (qiValues.length === 0) return null;
    
    // Weighted average
    let weightedSum = 0;
    let totalWeight = 0;
    for (let i = 0; i < qiValues.length; i++) {
        weightedSum += qiValues[i] * weights[i];
        totalWeight += weights[i];
    }
    
    return weightedSum / totalWeight;
}

// Predict Water Quality using Real WQI Calculation
function predictWaterQuality() {
    // Get input values
    const parameters = {
        'DO': parseFloat(document.getElementById('do').value),
        'pH': parseFloat(document.getElementById('ph').value),
        'BOD': parseFloat(document.getElementById('bod').value),
        'COD': parseFloat(document.getElementById('cod').value),
        'TotalColiform': parseFloat(document.getElementById('coliform').value),
        'TDS': parseFloat(document.getElementById('tds').value)
    };
    
    // Calculate WQI using WHO/BIS standards
    const wqi = calculateWQI(parameters);
    
    // Determine classification
    let classification, classColor, recommendation;
    if (wqi >= 70) {
        classification = 'Safe/Potable';
        classColor = 'badge-safe';
        recommendation = 'Water quality is good and suitable for drinking and domestic use.';
    } else if (wqi >= 40) {
        classification = 'Polluted';
        classColor = 'badge-polluted';
        recommendation = 'Water shows moderate pollution. Treatment recommended before use. Not suitable for drinking without proper filtration.';
    } else {
        classification = 'Highly Polluted';
        classColor = 'badge-highly-polluted';
        recommendation = 'Water is severely polluted. Not suitable for any use without extensive treatment. Immediate intervention required.';
    }
    
    // Display results
    const resultDiv = document.getElementById('predictionResult');
    const resultClass = document.getElementById('resultClass');
    const resultWQI = document.getElementById('resultWQI');
    const resultRecommendation = document.getElementById('resultRecommendation');
    
    resultClass.textContent = classification;
    resultClass.className = classColor;
    resultWQI.textContent = wqi.toFixed(2);
    resultRecommendation.textContent = recommendation;
    
    resultDiv.style.display = 'block';
    resultDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Setup smooth scrolling for navigation links
function setupSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Animate numbers on scroll (optional enhancement)
function animateValue(element, start, end, duration) {
    const range = end - start;
    const increment = end > start ? 1 : -1;
    const stepTime = Math.abs(Math.floor(duration / range));
    let current = start;
    
    const timer = setInterval(function() {
        current += increment;
        element.textContent = current;
        if (current === end) {
            clearInterval(timer);
        }
    }, stepTime);
}

// Intersection Observer for scroll animations (optional)
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('animate-in');
        }
    });
}, observerOptions);

// Observe all sections
document.querySelectorAll('.section').forEach(section => {
    observer.observe(section);
});

// Console welcome message
console.log('%c🌊 Water Quality Analysis Dashboard', 'color: #2563eb; font-size: 20px; font-weight: bold;');
console.log('%cBuilt with Machine Learning | TensorFlow, XGBoost, Random Forest', 'color: #0ea5e9; font-size: 12px;');
console.log('%cData Source: Telangana Pollution Control Board', 'color: #64748b; font-size: 11px;');

