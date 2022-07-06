# Import dependencies
import datetime as dt
import numpy as np
import pandas as pd

# SQLAlchemy dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Flask dependencies
from flask import Flask, jsonify

# Set Up the Database
engine = create_engine('sqlite:///hawaii.sqlite')

# Reflect the database into our classes
Base = automap_base()
Base.prepare(engine, reflect = True) # save our references to each table

# Create a variable for each class (table) for reference
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session link from Python to our database
session = Session(engine)

####### Define our app for our Flask application #########

# Set up Flask
app = Flask(__name__)

# Create the Welcome route
@app.route("/")
#add the routing information for each of the other routes
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!\n
    Available Routes:\n
    /api/v1.0/precipitation\n
    /api/v1.0/stations\n
    /api/v1.0/tobs\n
    /api/v1.0/temp/start/end\n
    ''')
# Precipitation Route
@app.route("/api/v1.0/precipitation")
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365) #code calculates the date one year ago from most recent in database
    precipitation = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date >= prev_year).all() # query to get the date and precipitation for the previous year
    precip = {date: prcp for date, prcp in precipitation} # create a dictionary with the date as the key and the precipitation as the value using jsonify()
    return jsonify(precip) 

# Stations Route
@app.route("/api/v1.0/stations") # define route name
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results)) #unravel into one-dimensional array and convert it into a list
    return jsonify(stations=stations) #stations=stations formast our list into JSON

# Monthly Temperature Route
@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all() #query the primary station USC00519281
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

#Statistics Route
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    
    if not end: #determine teh startind and ending date, add if-not to our code
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)





