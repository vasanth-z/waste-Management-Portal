from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'carbon_offset_admin'

mysql = MySQL(app)

# Route for Home
@app.route('/')
def home():
    return render_template('index.html')

# Route for adding industry details
@app.route('/add_industry', methods=['POST'])
def add_industry():
    industry_id = request.form['id']
    industry_name = request.form['name']
    email = request.form['mail']
    contact = request.form['phone']
    address = request.form['age']
    industry_type = request.form['myInput']
    password = request.form['password']
    
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO industries (industry_id, industry_name, email, contact, address, industry_type, password) VALUES (%s, %s, %s, %s, %s, %s, %s)", (industry_id, industry_name, email, contact, address, industry_type, password))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('home'))

# Route for viewing industry details
@app.route('/view_industries', methods=['GET'])
def view_industries():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM industries")
    industries = cursor.fetchall()
    cursor.close()
    return jsonify(industries)

# MySQL Database Schema
# CREATE DATABASE carbon_offset_admin;
# USE carbon_offset_admin;
# CREATE TABLE industries (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     industry_id VARCHAR(50),
#     industry_name VARCHAR(255),
#     email VARCHAR(255),
#     contact VARCHAR(20),
#     address TEXT,
#     industry_type VARCHAR(50),
#     password VARCHAR(255)
# );

if __name__ == '__main__':
    app.run(debug=True)