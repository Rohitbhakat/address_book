Address Book API ---

This is a FastAPI application for managing addresses and their geolocations. It provides endpoints for creating, updating, and finding addresses within a specified distance of a given location.

Features ---

1. Create new addresses with latitude and longitude coordinates.
2. Update existing addresses.
3. Retrieve addresses based on distance from a specified location.
4. Technologies Used (Python, FastAPI, SQLAlchemy, SQLite, Pydantic, Geopy, etc)
5. Using Poetry to install all the requirments

Setup Process ---

1. Install Poetry using (cmd- pip install poetry)
2. Install the req using potery (cmd- poetry install)
3. Run the server using (uvicorn app.main:app --host 0.0.0.0 --port 8080)

Example/Help ---
Have logged the longiture and latitude for help to search close location within the provided distance and latitude and longitude

Have used address as :- ("San Francisco, CA, USA", "New York City, NY, USA", "Sydney, Australia")

API to check swagger - http://localhost:8080/docs


