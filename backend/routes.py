# routes.py
from flask import request, jsonify
from app import app
from extensions import db  # folosește db din extensions
from models import User
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from models import Task


@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required."}), 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"error": "User already exists."}), 409

    new_user = User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User created successfully!"}), 201

@app.route('/login', methods=['POST'])
def login():
    date = request.get_json()
    username = date.get('username')
    password = date.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required."}), 400
    existing_user = User.query.filter_by(username=username).first()

    if not existing_user or not existing_user.check_password(password):
        return jsonify({"error": "Invalid username or password."}), 401

    access_token = create_access_token(identity=str(existing_user.id))

    return jsonify({"msg": "Login Successful",
                    "access_token": access_token
                    }), 200

@app.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    user_id = get_jwt_identity()
    data = request.get_json()
    title = data.get('title')
    status = data.get('status', 'To do')

    if not title:
        return jsonify({"error": "Title is required"}), 400

    new_task = Task(title=title, status=status, user_id=user_id)
    db.session.add(new_task)
    db.session.commit()

    return jsonify({"msg": "Task created successfully"}), 201

@app.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    user_id = get_jwt_identity()
    tasks = Task.query.filter_by(user_id=user_id).all()

    task_list = [
        {"id": t.id, "title": t.title, "status": t.status}
        for t in tasks
    ]

    return jsonify(task_list), 200


@app.route('/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    title = data.get('title')
    status = data.get('status')

    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return jsonify({"error": "Task not found."}), 404

    if title:
        task.title = title
    if status:
        task.status = status

    db.session.commit()
    return jsonify({"msg": "Task updated successfully"}), 200

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()

    if not task:
        return jsonify({"error": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({"msg": "Task deleted successfully"}), 200


@app.route('/tasks/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()

    if not task:
        return jsonify({"error": "Task not found"}), 404

    return jsonify({
        "id": task.id,
        "title": task.title,
        "status": task.status
    }), 200
