import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    f=open("books.csv")
    reader=csv.reader(f)
    for isbn,name,author,year in reader:
        if isbn != 'isbn':
            db.execute("INSERT INTO books (isbn,name,author,year) VALUES(:isbn, :name, :author, :year)",
                {"isbn": isbn, "name": name, "author": author, "year": year})
    db.commit()

if __name__ == "__main__":
    main()
