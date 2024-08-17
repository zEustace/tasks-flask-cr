from flask import Flask, request, jsonify
from models.task import task

app = Flask(__name__)

# CRUD
# Create, Read, Update and Delete

tasks = []
task_id_control = 1

@app.route('/tasks', methods=['POST'])
def create_task():
    global task_id_control
    data = request.get_json()
    new_task = task(id=task_id_control,title=data.get("title"), description=data.get("description", ""))
    task_id_control +=1
    tasks.append(new_task)
    print(tasks)
    return jsonify({"message": "New task created"})

@app.route('/tasks', methods=['GET'])
def get_tasks():
    #task_list = []
    #for task in tasks:
    #    task_list.append(task.to_dict())
    task_list = [task.to_dict() for task in tasks]
    output = {
            "tasks": task_list,
            "total_tasks": len(task_list)
            }
    return jsonify(output)

@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            return jsonify(t.to_dict())
    
    return jsonify({"message": "Activity requested not found."}), 404


@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t
            break

    if task == None:
        return jsonify({"message": "Activity requested not found."}), 404
    
    data = request.get_json()
    task.title = data['title']
    task.description = data['description']
    task.completed = data['completed']

    return jsonify({"message": "Task updated."})

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t
            break
    
    if not task:
        return jsonify({"message": "Activity requested not found."}), 404
    
    tasks.remove(task)
    return jsonify({"message": "Task deleted."})
      
if __name__ == "__main__":
    app.run(debug=True)


