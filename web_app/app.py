from flask import (Flask, render_template, request, redirect, url_for, session)
from app.models.models import (
    db,
    User,
    Student,
    Subject
)

app = Flask(__name__)
app.secret_key = "edusphere_secret_key"
# ---------------- DATABASE CONFIG ----------------
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# ---------------- CREATE DATABASE ----------------
with app.app_context():
    db.create_all()


# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():

    error = ""

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        user = User.query.filter_by(
            username=username,
            password=password
        ).first()

        if user:
            session["user_id"] = user.id
            session["username"] = user.username
            session["role"] = user.role
            return redirect(
                url_for("dashboard")
            )

        else:
            error = "Invalid Username or Password ❌"

    return render_template(
        "login.html",
        error=error
    )


# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():

    message = ""

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]
@app.route("/register", methods=["GET", "POST"])
def register():

    message = ""

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        role = request.form["role"]
        existing_user = User.query.filter_by(
            username=username
        ).first()

        if existing_user:

            message = "Username already exists ❌"

        else:
            new_user = User(
                username=username,
                password=password,
                role=role
            )

            db.session.add(new_user)

            db.session.commit()

            message = "Registration Successful ✅"

    return render_template(
        "register.html",
        message=message
    )


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        username=session["username"],
        role=session["role"]
    )


# ---------------- ADD STUDENT ----------------
@app.route("/add_student", methods=["GET", "POST"])
def add_student():

    if request.method == "POST":

        student_id = request.form["student_id"]

        name = request.form["name"]

        department = request.form["department"]

        student = Student(
            student_id=student_id,
            name=name,
            department=department
        )

        db.session.add(student)

        db.session.commit()

        subjects = request.form.getlist("subject")

        marks = request.form.getlist("mark")

        for sub, mark in zip(subjects, marks):

            if sub and mark:

                mark = int(mark)

                status = "Pass"

                if mark < 40:
                    status = "Fail"

                new_subject = Subject(
                    subject_name=sub,
                    mark=mark,
                    status=status,
                    student_id=student.id
                )

                db.session.add(new_subject)

        db.session.commit()

        return redirect(
            url_for("view_students")
        )

    return render_template(
        "add_student.html"
    )


# ---------------- VIEW STUDENTS ----------------
@app.route("/view_students")
def view_students():

    students = Student.query.filter_by(
        is_deleted=False
    ).all()

    return render_template(
        "view_students.html",
        students=students
    )


# ---------------- UPDATE STUDENT ----------------
@app.route("/update_student/<int:id>",
           methods=["GET", "POST"])
def update_student(id):

    student = Student.query.get(id)

    if request.method == "POST":

        student.name = request.form["name"]

        student.department = request.form["department"]

        db.session.commit()

        return redirect(
            url_for("view_students")
        )

    return render_template(
        "update_student.html",
        student=student
    )


# ---------------- DELETE STUDENT ----------------
@app.route("/delete_student/<int:id>")
def delete_student(id):

    student = Student.query.get(id)

    if student:

        student.is_deleted = True

        db.session.commit()

    return redirect(
        url_for("view_students")
    )
@app.route("/deleted_students")
def deleted_students():

    students = Student.query.filter_by(
        is_deleted=True
    ).all()

    return render_template(
        "deleted_students.html",
        students=students
    )
@app.route("/restore_student/<int:id>")
def restore_student(id):

    student = Student.query.get(id)

    if student:

        student.is_deleted = False

        db.session.commit()

    return redirect(
        url_for("deleted_students")
    )
# ---------------- RANKING ----------------
@app.route("/ranking")
def ranking():

    students = Student.query.all()

    student_data = []

    for student in students:

        subjects = Subject.query.filter_by(
            student_id=student.id
        ).all()

        total = sum(
            s.mark for s in subjects
        )

        average = total / len(subjects)

        weak_subject = min(
            subjects,
            key=lambda x: x.mark
        )

        student_data.append({

            "student": student,

            "average": average,

            "weak_subject":
                weak_subject.subject_name,

            "weak_mark":
                weak_subject.mark
        })

    ranked_students = sorted(

        student_data,

        key=lambda x: x["average"],

        reverse=True
    )

    return render_template(

        "ranking.html",

        students=ranked_students
    )


# ---------------- REPORT ----------------
@app.route("/report/<int:id>")
def report(id):

    student = Student.query.get(id)

    subjects = Subject.query.filter_by(
        student_id=id
    ).all()

    total = 0

    fail_count = 0

    for s in subjects:

        total += s.mark

        if s.status == "Fail":
            fail_count += 1

    average = total / len(subjects)

    result = "Pass"

    if fail_count > 0:
        result = "Fail"

    return render_template(

        "report.html",

        student=student,

        subjects=subjects,

        total=total,

        average=average,

        result=result
    )


# ---------------- RUN APP ----------------
if __name__ == "__main__":

    app.run(debug=True)