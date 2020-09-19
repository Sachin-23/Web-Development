#!/bin/python

import os
import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


engine = create_engine(os.getenv("DATABASE_URL")) # 

db = scoped_session(sessionmaker(bind=engine))  #
'''
fd = open("books.csv", "r")
data = list(csv.reader(fd, delimiter=","))
print(fd != 0)
for i in range(1, len(data)):
    print(i)
    db.execute("INSERT INTO books (ISBN, title, author, year) VALUES (:ISBN, :title, :author, :year)", {"ISBN": data[i][0], "title": data[i][1], "author": data[i][2], "year": data[i][3]})
db.commit()
'''
#data1 = db.execute("SELECT * FROM books WHERE ISBN='0553262149';").fetchall()
data1 = db.execute("SELECT * FROM books;").fetchall()
print(data1)
#data3 = db.execute("SELECT * FROM users;").fetchall()
#data1 = db.execute("SELECT * FROM books;").fetchall()
#for i in data1:
#    print(i)
