from flask import Flask, render_template, request, jsonify, send_file
import os
import joblib
import pandas as pd
import numpy as np
import sqlite3
import json
from datetime import datetime
from database import Database

# === added: create Flask app and upload folder early ===
app = Flask(__name__, static_folder='static', template_folder='templates')
app.config.setdefault('UPLOAD_FOLDER', os.path.join(os.getcwd(), 'uploads'))

import preprocessing  # Asegúrate de que preprocessing.py esté en el mismo directorio o en el path

# Hacer que RidePreprocessor exista en el namespace principal (__main__) para que
# pickle/joblib la encuentre si el modelo fue serializado bajo __main__
try:
    RidePreprocessor = preprocessing.RidePreprocessor
    TimeFeatures = preprocessing.TimeFeatures
    RareCategoryGrouper = preprocessing.RareCategoryGrouper
except AttributeError:
    raise ImportError("No se encontró la clase RidePreprocessor en preprocessing.py")

# Cargar el modelo
MODEL_PATH = os.path.join('models', 'booking_status_rf_model.joblib')
model = joblib.load(MODEL_PATH)

# Inicializar base de datos
db = Database()

# Categorías para los selectores
VEHICLE_TYPES = ['Auto', 'eBike', 'Go Sedan', 'Prime Sedan', 'Prime SUV']
LOCATIONS = ['Connaught Place', 'Dwarka', 'Gurgaon Sector 56', 'Jhilmil', 'Khandsa', 
             'Malviya Nagar', 'Palam Vihar', 'Shastri Nagar']
PAYMENT_METHODS = ['Cash', 'Credit Card', 'Debit Card', 'UPI', 'Wallet']
DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 
          'July', 'August', 'September', 'October', 'November', 'December']

# --- added: helper para crear features que espera el pipeline ---
def prepare_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # asegurar tipos
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df['day_of_week'] = df['date'].dt.day_name()
        df['is_weekend'] = (df['date'].dt.dayofweek >= 5).astype(int)
        df['month'] = df['date'].dt.month
    if 'time' in df.columns:
        # intento 1: formato HH:MM (rápido y consistente)
        df['time'] = pd.to_datetime(df['time'], format='%H:%M', errors='coerce')
        # si todo salió NaT, intentar inferencia (fallback)
        if df['time'].isna().all():
            df['time'] = pd.to_datetime(df['time'].astype(str), errors='coerce')
        df['hour'] = df['time'].dt.hour.fillna(0).astype(int)
    if 'day' not in df.columns and 'day_of_week' in df.columns:
        df['day'] = df['day_of_week']

    # --- added: garantizar columnas que el pipeline espera (rellenar con NaN/0) ---
    expected_cols = [
        'avg_vtat', 'avg_ctat', 'booking_value', 'ride_distance',
        'driver_ratings', 'customer_rating',
        'month', 'day_of_week', 'is_weekend', 'hour'
    ]
    for c in expected_cols:
        if c not in df.columns:
            df[c] = np.nan

    return df

# helper: persist batch to DB (tries Database API, else sqlite fallback)
def _save_batch_results(df_results: pd.DataFrame, filename: str, report: dict):
    """Guarda predicciones en detailed_predictions solamente."""
    try:
        db_path = os.path.join(os.getcwd(), "predictions.db")
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        # Crear tabla si no existe
        table_name = "detailed_predictions"
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT,
                created_at TEXT
            )
        """)

        # Añadir columnas faltantes
        cur.execute(f"PRAGMA table_info({table_name})")
        existing_cols = {row[1] for row in cur.fetchall()}
        
        for col in df_results.columns:
            safe_col = col.replace(" ", "_").replace("-", "_")
            if safe_col not in existing_cols:
                cur.execute(f'ALTER TABLE {table_name} ADD COLUMN "{safe_col}" TEXT')

        # Insertar registros
        now = datetime.utcnow().isoformat()
        cols = [c.replace(" ", "_").replace("-", "_") for c in df_results.columns]
        placeholders = ", ".join(["?"] * (2 + len(cols)))
        col_quoted = ", ".join([f'"{c}"' for c in cols])
        
        insert_sql = f'INSERT INTO {table_name} (filename, created_at, {col_quoted}) VALUES ({placeholders})'
        
        rows = []
        for _, r in df_results.iterrows():
            vals = [filename, now] + [str(r.get(c, "")) for c in df_results.columns]
            rows.append(vals)
        
        cur.executemany(insert_sql, rows)
        conn.commit()
        print(f"Saved {len(rows)} predictions to database")
        
        return True

    except Exception as e:
        print(f"Error saving to database: {e}")
        return False

@app.route('/')
def index():
    return render_template('index.html', 
                         vehicle_types=VEHICLE_TYPES,
                         locations=LOCATIONS,
                         payment_methods=PAYMENT_METHODS,
                         days=DAYS,
                         months=MONTHS)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        # Crear DataFrame con los datos
        df = pd.DataFrame([{
            'date': pd.to_datetime(data['date']),
            'time': pd.to_datetime(data['time'], format='%H:%M'),
            'vehicle_type': data['vehicle_type'],
            'pickup_location': data['pickup_location'],
            'drop_location': data['drop_location'],
            'avg_vtat': float(data['avg_vtat']),
            'avg_ctat': float(data['avg_ctat']),
            'booking_value': float(data['booking_value']),
            'ride_distance': float(data['ride_distance']),
            'driver_ratings': float(data['driver_ratings']),
            'customer_rating': float(data['customer_rating']),
            'payment_method': data['payment_method'],
            'day': data.get('day', None),
            'month': data.get('month', None)
        }])
        
        # preparar features requeridas por el pipeline
        df = prepare_features(df)
        
        # Realizar predicción
        prediction = model.predict(df)[0]
        probabilities = model.predict_proba(df)[0]
        
        # Obtener las clases
        classes = model.named_steps['model'].classes_
        prob_dict = {cls: float(prob) for cls, prob in zip(classes, probabilities)}
        
        # Guardar en base de datos
        db.save_prediction(data, prediction, prob_dict)
        
        return jsonify({
            'success': True,
            'prediction': prediction,
            'probabilities': prob_dict
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/batch_predict', methods=['POST'])
def batch_predict():
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file uploaded'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400

        # Leer CSV y preparar datos
        df = pd.read_csv(file)
        df_prepared = prepare_features(df.copy())

        # Realizar predicciones
        preds = model.predict(df_prepared)
        probs = model.predict_proba(df_prepared)
        classes = list(model.named_steps['model'].classes_)

        # Guardar cada predicción usando el mismo método que predicciones individuales
        for idx, row in df.iterrows():
            data = row.to_dict()
            prediction = preds[idx]
            probabilities = {cls: float(prob) for cls, prob in zip(classes, probs[idx])}
            
            # Usar el mismo método de guardado que predict()
            db.save_prediction(data, prediction, probabilities)

        # Generar reporte y CSV de resultados
        results = df.copy()
        results['prediction'] = preds
        for i, cls in enumerate(classes):
            results[f"prob_{cls}"] = probs[:, i]

        # Guardar CSV en uploads
        timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        out_filename = f"predictions_{timestamp}.csv"
        uploads_dir = app.config.get('UPLOAD_FOLDER', os.path.join(os.getcwd(), 'uploads'))
        os.makedirs(uploads_dir, exist_ok=True)
        out_path = os.path.join(uploads_dir, out_filename)
        results.to_csv(out_path, index=False)

        # Preparar reporte
        report = {
            "total": len(results),
            "counts": results['prediction'].value_counts().to_dict(),
            "mean_probability_by_class": {
                str(c): float(results[f"prob_{c}"].mean()) 
                for c in classes
            },
            "saved_file": out_filename,
            "saved_at": datetime.utcnow().isoformat(),
            "download_url": f"/download_predictions/{out_filename}"
        }

        return jsonify({'success': True, 'report': report}), 200

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# reemplazar/añadir endpoint para descargar archivo por nombre
@app.route('/download_predictions/<filename>')
def download_predictions(filename):
    uploads_dir = app.config.get('UPLOAD_FOLDER', os.path.join(os.getcwd(), 'uploads'))
    path = os.path.join(uploads_dir, filename)
    if not os.path.exists(path):
        return jsonify({'error': 'file not found'}), 404
    return send_file(path, as_attachment=True)

@app.route('/history')
def history():
    predictions = []
    try:
        # 1) intenta usar Database wrapper (probablemente falla o retorna vacío)
        if 'db' in globals() and db is not None and hasattr(db, 'get_all_predictions'):
            try:
                predictions = db.get_all_predictions() or []
            except Exception as e:
                print("db.get_all_predictions() failed:", e)
                predictions = []

        # 2) fallback sqlite (probablemente no encuentra la tabla o está vacía)
        if not predictions:
            db_path = os.path.join(os.getcwd(), "predictions.db")
            if os.path.exists(db_path):
                conn = sqlite3.connect(db_path)
                conn.row_factory = sqlite3.Row
                cur = conn.cursor()
                cur.execute("SELECT * FROM detailed_predictions ORDER BY id DESC LIMIT 500")
                rows = cur.fetchall()
                for r in rows:
                    d = {k: (v if v is not None else "") for k, v in dict(r).items()}
                    predictions.append(d)
                conn.close()
    except Exception as e:
        print("Error loading history:", e)

    return render_template('history.html', predictions=predictions)

@app.route('/feature_importance')
def feature_importance():
    # Obtener importancia de características
    feature_names = model.named_steps['prep'].get_feature_names()
    importances = model.named_steps['model'].feature_importances_
    
    # Ordenar por importancia
    indices = np.argsort(importances)[::-1][:15]
    
    data = {
        'features': [feature_names[i] for i in indices],
        'importances': [float(importances[i]) for i in indices]
    }
    
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
