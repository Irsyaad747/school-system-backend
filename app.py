from flask import ( Flask, request, jsonify
)
from flask_cors import CORS
from flask_jwt_extended import ( JWTManager,    create_access_token,    jwt_required,   get_jwt_identity
)
from database import db
from models.student import Student
from models.teacher import Teacher
from models.attendance import Attendance
from datetime import timedelta
import os
from werkzeug.utils import secure_filename
from flask import send_from_directory


app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

app.config[
    "UPLOAD_FOLDER"
] = UPLOAD_FOLDER

CORS(app)

app.config["JWT_SECRET_KEY"] = (
    os.getenv("JWT_SECRET_KEY")
    or "school-system-secret-key"
)

app.config[
    "JWT_ACCESS_TOKEN_EXPIRES"
] = timedelta(days=7)


jwt = JWTManager(app)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    os.getenv("MYSQL_URL")
    or "mysql+pymysql://root:@localhost/school_db"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/api/students")
@jwt_required()
def students():

    data = Student.query.all()

    return [
        student.to_dict()
        for student in data
    ]


@app.route("/api/students", methods=["POST"])
@jwt_required()
def create_student():

    data = request.get_json()

    student = Student(
        nama=data["nama"],
        kelas=data["kelas"],
        avatar=data.get("avatar")
    )

    db.session.add(student)
    db.session.commit()

    return {
        "message": "Siswa berhasil ditambahkan"
    }, 201

@app.route("/api/students/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_student(id):

    student = Student.query.get(id)

    if not student:
        return {
            "message": "Siswa tidak ditemukan"
        }, 404

    db.session.delete(student)
    db.session.commit()

    return {
        "message": "Siswa berhasil dihapus"
    }

@app.route("/api/students/<int:id>", methods=["PUT"])
@jwt_required()
def update_student(id):

    student = Student.query.get(id)

    if not student:
        return {
            "message": "Siswa tidak ditemukan"
        }, 404

    data = request.get_json()

    student.nama = data["nama"]
    student.kelas = data["kelas"]
    student.avatar = data.get("avatar", student.avatar)

    db.session.commit()

    return {
        "message": "Siswa berhasil diperbarui"
    }

@app.route("/api/teachers")
@jwt_required()
def teachers():

    data = Teacher.query.all()

    return [
        teacher.to_dict()
        for teacher in data
    ]

@app.route("/api/teachers", methods=["POST"])
@jwt_required()
def create_teacher():

    data = request.get_json()

    teacher = Teacher(
    nama=data["nama"],
    mapel=data["mapel"],
    avatar=data.get("avatar")
)

    db.session.add(teacher)
    db.session.commit()

    return {
        "message": "Guru berhasil ditambahkan"
    }, 201

@app.route("/api/teachers/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_teacher(id):

    teacher = Teacher.query.get(id)

    if not teacher:
        return {
            "message": "Guru tidak ditemukan"
        }, 404

    db.session.delete(teacher)
    db.session.commit()

    return {
        "message": "Guru berhasil dihapus"
    }

@app.route("/api/teachers/<int:id>", methods=["PUT"])
@jwt_required()
def update_teacher(id):

    teacher = Teacher.query.get(id)

    if not teacher:
        return {
            "message": "Guru tidak ditemukan"
        }, 404

    data = request.get_json()

    teacher.nama = data["nama"]
    teacher.mapel = data["mapel"]

    teacher.avatar = data.get("avatar", teacher.avatar)

    db.session.commit()

    return {
        "message": "Guru berhasil diperbarui"
    }

@app.route("/api/attendance")
@jwt_required()
def attendance():

    data = Attendance.query.all()

    return [
        item.to_dict()
        for item in data
    ]

@app.route("/api/attendance", methods=["POST"])
@jwt_required()
def create_attendance():

    data = request.get_json()

    attendance = Attendance(
        student_id=data["student_id"],
        tanggal=data["tanggal"],
        status=data["status"]
    )

    db.session.add(attendance)
    db.session.commit()

    return {
        "message":
        "Absensi berhasil ditambahkan"
    }, 201

@app.route("/api/login", methods=["POST"])
def login():

    data = request.json

    username = data.get("username")
    password = data.get("password")

    if (
        username == "admin"
        and
        password == "admin123"
    ):

        token = create_access_token(
            identity=username
        )

        return jsonify({
            "token": token
        })

    return jsonify({
        "message":
        "Username atau password salah"
    }), 401

@app.route("/api/attendance/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_attendance(id):

    attendance = Attendance.query.get(id)

    if not attendance:
        return {
            "message": "Data tidak ditemukan"
        }, 404

    db.session.delete(attendance)
    db.session.commit()

    return {
        "message": "Absensi berhasil dihapus"
    }

@app.route(
    "/api/upload-avatar",
    methods=["POST"]
)
@jwt_required()
def upload_avatar():

    if "file" not in request.files:

        return {
            "message":
            "Tidak ada file"
        }, 400

    file = request.files["file"]

    filename = secure_filename(
        file.filename
    )

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    file.save(filepath)

    return {
        "filename":
        filename
    }


@app.route(
    "/uploads/<filename>"
)
def uploaded_file(filename):

    return send_from_directory(
        app.config[
            "UPLOAD_FOLDER"
        ],
        filename
    )


if __name__ == "__main__":
    app.run(debug=True)