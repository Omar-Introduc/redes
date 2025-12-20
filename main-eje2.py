import os
import time
from flask import Flask, jsonify

app = Flask(__name__)

# Simulación de carga de inicio
START_TIME = time.time()

# Variable sensible inyectada por Kubernetes
API_KEY = os.getenv("TRANS_API_KEY", "Inseguro")

@app.route('/')
def home():
    # Retorna el nombre del pod (hostname) para verificar balanceo de carga
    return jsonify({
        "status": "ready",
        "worker": os.getenv("HOSTNAME"),
        "key_loaded": API_KEY != "Inseguro"
    })

@app.route('/health')
def health():
    # Simula que la app tarda 10 segundos en estar lista (Startup Probe)
    if time.time() - START_TIME < 10:
        return jsonify({"status": "starting"}), 503
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    # Puerto 3000
    app.run(host='0.0.0.0', port=3000)