# Import libraries
from flask import Flask, render_template, request, url_for, redirect, session, jsonify
from pymongo import MongoClient
import bcrypt
from bson.objectid import ObjectId


app = Flask(__name__)

app.secret_key = "testing"

client = MongoClient('localhost', 27017)

db = client.Technical_Interview
users = db.users


####### Registration#######

@app.route("/registration", methods=['post', 'get'])
def registration():
    message = ''
    if "email" in session:
        return redirect(url_for("profile"))
    if request.method == "POST":
        user = request.form.get("fullname")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user_found = users.find_one({"name": user})
        email_found = users.find_one({"email": email})

        if user_found:
            message = 'There already is a user by that name'
            return render_template('registration.html', message=message)
        if email_found:
            message = 'This email already exists in database'
            return render_template('registration.html', message=message)
        if password1 != password2:
            message = 'Passwords should match!'
            return render_template('registration.html', message=message)
        else:
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
            user_input = {'name': user, 'email': email,
                          'password': hashed, 'balance': 100}
            users.insert_one(user_input)

            user_data = users.find_one({"email": email})
            new_email = user_data['email']

            return render_template('registration.html', email=new_email)
    return render_template('registration.html')


####### Login#######
@app.route("/login", methods=["POST", "GET"])
def login():
    message = 'Please login to your account'
    if "email" in session:
        return redirect(url_for("list_users"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        email_found = users.find_one({"email": email})
        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']

            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                return redirect(url_for('list_users'))
            else:
                if "email" in session:
                    return redirect(url_for("list_users"))
                message = 'Wrong password'
                return render_template('login.html', message=message)
        else:
            message = 'Email not found'
            return render_template('login.html', message=message)
    return render_template('login.html', message=message)



####### Profile #######

@app.route('/profile', methods=('GET', 'POST'))
def profile():
    if request.method == "GET":
        #  get the id of the user to edit
        email = session["email"]

        # get the user details from the db
        user = users.find_one({"email": email})

        # direct to edit user page
        return render_template('profile.html', user=user)

    elif request.method == "POST":

        # get the data of the user
        userId = request.form['_id']

        password = request.form['password']
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # update the data in the db
        user = users.update_one({"_id": ObjectId(userId)}, {
                                "$set": {"password": hashed}})

        return render_template('profile.html', user=user)


####### list of users #######

@app.route('/list-users', methods=('GET', 'POST'))
def list_users():
    all_users = users.find()
    return render_template('list-users.html', users=all_users)


####### Show User Profile #######

@app.route('/show-user-profile/<id>', methods=('GET', 'POST'))
def show_user_profile(id):

    if request.method == "GET":

        # get the id of the user to edit
        userId = request.args.get('form')

        # get the user details from the db
        user = users.find_one({"_id": ObjectId(id)})

        # direct to edit user page
        return render_template('show-user-profile.html', user=user)

    elif request.method == "POST":

        # get the data of the user
        userId = request.form['_id']

        password = request.form['password']
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # update the data in the db
        user = users.update_one({"_id": ObjectId(userId)}, {
                                "$set": {"password": hashed}})

        # redirect to show user profile page
        return render_template('show-user-profile.html', user=user)



####### Send money  #######

@app.route('/send-money/', methods=('GET', 'POST'))
def send_money():

    if request.method == "GET":

        email = session["email"]
        users = db.users

        # get the user details from the db
        user = users.find_one({'email': email})

        # direct to edit user page
        return render_template('send-money.html', user=user)

    elif request.method == "POST":

        # get the data of the user
        userId = request.form['_id']

        balanceAdded = request.form['balance']
        newBalance = int(100) + int(balanceAdded)

        # update the data in the db
        users = db.users
        user = users.update_one({"_id": ObjectId(userId)}, {
            "$set": {"balance": newBalance}})

        users = db.users["name"]

        name = request.form['name']  # form input on initial name

        check_db = users.find()  # check  document in collection
        for i in check_db:
            if (name in i['name']):
                return render_template('send-money.html', user=user)
            else:
                return 'sorry name not found'

        return render_template('send-money.html', user=user)


# logout page
@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
        return render_template("signout.html")
    else:
        return render_template('login.html')


if __name__ == "__main__":

    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    session.init_app(app)

    app.debug = True
    app.run()
