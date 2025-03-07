from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ngo_requests.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# NGO Pickup Request Model
class NGOPickup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    item_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)

# Create database tables
with app.app_context():
    db.create_all()

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
    item_type = data.get("item_type")
    description = data.get("description")

    new_request = NGOPickup(
        name=name, email=email, phone=phone, address=address,
        item_type=item_type, description=description
    )
    
    db.session.add(new_request)
    db.session.commit()

    return jsonify({"message": "Request submitted successfully!"}), 201

@app.route("/requests", methods=["GET"])
def get_requests():
    requests = NGOPickup.query.all()
    data = [
        {
            "id": req.id,
            "name": req.name,
            "email": req.email,
            "phone": req.phone,
            "address": req.address,
            "item_type": req.item_type,
            "description": req.description
        }
        for req in requests
    ]
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
