from flask import Flask, request, jsonify
from sqlcommands import verify_user
from flask_cors import CORS  # to allow frontend requests

app = Flask(__name__)
CORS(app)  # enable CORS for all routes

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    print(data)
    username = data.get('username')
    password = data.get('password')

    AppUser = verify_user(username, password)

    if AppUser:
        return jsonify({"success": True, "role": AppUser["role"]})
    else:
        return jsonify({"success": False, "message": "Invalid credentials"}), 401

@app.route('/createLesson', methods=['POST'])
def create_lesson():
    data = request.get_json()
    print(data)
    # TODO Add creation logic
    return jsonify({"success": True, "message": "Lesson created successfully"})

if __name__ == '__main__':
    app.run(debug=True)
