from flask import Flask, jsonify, render_template_string
import random

app = Flask(__name__)

# Sistemas y códigos
systems = ["navigation", "communications", "life_support", "engines", "deflector_shield"]
system_codes = {
    "navigation": "NAV-01",
    "communications": "COM-02",
    "life_support": "LIFE-03",
    "engines": "ENG-04",
    "deflector_shield": "SHLD-05"
}

# Variable global para guardar el sistema dañado
current_damaged_system = None

@app.route('/status', methods=['GET'])
def status():
    global current_damaged_system
    current_damaged_system = random.choice(systems)  # Elegir un sistema dañado al azar
    return jsonify({"damaged_system": current_damaged_system})

@app.route('/repair-bay', methods=['GET'])
def repair_bay():
    if current_damaged_system is None:
        return jsonify({"error": "No damaged system found. Please call /status first."}), 400
    
    system_code = system_codes[current_damaged_system]
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Repair</title>
    </head>
    <body>
    <div class="anchor-point">{system_code}</div>
    </body>
    </html>
    """
    
    return render_template_string(html_content)

@app.route('/teapot', methods=['POST'])
def teapot():
    return '', 418  # Retornar el código 418

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
