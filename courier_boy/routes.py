# imports----------------------------------------------------------------------------------------------------------------------
from flask import Blueprint,session,render_template,request,flash,redirect,url_for
from database import mysql
from flask_mysqldb import MySQLdb
import bcrypt

# create blueprint of courier_boy----------------------------------------------------------------------------------------------
courier_boy = Blueprint('courier_boy', __name__, url_prefix='/courier_boy', template_folder='templates',static_folder='static')

# courier boy main page-------------------------------------------------------------------------------------------------------
@courier_boy.route('/')
def courier_boy_index():
    return render_template('courier_boy/index.html')

# courier boy login------------------------------------------------------------------------------------------------------------
@courier_boy.route('/courier_boy/courier_boy_login',methods=["GET","POST"])
@courier_boy.route('/courier_boy_login',methods=["GET","POST"])
def courier_boy_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM courierboylog WHERE email=%s",(email,))
        user = curl.fetchone()
        curl.close()

        if (user):
            if bcrypt.hashpw(password, user["password"].encode('utf-8')) == user["password"].encode('utf-8'):
                session['name'] = user['name']
                session['email'] = user['email']
                return render_template("courier_boy/index.html")
            else:
                flash('email and password not match')
            return redirect(url_for('courier_boy.courier_boy_login'))
        else:
            flash('wrong email id')
            return redirect(url_for('courier_boy.courier_boy_login'))
    else:
        return render_template("courier_boy/courier_boy_login.html")

# courier boy application ------------------------------------------------------------------------------------------------------
@courier_boy.route('courier_boy/courierBoyApplication',methods=["GET","POST"])
@courier_boy.route('/courierBoyApplication',methods=["GET","POST"])
def courierBoyApplication():
    if request.method == 'GET':
            return render_template("courier_boy/courierBoyApplication.html")
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
        cur.execute("INSERT INTO courierboydb (first_name,last_name,email,phone,address,address2,city,state,zip) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",(first_name,last_name,email,phone,address,address2,city,state,zip))
        mysql.connection.commit()
        flash('register successful')
        return redirect(url_for('courier_boy.courierBoyApplication'))

# courier boy forget password----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@courier_boy.route('courier_boy/forget_password')
def forget_password():
    return render_template('courier_boy/forget_password.html')

# courier details----------------------------------------------------------------------------------------------------------------------------------------
@courier_boy.route('/couriers')
def couriers():
    return render_template('courier_boy/couriers.html')

# end of code===========================================================================================================================================