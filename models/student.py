from database import db

class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    kelas = db.Column(db.String(50), nullable=False)
    avatar = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "nama": self.nama,
            "kelas": self.kelas,
            "avatar": self.avatar
        }