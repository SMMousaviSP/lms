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

    def is_admin(self):
        return bool(session["User"]["is_admin"])

    def __repr__(self):
        return f"<{self.id}>"


@login_manager.user_loader
def load_user(userid):
    return User(userid)


@app.route("/")
@login_required
def index():
    success, message, student_course_list = model.get_student_course_list(
        current_user.id
    )
    if not success:
        flash(message, "warning")
        return redirect(url_for("index"))
    success, message, teacher_course_list = model.get_teacher_course_list(
        current_user.id
    )
    if not success:
        flash(message, "warning")
        return redirect(url_for("index"))
    return render_template(
        "index.html",
        teacher_course_list=teacher_course_list,
        student_course_list=student_course_list,
    )


@app.route("/course/<int:CourseID>")
@login_required
def course(CourseID):
    success, message, is_teacher = model.is_teacher(current_user.id, CourseID)
    if not success:
        flash(message, "warning")
        return redirect(url_for("index"))
    success, message, course_data = model.get_course(CourseID)
    if not success:
        flash(message, "warning")
        return redirect(url_for("index"))
    if not course_data:
        flash("This course does not exist or you don't have access to it", "warning")
        return redirect(url_for("index"))
    success, message, content_list = model.get_content_list(CourseID)
    if not success:
        flash(message, "warning")
        return redirect(url_for("index"))
    return render_template(
        "course.html",
        is_teacher=is_teacher,
        course_data=course_data,
        content_list=content_list,
    )


@app.route("/login/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("You are currently logged in", "primary")
        return redirect(url_for("index"))
    if request.method == "POST":
        Username = request.form.get("Username", "")
        Password = request.form.get("Password", "")
        success, message, raw_user = model.check_login(Username, Password)
        if success:
            login_user(User(raw_user["ID"]))
            session["User"] = raw_user
            success2, message2, is_manager = model.is_manager(current_user.id)
            if success2:
                session["User"]["is_manager"] = is_manager
            else:
                flash(message2, "warning")
                return redirect(url_for("login"))
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


@app.route("/users/")
@login_required
def user_list():
    success, message, user_list = model.get_user_list()
    if not success:
        flash(message, "warning")
        return redirect(url_for("index"))
    return render_template("user_list.html", user_list=user_list)


@app.route("/profile/<int:ID>/", methods=["GET", "POST"])
@login_required
def profile(ID):
    if request.method == "POST":
        Username = request.form.get("Username", "")
        LastName = request.form.get("LastName", "")
        FirstName = request.form.get("FirstName", "")
        PhoneNumber = request.form.get("PhoneNumber", "")
        Email = request.form.get("Email", "")
        Faculty = request.form.get("Faculty", "")
        Institution = request.form.get("Institution", "")
        Address = request.form.get("Address", "")
        success, message = model.edit_user_profile(
            ID=ID,
            Username=Username,
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
                "Profile updated successfully.",
                "success",
            )
            return redirect(url_for("profile", ID=ID))
        flash(message, "warning")
    success, message, raw_user = model.get_user_profile(ID)
    if not success:
        flash(
            "No such user exists, or you don't have access to it's profile.", "warning"
        )
        return redirect(url_for("index"))
    success, message, course_list = model.get_all_course_list()
    if not success:
        flash(message, "warning")
        return redirect(url_for("index"))
    success, message, student_course_list = model.get_student_course_list(ID)
    if not success:
        flash(message, "warning")
        return redirect(url_for("index"))
    success, message, cluster_list = model.get_cluster_list(
        current_user.id, current_user.is_admin()
    )
    if not success:
        flash(message, "warning")
        return redirect(url_for("index"))
    success, message, user_cluster_list = model.get_cluster_list(ID)
    if not success:
        flash(message, "warning")
        return redirect(url_for("index"))
    return render_template(
        "profile.html",
        user=raw_user,
        course_list=course_list,
        student_course_list=student_course_list,
        cluster_list=cluster_list,
        user_cluster_list=user_cluster_list,
    )


@app.route("/clusters/", methods=["GET", "POST"])
@login_required
def cluster_list():
    if request.method == "POST":
        Name = request.form.get("Name", "DEFAULT")
        success, message = model.create_cluster(Name)
        if success:
            flash(message, "success")
            return redirect(url_for("cluster_list"))
        flash(message, "warning")
        return redirect(url_for("cluster_list"))
    success, message, cluster_list = model.get_cluster_list(
        current_user.id, current_user.is_admin()
    )
    if not success:
        flash(message, "warning")
        return redirect(url_for("cluster_list"))
    return render_template("cluster.html", cluster_list=cluster_list)


@app.route("/make_manager/<int:ManagerID>/", methods=["POST"])
@login_required
def make_manager(ManagerID):
    ClusterID = request.form.get("ClusterID", "")
    success, message = model.create_manager_cluster(ManagerID, ClusterID)
    if success:
        flash(message, "success")
    else:
        flash(message, "warning")
    return redirect(url_for("profile", ID=ManagerID))


@app.route("/courses/", methods=["GET", "POST"])
@login_required
def course_list():
    if request.method == "POST":
        Name = request.form.get("Name", "DEFAULT")
        ClusterID = request.form.get("ClusterID", "DEFAULT")
        TeacherID = request.form.get("TeacherID", "DEFAULT")
        success, message = model.create_course(Name, TeacherID, ClusterID)
        if success:
            flash(message, "success")
            return redirect(url_for("course_list"))
        flash(message, "warning")
        return redirect(url_for("course_list"))
    success, message, course_list = model.get_all_course_list()
    if not success:
        flash(message, "warning")
        return redirect(url_for("course_list"))
    success, message, cluster_list = model.get_cluster_list(
        current_user.id, current_user.is_admin()
    )
    if not success:
        flash(message, "warning")
        return redirect(url_for("index"))
    success, message, user_list = model.get_user_list()
    if not success:
        flash(message, "warning")
        return redirect(url_for("index"))
    return render_template(
        "course_list.html",
        course_list=course_list,
        cluster_list=cluster_list,
        user_list=user_list,
    )


@app.route("/participate/<int:StudentID>", methods=["POST"])
@login_required
def participate(StudentID):
    CourseID = request.form.get("CourseID", "")
    success, message = model.create_student_course(StudentID, CourseID)
    if success:
        flash(message, "success")
    else:
        flash(message, "warning")
    return redirect(url_for("profile", ID=StudentID))


@app.route("/students/<int:CourseID>/")
@login_required
def student_list(CourseID):
    success, message, student_list = model.get_course_student_list(CourseID)
    if not success:
        flash(message, "warning")
        return redirect(url_for("course", CourseID=CourseID))
    return render_template("course_student.html", student_list=student_list)


@app.route("/newcontent/<int:CourseID>/", methods=["GET", "POST"])
@login_required
def new_content(CourseID):
    if request.method == "POST":
        Title = request.form.get("Title", "")
        TextContent = request.form.get("TextContent", "")
        success, message = model.create_content(CourseID, Title, TextContent)
        if success:
            flash("Content created successfully.", "success")
            return redirect(url_for("course", CourseID=CourseID))
        flash(message, "warning")
        return redirect(url_for("course", CourseID=CourseID))
    return render_template("new_content.html", CourseID=CourseID)
