from flask import Flask, request, render_template
import mysql.connector

app = Flask(__name__)

# Replace 'your_username', 'your_password', and 'your_database' with your MySQL credentials
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="arun",
    database="arun",
auth_plugin="mysql_native_password"
)



cursor = db.cursor()

# Create tables if not exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS student_details (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_name VARCHAR(255),
    student_email VARCHAR(255)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS parent_details (
    id INT AUTO_INCREMENT PRIMARY KEY,
    parent_name VARCHAR(255),
    parent_email VARCHAR(255)
)
""")
@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    student_name = request.form['student_name']
    student_email = request.form['student_email']
    parent_name = request.form['parent_name']
    parent_email = request.form['parent_email']

    # Insert data into student_details table
    cursor.execute("INSERT INTO student_details (student_name, student_email) VALUES (%s, %s)",
                   (student_name, student_email))
    db.commit()

    # Get the student's ID
    cursor.execute("SELECT LAST_INSERT_ID()")
    student_id = cursor.fetchone()[0]

    # Insert data into parent_details table
    cursor.execute("INSERT INTO parent_details (parent_name, parent_email, student_id) VALUES (%s, %s, %s)",
                   (parent_name, parent_email, student_id))
    db.commit()

    return "Register/Login successful"

if __name__ == '__main__':
    app.run(debug=True)
