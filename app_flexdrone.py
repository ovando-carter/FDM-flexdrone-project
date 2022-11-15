from flask_login import login_user, login_required, logout_user, UserMixin, current_user, AnonymousUserMixin
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.exceptions import abort # makes the webpage respond with 404 error if the page does not exsist
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3  # to connect to sqlite3
from datetime import datetime # to modify dates to the SQL standard
from datetime import timedelta
from datetime import date


'''
note: to kill the process running on 5000 use 
npx kill-port 5000
'''

class User(UserMixin):
    def __init__(self, id, fname, lname, active=True):
        self.id = id
        self.fname = fname
        self.lname = lname
        self.active = active

    def is_active(self):
        # Here you should write whatever the code is
        # that checks the database if your user is active
        return self.active

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

#class Anonymous(AnonymousUserMixin):
#    def __init__(self):
#        self.fname = 'Flexdrone'
#        self.lname = 'Guest'

###################################################################################################################################################################################
# Get Data from sign in 
###################################################################################################################################################################################


app = Flask(__name__)

app.secret_key = 'flexdrone'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user_login'

@app.route('/')


def flexdronehome():
    if current_user.is_authenticated:
        return render_template('flexdrone_home.html', fname=current_user.fname, lname=current_user.lname)
    else:
        return render_template('flexdrone_home.html')

#@app.route('/user_signup.html')
#def user_signup():
#
#    return render_template('user_signup.html')


@app.route('/user_signup', methods=('GET', 'POST'))
def user_signup():
    if request.method == 'POST':
        email = request.form['email']
        psw = request.form['psw']
        fname = request.form['fname']
        lname = request.form['lname']
        db = request.form['dateofbirth']
        addressline1 = request.form['addressline1']
        addressline2 = request.form['addressline2']
        town = request.form['town']
        city = request.form['city']
        country = request.form['country']
        postcode = request.form['postcode']
        number1 = request.form['number1']
        number2 = request.form['number2']
        occupation = request.form['occupation']
        flyerID = request.form['flyerID']
        operatorID = request.form['operatorID']
        NAAID = request.form['NAAID']
        
        psw = generate_password_hash(psw, method='sha256') # generates hashed password

        #should send the data to the database.
        connection = sqlite3.connect("./templates/database/flexdrone.db")
        # connection.cursor() returns a Cursor object. 
        # Cursor objects allow us to send SQL statements 
        # to a SQLite database using cursor.execute().
        cursor = connection.cursor()

        # use SQL-parameters to insert the data into to the INSERT statement
        params = (email, psw, db, fname, lname, addressline1, addressline2, town, city, country, postcode,
                  number1, number2, occupation, flyerID, operatorID, NAAID)

        # Insert data into table
        cursor.execute('''INSERT INTO  User (email, psw, Date_of_Birth, First_Name, Last_Name, addressline1, addressline2,
                       town, city, country, postcode, number1, number2, occupation, flyerID, operatorID, NAAID) 
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', params)


        # Save the changes to the database
        connection.commit()
        connection.close()

        # shows me in the terminal that it is in the python code
        #print('inside: ', fname)

        # shows me on the website that the information was saved somewhere
        return render_template('flexdrone_home.html', email=email, psw=psw, fn=fname, ln=lname, db=db, ad1=addressline1, ad2=addressline2, 
                            town=town, city=city, country=country, pc=postcode, num1=number1, num2=number2, 
                            occ=occupation, flyerID=flyerID, operatorID=operatorID, NAAID=NAAID)
    return render_template('user_signup.html')

# either 1. put the sqlite connector inside the get request or 
# 2. return the value and put it outside the getvalue


@app.route('/user_login', methods=('GET', 'POST'))
def user_login():
    if request.method == 'POST':
        email = request.form['email']
        psw = request.form['psw']
        
        connection = sqlite3.connect("./templates/database/flexdrone.db")
        cursor = connection.cursor()

        # use SQL-parameters to insert the data into to the INSERT statement

        # Insert data into table
        user=cursor.execute(" SELECT user_id, psw, first_name, last_name FROM User WHERE email = ?; ", [email]).fetchall()
        connection.close()
        
        if user:
            db_psw=user[0][1]
            user_model=User(user[0][0], user[0][2], user[0][3], True)
        else:
            db_psw=""
            user_model=User("", "", "")
        
        
        if not email or not check_password_hash(db_psw, psw):
            return render_template('user_login.html', Title='Login failed try again')
        else:
            login_user(user_model, remember=True)
            return redirect(url_for('flexdrone_drone', id=1))
    
    return render_template('user_login.html', Title='Login to your account')

@app.route('/user_logout', methods=('GET', 'POST'))
def user_logout():
    logout_user()
    return render_template('user_logout.html')

@app.route('/my_account', methods=('GET', 'POST'))
def my_account():
    id=current_user.id

    connection = sqlite3.connect("./templates/database/flexdrone.db")
    cursor = connection.cursor()
    user=cursor.execute(" SELECT flyerID, operatorID FROM User WHERE user_id = ?; ", [id]).fetchall()
    connection.close()
    
    return render_template('my_account.html', fname=current_user.fname, lname=current_user.lname, fid=user[0][0], oid=user[0][1])

@login_manager.user_loader
def load_user(id):
    
    param = id
    
    connection = sqlite3.connect("./templates/database/flexdrone.db")
    cursor = connection.cursor()

    # use SQL-parameters to insert the data into to the INSERT statement

    # Insert data into table
    user=cursor.execute(" SELECT user_id, psw, first_name, last_name FROM User WHERE user_id = ?; ", [param]).fetchall()
    connection.close()
    
    user_model=User(user[0][0], user[0][2], user[0][3], True)
    
    return User(user_model.id, user_model.fname, user_model.lname)




@app.route('/flexdrone_drone/<int:id>')
def flexdrone_drone(id):
    connection = sqlite3.connect("./templates/database/flexdrone.db")
    cursor = connection.cursor()
    Drone=cursor.execute("SELECT * FROM Drone WHERE drone_id=?", (id,)).fetchall()
    connection.close()
    
    if current_user.is_authenticated:
        return render_template('flexdrone_drone.html', fname=current_user.fname, lname=current_user.lname, drone_name=Drone[0][1],
                               model_number=Drone[0][2], description=Drone[0][3], model_link=Drone[0][9])
    else:
        return render_template('flexdrone_drone.html', drone_name=Drone[0][1], model_number=Drone[0][2], description=Drone[0][3])


@app.route('/terms_and_conditions', methods=('GET', 'POST'))
def terms_and_conditions():
    return render_template('terms_and_conditions.html')



# check out page
#@app.route('/checkout_form.html')
#def checkout_form():
#    
#    return render_template('checkout_form.html')


@app.route('/checkout_form', methods=('GET', 'POST'))
@login_required
def checkout_form():
    if request.method == 'POST':
        # call up user information
        # need to write the code to do this
        email = request.form['email']
        fname = request.form['fname']
        lname = request.form['lname']
        cname = request.form['cname']
        userID = current_user.id

        orderID = 2
        droneID = 1

        # order and delivery date
        purchase_date = date.today()
        delivery_date = purchase_date + timedelta(days=2) # gets the order to them within 2 days

        # billing details
        addressline1 = request.form['baddressline1']
        addressline2 = request.form['baddressline2']
        town = request.form['btown']
        city = request.form['bcity']
        country = request.form['bcountry']
        postcode = request.form['bpostcode']

        # check if the billing address is the same as the delivery address
        billing_is_delivery = request.form['sameadr'] # need to add this to the form
        if billing_is_delivery == 'on':
            # delivery details
            d_addressline1 = addressline1
            d_addressline2 = addressline2
            d_town = town
            d_city = city
            d_country = country
            d_postcode = postcode
        else:
            # delivery details
            d_addressline1 = request.form['daddressline1'] # need to add this to the form
            d_addressline2 = request.form['daddressline2']# need to add this to the form
            d_town = request.form['dtown'] # need to add this to the form
            d_city = request.form['dcity'] # need to add this to the form
            d_country = request.form['dcountry'] # need to add this to the form
            d_postcode = request.form['dpostcode']# need to add this to the form

        # check if the clients wants a delivery or a pick up 
        if request.form['deliver_pickup'] == 'on':
            deliver_pickup = 'Delivery'
        else:
            deliver_pickup = 'Pickup' # need to add this to the form


        # orders 
        order_status = 'Order placed'
        camera_component_id = 1
        landing_component_id = None
        blade_component_id = None
        total = 300.00 # I need to write some code that will calculate the total based on the products they have chosen.
        # could be done with a function that takes in a dictionary of the items and their prices and then adds them together and returns the total. 
        # or each product could be calculated in a function and then the total price summed here. 

        # card details
        cardname = request.form['cardname']
        cardnumber = request.form['cardnumber']
        expmonth = request.form['expmonth']
        expyear = request.form['expyear']
        cvv = request.form['cvv']



        #should send the data to the database.
        connection = sqlite3.connect("./templates/database/flexdrone.db")
        # connection.cursor() returns a Cursor object. 
        # Cursor objects allow us to send SQL statements 
        # to a SQLite database using cursor.execute().
        cursor = connection.cursor()

        # use SQL-parameters to insert the data into to the INSERT statement
        params = (  userID, droneID, camera_component_id, landing_component_id, blade_component_id,  total,
                    deliver_pickup, d_addressline1, d_addressline2, d_town, d_city, d_country, d_postcode,
                    addressline1, addressline2, town, city, country, postcode, purchase_date, delivery_date, order_status,                    
                    cardname, cardnumber, expmonth, expyear, cvv, cname)

        # Insert data into table
        cursor.execute('''INSERT INTO  Orders (user_id, drone_id, camera_component_id, landing_component_id, blade_component_id, total,
                                            deliver_pickup, delivery_address_line_1, delivery_address_line_2, delivery_town, delivery_city,
                                            delivery_country, delivery_postcode, billing_address_line_1, billing_address_line_2, billing_town,
                                            billing_city, billing_country, billing_postcode, purchase_date, delivery_date, order_status,
                                            cardname, cardnumber, expmonth, expyear, cvv, company_name)
                                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', params)


        # Save the changes to the database
        connection.commit()
        
        order_id=cursor.execute("SELECT MAX(order_id) FROM Orders").fetchall()
        
        connection.close()

        return redirect(url_for('order_confirmation', id=order_id[0][0]))

    return render_template('checkout_form.html')


@app.route('/order_confirmation/<int:id>')
def order_confirmation(id):
    
    connection = sqlite3.connect("./templates/database/flexdrone.db")
    cursor = connection.cursor()
    
    order_info=cursor.execute("SELECT * FROM Orders WHERE order_id=?", (id,)).fetchall()
    user_info=cursor.execute("SELECT * FROM User WHERE user_id=?", (order_info[0][1],)).fetchall()
    drone_info=cursor.execute("SELECT * FROM Drone WHERE drone_id=?", (order_info[0][2],)).fetchall()
    if order_info[0][3]:
        cam_component_info=cursor.execute("SELECT * FROM Component WHERE component_id=?", (order_info[0][3],)).fetchall()
    else:
        cam_component_info=None
    if order_info[0][4]:
        land_component_info=cursor.execute("SELECT * FROM Component WHERE component_id=?", (order_info[0][4],)).fetchall()
    else:  
        land_component_info=None
    if order_info[0][5]:
        blade_component_info=cursor.execute("SELECT * FROM Component WHERE component_id=?", (order_info[0][5],)).fetchall()
    else:
        blade_component_info=None
        
    connection.close()
    
    if cam_component_info:
        cn1=cam_component_info[0][1]
    else:
        cn1=None
    if land_component_info:
        cn2=land_component_info[0][1]
    else:
        cn2=None
    if blade_component_info:
        cn3=blade_component_info[0][1]
    else:
        cn3=None
    
    return render_template('order_confirmation.html', fn=user_info[0][4], ln=user_info[0][5], dn=drone_info[0][1], cn1=cn1,
                           cn2=cn2, cn3=cn3, ad1=order_info[0][8], ad2=order_info[0][9],
                           town=order_info[0][10], city=order_info[0][11], country=order_info[0][12], pc=order_info[0][13])



# this allows you to run the flassk app using python3 rather than flask run 
if __name__ == '__main__':
    app.run(debug=True)



