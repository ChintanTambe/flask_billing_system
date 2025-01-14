import io
import MySQLdb
from flask import Flask, flash, json, jsonify, render_template,request, redirect, send_file, url_for,session
from flask_mysqldb import MySQL
from werkzeug.security import check_password_hash
from reportlab.lib.pagesizes import letter
from fpdf import FPDF
import os


# Initialize the Flask application
app = Flask(__name__)

secret_key = os.urandom(24)  # Generates a random 24-byte string

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'        # Your MySQL host, e.g., 'localhost'
app.config['MYSQL_USER'] = 'root'     # Your MySQL username
app.config['MYSQL_PASSWORD'] = 'CHintan123!@#'  # Your MySQL password
app.config['MYSQL_DB'] = 'ebill'        # Your MySQL database name
app.config['SECRET_KEY'] = secret_key

# Initialize MySQL
mysql = MySQL(app)

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check credentials against the database
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()

        # Debugging: Print the retrieved user
        print(f"Retrieved user: {user}")

        if user and user[2] == password:  # Assuming user[2] is the plain text password
            session['user_id'] = user[0]  # Store user ID in session
            flash("Login successful!", "success")
            return redirect(url_for('dashboard'))  # Redirect to dashboard
        else:
            flash("Incorrect email or password.", "danger")  # Use flash for better UX
            return redirect(url_for('login'))  # Redirect back to login page

    return render_template('login.html')  # Render login page if GET request

@app.route('/services')
def services():
    return render_template('services.html')

# Route for the create bill page
@app.route('/create_bill', methods=['GET', 'POST'])
def create_bill():
    if request.method == 'POST':
        product_name = request.form['product_name']
        quantity = request.form['quantity']

        # Insert product details into the database
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO items (bill_id, item_description, quantity, unit_price) VALUES (%s, %s, %s, %s)",
                    (1, product_name, quantity, 10.00))  # Replace bill_id and unit_price as needed
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('create_bill'))

    return render_template('createbill.html')


# Route for the contact page
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        # Store contact info in the database
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)", (name, email, message))
        mysql.connection.commit()
        cur.close()
        
        return redirect(url_for('index', message="Thank you for contacting us!"))

    return render_template('contact.html')



# Route for the settings page
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    username = session.get('username', 'Guest')
    email = "admin@example.com"  # Replace with real email from database if needed

    if request.method == 'POST':
        # Here, you would add code to update the user's settings in the database
        new_username = request.form['username']
        new_email = request.form['email']
        new_password = request.form['password']  # Optional

        # Update the database logic goes here
        # Example: update users set username = %s, email = %s where id = %s

        # Flash success message or redirect after saving
        return redirect(url_for('settings', message="Settings updated successfully!"))

    return render_template('settings.html', username=username, email=email)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')  # Renders the dashboard.html template

@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove user ID from session
    flash("You have been logged out.")
    return redirect(url_for('login'))  


@app.route('/view_bills')
def view_bills():
    # Connect to the database
    db = MySQLdb.connect(host='localhost', user='root', password='CHintan123!@#', database='ebill')
    cur = db.cursor()

    # Modify your query to exclude created_at if it's not present
    cur.execute("SELECT * FROM items")
    bills = cur.fetchall()

    # Close the cursor and connection
    cur.close()
    db.close()

    return render_template('view_bills.html', bills=bills)

@app.route('/profile')
def profile():
    return render_template('profile.html')

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
