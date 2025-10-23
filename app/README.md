# Uber Ride Analytics - Flask Application

Aplicación web para predecir el estado de reservas de Uber utilizando Machine Learning.

## Características

- 🎯 **Predicción Individual**: Formulario interactivo para predecir el estado de un viaje
- 📊 **Predicción por Lotes**: Carga archivos CSV para procesar múltiples predicciones
- 📈 **Visualización**: Gráficos de importancia de características
- 💾 **Historial**: Almacenamiento de todas las predicciones en base de datos SQLite
- 🐳 **Docker**: Soporte completo para contenedores

## Instalación Local

### Requisitos
- Python 3.11+
- pip

### Pasos

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Ejecutar la aplicación:
```bash
python app.py
```

3. Abrir en el navegador:
```
http://localhost:5000
```

## Instalación con Docker

### Requisitos
- Docker
- Docker Compose

### Pasos

1. Construir y ejecutar:
```bash
docker-compose up --build
```

2. Abrir en el navegador:
```
http://localhost:5000
```

## Uso

### Predicción Individual

1. Completa el formulario con los datos del viaje:
   - Fecha y hora
   - Tipo de vehículo
   - Ubicaciones de origen y destino
   - Métricas del viaje (VTAT, CTAT, distancia, etc.)
   - Calificaciones
   - Método de pago

2. Haz clic en "Predecir Estado"

3. Visualiza el resultado y las probabilidades

### Predicción por Lotes

1. Prepara un archivo CSV con las siguientes columnas:
   - date, time, vehicle_type, pickup_location, drop_location
   - avg_vtat, avg_ctat, booking_value, ride_distance
   - driver_ratings, customer_rating, payment_method
   - day, month

2. Sube el archivo usando el formulario

3. Descarga el archivo con las predicciones

### Historial

- Accede a `/history` para ver todas las predicciones realizadas
- Incluye detalles de entrada y probabilidades

## Estructura del Proyecto

```
app/
├── app.py                 # Aplicación Flask principal
├── database.py            # Gestión de base de datos
├── requirements.txt       # Dependencias Python
├── Dockerfile            # Configuración Docker
├── docker-compose.yml    # Orquestación Docker
├── templates/            # Plantillas HTML
│   ├── index.html
│   └── history.html
├── static/              # Archivos estáticos
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
├── models/              # Modelos ML (enlace simbólico)
├── uploads/             # Archivos subidos
└── predictions.db       # Base de datos SQLite
```

## API Endpoints

- `GET /` - Página principal
- `POST /predict` - Predicción individual (JSON)
- `POST /batch_predict` - Predicción por lotes (CSV)
- `GET /history` - Historial de predicciones
- `GET /feature_importance` - Importancia de características
- `GET /download_predictions` - Descargar resultados

## Tecnologías

- **Backend**: Flask, Python
- **ML**: scikit-learn, pandas, numpy
- **Frontend**: Bootstrap 5, Chart.js
- **Base de Datos**: SQLite
- **Contenedores**: Docker, Docker Compose

## Notas

- El modelo debe estar en `../models/booking_status_rf_model.joblib`
- Las predicciones se guardan automáticamente en la base de datos
- Los archivos CSV procesados se guardan en `uploads/`

## Autor

Dylan Elizondo Alvarado
