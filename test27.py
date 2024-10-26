from flask import Flask, jsonify, request

app = Flask(__name__)

# Datos críticos
critical_pressure = 10  # MPa
critical_volume_liquid = 0.0035  # m3/kg
critical_volume_vapor = 30  # m3/kg

# Volúmenes específicos para distintas presiones
def get_specific_volumes(pressure):
    if pressure < 0.5:  # Para presiones muy bajas
        specific_volume_liquid = 0.00105
        specific_volume_vapor = 30  # Valor representativo
    elif 0.5 <= pressure < critical_pressure:  # Línea de líquido saturado
        specific_volume_liquid = 0.00105 + (critical_volume_liquid - 0.00105) * ((pressure - 0.5) / (critical_pressure - 0.5))
        specific_volume_vapor = 30 - (30 - critical_volume_vapor) * ((pressure - 0.5) / (critical_pressure - 0.5))
    elif pressure == critical_pressure:  # En el punto crítico
        specific_volume_liquid = critical_volume_liquid
        specific_volume_vapor = critical_volume_vapor
    elif critical_pressure < pressure <= 30:  # Línea de vapor saturado
        specific_volume_liquid = critical_volume_liquid  # Se mantiene constante
        specific_volume_vapor = critical_volume_vapor - (critical_volume_vapor - 0.05) * ((pressure - critical_pressure) / (30 - critical_pressure))
    else:  # Fuera de los límites
        return None, None  # Manejo de error

    return specific_volume_liquid, specific_volume_vapor

@app.route('/phase-change-diagram', methods=['GET'])
def phase_change_diagram():
    try:
        pressure = float(request.args.get('pressure'))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid pressure value"}), 400
    
    if pressure < 0 or pressure > 30:
        return jsonify({"error": "Pressure out of bounds"}), 400
    
    specific_volume_liquid, specific_volume_vapor = get_specific_volumes(pressure)

    # Manejo de caso en que los valores devueltos sean None
    if specific_volume_liquid is None or specific_volume_vapor is None:
        return jsonify({"error": "Unable to calculate specific volumes"}), 500

    return jsonify({
        "specific_volume_liquid": specific_volume_liquid,
        "specific_volume_vapor": specific_volume_vapor
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
