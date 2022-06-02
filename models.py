from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()


# Create venue table
class Venue(db.Model):
  __tablename__ = 'venue'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))
  address = db.Column(db.String(120))
  phone = db.Column(db.String(120))
  image_link = db.Column(db.String(500))
  facebook_link = db.Column(db.String(120))
  genres = db.Column(db.ARRAY(db.String(120)))
  website_link = db.Column(db.String(120))
  seeking_talent = db.Column(db.Boolean(), default=True)
  seeking_description = db.Column(db.String(120))
  show = db.relationship('Show', backref='venue', lazy=True)
   
  # TODO: implement any missing fields, as a database migration using Flask-Migrate
  # Status = Done
  
  
# Create artist table
class Artist(db.Model):
  __tablename__ = 'artist'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))
  phone = db.Column(db.String(120))
  genres = db.Column(db.ARRAY(db.String(120)))
  image_link = db.Column(db.String(500))
  facebook_link = db.Column(db.String(120))
  website_link = db.Column(db.String(120))
  seeking_venue = db.Column(db.Boolean(), default=True)
  seeking_description = db.Column(db.String(120))
  show = db.relationship('Show', backref='artist', lazy=True)
  
  # TODO: implement any missing fields, as a database migration using Flask-Migrate
  # Status = Done

# Create show table  
class Show(db.Model):
  __tablename__ = 'show'
  id = db.Column(db.Integer, primary_key=True)
  venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
  artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
  start_time = db.Column(db.DateTime, nullable=False)
  

  # TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
   # Status = Done
   