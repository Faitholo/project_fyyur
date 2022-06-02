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
from sqlalchemy import desc
from models import db, Venue, Artist, Show
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

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  if isinstance(value, str):
    date = dateutil.parser.parse(value)
  else:
    date = value
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
  # num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  
  #declare data variable as an empty list and get distinct vennue__list by querying the venue table
  data = []
  venue_list = Venue.query.distinct(Venue.city, Venue.state).order_by(desc(Venue.city)).all()
  
  # Use a for loop to iterate throuhg the distinct venue_list and do a subquery for further filtering
  for venue in venue_list:
    city_n_state = {"city": venue.city, "state": venue.state}
    
    venues = Venue.query.filter_by(city = venue.city, state = venue.state).all()
    
    # Use a for loop to iterate the filtered query and append in the ampty result variable
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
  
  # Retrieve the search term and query the venue table, filter results like the search term.
  search_term = request.form.get('search_term')
  search_results = Venue.query.filter(
  Venue.name.ilike('%{}%'.format(search_term))).all()
  
  
  # Count the number of related searches and append the names like search term
  results = {}
  results['count'] = len(search_results)
  results['data'] = search_results
  
  return render_template('pages/search_venues.html', results=results, search_term=request.form.get('search_term', ''))

  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  # Status = Done!


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # Query the venue table by the venue_id
  venue = Venue.query.get(venue_id)
  
  # Filter the past shows as less than current datetime
  past_shows = list(filter(lambda prev_show: prev_show.start_time < datetime.now(), venue.show)) 
  
  # Filter the upcoming shows as greater than current datetime
  upcoming_shows = list(filter(lambda prev_show: prev_show.start_time > datetime.now(), venue.show))
  
  # iterate through past shows and append the required rows of each queried table column
  shows = []
  for show in past_shows:
    item = {}
    item["artist_name"] = show.artist.name
    item["artist_id"] = show.artist.id
    item["artist_image_link"] = show.artist.image_link
    item["start_time"] = show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
    shows.append(item)

  # set venue as the value of past shows and total number of upcoming shows
  # as past shows and past_shows_count)
  setattr(venue, "past_shows", shows)
  setattr(venue,"past_shows_count", len(past_shows))

  # iterate through upcoming shows and append the required rows of each queried table column
  shows = []
  for show in upcoming_shows:
      item = {}
      item["artist_name"] = show.artist.name
      item["artist_id"] = show.artist.id
      item["artist_image_link"] = show.artist.image_link
      item["start_time"] = show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
      shows.append(item)

  # set venue as the value of upcoming shows and total number of upcoming shows
  # as upcoming shows and upcoming_shows_count)
  setattr(venue, "upcoming_shows", shows)    
  setattr(venue,"upcoming_shows_count", len(upcoming_shows))
  
  
  return render_template('pages/show_venue.html', venue=venue)

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
  
  # Request data from the Venue Form
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
    # Add and commit the received form input
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


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  
  # Query the venue id to edit and retrieve previously stored data
  venue = Venue.query.get(venue_id)
  form = VenueForm(obj=venue)
  
  return render_template('forms/edit_venue.html', form=form, venue=venue)
  # TODO: populate form with values from venue with ID <venue_id>
  # Status = Done


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  
  # Retrieve the new updates in the form
  form = VenueForm(request.form)
  if request.method == 'POST':
    venue = Venue.query.get(venue_id)

    venue.name = form.name.data
    venue.city=form.city.data
    venue.state=form.state.data
    venue.phone=form.phone.data
    venue.genres=form.genres.data
    venue.facebook_link=form.facebook_link.data
    venue.image_link=form.image_link.data
    venue.seeking_talent=form.seeking_talent.data
    venue.seeking_description=form.seeking_description.data
    venue.website_link=form.website_link.data

    # Add and commit the new updates
    db.session.add(venue)
    db.session.commit()
    flash("Artist " + venue.name + " was successfully edited!")
  else:
    db.session.rollback()
    print(sys.exc_info())
    flash("Sorry, Artist could not be edited.")
  
  return redirect(url_for('show_venue', venue_id=venue_id))
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  # Status = Done!
  
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  # Status = Done!
  
  
@app.route('/venues/<int:venue_id>/delete', methods=['GET'])
def delete_venue(venue_id):
      
  # Query the venue id and delete records related to that id
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
  # Status = Done
  
  # Retrieve the search term and query the artist table, filter results like the search term.
  search_term = request.form.get('search_term')
  search_results = Artist.query.filter(
  Artist.name.ilike('%{}%'.format(search_term))).all()  # search results by ilike matching partern to match every search term

  # Count the number of related searches and append the names like search term
  results = {}
  results['count'] = len(search_results)
  results['data'] = search_results
  
  return render_template('pages/search_artists.html', results=results, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
      
  # Query the venue table by the venue_id
  artist = Artist.query.get(artist_id)
  
  # Filter the past shows as less than current datetime
  past_shows = list(filter(lambda prev_show: prev_show.start_time < datetime.now(), artist.show))
  
  # Filter the upcoming shows as greater than current datetime
  upcoming_shows = list(filter(lambda prev_show: prev_show.start_time > datetime.now(), artist.show))
  
  # iterate through past shows and append the required rows of each queried table column
  shows = []
  for show in past_shows:
      item = {}
      item["venue_name"] = show.venue.name
      item["venue_id"] = show.venue.id
      item["venue_image_link"] = show.venue.image_link
      item["start_time"] = show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
      shows.append(item)

  # set artist as the value of past shows and total number of upcoming shows
  # as past_shows and past_shows_count)
  setattr(artist, "past_shows", shows)
  setattr(artist,"past_shows_count", len(past_shows))

  # iterate through upcoming shows and append the required rows of each queried table column
  shows = []
  for show in upcoming_shows:
      item = {}
      item["venue_name"] = show.venue.name
      item["venue_id"] = show.venue.id
      item["venue_image_link"] = show.venue.image_link
      item["start_time"] = show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
      shows.append(item)

  # set artist as the value of upcoming shows and total number of upcoming shows
  # as upcoming shows and upcoming_shows_count)
  setattr(artist, "upcoming_shows", shows)
  setattr(artist,"upcoming_shows_count", len(upcoming_shows))
  return render_template('pages/show_artist.html', artist=artist)

  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  # Status = Done
  

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):

  # Retrieve data from the database by querying artist_id
  artist = Artist.query.get(artist_id)
  form = ArtistForm(obj=artist)
  
  return render_template('forms/edit_artist.html', form=form, artist=artist)

  # TODO: populate form with fields from artist with ID <artist_id>
  # Status = Done

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):

  # Update the form with new information
  form = ArtistForm(request.form)
  if request.method == 'POST':
    artist = Artist.query.get(artist_id)

    artist.name = form.name.data
    artist.city=form.city.data
    artist.state=form.state.data
    artist.phone=form.phone.data
    artist.genres=form.genres.data
    artist.facebook_link=form.facebook_link.data
    artist.image_link=form.image_link.data
    artist.seeking_venue=form.seeking_venue.data
    artist.seeking_description=form.seeking_description.data
    artist.website_link=form.website_link.data

    # Add the updated data and commit
    db.session.add(artist)
    db.session.commit()
    flash("Artist " + artist.name + " was successfully edited!")
  else:
    db.session.rollback()
    print(sys.exc_info())
    flash("Sorry," + artist.name + " could not be edited.")

  return redirect(url_for('show_artist', artist_id=artist_id))

  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  # Status = Done


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
   
  # # Create new artist data using form input   
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

    # Add the artist data and commit to the database
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
      
  # Get artist id and delete all data attributed the the id
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
      
  # Query the shows table and join the artist and venue tables
  data = db.session.query(Show).join(Venue, Artist).all()
  shows = []
  for show in data:
    shows.append({
        'venue_id': show.venue.id,
        'venue_name': show.venue.name,
        'artist_id': show.artist.id,
        'artist_name': show.artist.name,
        'artist_image_link': show.artist.image_link,
        'start_time': show.start_time
    })
  
  return render_template('pages/shows.html', shows=shows)

  # displays list of shows at /shows
  # TODO: replace with real venues data.


@app.route('/show/')
def search_show():
  
   # Retrieve the search term and query the artist table, filter results like the search term.
  search_term = request.form.get('search_term')
  search_results = Artist.query.filter(
  Artist.name.ilike('%{}%'.format(search_term))).all()  # search results by ilike matching partern to match every search term

  # Count the number of related searches and append the names like search term
  results = {}
  results['count'] = len(search_results)
  results['data'] = search_results
  return render_template('pages/show.html', results=results, search_term=request.form.get('search_term', ''))

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # Retrieve form data
  form = ShowForm()
  if request.method == "POST":
    
    show = Show(
    artist_id = form.artist_id.data,
    venue_id = form.venue_id.data,
    start_time = form.start_time.data
    )
    
    # Add and commit data
    db.session.add(show)
    db.session.commit()
    flash('Show was successfully listed!')

    db.session.close()
  else:
    flash('An error occurred. Show could not be listed.')
    db.session.rollback()
  
  return render_template('pages/home.html')
  
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead.
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  # Status = Done!


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
