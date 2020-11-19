from db import db


class ProjectModel(db.Model):
    __tablename__ = 'project'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    date = db.Column(db.Float(precision=2))

    activities = db.relationship('ActivityModel', lazy='dynamic')   # lazy means- get activities one by one from db

    def __init__(self, name, date):
        self.name = name
        self.date = date

    def json(self):
        return {'name': self.name, 'date': self.date, 'activities': [activity.json() for activity in self.activities.all()]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
