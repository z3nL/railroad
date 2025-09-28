import asyncio
from multi_tool_agent.agent import main
from flask import Flask, request, jsonify
from sqlcommands import verify_user, add_lesson, upload_directory, add_step, clear_generated_images
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

    title = data.get('title')
    topic = data.get('topic')
    level = data.get('level')
    description = data.get('description')

    lesson, error = add_lesson(title, description, level)
    if error:
        return jsonify({"success": False, "message": error}), 400
    
    lesson_id = lesson['lesson_id']

    steps_array = asyncio.run(main(topic, description, level))

    # Upload images and get their URL's
    file_urls = upload_directory()
    clear_generated_images()

    for i, file_url in enumerate(file_urls):
        step_description = steps_array[i] if i < len(steps_array) else "Step description missing"
        add_step(lesson_id, i + 1, step_description, file_url)

    return jsonify({"success": True, "message": "Lesson created successfully", "lesson_id": lesson_id})

if __name__ == '__main__':
    app.run(debug=True)
