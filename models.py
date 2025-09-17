
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)  
    author = db.Column(db.String(80), nullable=False)
    editorial = db.Column(db.String(80), nullable=False)
    edition = db.Column(db.Integer)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'editorial': self.editorial,
            'edition': self.edition
        }