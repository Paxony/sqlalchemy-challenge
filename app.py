from  flask import Flask, jsonify
import numpy as np 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine,func

#Database setup
engine=create_engine("sqlite:///hawaii.sqlite")
Base=automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

#create an app
app =Flask (__name__)

#Home page.
#List all routes that are available.
@app.route("/")
def home():
    return (f'''
    Available routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/start
    /api/v1.0/start/end
''')

#Convert the query results to a Dictionary using date as the key and prcp as the value.
#Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precipitation():
    session=Session(engine)
    results=session.query(Measurement.date,Measurement.prcp).all()
    session.close()
    all_precipitation=[]
    for date, prcp in results:
        precipitation_dic={}
        precipitation_dic["date"]=date
        precipitation_dic["prcp"]=prcp
        all_precipitation.append(precipitation_dic)
    return jsonify(all_precipitation)

#Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    session=Session(engine)
    results=session.query(Station.name, Station.station).all()
    session.close()
    stations_names=list(results)
    return jsonify(stations_names)

#query for the dates and temperature observations from a year from the last data point.
#Return a JSON list of Temperature Observations (tobs) for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
    session=Session(engine)
    results=session.query(Station.name,Measurement.date,Measurement.tobs).\
         filter(Measurement.date >= '2016-08-23').\
          order_by(Measurement.date).all()
    session.close()
    LastYearTobs=list(results)
    return jsonify(LastYearTobs)

#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
#When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
#When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
@app.route("/api/v1.0/<start>/<end>")
def start(start,end):
    session=Session(engine)
    results= session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()
    dateStats=list(results)
    return jsonify(dateStats)


if __name__=="__main__":
    app.run(debug=True)
