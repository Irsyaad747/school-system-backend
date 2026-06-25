from database import db


class Attendance(db.Model):
    __tablename__ = "attendance"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    student_id = db.Column(
        db.Integer,
        nullable=False
    )

    tanggal = db.Column(
        db.String(20),
        nullable=False
    )

    status = db.Column(
        db.String(20),
        nullable=False
    )

    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "tanggal": self.tanggal,
            "status": self.status
        }