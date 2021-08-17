#imports-------------------------------------------------------------------------------------------------------
from flask import Blueprint,render_template, request, redirect, url_for, session,flash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import bcrypt #pip install bcrypt https://pypi.org/project/bcrypt/
from database import mysql
from flask_mysqldb import MySQLdb

#create blueprint of customer------------------------------------------------------------------------------------
customer = Blueprint('customer', __name__, url_prefix='/', template_folder='templates',static_folder="static")

#main page index-------------------------------------------------------------------------------------------------
@customer.route('/')
@customer.route('/index')
def customer_index():
    return render_template('customer/index.html')

@customer.route('/profile', methods=["GET", "POST"])
def profile():
    try:
        if request.method == 'POST':
            uid=session['email']
            curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            curl.execute("SELECT * FROM users ")
            user = curl.fetchall()
            curl.close()
            nm = request.form['name']
            em = request.form['email']
            cur = mysql.connection.cursor()
            cur.execute('UPDATE users SET name="{}",email="{}"  WHERE email="{}"'.format(nm,em,uid))
            mysql.connection.commit()
            user = curl.fetchone()
            cur.close()
            session['name'] = nm
            session['email'] = em
            
            flash('profile update successful')
            return redirect(url_for('.customer_index'))
        else:
            return render_template('customer/index.html')
    except:
        flash('Mail already exist')
        return redirect(url_for('customer.customer_index'))

# customer registration----------------------------------------------------------------------------------------
@customer.route('/register', methods=["GET", "POST"]) 
def register():
    try:
        if request.method == 'GET':
            return render_template("customer/register.html")
        elif request.method == 'POST':
            curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            curl.execute("SELECT * FROM users")
            user = curl.fetchall()
            curl.close()
            if request.form['email'] == user:
                flash('Mail already exist')
                return redirect(url_for('customer.register'))
            else:
                name = request.form['name']
                email = request.form['email']
                password = request.form['password'].encode('utf-8')
                hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO users (name, email, password) VALUES (%s,%s,%s)",(name,email,hash_password,))
                mysql.connection.commit()
                cur.close()

                session['name'] = request.form['name']
                session['email'] = request.form['email']
                flash('register successful')
                return redirect(url_for('customer.customer_index'))
    except:
        flash('Mail already exist')  
        return redirect(url_for('customer.register'))

# customer login---------------------------------------------------------------------------------------------------------
@customer.route('/login',methods=["GET","POST"])
def cu_login():
    # try:
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password'].encode('utf-8')

            curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            curl.execute("SELECT * FROM users WHERE email=%s",(email,))
            user = curl.fetchone()
            curl.close()

            if (user):
                if bcrypt.hashpw(password, user["password"].encode('utf-8')) == user["password"].encode('utf-8'):
                    session['name'] = user['name']
                    session['email'] = user['email']
                    return render_template("customer/index.html")
                else:
                    flash('Error password and email not match')
                    return redirect(url_for('customer.cu_login'))
            else:
                flash('user not found! please register.')
                return redirect(url_for('customer.cu_login'))

        else:
            return render_template("customer/index.html")
    # except:
        flash("server busy, try again later...")
        return render_template("customer/index.html")

#reset password---------------------------------------------------------------------------------------------------
@customer.route('/reset_request')
def reset_request():
    return render_template("customer/reset_request.html")

#courier transaction---------------------------------------------------------------------------------------------
@customer.route('/transaction')
def transaction():
    
    return render_template("customer/transaction.html")

# customer logout-----------------------------------------------------------------------------------------------
@customer.route('/logout')
def logout():
    session.clear()
    return render_template("customer/index.html")

#customer_feedback---------------------------------------------------------------------------------------------------
@customer.route('/feedback', methods=["POST"])
def feedback():
    if request.method == 'POST':   
        cid = ""
        email = request.form['email']
        message  = request.form['message']
        operation = 'feedback'
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO com_feed (cid, email, message, operation) VALUES (%s,%s,%s,%s)",(cid,email,message,operation,))
        mysql.connection.commit()
        cur.close()

        flash('feedback sucssusfull')
        return redirect(url_for('.customer_index'))

#customer_complaint---------------------------------------------------------------------------------------------------
@customer.route('/complaint', methods=["POST"])
def complaint():
    if request.method == 'POST':   

        cid = request.form['cid']
        email = session['email']
        message  = request.form['message']
        operation = 'complaint'
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO com_feed (cid, email, message, operation) VALUES (%s,%s,%s,%s)",(cid,email,message,operation,))
        mysql.connection.commit()
        cur.close()

        flash('compalint sucssusfull')
        return redirect(url_for('.customer_index'))

@customer.route('change_password',methods=['POST'])
def change_password():
    if request.method == 'POST':
        email = session['email']
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM users WHERE email=%s",(email,))
        user = curl.fetchone()
        curl.close()

        password = request.form['old_password'].encode('utf-8')

        if (user):
            if bcrypt.hashpw(password, user["password"].encode('utf-8')) == user["password"].encode('utf-8'):
                new_password = request.form['new_password'].encode('utf-8')
                hash_password = bcrypt.hashpw(new_password, bcrypt.gensalt())

                cur = mysql.connection.cursor()
                cur.execute('UPDATE users SET password="{}" WHERE email="{}"'.format(hash_password,email))
                mysql.connection.commit()
                cur.close()
                flash(print(hash_password))
            else:
                flash('password not match, try again.')    
                return redirect(url_for('.customer_index'))

    return redirect(url_for('.customer_index'))
        
# end of code===================================================================================================
# b'$2b$12$6UmsrTNGb275kY6V19qGMenyIBCT.zSfOZy/RvfV8Q6ULR6UPB6L2'
# $2b$12$sE8WZatMtrrmTZhY6tNfC.8CQvw9cdhg0Bk.9hymhURKy772FxTnq
# b'$2b$12$ZHgvZagdTuH9beY02EZDwePhiiYxFygOm8TYsyWYERsoPWe3ZLIYG'
