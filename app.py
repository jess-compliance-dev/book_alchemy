import os
from flask import Flask, render_template, request
from data_models import db, Author, Book


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
        name = request.form.get("name")
        birth_date = request.form.get("birth_date")
        date_of_death = request.form.get("date_of_death")

        new_author = Author(
            name=name,
            birth_date=birth_date,
            date_of_death=date_of_death
        )

        db.session.add(new_author)
        db.session.commit()

        message = "Author successfully added."

    return render_template("add_author.html", message=message)


if __name__ == "__main__":
    app.run()


# with app.app_context():
#   db.create_all()