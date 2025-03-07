from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import random
import string

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///workers.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Worker Model
class Worker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    worker_id = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    contact = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    work_zone = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Hashed password

# Create the database
with app.app_context():
    db.create_all()

def generate_password(length=8):
    chars = string.ascii_letters + string.digits + "@#$%&*!"
    return ''.join(random.choice(chars) for _ in range(length))

@app.route("/")
def home():
    return render_template("dashboard.html")  # Ensure your HTML file is in a 'templates' folder

@app.route("/add_worker", methods=["POST"])
def add_worker():
    data = request.get_json()
    worker_id = data.get("worker_id")
    name = data.get("name")
    age = data.get("age")
    contact = data.get("contact")
    email = data.get("email")
    work_zone = data.get("work_zone")

    # Check if worker already exists
    existing_worker = Worker.query.filter_by(worker_id=worker_id).first()
    if existing_worker:
        return jsonify({"message": "Worker ID already exists"}), 400

    password = generate_password()
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    new_worker = Worker(worker_id=worker_id, name=name, age=age, contact=contact, email=email, work_zone=work_zone, password=hashed_password)
    db.session.add(new_worker)
    db.session.commit()

    return jsonify({"message": "Worker added successfully", "password": password}), 201

@app.route("/get_workers", methods=["GET"])
def get_workers():
    workers = Worker.query.all()
    worker_list = []
    for worker in workers:
        worker_list.append({
            "worker_id": worker.worker_id,
            "name": worker.name,
            "age": worker.age,
            "contact": worker.contact,
            "email": worker.email,
            "work_zone": worker.work_zone,
            "password": worker.password
        })
    return jsonify(worker_list)

@app.route("/delete_worker/<worker_id>", methods=["DELETE"])
def delete_worker(worker_id):
    worker = Worker.query.filter_by(worker_id=worker_id).first()
    if not worker:
        return jsonify({"message": "Worker not found"}), 404

    db.session.delete(worker)
    db.session.commit()
    return jsonify({"message": "Worker deleted successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)
