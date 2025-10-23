from flask import Flask, render_template, request, jsonify, send_file
import joblib
import pandas as pd
import numpy as np
from datetime import datetime
import os
from database import Database
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

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
            'day': data['day'],
            'month': data['month']
        }])
        
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
        
        # Leer CSV
        df = pd.read_csv(file)
        
        # Convertir columnas de fecha
        df['date'] = pd.to_datetime(df['date'])
        df['time'] = pd.to_datetime(df['time'], format='%H:%M')
        
        # Realizar predicciones
        predictions = model.predict(df)
        probabilities = model.predict_proba(df)
        
        # Agregar predicciones al DataFrame
        df['prediction'] = predictions
        
        # Guardar resultados
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'predictions.csv')
        df.to_csv(output_path, index=False)
        
        return jsonify({
            'success': True,
            'total_predictions': len(predictions),
            'download_url': '/download_predictions'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/download_predictions')
def download_predictions():
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'predictions.csv')
    return send_file(output_path, as_attachment=True)

@app.route('/history')
def history():
    predictions = db.get_all_predictions()
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
