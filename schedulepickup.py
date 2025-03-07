from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///waste_requests.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Waste Pickup Model
class WastePickup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    waste_type = db.Column(db.String(50), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    carbon_footprint = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)

# Create database tables
with app.app_context():
    db.create_all()

# Carbon footprint calculation function
def calculate_carbon_footprint(waste_type, weight):
    carbon_factors = {
        "organic": 0.1,
        "plastic": 2.5,
        "electronic": 1.8,
        "hazardous": 3.0,
        "general": 1.2
    }
    return round(weight * carbon_factors.get(waste_type, 0), 2)

@app.route("/")
def index():
    return render_template("pickup_form.html")  # Ensure your HTML file is inside the "templates" folder

@app.route("/submit_request", methods=["POST"])
def submit_request():
    data = request.get_json()
    
    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")
    address = data.get("address")
    waste_type = data.get("waste_type")
    weight = float(data.get("weight"))
    description = data.get("description")

    carbon_footprint = calculate_carbon_footprint(waste_type, weight)

    new_request = WastePickup(
        name=name, email=email, phone=phone, address=address,
        waste_type=waste_type, weight=weight, carbon_footprint=carbon_footprint, description=description
    )
    
    db.session.add(new_request)
    db.session.commit()

    return jsonify({"message": "Request submitted successfully!", "carbon_footprint": carbon_footprint}), 201

@app.route("/requests", methods=["GET"])
def get_requests():
    requests = WastePickup.query.all()
    data = [
        {
            "id": req.id,
            "name": req.name,
            "email": req.email,
            "phone": req.phone,
            "address": req.address,
            "waste_type": req.waste_type,
            "weight": req.weight,
            "carbon_footprint": req.carbon_footprint,
            "description": req.description
        }
        for req in requests
    ]
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
