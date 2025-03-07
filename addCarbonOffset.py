from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import random
import string

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///carbon_offset_admins.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Admin Model
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    work_region = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Hashed password

# Create the database
with app.app_context():
    db.create_all()

def generate_password(length=8):
    chars = string.ascii_letters + string.digits + "@#$%&*!"
    return ''.join(random.choice(chars) for _ in range(length))

@app.route("/")
def home():
    return render_template("dashboard.html")  # Ensure your HTML file is inside a "templates" folder

@app.route("/add_admin", methods=["POST"])
def add_admin():
    data = request.get_json()
    admin_id = data.get("admin_id")
    name = data.get("name")
    work_region = data.get("work_region")
    contact = data.get("contact")
    email = data.get("email")
    role = data.get("role")

    # Check if the admin already exists
    existing_admin = Admin.query.filter_by(admin_id=admin_id).first()
    if existing_admin:
        return jsonify({"message": "Admin ID already exists"}), 400

    password = generate_password()
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    new_admin = Admin(
        admin_id=admin_id, name=name, work_region=work_region, contact=contact, email=email, role=role, password=hashed_password
    )
    db.session.add(new_admin)
    db.session.commit()

    return jsonify({"message": "Admin added successfully", "password": password}), 201

@app.route("/get_admins", methods=["GET"])
def get_admins():
    admins = Admin.query.all()
    admin_list = []
    for admin in admins:
        admin_list.append({
            "admin_id": admin.admin_id,
            "name": admin.name,
            "work_region": admin.work_region,
            "contact": admin.contact,
            "email": admin.email,
            "role": admin.role,
            "password": admin.password
        })
    return jsonify(admin_list)

@app.route("/delete_admin/<admin_id>", methods=["DELETE"])
def delete_admin(admin_id):
    admin = Admin.query.filter_by(admin_id=admin_id).first()
    if not admin:
        return jsonify({"message": "Admin not found"}), 404

    db.session.delete(admin)
    db.session.commit()
    return jsonify({"message": "Admin deleted successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)
