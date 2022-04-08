from typing import List
from datetime import datetime, timedelta
from enum import unique
from urllib.request import Request
from flask import Flask, render_template, url_for, flash, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from markupsafe import Markup


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///assignment3.db'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes = 60)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
#------------------------------------ Models ------------------------------------#

class User(db.Model): #Creation/Query works.
    __tablename__ = 'User'
    uid = db.Column(db.Integer, primary_key = True, unique = True, nullable = False) #Utorid equilvant [For login]
    password = db.Column(db.String(20), nullable = False) #[for login]
    first_name = db.Column(db.String(20), nullable = False)
    last_name =  db.Column(db.String(20), nullable = False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    account_type = db.Column(db.String(20), nullable = False) #student,teacher

    def __init__(self, uid, password, first_name,last_name, email, account_type):
        self.uid = uid
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.account_type = account_type

    def get_user_info(self):#We dont wanna return password hash
        return {"uid": self.uid, "first_name": self.first_name, "last_name": self.last_name, "email": self.email, "account_type": self.account_type, "password": self.password}
        
    def get_user_preview(self):
        return {"uid": self.uid, "first_name": self.first_name, "last_name": self.last_name}

    def get_teacher_details(self):
        return self.first_name + ' ' + self.last_name


    def __repr__(self):
        return f"User('{self.uid}', '{self.first_name}', '{self.last_name}', '{self.account_type}')"

class StudentMarks(db.Model): #Creation/Query not tested but should work.
    __tablename__ = 'StudentMarks'
    #Student UserID
    uid = db.Column(db.Integer, db.ForeignKey('User.uid'),primary_key = True, nullable = False)
    #Assignment Marks
    A1 = db.Column(db.Integer,nullable = True)
    A2 = db.Column(db.Integer,nullable = True)
    A3 = db.Column(db.Integer,nullable = True)
    #Lab Marks
    Lab1 = db.Column(db.Integer,nullable = True)
    Lab2 = db.Column(db.Integer,nullable = True)
    Lab3 = db.Column(db.Integer,nullable = True)
    #Exan Marks
    Midterm = db.Column(db.Integer,nullable = True)
    Final = db.Column(db.Integer,nullable = True)
    
    def __init__(self, uid, Assignment1, Assignment2, Assignment3, Lab1, Lab2, Lab3, Midterm, Final):
        self.uid = uid #int
        self.A1 = Assignment1
        self.A2 = Assignment2
        self.A3 = Assignment3
        self.Lab1 = Lab1
        self.Lab2 = Lab2
        self.Lab3 = Lab3
        self.Midterm = Midterm
        self.Final = Final

    def get_mark_info(self):
        return {"uid": self.uid, "A1": self.A1, "A2": self.A2, "A3":self.A3, "Lab1": self.Lab1, "Lab2": self.Lab2,  "Lab3": self.Lab3, "Midterm":self.Midterm, "Final": self.Final}

        
    def __repr__(self):
        return f"StudentMarks('{self.uid}')"


class RegradeRequests(db.Model): #Creation/Query works. RegradeRequests.uid
    __tablename__ = 'RegradeRequests'
    req_id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, nullable = False, unique = False)
    assessmentRequestType = db.Column(db.String(300), nullable=False, unique = False) #What assignment do they want a remark on. 
    comment = db.Column(db.String(300), nullable=False, unique = False)

    def __init__(self, uid, assessmentRequestType, comment):
        self.uid = uid
        self.assessmentRequestType = assessmentRequestType
        self.comment = comment

    def getRegradeRequestInfo(self):
        return {"uid": self.uid, "assessmentRequestType": self.assessmentRequestType, "comment": self.comment}
    def __repr__(self):
        return f"RegradeRequests('{self.uid}', '{self.assessmentRequestType}', '{self.comment}')"

class FeedBack(db.Model): #Creation/Query works. RegradeRequests.uid
    __tablename__ = 'FeedBack'
    feedbackid = db.Column(db.Integer, primary_key=True) #Anon
    Q1feedback = db.Column(db.String(300), nullable=False, unique = False) 
    Q2feedback = db.Column(db.String(300), nullable=False, unique = False)
    Q3feedback = db.Column(db.String(300), nullable=False, unique = False)
    Q4feedback = db.Column(db.String(300), nullable=False, unique = False)
    uid = db.Column(db.Integer, db.ForeignKey('User.uid'),primary_key = True, nullable = False)
    def __init__(self, Q1feedback, Q2feedback, Q3feedback, Q4feedback,uid):
        self.Q1feedback = Q1feedback
        self.Q2feedback = Q2feedback
        self.Q3feedback = Q3feedback
        self.Q4feedback = Q4feedback
        self.uid = uid

    def getFeedBackInfo(self):
        return {"Q1feedback": self.Q1feedback, "Q2feedback": self.Q2feedback, "Q3feedback": self.Q3feedback, "Q4feedback": self.Q4feedback, "uid": self.uid}


    def __repr__(self):
        return f"FeedBack('{self.Q1feedback}', '{self.Q2feedback}','{self.Q3feedback}','{self.Q4feedback}','{self.uid}')"

#------------------------------------ Routes ------------------------------------#

#------------------------------------ DEBUG CODE---------------------------------#
#Sample code to help assist with development
#To see how it all works
#username = '205020521'
# password = 'ohmama'
@app.route("/debug/add")
def add_user_debug():
    #Test code on how adding user to a database works
    # username = '205020521'
    # password = 'ohmama'
    # hashed_password =  bcrypt.generate_password_hash(password).decode('utf8')
    # firstname = 'ryangod'
    # lastname = 'jgod'
    # email = "name3@google.com"
    # account_type = 'admin'

    # me = User(username,hashed_password, firstname, lastname, email, account_type) #We first have to create an object of the User, and fill it up
    # db.session.add(me) #U have to save it in a database session log, [different from user auth sessions]
    # db.session.commit() #Then u commit to have the changes in db.dession applied to commit
    usernamee = '10201022'
    passwordd = 'hellolol'
    hashed_passwordd = bcrypt.generate_password_hash(passwordd).decode('utf8')
    firstnamee = 'hellolol'
    lastnamee = 'worldlol'
    emaill = "helloworldlol@gmail.com"
    account_typee = 'admin'
    mee = User(usernamee,hashed_passwordd,firstnamee,lastnamee,emaill,account_typee)
    db.session.add(mee)
    db.session.commit()
    return "added successfully"

@app.route("/debug/readUsers")
def readUsers_debug():
    #Test code on dumping everything in database. 
    result = User.query.all() #Queries all users
    user_dict = [] 
    for user in result: #For each user object in db
        account = user.get_user_info() #call helper function in class
        user_dict.append(account) #add that to user dict
    return str(user_dict)

@app.route("/debug/readMarks")
def readMarks_debug():
    #Test code on dumping everything in database. 
    result = StudentMarks.query.all() #Queries all users
    user_dict = [] 
    for user in result: #For each user object in db
        account = user.get_mark_info() #call helper function in class
        user_dict.append(account) #add that to user dict
    return str(user_dict)



@app.route("/debug/readUsersSpecificByFilter")
def readUsersQuery_debug():
    #If we want a column to have a specific value. #We need the .all() o/w it just retuns an sql query in results
    result = User.query.filter_by(uid = '123234', account_type='admin').all()
    return str(result)

@app.route("/debug/readUsersSpecificByFilterAndGetValue")
def readUsersQueryBySpecificValue_debug():
    #If we want a column to have a specific value. #We need the .all() o/w it just retuns an sql query in results
    #Result is an array of user objects that matches the follow query
    result = User.query.filter_by(uid = '123234', account_type='admin').all()
    #get the first element in results
    #Result[0] is a User type object.
    #Call get_user_info in the class to extract all information about user object
    #it returns a hash map where we can just get the exact information we want. 
    name = result[0].get_user_info()

    return str(name)

@app.route("/whosLoggedIn")
def whosLoggedIn():
    if 'name' in session:
         return session['name']
    return "Nobody is logged in"


#--------------------------------------Debug Code END ---------------------------------#
#Main Route Code
#Rules
#Do not do any calculation or manipulation of data in the routes function
# The route function must only accept return values from functions
# Or call other functions with params. 
# The route should take input from form/post/get requests, sends it to the function to do work
# and return the results as a html_render.

@app.route("/login", methods = ['GET','POST'])
def login():
    #If its a POST request it means the user entered detail on the login form and entered
    #If its a get request it means that the user vistited the login page. 
    #added this
    if 'name' in session:
        return redirect(url_for('home'))
    ##
    result = ''
    if request.method == 'POST':
        username = request.form.get('uid')
        password = request.form.get('password')
        result = check_login(username, password)
        
        if(result):
            return redirect(url_for('home'))
        else:
            result = 'Incorrect credentials. Try again.'
    
    return render_template('login.html', msg = result)


@app.route("/logout")
def logout():
    session.pop('name', default = None)
    return redirect(url_for('login'))
    
@app.route("/")
def home():
    if 'name' not in session:
        return redirect(url_for('login'))
        
    return render_template('home.html', pagename = "B20 Home")



@app.route("/register", methods = ['GET','POST'])
def register():
    if 'name' in session:
        return redirect(url_for('home'))
    msg_holder = ''
    if request.method == 'POST': #Check if its post, o/w default to get
        username = request.form.get('userid') #UID
        password = request.form.get('password')
        first_name = request.form.get('firstname')
        last_name = request.form.get('lastname')
        email  = request.form.get('email')
        
        nonempty_fields = has_empty_input(username, password, first_name,last_name, email)
        uid_exists = user_id_exists(username) #If true then uid doesn't exist [good]
        email_exists = email_taken(email)


        if(nonempty_fields): #hows it looking W
            msg_holder = 'Make sure the fields are not empty'
            print("Make sure the fields are not empty")
        elif(not(validID(username))):
            msg_holder = 'Your Student ID must be digits only'
        elif(uid_exists):
            msg_holder = 'User ID already exists'
            print("UserID already exists")
        elif(email_exists):
            msg_holder = 'Email is already taken.'
            print("Email already exists")
        elif '@' not in email:
            msg_holder = 'Please provide a valid email'
            print("Please provide a valid email")
        # regex 
        # @ryan is this elif not good enough?
        else:#Checks are good, create account and redirect to homepage. 
            create_user(username, password, first_name, last_name, email)
            check_login(username, password) #Correct password by precondition
            return redirect(url_for('home'))
    return render_template('register.html', msg = msg_holder)
        

@app.route("/home")
def homepage():
    if 'name' not in session:
        return redirect(url_for('login'))
    else:
        return render_template('home.html')

@app.route("/syllabus")
def syllabus():
    if 'name' not in session:
        return redirect(url_for('login'))
    else:
        return render_template('syllabus.html')

@app.route("/assignments")
def assignments():
    if 'name' not in session:
        return redirect(url_for('login'))
    else:
        return render_template('assignments.html')

@app.route("/labs")
def labs():
    if 'name' not in session:
        return redirect(url_for('login'))
    else:
        return render_template('labs.html')


@app.route("/grades", methods = ['GET','POST']) 
def mark_page():
    if 'name' not in session:
        return redirect(url_for('login'))
    user_role =  session['name']['account_type']
    if(user_role == 'student'):
        result = getMarkList(session['name']['uid'])
        result.pop('uid')
        return render_template('studentmarkview.html', marks = result)
    
    user = readUsers() #gives us a set of all users
    regrade = readRegrade()

    return render_template('teachersearch.html', user_list = user, regrade_req = regrade)


@app.route("/grades/<id>", methods = ['GET','POST']) 
def mark_page_generic(id):
    if 'name' not in session:
        return redirect(url_for('login'))
    user_role =  session['name']['account_type']

    if(user_role == 'student'):
        return redirect(url_for('mark_page'))
    sanitized_id = 0
    try:
        sanitized_id = int(id)
    except:
        return redirect(url_for('mark_page'))
    #Check if its a valid id. 
    exist = user_id_exists(sanitized_id)
    if(not(exist)):
        return redirect(url_for('mark_page'))


    result = getMarkList(id)
    result.pop('uid')
    
    if request.method == 'POST': #Check if its post, o/w default to get
        assessment = request.form.get('assign-name') #UID
        new_mark = request.form.get('new-mark')
        status = updateMark(assessment, new_mark, sanitized_id)
        if(status == True):
            flash('Mark has been updated sucessfully.')
            result = getMarkList(id)
            result.pop('uid')

            return render_template('teachermarkview.html', marks = result, id = id)
        else:
            flash('Invalid Assignment Name and/or Mark Entered')
            return render_template('teachermarkview.html', marks = result, id = id)
    

    return render_template('teachermarkview.html', marks = result, id = id)



def updateMark(assignment:str, newMark:int, student_id:int)->bool:
    #Get the id, of the student
    #Get the account detail
    try:
        account = StudentMarks.query.filter_by(uid = student_id).first() 
        assignment = assignment.lower()
        assignment = assignment.capitalize()
        newMark = int(newMark)
    except:
        return False

    if(newMark == None or newMark == '' or  newMark >= 101 or newMark <= -1):
        return False

    try:
        print(str(account), assignment, newMark)
        print(str(dir(account)))
        setattr(account, assignment, newMark)
        db.session.commit()
    except Exception as e:
        print(e)

        return False

    return True




#how do i update given a column name 

def readUsers() -> List[List]: #Returns a list of dicts of all students in the db
    result = User.query.filter_by(account_type='student').all() #Queries all users that are students
    user_dict = []
    for user in result:
        account = user.get_user_preview()
        user_dict.append(account)
    return user_dict

def readRegrade() -> List[List]: #Returns a list of dicts of all students in the db
    result = RegradeRequests.query.all() #Queries all users
    regrade_dict = []
    for regrade in result:
        request = regrade.getRegradeRequestInfo()
        regrade_dict.append(request)
    return regrade_dict

def readFeedback() -> List[List]: #Returns a list of dicts of all students in the db
    result = FeedBack.query.all() #Queries all users
    feedback_dict = []
    for feedback in result:
        studentfeedback = feedback.
        feedback_dict.append(request)
    return regrade_dict



#its on now
#yo debug mode is off
#Teachers Mark View

#Show All Regrade Requests
#Show all Students 


#Teacher Single View
#-> Show students grades
#-> Add ability to upgrade Grades
#-> Show students regrade Requests



#If the person for somereason went to this url, then redirect them to the mark page. 
#Only post requests can be done.
@app.route("/markSendRegrade", methods = ['POST']) 
def sendRegrade():
    #Check if name in session
    #Check if student type
    if 'name' not in session:
        return redirect(url_for('login'))

    if request.method == 'GET':
        return redirect(url_for('login'))

    type = request.form.get('EvaluationName') #UID
    reason = request.form.get('reason')
    uid = session['name']['uid']
    #ook
    ##can u add our navbar logo from a2 into images 
    regradeObj =  RegradeRequests(uid, type, reason) #i'm gonna change the param to uid

    try:
        db.session.add(regradeObj)
        db.session.commit()
    except Exception as e:
        print(e)

    return redirect(url_for('mark_page'))



#-------------------------------------------------------------------------------------------------------#





#-------------------------------------------------------------------------------------------------------#


@app.route("/studentfeedback", methods = ['GET','POST']) 
def StudentFeedback():# should i off it
    if 'name' not in session:
        return redirect(url_for('login'))

    result = User.query.filter(User.account_type.like('admin'))
    teachers = []
    for user in result:
        account = user.get_teacher_details()
        teachers.append(account)

    if request.method == 'POST':
        Q1Answer = request.form.get('Question1') 
        Q2Answer = request.form.get('Question2')
        Q3Answer = request.form.get('Question3')
        Q4Answer = request.form.get('Question4')
        uid = request.form.get('ChooseTeacher')
        FeedbackObj = FeedBack(Q1Answer,Q2Answer,Q3Answer,Q4Answer,uid)
        db.session.add(FeedbackObj)
        db.session.commit()
        return render_template('studentfeedbackview.html', teachers = teachers)

    return render_template('studentfeedbackview.html', teachers = teachers)
    
    #test it
#--------------------------------------Helper Functions ---------------------------------#
# why this shiot keep reverting i cant even do anything frontend cuz of this 
#idk why but the statements keep getting edited in this func
#haunted shit hell nah is that u
#yo for this func why is my thing underlined 
#it should be correct no?
#wtf is that syntax error
#now it is me
#i changed it to 100 earlier mb
#nw ima test it
#nah someone changed the default from 0 to 100
#why all my marks 100 did u guys do that
#check if ur keys are sticking or somethin


def getMarkList(username:int):
    #Precondition: username exists and is a student type. 
    #Given a username 
    #iterate through the mark list, and return a html string
    result = StudentMarks.query.filter_by(uid = int(username)) #Query user who has that specific userid
    result = result[0].get_mark_info()
    return result
    


def validID(username:str):
    return username.isdigit()


def has_empty_input(username:str, password:str, first_name:str, last_name:str, email:str)->bool:
    if(username == None or password == None or first_name == None or last_name == None or email == None):

        return True
     
    #Strip
    username = username.strip()
    password = password.strip()
    first_name = first_name.strip()
    last_name = last_name.strip()
    email = email.strip()

    if((len(username) == 0 or  len(password) == 0 or len(first_name) == 0 or len(last_name) == 0 or len(email) == 0)):
        #If any of them are length 0
        return True

    return False

def user_id_exists(uid: int) -> bool: #Checks if the uid is in the database
    uid_exist = User.query.filter_by(uid = uid).first()
    return True if (uid_exist != None) else False

def email_taken(email: str) -> bool: #Checks if the email is in db
    email_exists = User.query.filter_by(email = email).first()
    return True if (email_exists != None) else False


def check_login(uid: str, password: str) -> bool:
    #Gets the userid/password in raw form [Given in param] 
    #Do bcrypt on the provided userid
    #Check if the user exists ie uuid exists in the database by quering password with userid
    #If the result is empty, then return a note saying user or password is not correct
    #If the password is incorrect return the same note

    #If its correct, then add it to the session and send a redirect to the homepage

    if(not(len(uid) and len(password))):
        print("No password entered")
        return False

    if(user_id_exists(uid) == True):
        account = User.query.filter_by(uid = uid).first() 
        account = account.get_user_info()
            
        if not bcrypt.check_password_hash(account['password'], password):
            print("Password is incorrect. Try again.")
            return False
        else:
            print("Login Success")
            session['name'] = account #hashmap of account information
            return True
    else:
        print("Login Failed")
        return False
     
    #yeo, check if user is in the database ye. user will be empty type if it is not in it
    #then hash password and check if its valid only if user exists. 
    #ok
    #use the user_exist function 
    
    
#Registration
#dont touch this code it works fine 
def create_user(username:str, password:str , firstname:str ,lastname:str, email:str) -> str:
    #Test code on how adding user to a database works
    account_type = 'student' #By default. 
    hashed_password =  bcrypt.generate_password_hash(password).decode('utf8')
    user = User(int(username),hashed_password, firstname, lastname, email, account_type) #We first have to create an object of the User, and fill it up
    db.session.add(user) #U have to save it in a database session log, [different from user auth sessions]
    db.session.commit() #Then u commit to have the changes in db.dession applied to commit
    #Add user marking 
    student_mark = StudentMarks(int(username), 0, 0, 0, 0, 0 ,0 ,0 ,0) #Everyone starts off at 0, and earn their grade up.
    db.session.add(student_mark)
    db.session.commit()


    print("Account creation successful")

    return     
#-----------------------------------------------------------------------------------------------------------------------------------#
##Marks section Code



#d

#We put this function on top of any page that we wanna protect, and just check the session 
#If the session is valid ie user is logged in then it does nothing
#Otherwise it just redirects them back to the page.




if __name__ == "__main__":
    app.secret_key = b"secretkey"
    db.create_all() #Creates the tables if it does not already exist.
    app.run(debug=True)
