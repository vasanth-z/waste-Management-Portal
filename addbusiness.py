from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)
# Database connection
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="siva1234",  # Change this to your actual MySQL password
        database="adminuser"  # Change to your actual database name
    )
    cursor = db.cursor()
    print("Database connected successfully!")
except mysql.connector.Error as err:
    print("Database connection error:", err)

# API to add business details
@app.route("/add_business", methods=["POST"])
def add_business():
    data = request.json
    try:
        query = """INSERT INTO businessdetiles (userid, username, contactno, region, email, userrole, userpassword)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        values = (data['id'], data['name'], data['phone'], data['region'], data['mail'], data['role'], data['password'])
        
        cursor.execute(query, values)
        db.commit()
        return jsonify({"message": "Business details added successfully!"})
    
    except mysql.connector.Error as err:
        db.rollback()
        return jsonify({"error": str(err)}), 500

if __name__ == "__main__":
    app.run(debug=True)