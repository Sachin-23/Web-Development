from flask import Flask
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


engine = create_engine(os.getenv("DATABASE_URL"))


db = scoped_session(sessionmaker(bind=engine))  

app = Flask(__name__)

@app.route("/")
def hello():
    flights = db.execute("SELECT * FROM users")
    return flights[0]



