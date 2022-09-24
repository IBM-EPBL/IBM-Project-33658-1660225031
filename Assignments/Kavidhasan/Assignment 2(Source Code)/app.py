from flask import Flask,render_template,flash,request,redirect,url_for
import sqlite3
app = Flask(__name__)
@app.route("/",methods=["GET","POST"])
def signup():
    if (request.method=="POST"):
        rno = request.form.get("rno",'')
        email = request.form.get("email")
        username = request.form.get("username",'')
        password = request.form.get("password",'')

        with sqlite3.connect("users.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO user (roll_number,email,username,password) VALUES (?,?,?,?)",(rno,email,username,password) )
            con.commit()
        return redirect(url_for('login'))
    return render_template("signup.html")
@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        username = request.form.get("username",'')
        password = request.form.get("password",'')
        with sqlite3.connect("users.db") as con:
            cur = con.cursor()
            cur.execute("select * from user where username=(?) and password=(?)",(username,password))
            result = cur.fetchone()
            con.commit()
            if result==None:
                return render_template("login.html",msg="Invalid Username and password")
            else:
                return render_template("home.html",username=result[1])
    return render_template("login.html")


if __name__=="__main__":
    app.run(debug=True)