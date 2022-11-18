from flask import Flask,render_template,request,flash,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from flask_bcrypt import Bcrypt
from flask_login import LoginManager,login_user,current_user,login_required,logout_user,current_user
app = Flask(__name__)
login_manager = LoginManager(app)
app.config['SECRET_KEY'] = 'c\xae_O#H\xbdjTD\xed\xcf\x9e\x0f\xa3,\xbb\xcd:\x08\x05\xb8>\x18'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
login_manager.login_view = "login"
from .models import User,Category,Budget

@app.route("/dashboard")
@login_required
def dashboard():
	if request.method=="POST":
		bud = Budget()
	return render_template("dashboard.html",budgets= Budget.query.order_by(Budget.id.desc()).filter_by(user=current_user.id))

@app.route("/")
def hello():
	return "Personal Expense Tracker"

@app.route("/login",methods=["POST","GET"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for("dashboard"))
	if request.method == "POST":
		email = request.form.get("email",'').lower()
		password = request.form.get("password",'')
		user = User.query.filter_by(email=email).first()
		obj = Bcrypt()
		redirect_to = request.args.get("next","/dashboard")
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
		return redirect(url_for("dashboard"))
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

@app.route("/create-budget",methods=["POST","GET"])
@login_required
def createBudget():
	if request.method=="POST":
		from .models import Budget
		budget = Budget(name=request.form.get("name"),amount=request.form.get("amount"),user=User.query.filter_by(id=current_user.id).first().id,is_active=True)
		db.session.add(budget)
		db.session.commit()
		totalCategory = Category(amount = request.form.get("amount"),category="Total",budget=budget.id)
		db.session.add(totalCategory)
		db.session.commit()
		flash("Created budget successfully")
		return redirect("dashboard")
	return render_template("addbudget.html")
@app.route("/budget/<id>/",methods=["GET"])
def budgetID(id):
	return render_template("budgetID.html",budget=Budget.query.get(id))

@app.route("/budget/<id>/delete")
def deleteBudget(id):
	budget = Budget.query.get(id)
	db.session.delete(budget)
	db.session.commit()
	flash("Budget deleted successfully")
	return redirect(url_for("dashboard"))