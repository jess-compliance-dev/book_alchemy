import os
from flask import Flask
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


with app.app_context():
  db.create_all()