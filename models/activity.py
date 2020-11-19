from db import db


class ActivityModel(db.Model):
    __tablename__ = 'activity'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    date = db.Column(db.Float(precision=2))

    project_id = db.Column(db.Integer, db.ForeignKey('project.id', on_delete='models.DO_NOTHING'))
    project = db.relationship('ProjectModel')

    def __init__(self, name, date, project_id):
        self.name = name
        self.date = date
        self.project_id = project_id

    def json(self):
        return {'name': self.name, 'date': self.date}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
