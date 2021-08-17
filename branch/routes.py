# imports--------------------------------------------------------------------------------------------------------
from flask import Blueprint,render_template,request,redirect,url_for,session
import random
from courier.routes import courier
from flask.helpers import flash
from database import mysql
from flask_mysqldb import MySQLdb
import bcrypt

# creation of branch blueprint-----------------------------------------------------------------------------------
branch = Blueprint('branch', __name__, url_prefix='/branch', template_folder='templates',static_folder="static")

# branch index --------------------------------------------------------------------------------------------------
@branch.route('/')
def branch_index():
    return render_template('/branch/index.html')

# existing courier boys-------------------------------------------------------------------------------------------
@branch.route('branch/existing_courierboy')
@branch.route('/existing_courierboy')
def existing_courierboy():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM courierboydb where status="accepted"')
    data = cur.fetchall()
    cur.close()
    return render_template('branch/existing_courierboy.html',contacts = data)

# [delete courier boys]
@branch.route('branch/delete/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('DELETE FROM branchDb WHERE id = {0}'.format(id))
    mysql.connection.commit()
    return redirect(url_for('admin.existing_branch'))

# branch login---------------------------------------------------------------------------------------------------
@branch.route('/branch/branch_login',methods=["GET","POST"])
@branch.route('/branch_login',methods=["GET","POST"])
def branch_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
 
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM branchlog WHERE email=%s",(email,))
        user = curl.fetchone()
        curl.close()
 
        if (user):
            if bcrypt.hashpw(password, user["password"].encode('utf-8')) == user["password"].encode('utf-8'):
                session['name'] = user['name']
                session['email'] = user['email']
                return render_template("branch/index.html")
            else:
                flash('email and password not match')
            return redirect(url_for('branch.branch_login'))
        else:
            flash('wrong email id')
            return redirect(url_for('branch.branch_login'))
    else:
        return render_template("branch/branch_login.html")

# courierboys------------------------------------------------------------------------------------------------------
@branch.route('/courierBoys')
def courierBoys():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM courierboydb where status=""')
    data = cur.fetchall()
    cur.close()
    return render_template('branch/courierBoys.html',contacts = data)

# branch application----------------------------------------------------------------------------------------------
@branch.route('branch/branch_application',methods=["GET","POST"])
@branch.route('branch/branch/branch_application',methods=["GET","POST"])
def branch_application():
    if request.method == 'GET':
        return render_template("branch/branch_application.html")
    else:
        first_name = request.form['first_name'] 
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        address2 = request.form['address2']
        city = request.form['city']
        state = request.form['state']
        zip = request.form['zip']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO branchDb (first_name,last_name,email,phone,address,address2,city,state,zip) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",(first_name,last_name,email,phone,address,address2,city,state,zip))
        mysql.connection.commit()
        flash('register successful')
        return render_template('branch/branch_application.html')

# decline of courier boys application----------------------------------------------------------------------------
@branch.route('branch/decline/<string:id>')
def decline_contact(id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('DELETE FROM courierboydb WHERE id = {0}'.format(id))
    mysql.connection.commit()
    return redirect(url_for('branch.courierBoys'))

# accept of courier boys application----------------------------------------------------------------------------
@branch.route('branch/accept/<string:id>')
def accept(id):
    st="accepted"
    cur = mysql.connection.cursor()
    cur.execute('UPDATE courierboydb SET status="{}" WHERE id={}'.format(st,id))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('branch.courierBoys'))

# trancation---------------------------------------------------------------------------------------------------
@branch.route('/branch/transaction')
@branch.route('/transaction')
def transaction():
    return "transaction"

# end of code==================================================================================================