# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, distinct

from flask import Flask, jsonify
#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# Declare a Base using `automap_base()`
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(engine, reflect=True)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
measurement = Base.classes.measurement
station = Base.classes.station
# Create a session

session = Session(engine)
#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
# Define a root route
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

# Define precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipitation data for the last year."""
    # Query precipitation data for the last year
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= '2016-08-23').all()

    # Convert the query results to a dictionary
    precipitation_data = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict[date] = prcp
        precipitation_data.append(precipitation_dict)

    return jsonify(precipitation_data)

# Define stations route
@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations."""
    # Query all stations
    results = session.query(Station.station).all()

    # Convert list of tuples into normal list
    stations_list = list(np.ravel(results))

    return jsonify(stations_list)

# Define temperature observations route
@app.route("/api/v1.0/tobs")
def tobs():
    """Return the temperature observations for the last year."""
    # Query temperature observations for the last year for the most active station
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= '2016-08-23').all()

    # Convert the query results to a dictionary
    tobs_data = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict[date] = tobs
        tobs_data.append(tobs_dict)

    return jsonify(tobs_data)

# Define start route
@app.route("/api/v1.0/<start>")
def start_date(start):
    """Return TMIN, TAVG, and TMAX for all dates greater than and equal to the start date."""
    # Query TMIN, TAVG, and TMAX for all dates greater than and equal to the start date
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    # Convert list of tuples into normal list
    start_list = list(np.ravel(results))

    return jsonify(start_list)

# Define start and end route
@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    """Return TMIN, TAVG, and TMAX for dates between the start and end date inclusive."""
    # Query TMIN, TAVG, and TMAX for dates between the start and end date inclusive
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    # Convert list of tuples into normal list
    start_end_list = list(np.ravel(results))

    return jsonify(start_end_list)

if __name__ == '__main__':
    app.run(debug=True)