from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# ---------------- USER TABLE ----------------
class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(100),
        nullable=False
    )
    role = db.Column(
        db.String(20),
        default="student"
)

# ---------------- STUDENT TABLE ----------------
class Student(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    student_id = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    department = db.Column(
        db.String(100),
        nullable=False
    )
    is_deleted = db.Column(
        db.Boolean,
        default=False
    )
    subjects = db.relationship(
        "Subject",
        backref="student"
    )


# ---------------- SUBJECT TABLE ----------------
class Subject(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    subject_name = db.Column(
        db.String(100),
        nullable=False
    )

    mark = db.Column(
        db.Integer,
        nullable=False
    )

    status = db.Column(
        db.String(20),
        nullable=False
    )

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("student.id")
    )