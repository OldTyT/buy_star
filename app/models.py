from app import db
from datetime import datetime
from app.rnd_id import random_cosmic_id

class cosmic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cosmic_id = db.Column(db.String(), default=random_cosmic_id, index=True, unique=True)
    first_name = db.Column(db.String(), index=True)
    last_name = db.Column(db.String(), index=True)
    middle_name = db.Column(db.String(), index=True)
    datetime = db.Column(db.DateTime(), default=datetime.now, index=True)
    name_cosmic = db.Column(db.String(), index=True)

    def __repr__(self):
        return f'<id - {self.id}. cosmic_id - {self.cosmic_id}>'
