from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database connection
db = mysql.connector.connect(
   host="localhost",
        user="root",
        password="siva1234",  # Change this to your actual MySQL password
        database="adminuser"
)
cursor = db.cursor()

# Add NGO API
@app.route("/add_ngo", methods=["POST"])
def add_ngo():
    data = request.json
    try:
        query = """INSERT INTO ngodetiles (userid, username, contactno, email, incharge, adress, userpassword) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        values = (data['id'], data['name'], data['phone'], data['email'], data['incharge'], data['address'], data['password'])
        
        cursor.execute(query, values)
        db.commit()
        return jsonify({"message": "NGO added successfully!"})
    
    except mysql.connector.Error as err:
        db.rollback()
        return jsonify({"error": str(err)}), 500

if __name__ == "__main__":
    app.run(debug=True)