# 🚗 Uber Ride Analytics - Aplicación Flask

## 📋 Descripción

Aplicación web completa para predecir el estado de reservas de Uber utilizando el modelo de Machine Learning entrenado en el proyecto.

## ✨ Características Principales

### 1. Predicción Individual
- Formulario interactivo con todos los campos necesarios
- Validación de datos en tiempo real
- Visualización de probabilidades para cada estado posible
- Interfaz intuitiva y responsive

### 2. Predicción por Lotes
- Carga de archivos CSV con múltiples viajes
- Procesamiento automático de todas las filas
- Descarga de resultados con predicciones incluidas
- Archivo de ejemplo incluido: `example_batch.csv`

### 3. Historial de Predicciones
- Almacenamiento automático en base de datos SQLite
- Visualización de todas las predicciones realizadas
- Filtrado y búsqueda de predicciones anteriores
- Exportación de datos históricos

### 4. Visualizaciones
- Gráfico de importancia de características
- Distribución de probabilidades
- Estadísticas de uso

### 5. Dockerización
- Dockerfile optimizado
- Docker Compose para fácil despliegue
- Volúmenes persistentes para datos

## 🚀 Instalación y Uso

### Opción 1: Instalación Local (Recomendada para desarrollo)

#### Windows:
```bash
# Simplemente ejecuta el script de inicio
start.bat
```

#### Linux/Mac:
```bash
# Dale permisos de ejecución
chmod +x start.sh

# Ejecuta el script
./start.sh
```

#### Manual:
```bash
# 1. Crear entorno virtual
python -m venv venv

# 2. Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar configuración
python setup.py

# 5. Iniciar aplicación
python app.py
```

### Opción 2: Docker (Recomendada para producción)

```bash
# Construir y ejecutar
docker-compose up --build

# Ejecutar en segundo plano
docker-compose up -d

# Detener
docker-compose down
```

## 📊 Uso de la Aplicación

### Predicción Individual

1. **Accede a la página principal**: http://localhost:5000

2. **Completa el formulario** con los siguientes datos:
   - **Fecha y Hora**: Cuándo se realizará el viaje
   - **Tipo de Vehículo**: Auto, eBike, Go Sedan, Prime Sedan, Prime SUV
   - **Ubicaciones**: Origen y destino del viaje
   - **VTAT (Vehicle Trip Acceptance Time)**: Tiempo promedio de aceptación (minutos)
   - **CTAT (Customer Trip Acceptance Time)**: Tiempo promedio del viaje (minutos)
   - **Valor de Reserva**: Precio del viaje
   - **Distancia**: Kilómetros del recorrido
   - **Calificaciones**: Del conductor y del cliente (1-5)
   - **Método de Pago**: Cash, Credit Card, Debit Card, UPI, Wallet
   - **Día y Mes**: Del viaje

3. **Haz clic en "Predecir Estado"**

4. **Visualiza los resultados**:
   - Estado predicho (Completed, Cancelled by Driver, etc.)
   - Probabilidades para cada estado posible
   - Gráfico de barras con las probabilidades

### Predicción por Lotes

1. **Prepara tu archivo CSV** con las columnas necesarias (ver `example_batch.csv`)

2. **Formato del CSV**:
```csv
date,time,vehicle_type,pickup_location,drop_location,avg_vtat,avg_ctat,booking_value,ride_distance,driver_ratings,customer_rating,payment_method,day,month
2024-01-15,14:30,Auto,Connaught Place,Dwarka,5.2,25.5,350.00,12.5,4.8,4.7,UPI,Monday,January
```

3. **Sube el archivo** usando el formulario de "Predicción por Lotes"

4. **Descarga los resultados** con la columna de predicción agregada

### Historial

1. **Accede a**: http://localhost:5000/history

2. **Visualiza todas las predicciones** realizadas con:
   - ID único
   - Fecha y hora de la predicción
   - Datos de entrada
   - Resultado predicho
   - Probabilidad del resultado

## 📁 Estructura del Proyecto

```
app/
├── app.py                      # Aplicación Flask principal
├── database.py                 # Gestión de base de datos SQLite
├── setup.py                    # Script de configuración inicial
├── requirements.txt            # Dependencias Python
├── Dockerfile                  # Configuración Docker
├── docker-compose.yml          # Orquestación Docker
├── .dockerignore              # Archivos ignorados por Docker
├── .gitignore                 # Archivos ignorados por Git
├── .env.example               # Ejemplo de variables de entorno
├── start.bat                  # Script de inicio Windows
├── start.sh                   # Script de inicio Linux/Mac
├── example_batch.csv          # Ejemplo de CSV para lotes
├── README.md                  # Documentación en inglés
├── INSTRUCCIONES.md           # Este archivo
│
├── templates/                 # Plantillas HTML
│   ├── index.html            # Página principal
│   └── history.html          # Página de historial
│
├── static/                    # Archivos estáticos
│   ├── css/
│   │   └── style.css         # Estilos personalizados
│   └── js/
│       └── main.js           # JavaScript principal
│
├── models/                    # Modelos ML (enlace a ../models)
│   └── booking_status_rf_model.joblib
│
├── uploads/                   # Archivos CSV subidos
│   └── .gitkeep
│
└── predictions.db            # Base de datos SQLite (se crea automáticamente)
```

## 🔧 Configuración Avanzada

### Variables de Entorno

Copia `.env.example` a `.env` y ajusta los valores:

```bash
cp .env.example .env
```

### Personalización

#### Cambiar Puerto
En `app.py`, línea final:
```python
app.run(debug=True, host='0.0.0.0', port=5000)  # Cambia 5000 por tu puerto
```

#### Cambiar Límite de Archivo
En `app.py`:
```python
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
```

#### Agregar Nuevas Ubicaciones
En `app.py`, modifica la lista `LOCATIONS`:
```python
LOCATIONS = ['Connaught Place', 'Dwarka', 'Tu Nueva Ubicación']
```

## 🐛 Solución de Problemas

### Error: "No se encuentra el modelo"
**Solución**: Asegúrate de haber ejecutado el notebook `002_Uber2024-Models.ipynb` y que el archivo `booking_status_rf_model.joblib` existe en `../models/`

### Error: "ModuleNotFoundError"
**Solución**: Instala las dependencias:
```bash
pip install -r requirements.txt
```

### Error: "Puerto 5000 en uso"
**Solución**: Cambia el puerto en `app.py` o detén el proceso que usa el puerto 5000

### Error al subir CSV
**Solución**: Verifica que el CSV tenga todas las columnas necesarias y el formato correcto

## 📊 API Endpoints

Si quieres integrar la aplicación con otros sistemas:

### POST /predict
Predicción individual (JSON)
```json
{
  "date": "2024-01-15",
  "time": "14:30",
  "vehicle_type": "Auto",
  ...
}
```

### POST /batch_predict
Predicción por lotes (multipart/form-data con archivo CSV)

### GET /feature_importance
Obtiene la importancia de características (JSON)

### GET /history
Página HTML con historial

### GET /download_predictions
Descarga el último archivo de predicciones procesado

## 🎨 Personalización de la Interfaz

### Cambiar Colores
Edita `static/css/style.css`:
```css
.btn-primary {
    background-color: #tu-color;
}
```

### Agregar Logo
Coloca tu logo en `static/` y actualiza `templates/index.html`

## 🔒 Seguridad

Para producción, considera:

1. **Cambiar SECRET_KEY** en `.env`
2. **Desactivar DEBUG** en `app.py`
3. **Usar HTTPS** con certificado SSL
4. **Limitar tamaño de archivos** subidos
5. **Validar entrada de usuarios**
6. **Usar base de datos más robusta** (PostgreSQL)

## 📈 Mejoras Futuras

- [ ] Autenticación de usuarios
- [ ] API REST completa
- [ ] Exportación a Excel
- [ ] Gráficos más avanzados
- [ ] Comparación de predicciones
- [ ] Notificaciones por email
- [ ] Dashboard de estadísticas
- [ ] Integración con Uber API

## 🤝 Contribuciones

Este proyecto es parte del análisis de Uber Ride Analytics. Para contribuir:

1. Fork el repositorio
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📝 Licencia

MIT License - Ver archivo LICENSE para más detalles

## 👨‍💻 Autor

**Dylan Elizondo Alvarado**
- Email: dylalva1933@gmail.com
- GitHub: github.com/Dylalva

## 🙏 Agradecimientos

- Dataset: Uber Ride Analytics 2024
- Framework: Flask
- ML: scikit-learn
- UI: Bootstrap 5

---

**¿Necesitas ayuda?** Abre un issue en GitHub o contacta al autor.

**¡Disfruta prediciendo viajes de Uber! 🚗💨**
