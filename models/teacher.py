from database import db

class Teacher(db.Model):

    __tablename__ = "teachers"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nama = db.Column(
        db.String(100),
        nullable=False
    )

    mapel = db.Column(
        db.String(100),
        nullable=False
    )

    avatar = db.Column(
        db.String(255),
        nullable=True
    )

    def to_dict(self):

        return {
            "id": self.id,
            "nama": self.nama,
            "mapel": self.mapel,
            "avatar": self.avatar
        }