
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'siva1234'
app.config['MYSQL_DB'] = 'admin_dashboard'

mysql = MySQL(app)

# Route for Hom
@app.route('/')
def home():
    return render_template('index.html')

# Route for adding people
@app.route('/add_people', methods=['POST'])
def add_people():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO people (name, age) VALUES (%s, %s)", (name, age))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('home'))

# Route for viewing people
@app.route('/view_people', methods=['GET'])
def view_people():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM people")
    people = cursor.fetchall()
    cursor.close()
    return jsonify(people)

# Route for adding industries
@app.route('/add_industry', methods=['POST'])
def add_industry():
    industry_name = request.form['industry_name']
    location = request.form['location']
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO industries (industry_name, location) VALUES (%s, %s)", (industry_name, location))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('home'))

# Route for viewing industries
@app.route('/view_industries', methods=['GET'])
def view_industries():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM industries")
    industries = cursor.fetchall()
    cursor.close()
    return jsonify(industries)

# Route for adding announcements
@app.route('/add_announcement', methods=['POST'])
def add_announcement():
    announcement = request.form['announcement']
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO announcements (announcement) VALUES (%s)", (announcement,))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('home'))

# MySQL Database Schema
# CREATE DATABASE admin_dashboard;
# USE admin_dashboard;
# CREATE TABLE people (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), age INT);
# CREATE TABLE industries (id INT AUTO_INCREMENT PRIMARY KEY, industry_name VARCHAR(255), location VARCHAR(255));
# CREATE TABLE announcements (id INT AUTO_INCREMENT PRIMARY KEY, announcement TEXT);

if __name__ == '__main__':
    app.run(debug=True)