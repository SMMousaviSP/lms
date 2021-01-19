from flask import Flask, render_template, request, redirect, flash, url_for
from . import model


app = Flask(__name__)
# Secret key should be changed in the development
app.config["SECRET_KEY"] = "gPo4xFh0KnZsUbf2cOXAC9RxdBA2VSEI"


@app.route("/")
def index():
    return render_template("base.html")


@app.route("/login/")
def login():
    return render_template("login.html")


@app.route("/logout/")
def logout():
    pass


@app.route("/register/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        Username = request.form.get("Username", "")
        Password = request.form.get("Password", "")
        LastName = request.form.get("LastName", "")
        FirstName = request.form.get("FirstName", "")
        PhoneNumber = request.form.get("PhoneNumber", "")
        Email = request.form.get("Email", "")
        Faculty = request.form.get("Faculty", "")
        Institution = request.form.get("Institution", "")
        Address = request.form.get("Address", "")
        success, message = model.create_user(
            Username=Username,
            Password=Password,
            LastName=LastName,
            FirstName=FirstName,
            PhoneNumber=PhoneNumber,
            Email=Email,
            Faculty=Faculty,
            Institution=Institution,
            Address=Address,
        )
        if success:
            flash(
                "Your account has been created successfully, you can login now.",
                "success",
            )
            return redirect(url_for("login"))
        flash(message, 'warning')
    return render_template("register.html")
