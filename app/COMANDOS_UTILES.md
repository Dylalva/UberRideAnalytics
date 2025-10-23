# 🛠️ Comandos Útiles - Uber Ride Analytics

## 🚀 Inicio Rápido

### Instalación y Ejecución
```bash
# Instalar dependencias
pip install -r requirements.txt

# Configurar aplicación
python setup.py

# Ejecutar aplicación
python app.py
```

---

## 🐳 Docker

### Comandos Básicos
```bash
# Construir y ejecutar
docker-compose up --build

# Ejecutar en segundo plano
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener
docker-compose down

# Detener y eliminar volúmenes
docker-compose down -v

# Reconstruir sin caché
docker-compose build --no-cache
```

### Comandos Avanzados
```bash
# Entrar al contenedor
docker-compose exec web bash

# Ver contenedores activos
docker ps

# Ver imágenes
docker images

# Limpiar todo
docker system prune -a
```

---

## 📦 Entorno Virtual

### Crear y Activar
```bash
# Crear entorno virtual
python -m venv venv

# Activar (Windows)
venv\Scripts\activate

# Activar (Linux/Mac)
source venv/bin/activate

# Desactivar
deactivate
```

### Gestión de Dependencias
```bash
# Instalar dependencias
pip install -r requirements.txt

# Actualizar pip
python -m pip install --upgrade pip

# Congelar dependencias actuales
pip freeze > requirements.txt

# Instalar paquete específico
pip install nombre-paquete==version
```

---

## 🗄️ Base de Datos

### SQLite
```bash
# Abrir base de datos
sqlite3 predictions.db

# Ver tablas
.tables

# Ver esquema
.schema predictions

# Consultar datos
SELECT * FROM predictions LIMIT 10;

# Exportar a CSV
.mode csv
.output predictions_export.csv
SELECT * FROM predictions;
.quit
```

### Limpiar Base de Datos
```bash
# Eliminar base de datos
rm predictions.db  # Linux/Mac
del predictions.db  # Windows

# La aplicación creará una nueva automáticamente
```

---

## 📊 Jupyter Notebooks

### Comandos
```bash
# Iniciar Jupyter
jupyter notebook

# Iniciar en puerto específico
jupyter notebook --port 8889

# Listar notebooks en ejecución
jupyter notebook list

# Detener servidor
jupyter notebook stop 8888
```

### Convertir Notebooks
```bash
# A HTML
jupyter nbconvert --to html notebook.ipynb

# A Python
jupyter nbconvert --to python notebook.ipynb

# A PDF (requiere LaTeX)
jupyter nbconvert --to pdf notebook.ipynb
```

---

## 🧪 Testing

### Pytest
```bash
# Instalar pytest
pip install pytest

# Ejecutar tests
pytest

# Con cobertura
pip install pytest-cov
pytest --cov=app tests/

# Verbose
pytest -v

# Test específico
pytest tests/test_app.py::test_predict
```

---

## 📝 Git

### Comandos Básicos
```bash
# Inicializar repositorio
git init

# Agregar archivos
git add .

# Commit
git commit -m "Mensaje descriptivo"

# Ver estado
git status

# Ver historial
git log --oneline

# Crear rama
git checkout -b feature/nueva-funcionalidad

# Cambiar de rama
git checkout main

# Merge
git merge feature/nueva-funcionalidad
```

### GitHub
```bash
# Agregar remoto
git remote add origin https://github.com/usuario/repo.git

# Push
git push -u origin main

# Pull
git pull origin main

# Clonar
git clone https://github.com/usuario/repo.git
```

---

## 🔍 Debugging

### Flask Debug Mode
```bash
# Activar debug en app.py
export FLASK_DEBUG=1  # Linux/Mac
set FLASK_DEBUG=1     # Windows

python app.py
```

### Ver Logs
```bash
# Logs de Flask
python app.py > app.log 2>&1

# Ver logs en tiempo real
tail -f app.log  # Linux/Mac
Get-Content app.log -Wait  # PowerShell
```

---

## 📦 Gestión de Archivos

### Limpiar Archivos Temporales
```bash
# Python cache
find . -type d -name __pycache__ -exec rm -r {} +  # Linux/Mac
for /d /r . %d in (__pycache__) do @if exist "%d" rd /s /q "%d"  # Windows

# Archivos .pyc
find . -name "*.pyc" -delete  # Linux/Mac
del /s /q *.pyc  # Windows
```

### Backup
```bash
# Backup de base de datos
cp predictions.db predictions_backup_$(date +%Y%m%d).db  # Linux/Mac
copy predictions.db predictions_backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%.db  # Windows

# Backup completo
tar -czf backup.tar.gz app/  # Linux/Mac
tar -a -c -f backup.zip app/  # Windows
```

---

## 🌐 Servidor

### Desarrollo
```bash
# Flask development server
python app.py

# Con auto-reload
export FLASK_ENV=development
python app.py
```

### Producción
```bash
# Instalar gunicorn
pip install gunicorn

# Ejecutar con gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Con logs
gunicorn -w 4 -b 0.0.0.0:5000 app:app --access-logfile access.log --error-logfile error.log
```

---

## 📊 Análisis de Datos

### Pandas
```python
# En Python/Jupyter
import pandas as pd

# Leer CSV
df = pd.read_csv('data.csv')

# Info básica
df.info()
df.describe()
df.head()

# Filtrar
df[df['column'] > value]

# Agrupar
df.groupby('column').mean()
```

### Verificar Modelo
```python
import joblib

# Cargar modelo
model = joblib.load('models/booking_status_rf_model.joblib')

# Ver información
print(model)
print(model.named_steps)
print(model.named_steps['model'].feature_importances_)
```

---

## 🔧 Mantenimiento

### Actualizar Dependencias
```bash
# Ver paquetes desactualizados
pip list --outdated

# Actualizar paquete específico
pip install --upgrade nombre-paquete

# Actualizar todos (con precaución)
pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1 | xargs -n1 pip install -U
```

### Verificar Salud de la App
```bash
# Verificar que Flask está corriendo
curl http://localhost:5000

# Verificar endpoint específico
curl http://localhost:5000/feature_importance

# Con formato JSON
curl -H "Content-Type: application/json" http://localhost:5000/predict
```

---

## 📈 Monitoreo

### Recursos del Sistema
```bash
# CPU y memoria (Linux/Mac)
top
htop

# Espacio en disco
df -h

# Procesos de Python
ps aux | grep python

# Windows
tasklist | findstr python
```

### Logs de Docker
```bash
# Ver logs del contenedor
docker-compose logs web

# Seguir logs en tiempo real
docker-compose logs -f web

# Últimas 100 líneas
docker-compose logs --tail=100 web
```

---

## 🎨 Desarrollo Frontend

### Verificar Archivos Estáticos
```bash
# Listar archivos CSS/JS
ls -la static/css/
ls -la static/js/

# Ver contenido
cat static/css/style.css
cat static/js/main.js
```

---

## 🔐 Seguridad

### Generar SECRET_KEY
```python
import secrets
print(secrets.token_hex(32))
```

### Verificar Permisos
```bash
# Linux/Mac
chmod 600 .env
chmod 755 start.sh

# Ver permisos
ls -la
```

---

## 📤 Exportar/Importar

### Exportar Predicciones
```python
import sqlite3
import pandas as pd

conn = sqlite3.connect('predictions.db')
df = pd.read_sql_query("SELECT * FROM predictions", conn)
df.to_csv('export_predictions.csv', index=False)
conn.close()
```

### Importar Datos
```python
import pandas as pd

df = pd.read_csv('new_data.csv')
# Procesar y predecir...
```

---

## 🆘 Solución Rápida de Problemas

```bash
# Reinstalar todo desde cero
rm -rf venv/
python -m venv venv
source venv/bin/activate  # o venv\Scripts\activate en Windows
pip install -r requirements.txt
python setup.py
python app.py

# Limpiar Docker completamente
docker-compose down -v
docker system prune -a
docker-compose up --build

# Verificar que todo funciona
python -c "import flask, pandas, sklearn, joblib; print('OK')"
```

---

**💡 Tip**: Guarda este archivo como referencia rápida para comandos comunes.
