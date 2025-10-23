"""
Script de configuración para la aplicación Flask
Ejecutar antes de iniciar la aplicación por primera vez
"""
import os
import sys

def setup():
    print("🚀 Configurando Uber Ride Analytics App...")
    
    # Crear directorios necesarios
    directories = ['uploads', 'models', 'static/css', 'static/js', 'templates']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Directorio creado: {directory}")
    
    # Verificar que existe el modelo
    model_path = os.path.join('..', 'models', 'booking_status_rf_model.joblib')
    if not os.path.exists(model_path):
        print("\n⚠️  ADVERTENCIA: No se encontró el modelo entrenado")
        print(f"   Por favor, asegúrate de que existe: {model_path}")
        print("   Ejecuta primero el notebook 002_Uber2024-Models.ipynb")
        return False
    
    print(f"✓ Modelo encontrado: {model_path}")
    
    # Verificar dependencias
    try:
        import flask
        import pandas
        import sklearn
        import joblib
        print("✓ Todas las dependencias están instaladas")
    except ImportError as e:
        print(f"\n⚠️  Falta instalar dependencias: {e}")
        print("   Ejecuta: pip install -r requirements.txt")
        return False
    
    print("\n✅ Configuración completada exitosamente!")
    print("\nPara iniciar la aplicación:")
    print("  python app.py")
    print("\nO con Docker:")
    print("  docker-compose up --build")
    
    return True

if __name__ == '__main__':
    success = setup()
    sys.exit(0 if success else 1)
