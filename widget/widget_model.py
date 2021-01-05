from db import db


class WidgetModel(db.Model):
    __tablename__ = "widgets"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True, index=False)
    color = db.Column(db.String(40), nullable=False, unique=False, index=False)
    weight = db.Column(db.Float, nullable=True, unique=False, index=False)

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first_or_404()

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "color": self.color,
            "weight": self.weight,
        }
