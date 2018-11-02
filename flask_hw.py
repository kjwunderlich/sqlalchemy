import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def welcome():
    # """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    session1 = Session(engine)

    year_percp = session1.query(func.sum(Measurement.prcp), Measurement.date).\
    filter(Measurement.date > '2016-08-23').group_by(Measurement.date).order_by(Measurement.date).all()

    result = dict(year_percp)
    return jsonify(result)

@app.route("/api/v1.0/stations")
def station():

    session2 = Session(engine)

    station_list = session2.query(Measurement.station).group_by('station').all()

    result2 = list(np.ravel(station_list))
    return jsonify(result2)


@app.route("/api/v1.0/tobs")
def tobs():

    session3 = Session(engine)

    target = 'USC00519281'
    temps_year = session3.query(Measurement.tobs).filter(Measurement.station == target).\
        filter(Measurement.date >= '2016-08-23').all()

    result3 = list(np.ravel(temps_year))
    return jsonify(result3)

@app.route("/api/v1.0/start_date")
def start():

    session5 = Session(engine)

    start_date = '2016-08-23'

    start = session5.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()

    result5 = list(np.ravel(start))
    return jsonify(result5)

@app.route("/api/v1.0/start_date/end_date")  
def calc_temps():

    session4 = Session(engine)

    start_date = '2016-08-23'
    end_date = '2017-08-23'

    stats = session4.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()


    result4 = list(np.ravel(stats))
    return jsonify(result4)

if __name__ == '__main__':
    app.run(debug=True)
