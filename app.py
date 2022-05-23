# Set Up the Flask Weather App
#################################################
# Import the Flask Dependency
#################################################

import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

from flask import Flask

# Create a New Flask App Instance- "Instance" is a general term in programming to refer to a singular version of something

app = Flask(__name__)
# Create Flask Routes

@app.route('/')
def hello_world():
    return 'Hello world'

# Run a Flask App - run "set FLASK_APP=app.py" and "flask run" in Anaconda Powershell after going to your desired folder.

#################################################
# Set Up the Database and Flask
# Module 9.5.1
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#Set Up Flask
app = Flask(__name__)

#################################################
# Create the Welcome Route
# Module 9.5.2
#################################################

@app.route('/')
def welcome():
    return(
        f"Welcome to the Hawaii Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end"
    )

# Run a Flask App - run "set FLASK_APP=app.py" and "flask run" in Anaconda Powershell after going to your desired folder.

#################################################
# Precipitation Route
# Module 9.5.3
#################################################
@app.route("/api/v1.0/precipitation")

def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

# Run a Flask App - run "set FLASK_APP=app.py" and "flask run" in Anaconda Powershell after going to your desired folder.

#################################################
# Stations Route
# Moudule 9.5.4
#################################################
@app.route("/api/v1.0/stations")

def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# Run a Flask App - run "set FLASK_APP=app.py" and "flask run" in Anaconda Powershell after going to your desired folder.

#################################################
# Monthly Temperature Route
# Moudule 9.5.5
#################################################
@app.route("/api/v1.0/tobs")

def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)   

# Run a Flask App - run "set FLASK_APP=app.py" and "flask run" in Anaconda Powershell after going to your desired folder.

#################################################
# Statistics Route
# Moudule 9.5.6
#################################################
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# Run a Flask App - run "set FLASK_APP=app.py" and "flask run" in Anaconda Powershell after going to your desired folder.
