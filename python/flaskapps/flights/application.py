import os
from flask import Flask, render_template, request , session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
Session(app)

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind = engine))

@app.route("/")
def index():
    flights = db.execute("SELECT * FROM flights").fetchall()
    return render_template("index.html", flights=flights)
    
@app.route("/book", methods=['POST'])
def book():
    """Book a flight. """
    name = request.form.get("name")
    try:
        flight_id = int(request.form.get("flight_id"))
    except ValueError:
        return render_template("error.html", message="Invalid flight number.")
    
    if db.execute("SELECT * FROM flights where id = :id", {"id": flight_id}).rowcount == 0:
        return render_template("error.html", message="No such flight.")
    db.execute("INSERT INTO passengers (name, flight_id) VALUES (:name, :flight_id)", {"name":name, "flight_id": flight_id})
    db.commit()
    return render_template("success.html", message="Passenger added successfully!")

@app.route("/flights")
def flights():
    """Get all flights. """

    flights = db.execute("SELECT * FROM flights").fetchall()
    if len(flights) == 0:
        return render_template("error.html", message="No flights found.")
    return render_template("flights.html", flights=flights)

@app.route("/flights/<int:flight_id>")
def flight(flight_id):
    """List Details for a flight"""
    flight = db.execute("SELECT * FROM flights WHERE id = :id", {"id": flight_id}).fetchone()
    if flight is None:
        return render_template("error.html", message="No such a flight.")
    passengers = db.execute("SELECT name FROM passengers where flight_id = :fid", {"fid" : flight_id})
    return render_template("flight.html", flight=flight, passengers=passengers)
    