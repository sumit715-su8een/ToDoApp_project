from flask import Flask, jsonify, request
import json, os

app = Flask(__name__)
DB_FILE = 'todos.json'

def load_todos():
    if os.path.exists(DB_FILE):
        with open(DB_FILE) as f:
            return json.load(f)
    return []

def save_todos(todos):
    with open(DB_FILE, 'w') as f:
        json.dump(todos, f)

@app.route('/')
def index():
    return jsonify({"status": "ok", "app": "ToDoApp"})

@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify(load_todos())

@app.route('/todos', methods=['POST'])
def add_todo():
    data = request.get_json()
    todos = load_todos()
    todos.append({"id": len(todos)+1, "title": data.get('title',''), "done": False})
    save_todos(todos)
    return jsonify(todos[-1]), 201

@app.route('/todos/<int:tid>', methods=['PUT'])
def update_todo(tid):
    data = request.get_json()
    todos = load_todos()
    for t in todos:
        if t['id'] == tid:
            t['done'] = data.get('done', t['done'])
            t['title'] = data.get('title', t['title'])
    save_todos(todos)
    return jsonify({"status": "updated"})

@app.route('/todos/<int:tid>', methods=['DELETE'])
def delete_todo(tid):
    todos = load_todos()
    todos = [t for t in todos if t['id'] != tid]
    save_todos(todos)
    return jsonify({"status": "deleted"})

@app.route('/health')
def health():
    return jsonify({"healthy": True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
