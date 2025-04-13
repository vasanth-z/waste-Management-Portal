from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="siva1234",
    database="adminuser"
)
cursor = db.cursor()

@app.route('/add_worker', methods=['POST'])
def add_worker():
    data = request.json  # Get JSON data from request

    try:
        # Validate if all required fields are present
        required_fields = ["id", "name", "age", "contact", "email", "workzone", "password"]
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        # SQL Query to insert worker data
        sql = """INSERT INTO workerdetilesdetiles
                 (userid, username, age, contactno, email, workzone, userpassword) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        values = (data["id"], data["name"], data["age"], data["contact"], data["email"], data["workzone"], data["password"])
        
        cursor.execute(sql, values)  # Execute SQL query
        db.commit()  # Save changes to the database

        return jsonify({"message": "Worker added successfully"}), 200

    except mysql.connector.Error as err:
        print("Database Error:", str(err))  # Print error in terminal
        return jsonify({"error": f"Database Error: {str(err)}"}), 500

    except Exception as e:
        print("Error:", str(e))  # Print error in terminal
        return jsonify({"error": f"Server Error: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Run Flask server