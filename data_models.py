from flask_sqlalchemy import SQLAlchemy

# Zugriff auf Datenbankobjekt
db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = 'authors'

    author_id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False
    )
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date, nullable=True)
    date_of_death = db.Column(db.Date, nullable=True)

    # Beziehung zu Büchern (ein Autor -> viele Bücher)
    books = db.relationship('Book', backref='author', lazy=True)

    def __repr__(self):
        return f"<Author {self.name}>"

    def __str__(self):
        return f"{self.name} ({self.birth_date} - {self.date_of_death})"


class Book(db.Model):
    __tablename__ = 'books'

    book_id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    publication_year = db.Column(db.Integer, nullable=True)

    # ✅ KORREKTER Foreign Key
    author_id = db.Column(
        db.Integer,
        db.ForeignKey('authors.author_id'),
        nullable=False
    )

    def __repr__(self):
        return f"<Book {self.title}>"

    def __str__(self):
        return f"{self.title} ({self.publication_year}) by {self.author.name if self.author else 'Unknown'}"