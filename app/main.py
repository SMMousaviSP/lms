from flask import Flask, render_template, request, redirect, flash, url_for, session
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from . import model


app = Flask(__name__)
app.config["SECRET_KEY"] = "Wfd8do6H7d74vdesbuRLlMFiAeXeJ7r"
# Flask login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message_category = "danger"


class User(UserMixin):
    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return f"<{self.id}>"


@login_manager.user_loader
def load_user(userid):
    return User(userid)


@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/login/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash(f"You are currently logged in", "primary")
        return redirect(url_for("index"))
    if request.method == "POST":
        Username = request.form.get("Username", "")
        Password = request.form.get("Password", "")
        success, message, raw_user = model.check_login(Username, Password)
        if success:
            login_user(User(raw_user["ID"]))
            session['User'] = raw_user
            return redirect("/")
        else:
            flash(message, "warning")
            return redirect(url_for("login"))
    return render_template("login.html")


@app.route("/logout/")
@login_required
def logout():
    logout_user()
    flash("You have logged out successfully", "success")
    return redirect(url_for("login"))


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
        flash(message, "warning")
    return render_template("register.html")

@app.route('/profile/')
@login_required
def profile():
    pass
