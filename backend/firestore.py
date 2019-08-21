import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth
from flask import *
import pyrebase
import secret


app = Flask(__name__)

# Auth -  getting user idToken
config = {
    "apiKey": secret.SECRET_KEY,
    "authDomain": "flask-auth-84403.firebaseapp.com",
    "databaseURL": "https://flask-auth-84403.firebaseio.com/",
    "storageBucket": "flask-auth-84403.appspot.com",
    "projectId": "flask-auth-84403"

}

firebase = pyrebase.initialize_app(config)
pyreAuth = firebase.auth()


@app.route('/user/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        checkauth = pyreAuth.sign_in_with_email_and_password(email, password)
        id_token = checkauth['idToken']
        verify(id_token)
        if verify(id_token) == "user":
            return redirect('/user/profile')
    return render_template('login.html')


@app.route('/business/login', methods=['GET', 'POST'])
def businesslogin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        checkauth = pyreAuth.sign_in_with_email_and_password(email, password)
        id_token = checkauth['idToken']
        verify(id_token)
        if verify(id_token) == "business":
            return redirect('/business/profile')
    return render_template('businessLogin.html')



def verify(id_token):
    decoded_token = auth.verify_id_token(id_token)
    uid = decoded_token['uid']
    print(uid)
    # check if user/ business
    users_ref = db.collection(u'users')
    userData = users_ref.stream()
    for user in userData:
        if uid in user.id:
            print('user logged in')
            return "user"

    business_ref = db.collection(u'business')
    businessData = business_ref.stream()
    for business in businessData:
        if uid in business.id:
            print('business logged in')
            return "business"


@app.route('/user/profile', methods=['GET', 'POST'])
def userprofile():
    email= "manloengchung@googlemail.com"
    user = auth.get_user_by_email(email)
    # print('Successfully fetched user data: {0}'.format(user.uid))
    return render_template('loggedIn.html')


@app.route('/business/profile', methods=['GET', 'POST'])
def businessprofile():
    email= "manloengchung@googlemail.com"
    user = auth.get_user_by_email(email)
    # print('Successfully fetched user data: {0}'.format(user.uid))
    return render_template('loggedIn.html')


# Admin SDK - setting up for admin privileges
cred = credentials.Certificate("firebase-private-key.json")
default_app = firebase_admin.initialize_app(cred)
# print(default_app)
db = firestore.client()


# adds user
@app.route('/user/signup', methods=['GET', 'POST'])
def usersignup():
    # need to use dynamic information from the frontend submission
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # could add name from req form
        try:
            # creates a new user in firebase (under the hood)
            user = auth.create_user(
                email=email,
                password=password,
                # display_name='John Doe',
            )
            # then logs in
            checkauth = pyreAuth.sign_in_with_email_and_password(email, password)
            # print(checkauth, "<-----")
            localId = checkauth['localId']
            # adds data into our data when user signs up and set up its own user obj
            # needs to be more accept a range of data
            doc_ref = db.collection(u'users').document(localId)
            doc_ref.set({u'email': email, u'name': '', u'avatar_url': 'https://placekitten.com/474/821'})
        except:
            # should print firebase error
            return jsonify({'messsage': "error"})
    return render_template('signup.html')


# adding business
@app.route('/business/signup', methods=['GET', 'POST'])
def businesssignup():
    # need to use dynamic information from the frontend submission
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        try:
            # creates a new user in firebase (under the hood)
            user = auth.create_user(
                email=email,
                password=password,
                display_name=name,
            )
            # then logs in
            checkauth = pyreAuth.sign_in_with_email_and_password(email, password)
            # print(checkauth, "<-----")
            localId = checkauth['localId']
            # adds data into our data when user signs up and set up its own user obj
            # needs to be more accept a range of data
            doc_ref = db.collection(u'business').document(localId)
            doc_ref.set({u'email': email, u'name': name})
        except:
            # should print firebase error
            return jsonify({'messsage': "error"})
    return render_template('businessSignup.html')


# fetches data from db with a where clause
@app.route('/', methods=['GET'])
def user_data():
    users_ref = db.collection(u'users').where(u'first', u'==', 'Ada')
    docs = users_ref.stream()

    for doc in docs:
        print(u'{} => {}'.format(doc.id, doc.to_dict()))
        return jsonify(doc.id, doc.to_dict())