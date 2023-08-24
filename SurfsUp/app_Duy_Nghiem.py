# Import the dependencies.
from statistics import mean
import pandas as pd
import numpy as np
import datetime as dt
import sqlalchemy 
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import flask
from flask import Flask , jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect = True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(bind=engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

# welcome page
@app.route("/")
def welcome():
    """List all available routes"""
    return (
        f"Available Routes: <br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/'start_date'/'end_date' <br/>"
    )

# precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    # precipitaion analysis
    prcp_results = session.query(Measurement.prcp, Measurement.date).\
    filter(Measurement.date > '2016-08-23').\
    order_by(Measurement.date).all()
    # close session
    session.close()

    # Create a dictionary for prcp results and make a list of the values
    prcp_list = []
    for prcp, date in prcp_results:
        prcp_dict = {}
        prcp_dict["Precipitation"] = prcp
        prcp_dict["Date"] = date
        prcp_list.append(prcp_dict)

    # return jsonify list
    return jsonify(prcp_list)

# stations
@app.route("/api/v1.0/stations")
def station():
    # get stations
    station_results = session.query(Station.station, Station.name).all()
    # close session
    session.close()

    # list
    station_list = []
    # loop like precipitation
    for station, name in station_results:
        station_dict = {}
        station_dict["Station"] = station
        station_dict["Name"] = name
        station_list.append(station_dict)

    # return
    return jsonify(station_list)

# tobs
@app.route("/api/v1.0/tobs")
def tobs():
    # Query the dates and temperature observations of the most-active station for the previous year of data.
    station_data = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date >= '2016-8-18').all()

    # close session
    session.close()

    # tobs list
    tobs_list = []
    # loop like above
    for date, tobs in station_data:
        station_dict = {}
        station_dict["Date"] = date
        station_dict["tobs"] = tobs
        tobs_list.append(station_dict)
    
    # return
    return jsonify(tobs_list)

# start and end date
@app.route("/api/v1.0/<start>/<end>")
def temperature(start, end):
    # Return a JSON list of the minimum temperature, the average temperature, \
    # and the maximum temperature for a specified start or start-end range.
    temp_results = session.query(Measurement).\
    filter(Measurement.date >= start).\
    filter(Measurement.date <= end)

    # close session
    session.close()

    temp_list = []
    for temp in temp_results:
        temp_list.append(temp.tobs)

    temp_dict = {
        "Min": min(temp_list),
        "Average": mean(temp_list),
        "Max": max(temp_list)
    }
    return jsonify(temp_dict)

# boilerplate
if __name__ == "__main__":
    app.run(debug=True)