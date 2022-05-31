#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import datetime
from distutils.command.install_lib import PYTHON_SOURCE_EXTENSION
from email.policy import default
from math import factorial
from os import urandom
import dateutil.parser
import babel
from flask import Flask, abort, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask import request
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
import sys
from sqlalchemy.orm import aliased
from sqlalchemy import desc
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.secret_key = "my secret key"
moment = Moment(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/Fyyur'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

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
  
  
  
  def __init__(self, name, city, state, address, phone, genres, image_link, facebook_link, website_link, seeking_talent, seeking_description):
    self.name = name
    self.city = city
    self.state = state
    self.phone = phone
    self.genres = genres
    self.facebook_link = facebook_link
    self.website_link = website_link
    self.seeking_description = seeking_description
    self.seeking_talent = seeking_talent
    self.image_link = image_link
    self.address = address

  # TODO: implement any missing fields, as a database migration using Flask-Migrate
  # Status = Done

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
  

  def __init__(self, name, city, state, phone, genres, image_link, facebook_link, website_link, seeking_venue, seeking_description):
    self.name = name
    self.city = city
    self.state = state
    self.phone = phone
    self.genres = genres
    self.facebook_link = facebook_link
    self.website_link = website_link
    self.seeking_description = seeking_description
    self.seeking_venue = seeking_venue
    self.image_link = image_link
  

  # TODO: implement any missing fields, as a database migration using Flask-Migrate
  # Status = Done
    
class Show(db.Model):
  __tablename__ = 'show'
  id = db.Column(db.Integer, primary_key=True)
  venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
  artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
  start_time = db.Column(db.String())
  
  
  def __init__(self, venue_id, artist_id, start_time):
    self.venue_id = venue_id
    self.artist_id = artist_id
    self.start_time = start_time

  # TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
   # Status = Done
   
#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  data = []
  venue_list = Venue.query.distinct(Venue.city, Venue.state).order_by(desc(Venue.city)).all()
  
  for venue in venue_list:
    city_n_state = {"city": venue.city, "state": venue.state}
    
    venues = Venue.query.filter_by(city = venue.city, state = venue.state).all()
    result = []
    for venue in venues:
      result.append({
        "id": venue.id,
        "name": venue.name
      })
      
    city_n_state["venues"] = result
    
    data.append(city_n_state)
    
  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  response={
    "count": 1,
    "data": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  data = Venue.query.get_or_404(venue_id)
  return render_template('pages/show_venue.html', venue=data)

  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  # Status = Done

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  if request.method == "POST":
    form = VenueForm()
    venue = Venue(name = form.name.data,
                  city = form.city.data,
                  state = form.state.data,
                  address = form.address.data,
                  phone = form.phone.data,
                  genres = form.genres.data,
                  image_link = form.image_link.data,
                  facebook_link = form.facebook_link.data,
                  website_link = form.website_link.data,
                  seeking_talent = form.seeking_talent.data,
                  seeking_description = form.seeking_description.data,
                )
    db.session.add(venue)
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully listed!')

    db.session.close()
  else:
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed!')
    db.session.rollback()
  
  return render_template('pages/home.html')
  

  # TODO: insert form data as a new Venue record in the db, instead
  # Status = Done
  # TODO: modify data to be the data object returned from db insertion
  # Status = Done

  # on successful db insert, flash success
  #flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  # Status = Done

  
  
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  # Status = Done!
@app.route('/venues/<int:venue_id>/delete', methods=['GET'])
def delete_venue(venue_id):
  if request.method == 'GET':
    venue = Venue.query.get(venue_id)
    db.session.delete(venue)
    db.session.commit()
    flash('Venue has been deleted successfully')
    
  else:
    db.session.rollback
    flash('Unsuccesful attenpt to delete venue')
    db.session.close()
  
  return redirect(url_for('venues', venue_id=venue_id))
  
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  # Status = Done!

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  data = Artist.query.all()
  return render_template('pages/artists.html', artists=data)

  # TODO: replace with real data returned from querying the database
  # Status = Done


@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  response={
    "count": 1,
    "data": [{
      "id": 4,
      "name": "Guns N Petals",
      "num_upcoming_shows": 0,
    }]
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  data = Artist.query.get_or_404(artist_id)
  return render_template('pages/show_artist.html', artist=data)

  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  # Status = Done
  

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.all()

  # TODO: populate form with fields from artist with ID <artist_id>
  # Status = not done... artist name hasnt been implemented
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
      
  if request.method == "POST":
    form = ArtistForm()
    artist = Artist(name = form.name.data,
                  city = form.city.data,
                  state = form.state.data,
                  phone = form.phone.data,
                  genres = form.genres.data,
                  image_link = form.image_link.data,
                  facebook_link = form.facebook_link.data,
                  website_link = form.website_link.data,
                  seeking_venue = form.seeking_venue.data,
                  seeking_description = form.seeking_description.data)
  
    db.session.add(artist)
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully listed!')

    db.session.close()
  else:
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed!')
    db.session.rollback()
  
  return render_template('pages/home.html')
  
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  # Status = Done

  # on successful db insert, flash success
  # flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  # Status = Done
  
@app.route('/artists/<int:artist_id>/delete', methods=['GET'])
def delete_artist(artist_id):
  if request.method == 'GET':
    artist = Artist.query.get(artist_id)
    db.session.delete(artist)
    db.session.commit()
    flash('Artist has been deleted successfully')
    
  else:
    db.session.rollback
    flash('Unsuccesful attenpt to delete artist')
    db.session.close()
  
  return redirect(url_for('artists', artist_id=artist_id))


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  shows_list = Show.query.all()
  shows = []
  for show in shows_list:
    shows.append(show)
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  return render_template('pages/shows.html', shows=shows)

@app.route('/show/')
def search_show():
  response={
      "count": 1,
      "data": [{
        "id": 4,
        "name": "Guns N Petals",
        "num_upcoming_shows": 0,
      }]
    }
  return render_template('pages/show.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  
  if request.method == "POST":
    artist_id = request.form['artist_id']
    venue_id = request.form['venue_id']
    start_time = request.form['start_time']
    
    show = Show(
      artist_id = artist_id,
      venue_id = venue_id,
      start_time = start_time
    )
    
    db.session.add(show)
    db.session.commit()
    flash('Show was successfully listed!')

    db.session.close()
  else:
    flash('An error occurred. Show could not be listed.')
    db.session.rollback()
  
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead.
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
