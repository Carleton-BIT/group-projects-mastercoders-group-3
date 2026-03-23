from flask import Flask, request, session, jsonify, send_from_directory

app = Flask(__name__)
app.secret_key = 'secret_key'

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_file(path):
    return send_from_directory('.', path)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username == 'user' and password == 'pass':
        session['user'] = username
        session.setdefault('address', '123 Example St')
        return jsonify(success=True, user=username, address=session['address'])

    return jsonify(success=False)

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('address', None)
    return jsonify(success=True)

@app.route('/user')
def get_user():
    if 'user' in session:
        return jsonify(user=session['user'], address=session.get('address', ''))
    return jsonify(user=None)

@app.route('/update_address', methods=['POST'])
def update_address():
    if 'user' not in session:
        return jsonify(success=False, error='Not logged in'), 401

    data = request.get_json()
    new_addr = data.get('address')
    session['address'] = new_addr
    return jsonify(success=True, address=new_addr)

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(host='127.0.0.1', port=5000, debug=True)