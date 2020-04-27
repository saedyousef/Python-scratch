import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind = engine))

def main():
    # List all flights
    flights = db.execute("SELECT origin, destination, duration FROM flights")
    for flight in flights:
        print(f"{flight.origin} to {flight.destination} lasting {flight.duration} mintues")
    # Prompt user to choose a flight.
    flight_id = int(input("\nFlight ID: "))
    flight = db.execute("SELECT origin, destination, duration from flights WHERE id = :id", {"id": flight_id}).fetchone()

    if flight is None:
        print("Error: No such flight.")
        return
    passengers = db.execute("SELECT name FROM passengers where flight_id = :fid", {"fid" : flight_id}).fetchall()
    print("\nPassengers")
    for passneger in passengers:
        print(passneger.name)
    if  len(passengers) == 0:
        print("No passengers.")



if __name__ == "__main__":
    main()
