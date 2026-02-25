import os
from flask import Flask, render_template, request
from data_models import db, Author, Book
from datetime import datetime  # Preventing date conversion error!!

# Create Flask app
app = Flask(__name__)

# Absolute path
basedir = os.path.abspath(os.path.dirname(__file__))

# Set database URI
app.config['SQLALCHEMY_DATABASE_URI'] = \
    f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"

# Connect Flask with SQLAlchemy
db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()


@app.route("/add_author", methods=["GET", "POST"])
def add_author():
    """Add a new author to the database."""
    message = None

    if request.method == "POST":
        # Convert strings from form into dates
        birth_date = datetime.strptime(request.form.get("birth_date"), "%Y-%m-%d").date() \
            if request.form.get("birth_date") else None
        date_of_death = datetime.strptime(request.form.get("date_of_death"), "%Y-%m-%d").date() \
            if request.form.get("date_of_death") else None

        # Create new Author object
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
    """Add a new book to the database."""
    message = None
    authors = Author.query.all()  # Dropdown for authors

    if request.method == "POST":
        # Get data from form and create Book object
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
    """Display all books with optional sorting and keyword search."""
    sort = request.args.get("sort")       # Sort parameter
    keyword = request.args.get("keyword") # Keyword search

    books_query = Book.query.join(Author)

    # Filter by keyword if provided
    if keyword:
        books_query = books_query.filter(
            (Book.title.ilike(f"%{keyword}%")) |
            (Author.name.ilike(f"%{keyword}%"))
        )

    # Apply sorting
    if sort == "title":
        books_query = books_query.order_by(Book.title)
    elif sort == "author":
        books_query = books_query.order_by(Author.name)

    # Execute query
    books = books_query.all()

    return render_template("home.html", books=books, keyword=keyword)


if __name__ == "__main__":
    app.run(debug=True)