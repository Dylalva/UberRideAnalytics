# 🚀 Inicio Rápido - Uber Ride Analytics App

## ⚡ 3 Pasos para Empezar

### 1️⃣ Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 2️⃣ Configurar
```bash
python setup.py
```

### 3️⃣ Ejecutar
```bash
python app.py
```

**¡Listo!** Abre http://localhost:5000 en tu navegador

---

## 🐳 Con Docker (Aún más fácil)

```bash
docker-compose up --build
```

---

## 📝 Ejemplo de Uso

### Predicción Individual:
1. Ve a http://localhost:5000
2. Completa el formulario
3. Haz clic en "Predecir Estado"
4. ¡Ve el resultado!

### Predicción por Lotes:
1. Usa `example_batch.csv` como plantilla
2. Sube tu CSV
3. Descarga los resultados

---

## 🆘 ¿Problemas?

**Error: No se encuentra el modelo**
→ Ejecuta primero el notebook `002_Uber2024-Models.ipynb`

**Error: ModuleNotFoundError**
→ `pip install -r requirements.txt`

**Puerto 5000 ocupado**
→ Cambia el puerto en `app.py` línea 95

---

## 📚 Más Información

- **Documentación completa**: Ver `INSTRUCCIONES.md`
- **README en inglés**: Ver `README.md`
- **Ejemplo de CSV**: Ver `example_batch.csv`

---

## 🎯 Características Principales

✅ Predicción individual con formulario interactivo
✅ Predicción por lotes con CSV
✅ Historial de predicciones en base de datos
✅ Visualización de importancia de características
✅ Interfaz responsive con Bootstrap
✅ Dockerizado y listo para producción

---

**¡Empieza a predecir viajes de Uber ahora! 🚗**
