from flask import Flask, request, jsonify
from flask_cors import CORS
from mongoengine import Document, StringField, connect

app = Flask(__name__)
CORS(app)
# Connect to MongoDB
connect(db="projectdatabase", host="mongodb://localhost:27017/projectdatabase")

# Define User model for authentication
class User(Document):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)

# Define Project model
class Project(Document):
    name = StringField(required=True)
    image = StringField()
    description = StringField()
    status = StringField(default="En cours")  # Default status

# Route to create a new project
@app.route("/projects", methods=["POST"])
def create_project():
    project_data = request.json
    if not project_data:
        return jsonify({"error": "Missing project data"}), 400

    project = Project(**project_data)
    project.save()

    return jsonify({"message": "Project created successfully", "project_id": str(project.id)}), 201

# Route to get all projects
@app.route("/projects", methods=["GET"])
def get_projects():
    projects = Project.objects.all()
    project_list = [{"_id": str(project.id), "name": project.name, "image": project.image, "description": project.description, "status": project.status} for project in projects]
    return jsonify({"projects": project_list}), 200


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    # Check if the username and password are provided
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    # Check if the user exists in the database
    user = User.objects(username=username, password=password).first()
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify({"success": True, "message": "Login successful"}), 200

if __name__ == "__main__":
    app.run(debug=True)
