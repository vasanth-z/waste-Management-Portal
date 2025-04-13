from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)  # Enable CORS

# Database connection
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="siva1234",  # Change this to your MySQL password
        database="adminuser"
    )
    cursor = db.cursor()
    print("Database connected successfully!")
except Exception as e:
    print("Database Connection Error:", str(e))

# API to add an officer
@app.route('/add_officer', methods=['POST'])
def add_officer():
    data = request.json
    try:
        sql = """INSERT INTO officerdetiles (userid, username, email, contactno, adress, position)
                 VALUES (%s, %s, %s, %s, %s, %s)"""
        values = (data["userid"], data["username"], data["email"], data["contactno"], data["adress"], data["position"])
        cursor.execute(sql, values)
        db.commit()
        return jsonify({"message": "Officer added successfully"}), 200
    except Exception as e:
        print("Error in add_officer:", str(e))
        return jsonify({"error": str(e)}), 500

# API to fetch officer list
@app.route('/get_officers', methods=['GET'])
def get_officers():
    try:
        cursor.execute("SELECT * FROM officerdetiles")
        officers = cursor.fetchall()
        officer_list = [
            {"userid": row[0], "username": row[1], "email": row[2], "contactno": row[3], "adress": row[4], "position": row[5]}
            for row in officers
        ]
        return jsonify(officer_list), 200
    except Exception as e:
        print("Error in get_officers:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)