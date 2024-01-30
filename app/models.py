from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Hero(db.Model):
    __tablename__ = 'heroes'  # change to plural

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)

    hero_power = db.relationship('HeroPower', backref='hero')

class Power(db.Model):
    __tablename__ = 'powers'  # change to plural

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)

    hero_power = db.relationship('HeroPower', backref='power')

class HeroPower(db.Model):
    __tablename__ = 'hero_powers'  # change to plural

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String)
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))  # change to plural
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))  # change to plural
