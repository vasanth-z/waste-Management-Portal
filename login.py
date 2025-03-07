from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dummy user data (replace with a database in production)
users = {
    "admin": {"password": "admin123", "role": "Admin"},
    "user": {"password": "user123", "role": "User"}
}

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    user_type = request.form.get("userType")

    if username in users and users[username]["password"] == password:
        if users[username]["role"] == user_type:
            return redirect(url_for("dashboard", user=username))
        else:
            return "Invalid user type selected", 403
    return "Invalid credentials", 401

@app.route("/dashboard")
def dashboard():
    user = request.args.get("user", "Guest")
    return f"<h2>Welcome, {user}!</h2><p>You have successfully logged in.</p>"

if __name__ == "__main__":
    app.run(debug=True)
