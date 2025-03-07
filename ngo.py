from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import string

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ngo_dashboard.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# NGO Model
class NGO(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reg_no = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(20), nullable=False)
    incharge = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(20), nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

# Password Generator
def generate_password(length=8):
    chars = string.ascii_letters + string.digits + "@#$%&*!"
    return ''.join(random.choice(chars) for _ in range(length))

# Add NGO
@app.route("/add_ngo", methods=["POST"])
def add_ngo():
    data = request.json
    reg_no = data.get("reg_no")
    name = data.get("name")
    contact = data.get("contact")
    incharge = data.get("incharge")
    email = data.get("email")
    address = data.get("address")
    password = generate_password()

    new_ngo = NGO(
        reg_no=reg_no, name=name, contact=contact,
        incharge=incharge, email=email, address=address, password=password
    )
    db.session.add(new_ngo)
    db.session.commit()

    return jsonify({"message": "NGO added successfully", "password": password})

# Fetch NGOs
@app.route("/get_ngos", methods=["GET"])
def get_ngos():
    ngos = NGO.query.all()
    ngo_list = [
        {
            "id": ngo.id,
            "reg_no": ngo.reg_no,
            "name": ngo.name,
            "contact": ngo.contact,
            "incharge": ngo.incharge,
            "email": ngo.email,
            "address": ngo.address,
            "password": ngo.password,
        }
        for ngo in ngos
    ]
    return jsonify(ngo_list)

# Remove NGO
@app.route("/remove_ngo/<int:ngo_id>", methods=["DELETE"])
def remove_ngo(ngo_id):
    ngo = NGO.query.get(ngo_id)
    if ngo:
        db.session.delete(ngo)
        db.session.commit()
        return jsonify({"message": "NGO removed successfully"})
    return jsonify({"error": "NGO not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
