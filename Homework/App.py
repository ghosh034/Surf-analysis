import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitaion<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of precipitation data"""
    # Query 12 months of precipitation data
    latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    latest_date = latest_date[0]
    year_ago = dt.datetime.strptime(latest_date, "%Y-%m-%d")- dt.timedelta(days=366)
    results = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date>= year_ago).all()

    # Return json list
    precipitation_dict = dict(results)
    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations(): 
    """Return a list of stations"""
    # Query stations
    stations =  session.query(Measurement.station).group_by(Measurement.station).all()
    # Return json list
    stations_list = list(np.ravel(stations))
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs(): 
    """Return a list of Temperature Stats"""

    # Query 12 months of temperature stats
    max_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    max_date = max_date[0]
    year_ago = dt.datetime.strptime(max_date, "%Y-%m-%d") - dt.timedelta(days=366)
    results_temp = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= year_ago).all()

    # Return json list
    temp_list = list(results_temp)
    return jsonify(temp_list)

if __name__ == '__main__':
    app.run(debug=True)
