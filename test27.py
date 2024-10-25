from flask import Flask, jsonify, render_template_string, request
import random
import os

app = Flask(__name__)

# Definición de los sistemas y códigos
systems = {
    "navigation": "NAV-01",
    "communications": "COM-02",
    "life_support": "LIFE-03",
    "engines": "ENG-04",
    "deflector_shield": "SHLD-05"
}

@app.route('/status', methods=['GET'])
def status():
    damaged_system = random.choice(list(systems.keys()))
    return jsonify({"damaged_system": damaged_system})

@app.route('/repair-bay', methods=['GET'])
def repair_bay():
    damaged_system = request.args.get('damaged_system')
    code = systems.get(damaged_system, "Unknown system")
    
    html_content = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Repair</title>
    </head>
    <body>
    <div class="anchor-point">{code}</div>
    </body>
    </html>
    '''
    
    return render_template_string(html_content)

@app.route('/teapot', methods=['POST'])
def teapot():
    return '', 418

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
