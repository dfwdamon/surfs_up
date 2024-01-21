# import dependencies
#@2023
import datetime as dt
import numpy as np
import pandas as pd
# import SQLAlchemy dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
# sets up db engine for access to the SQLite database.
engine = create_engine("sqlite:///hawaii.sqlite")
# Reflect our tablse, db into our classes.
Base = automap_base()
# Reflect the db
Base.prepare(engine, reflect=True)
# save our references to each table. Create a variable for each class to ref. later.]
Measurement = Base.classes.measurement
Station = Base.classes.station
# create a session link from Python with our db.
session = Session(engine)
# create a new instance Flask app called "app."
# However, when we run the script with python app.py, the __name__ 
# variable will be set to __main__. This indicates that we are not 
# using any other file to run this code.
app = Flask(__name__)
# Now build flask routes.
# 9.5.2
# All of your routes should go after the app = Flask(__name__) 
# line of code. Otherwise, your code may not run properly.
# create a Flask Route. starting point is root./ is hghest heirarchy level.
# Now add the routing information for other routes.

# Ctrl+C to quit in terminal.
# ?? Why does text show in one long line and not separate?
@app.route('/')
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs 
    api/v1.0/temp/start/end 
    ''')
# second route and define it.
@app.route("/api/v1.0/precipitation")
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)
# .\ tells query continue on next line.
# Jsonify() is a function that converts the dictionary to a JSON file.

# 9.5.4 Stations Route
# third route
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)
# 9.5.5 Monthly Temp Route, fourth route.
@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)
# 9.5.6 Statistics Route
@app.route("/api/v1.0/temp/start")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs),
    func.max(Measurement.tobs)]
    
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)
# result is [null,null,null] unless,
# query http://localhost:5000//api/v1.0/temp/2017-06-01/2017-06-30
# to see output of the 3 calculated temps.



