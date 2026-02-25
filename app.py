import os
from flask import Flask, render_template, request
from data_models import db, Author, Book
from datetime import datetime  # Preventing date conversion error!!

# Flask App erstellen
app = Flask(__name__)

# Absoluten Pfad
basedir = os.path.abspath(os.path.dirname(__file__))

# Datenbank URI setzen
app.config['SQLALCHEMY_DATABASE_URI'] = \
    f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"

# Flask mit SQLAlchemy verbinden
db.init_app(app)

# Tabellen erstellen
with app.app_context():
    db.create_all()


@app.route("/add_author", methods=["GET", "POST"])
def add_author():
    message = None

    if request.method == "POST":
        # Strings aus Formular in date umwandeln
        birth_date = datetime.strptime(request.form.get("birth_date"), "%Y-%m-%d").date() \
            if request.form.get("birth_date") else None
        date_of_death = datetime.strptime(request.form.get("date_of_death"), "%Y-%m-%d").date() \
            if request.form.get("date_of_death") else None

        # Neues Author-Objekt erstellen
        new_author = Author(
            name=request.form.get("name"),
            birth_date=birth_date,
            date_of_death=date_of_death
        )

        db.session.add(new_author)
        db.session.commit()

        message = "Author successfully added."

    return render_template("add_author.html", message=message)


@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    message = None
    authors = Author.query.all()  # Dropdown

    if request.method == "POST":
        # Daten aus Formular holen und direkt an Book übergeben
        new_book = Book(
            isbn=request.form.get("isbn"),
            title=request.form.get("title"),
            publication_year=request.form.get("publication_year"),
            author_id=request.form.get("author_id")
        )

        db.session.add(new_book)
        db.session.commit()

        message = "Book successfully added."

    return render_template("add_book.html", authors=authors, message=message)


@app.route("/")
def home():
    books = Book.query.all()
    return render_template("home.html", books=books)


if __name__ == "__main__":
    app.run(debug=True)


# with app.app_context():
#   db.create_all()