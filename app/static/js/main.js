// Predicción individual
document.getElementById('predictionForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        date: document.getElementById('date').value,
        time: document.getElementById('time').value,
        vehicle_type: document.getElementById('vehicle_type').value,
        pickup_location: document.getElementById('pickup_location').value,
        drop_location: document.getElementById('drop_location').value,
        avg_vtat: document.getElementById('avg_vtat').value,
        avg_ctat: document.getElementById('avg_ctat').value,
        booking_value: document.getElementById('booking_value').value,
        ride_distance: document.getElementById('ride_distance').value,
        driver_ratings: document.getElementById('driver_ratings').value,
        customer_rating: document.getElementById('customer_rating').value,
        payment_method: document.getElementById('payment_method').value,
        day: document.getElementById('day').value,
        month: document.getElementById('month').value
    };
    
    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            displayResult(result);
        } else {
            alert('Error: ' + result.error);
        }
    } catch (error) {
        alert('Error al realizar la predicción: ' + error);
    }
});

// Predicción por lotes
document.getElementById('batchForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const fileInput = document.getElementById('csvFile');
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    
    try {
        const response = await fetch('/batch_predict', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            const downloadUrl = data.report?.download_url || `/download_predictions/${data.report?.saved_file}`;
            // mostrar enlace o forzar descarga
            const linkEl = document.getElementById('download-link');
            if (linkEl) {
                linkEl.href = downloadUrl;
                linkEl.style.display = 'inline';
                linkEl.textContent = 'Descargar predicciones';
            } else {
                // forzar descarga
                window.location = downloadUrl;
            }
        } else {
            alert('Error: ' + data.error);
        }
    } catch (error) {
        alert('Error al procesar el archivo: ' + error);
    }
});

function displayResult(result) {
    const resultCard = document.getElementById('resultCard');
    const predictionResult = document.getElementById('predictionResult');
    const probabilitiesDiv = document.getElementById('probabilities');
    
    // Mostrar predicción
    const statusClass = result.prediction === 'Completed' ? 'alert-success' : 'alert-warning';
    predictionResult.className = `alert ${statusClass}`;
    predictionResult.innerHTML = `<strong>Predicción:</strong> ${result.prediction}`;
    
    // Mostrar probabilidades
    let probHtml = '<div class="list-group">';
    for (const [status, prob] of Object.entries(result.probabilities)) {
        const percentage = (prob * 100).toFixed(2);
        probHtml += `
            <div class="list-group-item">
                <div class="d-flex justify-content-between align-items-center">
                    <span>${status}</span>
                    <span class="badge bg-primary">${percentage}%</span>
                </div>
                <div class="progress mt-2" style="height: 5px;">
                    <div class="progress-bar" style="width: ${percentage}%"></div>
                </div>
            </div>
        `;
    }
    probHtml += '</div>';
    probabilitiesDiv.innerHTML = probHtml;
    
    resultCard.style.display = 'block';
}

// Cargar gráfico de importancia de características
async function loadFeatureImportance() {
    try {
        const response = await fetch('/feature_importance');
        const data = await response.json();
        
        const ctx = document.getElementById('featureChart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.features,
                datasets: [{
                    label: 'Importancia',
                    data: data.importances,
                    backgroundColor: 'rgba(13, 110, 253, 0.5)',
                    borderColor: 'rgba(13, 110, 253, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    x: { beginAtZero: true }
                }
            }
        });
    } catch (error) {
        console.error('Error al cargar importancia de características:', error);
    }
}

// Cargar al iniciar
if (document.getElementById('featureChart')) {
    loadFeatureImportance();
}
