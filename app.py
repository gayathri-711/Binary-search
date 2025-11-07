from flask import Flask, jsonify, request, send_from_directory
import threading
import json
import os

# Allow overriding the data file via environment for tests
DATA_FILE = os.environ.get('STUDENT_DATA_FILE') or os.path.join(os.path.dirname(__file__), 'student_data.json')
lock = threading.Lock()
app = Flask(__name__, static_folder='.', static_url_path='')


def read_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except Exception:
            return []


def write_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


@app.route('/')
def index():
    # serve the existing index.html in the workspace root
    return send_from_directory('.', 'index.html')


@app.route('/student.html')
def student_page():
    return send_from_directory('.', 'student.html')


@app.route('/api/students', methods=['GET', 'POST'])
def students():
    if request.method == 'GET':
        return jsonify(read_data())

    payload = request.get_json()
    if not payload or 'name' not in payload:
        return jsonify({'error': 'missing name'}), 400

    with lock:
        data = read_data()
        new_id = max([s.get('id', 0) for s in data] + [0]) + 1
        student = {
            'id': new_id,
            'name': payload['name'],
            'age': payload.get('age'),
            'grade': payload.get('grade')
        }
        data.append(student)
        write_data(data)

    return jsonify(student), 201


@app.route('/api/students/<int:sid>', methods=['GET', 'PUT', 'DELETE'])
def student_detail(sid):
    with lock:
        data = read_data()
        for i, s in enumerate(data):
            if s.get('id') == sid:
                if request.method == 'GET':
                    return jsonify(s)
                if request.method == 'PUT':
                    payload = request.get_json()
                    if not payload:
                        return jsonify({'error': 'missing body'}), 400
                    # allow updating name, age, grade
                    for key in ('name', 'age', 'grade'):
                        if key in payload:
                            s[key] = payload[key]
                    data[i] = s
                    write_data(data)
                    return jsonify(s)
                # DELETE
                data.pop(i)
                write_data(data)
                return jsonify({'deleted': sid})

    return jsonify({'error': 'not found'}), 404


if __name__ == '__main__':
    # Run on 127.0.0.1:5000 by default for local testing
    app.run(debug=True)
