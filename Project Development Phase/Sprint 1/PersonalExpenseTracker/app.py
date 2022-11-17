from flask import Flask,render_template,request,flash,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from flask_bcrypt import Bcrypt
from flask_login import LoginManager,login_user,current_user,login_required,logout_user
app = Flask(__name__)
login_manager = LoginManager(app)
app.config['SECRET_KEY'] = 'c\xae_O#H\xbdjTD\xed\xcf\x9e\x0f\xa3,\xbb\xcd:\x08\x05\xb8>\x18'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
login_manager.login_view = "login"
from .models import User

@app.route("/home")
@login_required
def home():
	return render_template("home.html")

@app.route("/")
def hello():
	return "Hello World"

@app.route("/dashboard")
@login_required
def dashboard():
	return render_template("dashboard.html")
@app.route("/login",methods=["POST","GET"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for("home"))
	if request.method == "POST":
		email = request.form.get("email",'').lower()
		password = request.form.get("password",'')
		user = User.query.filter_by(email=email).first()
		obj = Bcrypt()
		redirect_to = request.args.get("next","/home")
		if user and obj.check_password_hash(user.password,password):
			login_user(user,remember=True)
			return redirect(redirect_to)
		else:
			flash("Invalid credentials",'error')
	return render_template("login.html")

@app.route("/signup",methods=["GET","POST"])
def signup():
	from .validators import UserValidator
	if current_user.is_authenticated:
		return redirect(url_for("home"))
	if request.method=="POST":
		# Validation code for signup page
		firstName = request.form.get("firstName",'')
		lastName = request.form.get("lastName","")
		userName = request.form.get("userName",'')
		email = request.form.get("email",'').lower()
		password = request.form.get("password",'')
		msg = UserValidator()
		msg = msg.validate(firstName,lastName,userName,email,password)
		if msg==True:
			obj = Bcrypt()
			pwd = obj.generate_password_hash(password).decode("utf-8")
			user = User(firstName=firstName,lastName=lastName,email=email,userName=userName,password=pwd)
			db.session.add(user)
			db.session.commit()
			flash("Account created successfully",'success')
			return redirect(url_for("login"))
		else:
			flash(msg,'error')
	return render_template("signup.html")

@app.route("/logout",methods=["POST","GET"])
def logout():
	logout_user()
	return redirect(url_for("login"))