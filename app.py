import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################


@app.route("/")
def home():
    return (
    f"Welcome to Vince's API!<br/>"
    f"/api/v1.0/precipitation<br/>"
    f"/api/v1.0/stations<br/>"
    f"/api/v1.0/tobs<br/>"
    f"/api/v1.0/start<br/>"
    f"/api/v1.0/start/end<br/>"
    )

    


@app.route("/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all dates and precipitation"""
    # Query 
    results = session.query(Measurement.date,Measurement.prcp).all()

    session.close()

    # Convert list of tuples into normal list
    prcp = list(np.ravel(results))

    return jsonify(prcp)
    

@app.route("/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all stations
    results = session.query(Measurement.station).distinct().all()

    session.close()

    # Convert list of tuples into normal list
    prcp = list(np.ravel(results))

    return jsonify(prcp)

@app.route("/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all stations
    max_date= session.query(func.max(Measurement.date)).first()[0]
    year_before_max_date =  dt.datetime.strptime(max_date, '%Y-%m-%d') - dt.timedelta(days=365)
    results = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date >= year_before_max_date).all()

    session.close()

    # Convert list of tuples into normal list
    prcp = list(np.ravel(results))
    
    return jsonify(prcp)
    

@app.route("/<start_date>")
def start(start_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all stations
    results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all()

    session.close()

    # Convert list of tuples into normal list
    prcp = list(np.ravel(results))

    #return jsonify({f'Min Temperature : {prcp[0]}, Avg Temperature : {prcp[1]}, Max Temperature : {prcp[2]}'})
    return jsonify({'Result': f' Min Temp: {prcp[0]} Avg Temp: {prcp[1]} Max Temp: {prcp[2]}'})

@app.route("/<start_date>/<end_date>")
def startend(start_date,end_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all stations
    results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    session.close()

    # Convert list of tuples into normal list
    prcp = list(np.ravel(results))

    #return jsonify({f'Min Temperature : {prcp[0]}, Avg Temperature : {prcp[1]}, Max Temperature : {prcp[2]}'})
    return jsonify({'Result': f' Min Temp: {prcp[0]} Avg Temp: {prcp[1]} Max Temp: {prcp[2]}'})

if __name__ == "__main__":
    app.run(debug=True)
