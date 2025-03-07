from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "supersecretkey"  # For flash messages
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    contact = db.Column(db.String(15), nullable=False)
    address = db.Column(db.String(255), nullable=False)

# Create the database
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("signup.html")  # Ensure your HTML file is in a 'templates' folder

@app.route("/signup", methods=["POST"])
def signup():
    full_name = request.form.get("full_name")
    dob = request.form.get("dob")
    email = request.form.get("email")
    password = request.form.get("password")
    contact = request.form.get("contact")
    address = request.form.get("address")

    # Check if user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        flash("Email already registered. Please log in.", "danger")
        return redirect(url_for("home"))

    # Hash the password
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    # Save user to the database
    new_user = User(full_name=full_name, dob=dob, email=email, password=hashed_password, contact=contact, address=address)
    db.session.add(new_user)
    db.session.commit()

    flash("Signup successful! You can now log in.", "success")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
