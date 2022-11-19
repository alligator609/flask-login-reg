from flask import Flask, render_template, request, redirect, flash, session
from werkzeug.utils import secure_filename
import os
from flask_mysqldb import MySQL
 
app = Flask(__name__)
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345678'
app.config['MYSQL_DB'] = 'flask'
 
mysql = MySQL(app)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

""" app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = 'static/upload/'

conn = mysql.connector.connect(host="localhost", user="root", password="", database="ome")
cursor = conn.cursor() """


@app.route('/')
def hello():
    return redirect('/login')
@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        details = request.form
        username = details['email']
        password = details['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s AND password = %s", (username, password))
        account = cur.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            session['email'] = account[1]
            return redirect('/home')
        else:
            error = 'Incorrect email/password!'
    return render_template('login.html', error=error)


def ender_template( ):
    return ender_template('registration.html')

@app.route('/registration', methods = ['POST', 'GET'])
def registration():
    if request.method == 'GET':
            return render_template('registration.html')
     
    if request.method == 'POST':
        firstname = request.form['firstname'] 
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        address = request.form.get('address')
        contactno = request.form.get('contactno')
        password = request.form.get('password')
        confirmpassword = request.form.get('confirmpassword')

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(firstname, lastname, email, address, contactno, password) VALUES (%s, %s, %s, %s, %s, %s)", (firstname, lastname, email, address, contactno, password))
        mysql.connection.commit()
        cur.close()
        return redirect('/login')


@app.route('/home')
def home():
    if 'email' in session:
        return render_template('home.html')
    else:
        return redirect('/')
@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/')

@app.route('/accassories')
def accassories():
    return render_template('accassories.html')

@app.route('/gifts')
def gifts():
    return render_template('gifts.html')

@app.route('/houseware_item')
def houseware_item():
    return render_template('houseware_item.html')

@app.route('/student_essential')
def student_essential():
    return render_template('student_essential.html')
    



if __name__=="__main__":
    app.run(debug=True)