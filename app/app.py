from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_json', methods=['POST'])
def send_json():
    url = request.form['url']
    method = request.form['method']
    json_data = request.form['json_data']
    
    try:
        data = json.loads(json_data)
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON data"}), 400
    
    headers = {'Content-Type': 'application/json'}
    try:
        if method == 'POST':
            response = requests.post(url, data=json.dumps(data), headers=headers)
        elif method == 'GET':
            response = requests.get(url, headers=headers, params=data)
        elif method == 'PUT':
            response = requests.put(url, data=json.dumps(data), headers=headers)
        elif method == 'DELETE':
            response = requests.delete(url, data=json.dumps(data), headers=headers)
        else:
            return jsonify({"error": "Invalid HTTP method"}), 400
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500
    
    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify({"error": response.text}), response.status_code

if __name__ == "__main__":
    app.run(debug=True, port=2000)
