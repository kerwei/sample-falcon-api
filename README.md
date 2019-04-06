# Project: Customer Data API
This simple Flask application provides the endpoints to perform the CRUD operations for the Customer entity.

## REQUIREMENTS
  * python 3.6.2
  * flask
  * sqlalchemy
  * psycopg2

## INSTRUCTIONS
1. Set up a new environment with the packages listed in the *REQUIREMENTS* above
2. Create a new database named giga, and a new login user, also named giga
  - > sudo -u postgres psql postgres
  - > CREATE DATABASE giga;
  - > CREATE USER giga WITH PASSWORD 'agig';
3. Deploy the data model:
 - > python database_setup.py
4. Load the table with mock data
 - > python loaddata.py
5. Boot up the Flask application
 - > python api_site.py
6. Visit http://localhost:5000/ for the reference on the API usage