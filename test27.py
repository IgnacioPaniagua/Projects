from flask import Flask, jsonify, request

app = Flask(__name__)

# Datos críticos
critical_pressure = 10  # MPa
critical_volume_liquid = 0.0035  # m3/kg
critical_volume_vapor = 0.0035  # m3/kg

# Volúmenes específicos para distintas presiones
def get_specific_volumes(pressure):
    if pressure < 0.5:  # Para presiones muy bajas
        specific_volume_liquid = 0.00105
        specific_volume_vapor = 30  # Valor representativo
    elif 0.5 <= pressure < 10:  # Línea de líquido saturado
        # Interpolación para líquido saturado
        specific_volume_liquid = 0.00105 + (0.0035 - 0.00105) * ((pressure - 0.5) / (9.5))  # Rango de 0.5 a 10 MPa
        specific_volume_vapor = specific_volume_liquid + (0.0035 - specific_volume_liquid) * ((pressure - 0.5) / (9.5))  # Asumiendo que el vapor va subiendo
    elif pressure == 10:  # En el punto crítico
        specific_volume_liquid = 0.0035
        specific_volume_vapor = 0.0035
    elif 10 < pressure <= 30:  # Línea de vapor saturado
        specific_volume_liquid = 0.0035  # Se mantiene constante
        specific_volume_vapor = 30 - (pressure - 10) * (29.5 / 20)  # Decrece linealmente desde 30 a un valor a definir
    else:  # Fuera de los límites
        return jsonify({"error": "Pressure out of bounds"}), 400

    return specific_volume_liquid, specific_volume_vapor



@app.route('/phase-change-diagram', methods=['GET'])
def phase_change_diagram():
    pressure = float(request.args.get('pressure'))
    
    if pressure < 0 or pressure > 30:
        return jsonify({"error": "Pressure out of bounds"}), 400
    
    specific_volume_liquid, specific_volume_vapor = get_specific_volumes(pressure)
    
    return jsonify({
        "specific_volume_liquid": specific_volume_liquid,
        "specific_volume_vapor": specific_volume_vapor
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
