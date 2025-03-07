from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import random
import string

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///businesses.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Business Model
class Business(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    work_region = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Hashed password

# Create the database
with app.app_context():
    db.create_all()

# Function to generate a random password
def generate_password(length=8):
    chars = string.ascii_letters + string.digits + "@#$%&*!"
    return ''.join(random.choice(chars) for _ in range(length))

@app.route("/")
def home():
    return render_template("dashboard.html")  # Ensure your HTML file is inside a "templates" folder

@app.route("/add_business", methods=["POST"])
def add_business():
    data = request.get_json()
    business_id = data.get("business_id")
    name = data.get("name")
    work_region = data.get("work_region")
    contact = data.get("contact")
    email = data.get("email")
    role = data.get("role")

    # Check if business already exists
    existing_business = Business.query.filter_by(business_id=business_id).first()
    if existing_business:
        return jsonify({"message": "Business ID already exists"}), 400

    password = generate_password()
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    new_business = Business(
        business_id=business_id, name=name, work_region=work_region, contact=contact, email=email, role=role, password=hashed_password
    )
    db.session.add(new_business)
    db.session.commit()

    return jsonify({"message": "Business added successfully", "password": password}), 201

@app.route("/get_businesses", methods=["GET"])
def get_businesses():
    businesses = Business.query.all()
    business_list = []
    for business in businesses:
        business_list.append({
            "business_id": business.business_id,
            "name": business.name,
            "work_region": business.work_region,
            "contact": business.contact,
            "email": business.email,
            "role": business.role,
            "password": business.password
        })
    return jsonify(business_list)

@app.route("/delete_business/<business_id>", methods=["DELETE"])
def delete_business(business_id):
    business = Business.query.filter_by(business_id=business_id).first()
    if not business:
        return jsonify({"message": "Business not found"}), 404

    db.session.delete(business)
    db.session.commit()
    return jsonify({"message": "Business deleted successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)
