#Import Flask
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#Create app
app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )
@app.route("/api/v1.0/precipitation")
def prcp():
    # Perform a query to retrieve the data and precipitation scores
    lastyear_query = session.query(measurement.date, measurement.prcp).\
    filter(func.strftime(measurement.date) >= "2016-08-23").all()
    prcp_dictionary = [{element[0]: element[1]} for element in lastyear_query]
    return jsonify(prcp_dictionary)

@app.route("/api/v1.0/stations")
def stations():
    station_names = session.query(station.station).all()
    return jsonify(station_names)

@app.route("/api/v1.0/tobs")
def tobs():
    station_tobs = session.query(measurement.tobs).\
    filter(measurement.station == "USC00519281").\
    filter(func.strftime(measurement.date) >= "2016-08-23").all()
    return jsonify(station_tobs)

@app.route("/api/v1.0/<start>")
def start_date(start):
    temp_data = session.query(func.min(measurement.tobs), \
    func.max(measurement.tobs), func.avg(measurement.tobs)).\
    filter(measurement.date >= start).all()
    return jsonify(temp_data)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    temp_dates = session.query(func.min(measurement.tobs), \
    func.max(measurement.tobs), func.avg(measurement.tobs)).\
    filter(measurement.date >= start).\
    filter(measurement.date <= end).all()
    return jsonify(temp_dates)

if __name__ == "__main__":
    app.run(debug=True)