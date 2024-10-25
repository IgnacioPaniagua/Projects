from flask import Flask, jsonify, request

app = Flask(__name__)

# Datos críticos
critical_pressure = 10  # MPa
critical_volume_liquid = 0.0035  # m3/kg
critical_volume_vapor = 0.0035  # m3/kg

# Volúmenes específicos para distintas presiones (simplificado)
def get_specific_volumes(pressure):
    if pressure < critical_pressure:
        specific_volume_liquid = 0.00105 + (critical_volume_liquid - 0.00105) * (pressure / critical_pressure)
        specific_volume_vapor = specific_volume_liquid + (critical_volume_vapor - specific_volume_liquid) * (pressure / critical_pressure)
    else:
        specific_volume_liquid = critical_volume_liquid
        specific_volume_vapor = critical_volume_vapor
    
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
