from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS  # Import Flask-CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="siva1234",
    database="adminuser"
)
cursor = db.cursor()

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    try:
        sql = "INSERT INTO userdetiles (userid, username, email, contactno, address, userpassword) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (data["id"], data["name"], data["email"], data["contact"], data["address"], data["password"])
        cursor.execute(sql, values)
        db.commit()
        return jsonify({"message": "User added successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)