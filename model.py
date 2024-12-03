from flask_sqlalchemy import SQLAlchemy
db= SQLAlchemy()

class HomeVideo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(120), nullable=False)
    year = db.Column(db.Integer, nullable=True)
    director = db.Column(db.String(120), nullable=True)


    def repr(self):
        return f'<HomeVideo {self.name}>'