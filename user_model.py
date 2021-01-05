from db import db


class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False, index=True)
    password = db.Column(db.String(40), unique=False, nullable=False, index=True)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    def json(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
        }
