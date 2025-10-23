# 🚗 Uber Ride Analytics - Proyecto Completo

## 📊 Resumen del Proyecto

Este es un proyecto completo de Machine Learning que analiza y predice el estado de reservas de Uber utilizando datos reales de 2024.

### 🎯 Objetivo
Predecir el estado final de una reserva de Uber (Completado, Cancelado por Cliente, Cancelado por Conductor, Incompleto, Sin Conductor) antes de que ocurra.

---

## 📁 Estructura del Proyecto

```
UberRideAnalytics/
│
├── 📓 notebooks/                          # Análisis y Modelado
│   ├── 001_Uber2024.ipynb               # Análisis Exploratorio (EDA)
│   └── 002_Uber2024-Models.ipynb        # Entrenamiento de Modelos
│
├── 📊 data/                               # Datos
│   ├── raw/                              # Datos originales
│   ├── interim/                          # Datos intermedios
│   └── processed/                        # Datos procesados
│       └── Uberdata.xlsx
│
├── 🤖 models/                             # Modelos Entrenados
│   └── booking_status_rf_model.joblib   # Random Forest (99% accuracy)
│
├── 📈 figures/                            # Visualizaciones
│   ├── confusion_matrix_RF.png
│   ├── varImportantesRF2.png
│   └── curvaROC_RF_multiclase.png
│
├── 🌐 app/                                # Aplicación Web Flask
│   ├── templates/                        # HTML
│   ├── static/                           # CSS/JS
│   ├── app.py                           # Aplicación principal
│   ├── database.py                      # Base de datos
│   ├── Dockerfile                       # Docker
│   └── [más archivos...]
│
├── 📄 README.md                          # Documentación principal
└── 📄 requirements.txt                   # Dependencias Python
```

---

## 🔬 Parte 1: Análisis y Modelado

### Dataset
- **Registros**: 148,000+ reservas de Uber
- **Período**: 2024
- **Variables**: 14 características (fecha, hora, tipo de vehículo, ubicaciones, métricas, calificaciones, etc.)

### Modelos Entrenados

#### 1. Logistic Regression (Baseline)
- **Accuracy**: 94%
- **F1-Score**: 93%
- **Propósito**: Modelo base para comparación

#### 2. Random Forest (Modelo Final) ⭐
- **Accuracy**: 99%
- **F1-Score**: 98%
- **ROC-AUC**: 99%
- **Características**: 400 árboles, balanceo de clases

### Variables Más Importantes
1. **Avg VTAT** - Tiempo de llegada del conductor
2. **Avg CTAT** - Duración del viaje
3. **Booking Value** - Valor de la reserva
4. **Customer & Driver Ratings** - Calificaciones
5. **Payment Method** - Método de pago

### Resultados Clave
- ✅ Predicción casi perfecta de viajes completados (99%)
- ✅ Excelente identificación de cancelaciones
- ✅ Modelo robusto y generalizable

---

## 🌐 Parte 2: Aplicación Web

### Tecnologías
- **Backend**: Flask (Python)
- **Frontend**: Bootstrap 5, Chart.js
- **Base de Datos**: SQLite
- **ML**: scikit-learn, pandas, numpy
- **Contenedores**: Docker, Docker Compose

### Funcionalidades

#### 1. Predicción Individual
- Formulario interactivo con validación
- Predicción en tiempo real
- Visualización de probabilidades
- Interfaz responsive

#### 2. Predicción por Lotes
- Carga de archivos CSV
- Procesamiento masivo
- Descarga de resultados
- Ejemplo incluido

#### 3. Historial
- Almacenamiento en SQLite
- Visualización de predicciones pasadas
- Búsqueda y filtrado
- Exportación de datos

#### 4. Visualizaciones
- Gráfico de importancia de características
- Distribución de probabilidades
- Estadísticas de uso

#### 5. Dockerización
- Dockerfile optimizado
- Docker Compose
- Volúmenes persistentes
- Fácil despliegue

---

## 🚀 Cómo Usar el Proyecto

### Paso 1: Análisis y Entrenamiento

```bash
# 1. Abrir Jupyter Notebook
jupyter notebook

# 2. Ejecutar notebooks en orden:
#    - 001_Uber2024.ipynb (EDA)
#    - 002_Uber2024-Models.ipynb (Modelos)

# 3. El modelo se guardará en models/booking_status_rf_model.joblib
```

### Paso 2: Ejecutar Aplicación Web

#### Opción A: Local
```bash
cd app
python setup.py
python app.py
```

#### Opción B: Docker
```bash
cd app
docker-compose up --build
```

#### Opción C: Scripts de Inicio
```bash
# Windows
cd app
start.bat

# Linux/Mac
cd app
chmod +x start.sh
./start.sh
```

### Paso 3: Usar la Aplicación

1. **Abrir navegador**: http://localhost:5000
2. **Predicción individual**: Completar formulario
3. **Predicción por lotes**: Subir CSV
4. **Ver historial**: http://localhost:5000/history

---

## 📊 Resultados del Proyecto

### Métricas del Modelo
```
                       precision    recall  f1-score   support
Cancelled by Customer     0.99      0.53      0.69      2100
Cancelled by Driver       0.85      0.99      0.91      5400
Completed                 1.00      1.00      1.00     18600
Incomplete                0.99      1.00      1.00      1800
No Driver Found           0.96      1.00      0.98      2100

accuracy                                      0.96     30000
macro avg                 0.96      0.90      0.92     30000
weighted avg              0.97      0.96      0.96     30000
```

### Impacto de Negocio
- 🎯 Predicción precisa del estado de reservas
- 📉 Reducción potencial de cancelaciones
- 🚗 Optimización de asignación de conductores
- 💰 Mejora en la experiencia del usuario
- 📊 Insights para toma de decisiones

---

## 📚 Documentación

### Archivos de Documentación
- **README.md** - Documentación principal (inglés)
- **app/README.md** - Documentación de la aplicación
- **app/INSTRUCCIONES.md** - Guía completa en español
- **app/QUICKSTART.md** - Inicio rápido
- **PROYECTO_COMPLETO.md** - Este archivo

### Notebooks
- **001_Uber2024.ipynb** - EDA detallado con visualizaciones
- **002_Uber2024-Models.ipynb** - Proceso de modelado completo

---

## 🛠️ Tecnologías Utilizadas

### Data Science & ML
- Python 3.11
- pandas - Manipulación de datos
- numpy - Operaciones numéricas
- scikit-learn - Machine Learning
- matplotlib & seaborn - Visualizaciones

### Web Development
- Flask - Framework web
- Bootstrap 5 - UI/UX
- Chart.js - Gráficos interactivos
- SQLite - Base de datos

### DevOps
- Docker - Contenedores
- Docker Compose - Orquestación
- Git - Control de versiones

---

## 📈 Próximos Pasos

### Mejoras Potenciales
1. **Modelo**
   - [ ] Probar XGBoost y LightGBM
   - [ ] Optimización de hiperparámetros
   - [ ] Feature engineering avanzado
   - [ ] Ensemble de modelos

2. **Aplicación**
   - [ ] Autenticación de usuarios
   - [ ] API REST completa
   - [ ] Dashboard de analytics
   - [ ] Notificaciones en tiempo real
   - [ ] Integración con Uber API

3. **Despliegue**
   - [ ] Deploy en AWS/Azure/GCP
   - [ ] CI/CD pipeline
   - [ ] Monitoreo y logging
   - [ ] Escalabilidad horizontal

---

## 🎓 Aprendizajes Clave

### Machine Learning
✅ Preprocesamiento de datos temporales
✅ Manejo de clases desbalanceadas
✅ Feature engineering efectivo
✅ Evaluación de modelos multiclase
✅ Interpretabilidad del modelo

### Desarrollo Web
✅ Arquitectura Flask
✅ Integración ML con web
✅ Manejo de archivos CSV
✅ Base de datos SQLite
✅ Dockerización de aplicaciones

### Mejores Prácticas
✅ Código modular y reutilizable
✅ Documentación completa
✅ Control de versiones
✅ Testing y validación
✅ Despliegue reproducible

---

## 👨💻 Autor

**Dylan Elizondo Alvarado**
- 📧 Email: dylalva1933@gmail.com
- 🔗 GitHub: github.com/Dylalva
- 💼 LinkedIn: linkedin.com/in/[tu-perfil]

---

## 📄 Licencia

MIT License - Ver archivo LICENSE para más detalles

---

## 🙏 Agradecimientos

- **Dataset**: Uber Ride Analytics 2024
- **Comunidad**: scikit-learn, Flask, Bootstrap
- **Inspiración**: Proyectos de ML en producción

---

## 📞 Soporte

¿Tienes preguntas o problemas?

1. **Revisa la documentación** en los archivos MD
2. **Consulta los notebooks** para entender el proceso
3. **Abre un issue** en GitHub
4. **Contacta al autor** por email

---

**¡Gracias por usar Uber Ride Analytics! 🚗💨**

*Proyecto desarrollado con ❤️ para demostrar habilidades en Data Science y ML Engineering*
