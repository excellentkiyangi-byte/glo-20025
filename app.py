import MySQLdb.cursors
from flask import Flask, redirect, render_template, session, request, flash, url_for
from flask_mysqldb import MySQL
from datetime import datetime
from config import password
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = "--------"
app.config['MYSQL_DB'] = "carwash_db"
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = password
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


# ============================================= User Interface ========================================================

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/service')
def service():
    return render_template('service.html')


@app.route('/offers', methods=['GET', 'POST'])
def offers():
    if request.method == "POST" and 'firstname' in request.form and 'lastname' in request.form and 'email' in request.form:
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM abonnee WHERE email = %s", (email,))
        unique_email = cursor.fetchone()
        if unique_email:
            flash('You are already subscribed to our Newsletters and Offers! Thank you!')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            pass
        else:
            cursor.execute("INSERT INTO abonnee VALUES (NULL, %s, %s, %s)", (firstname, lastname, email))
            mysql.connection.commit()
            flash("You have been successfully subscribed to our NewsLetters and Offers")
    return render_template('offers.html')


@app.route('/membership', methods=['GET', 'POST'])
def membership():
    if request.method == "POST":
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        city = request.form['city']
        postalcod = request.form['postalcod']
        country = request.form['country']
        gender = request.form['gender']
        offer = request.form['offertype']
        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash("Wrong email address!")
        elif re.match(r'\D', phone):
            flash('Wrong phone number')
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("INSERT INTO membership VALUES (NULL, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                           (firstname, lastname, email, phone, address, city, postalcod, country, offer, gender))
            mysql.connection.commit()
            flash("Order Received!")
    return render_template("membership.html")


@app.route('/reservation', methods=['GET', 'POST'])
def reservation():
    current_day = datetime.now().strftime("%Y-%m-%d")
    if request.method == "POST":
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        phone = request.form['phone']
        carmake = request.form['carmake']
        cartype = request.form['cartype']
        regnumber = request.form['regnumber']
        branch = request.form['branch']
        service = request.form['service']
        date = request.form['date']
        time = request.form['time']
        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash("Wrong Email")
        elif re.match(r'\D', phone):
            flash('Wrong phone number')
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("INSERT INTO reservations VALUES (NULL, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (
                firstname, lastname, email, phone, carmake, cartype, regnumber, branch, service, date, time))
            mysql.connection.commit()
            flash("Order placed with Success!")
    return render_template("reservations.html", current_day=current_day)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == "POST" and 'firstname' in request.form and 'lastname' in request.form and 'email' in \
            request.form and 'phone' in request.form:
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash("Wrong email address!")
        else:
            cursor.execute("INSERT INTO contact VALUES (NULL, %s, %s, %s, %s, %s)",
                           (firstname, lastname, email, phone, message))
            mysql.connection.commit()
            flash("Message sent with success!")
    return render_template("contact.html")


# ========================================= Employee Interface ========================================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST" and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['uid']
            session['username'] = account['username']
            flash("Logged in with success!")
            return render_template('employee.html')
        else:
            flash('Wrong username/password! Please, check your credentials!')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route('/employee')
def employee():
    if 'loggedin' in session:
        return render_template('employee.html')
    else:
        return '<h1>NOT AUTHORIZED!</h1>'


@app.route('/employee/reservations')
def employee_reservations():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT id,firstname,lastname,carmake,regnr FROM reservations ORDER BY id DESC")
        reservations_list = cursor.fetchall()
        return render_template('employee-reservations.html', reservations_list=reservations_list)
    else:
        return '<h1>NOT AUTHORIZED!</h1>'


@app.route('/employee/reservations/<int:id>')
def employee_reservations_detailed(id):
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM reservations WHERE id = %s", (id,))
        customer = cursor.fetchone()
        return render_template('reservation_details.html', customer=customer)
    else:
        return '<h1>NOT AUTHORIZED!</h1>'


@app.route('/employee/support_center')
def employee_support_center():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT id, firstname, lastname FROM contact ORDER BY id DESC")
        ticket_list = cursor.fetchall()
        return render_template('employee-support_center.html', ticket_list=ticket_list)
    else:
        return '<h1>NOT AUTHORIZED!</h1>'


@app.route('/employee/support_center/<int:id>')
def employee_support_center_ticket_details(id):
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM contact WHERE id = %s", (id,))
        ticket = cursor.fetchone()
        return render_template('support_ticket.html', ticket=ticket)
    else:
        return '<h1>NOT AUTHORIZED!</h1>'


@app.route('/employee/members')
def employee_members():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT id, firstname, lastname FROM membres ORDER BY id ASC")
        member_list = cursor.fetchall()
        return render_template('employee-members.html', member_list=member_list)
    else:
        return '<h1>NOT AUTHORIZED!</h1>'


@app.route('/employee/members/<int:id>')
def employee_members_details(id):
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM membres WHERE id = %s", (id,))
        member = cursor.fetchone()
        return render_template("member_details.html", member=member)


if __name__ == '__main__':
    app.run(debug=True)
