# Import python dependencies
import datetime as dt
import numpy as np
import pandas as pd

# Import SQLAlchemy dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Import flask dependencies
from flask import Flask, jsonify

# Access SQLite database with .sqlite file 
engine = create_engine('sqlite:///hawaii.sqlite')

# Reflect Database to new model and reflect the tables in file 
Base = automap_base()
Base.prepare(engine, reflect=True)

# --- How can we see the classes to do this?
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create session link from Python to the Database
session = Session(engine)

# --- Do not really understand this portion, what would an example of this be? Comment for now 
# Magic Method to determine if app is imported or running directly
#import app
#print("example __name__ = %s", __name__)

#if __name__ == "__main__":
#	print("example is being run directly.")
#else:
#	print("example is being imported")

# Set Up Flask
app = Flask(__name__)

# Welcome route setup
@app.route('/')

# Create welcome route function
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API! 
    Available Routes: 
    /api/v1.0/precipitation 
    /api/v1.0/stations 
    /api/v1.0/tobs 
    /api/v1.0/start/end 
    ''')

# Create Precipitation route
@app.route('/api/v1.0/precipitation')

#Create Precipitation function
def precipitation():
    # Calculate date one year ago from the most recent date
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # Query the date and precipitation for the previous year
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    # Add jsonify() function which will give results JSON structure
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

# Create Stations route
@app.route('/api/v1.0/stations')

#Create Station function
def stations():
    # Query the station results
    results = session.query(Station.station).all()
    # Unravel the results into a one demensional array and convert to list 
    stations = list(np.ravel(results))
    # Add jsonify() function which will give results JSON structure
    return jsonify(stations=stations)

# Create Temperature route
@app.route('/api/v1.0/tobs')

# Create Temperature function
def temp_monthly():
     # Calculate date one year ago from the most recent date
     prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
     # Query primary station for all temps 
     results = session.query(Measurement.tobs).\
         filter(Measurement.station == 'USC00519281').\
         filter(Measurement.date >= prev_year).all()
     # Unravel the results into a one demensional array and convert to list
     temps = list(np.ravel(results))
     # Add jsonify() function which will give results JSON structure
     return jsonify(temps=temps)

# Create Statistics route, need start and end dates
@app.route('/api/v1.0/temp/<start>')
@app.route('/api/v1.0/temp/<start>/<end>')

# Create Statistics function
# Add parameters to 'start' and 'end'
def stats(start=None, end=None):
    # Query by setting list (sel) to select min, avg, and max temps 
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    # If-not statement to determine start and end date
    # (*sel) indicates multiple results
    if not end:
        results = session.query(*sel).\
        filter(Measurement.date >= start).all()
        # Unravel the results into a one demensional array and convert to list
        temps = list(np.ravel(results))
        # Return these results with jsonify
        return jsonify(temps)
    # Query to calculate temperatures
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    # Unravel the results into a one demensional array and convert to list
    temps = list(np.ravel(results))
    # Add jsonify() function which will give results JSON structure
    return jsonify(temps)

