from flask import Flask, request, jsonify

app = Flask(__name__)

# Store distance data
ultrasonic_data = {"distance": 0}

@app.route('/api/update_distance', methods=['POST'])
def update_distance():
    global ultrasonic_data
    data = request.get_json()
    ultrasonic_data["distance"] = data.get("distance", 0)
    return jsonify({"message": "Distance updated", "data": ultrasonic_data})

@app.route('/api/get_data', methods=['GET'])
def get_distance():
    return jsonify(ultrasonic_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
