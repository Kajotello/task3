import sys
import pytest
from project.books.models import Book  # dopasuj ścieżkę importu


@pytest.mark.parametrize(
    "name, author, year_published, book_type, status",
    [
        ("Wiedźmin", "Andrzej Sapkowski", 1993, "Fantasy", "available"),

        # test polskich znaków
        ("Zażółć gęślą jaźń ĄĆĘŁŃÓŚŹŻ", "Grzegorz Brzęczyszczykiewicz", 2020, "Powieść", "wypożyczona"),

        # test innych znaków ASCII
        ("三体 (Problem trzech ciał)", "刘慈欣", 2008, "Literatura chińska", "available"),
        ("C++ & Python", "O'Connor", 2024, "IT", "reserved"),

        # warunki brzegowe
        ("A" * 64, "B" * 64, 2026, "C" * 20, "D" * 20),
        ("X", "Y", 0, "Z", "S"),
    ],
)
def test_valid_data(name, author, year_published, book_type, status):
    book = Book(
        name=name,
        author=author,
        year_published=year_published,
        book_type=book_type,
        status=status,
    )

    assert book.name == name
    assert book.author == author
    assert book.year_published == year_published
    assert book.book_type == book_type
    assert book.status == status



@pytest.mark.parametrize(
    "name, author, year_published, book_type, status",
    [
        # zbyt długie inputy
        ("A" * 100, "Autor", 2020, "Typ", "available"),
        ("Tytuł", "B" * 100, 2020, "Typ", "available"),
        ("Tytuł", "Autor", 2020, "C" * 100, "available"),
        ("Tytuł", "Autor", 2020, "Typ", "D" * 100),

        # ujemny rok wydania
        ("Tytuł", "Autor", -1, "Typ", "available"),

        # rok wydania jako str
        ("Tytuł", "Autor", 2020.5, "Typ", "available"),

        # rok wydania jako float
        ("Tytuł", "Autor", "2020", "Typ", "available"),
        
        # przepełnienie inta
        ("Tytuł", "Autor", sys.maxsize + 1, "Typ", "available"),
        
        # pusty tytuł
        ("", "Autor", 2020, "Typ", "available"),
        (None, "Autor", 2020, "Typ", "available"),

        # SQL injection
        ("'; DROP TABLE books; --", "Autor", 2020, "Typ", "available"),
        ("Tytuł", "1' OR '1'='1", 2020, "Typ", "available"),

        # JS injection
        ("<script>alert('XSS')</script>", "Autor", 2020, "Typ", "available"),
        ("Tytuł", "<img src=x onerror=alert(1)>", 2020, "Typ", "available"),
    ],
)
def test_invalid_data(name, author, year_published, book_type, status):
    with pytest.raises(ValueError):
        Book(
            name=name,
            author=author,
            year_published=year_published,
            book_type=book_type,
            status=status,
        )
