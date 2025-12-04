# src/examples_persistence.py
from models.book import Book
from persistence.db import DB_PATH, init_db
from persistence.repo import BookRepo, TransactionRepo, UserRepo


def get_or_create_user(username, password):
    u = UserRepo.get_by_username(username)
    if u:
        return u.id
    return UserRepo.add(username, password)


def get_or_create_book(title, author, tags):
    found = BookRepo.search(title)
    for b in found:
        if b.title == title:
            return b.id
    return BookRepo.add(Book(id=None, title=title, author=author, tags=tags, copies=1))


if __name__ == "__main__":
    init_db()
    uid = get_or_create_user("demo", "demo123")
    bid = get_or_create_book("Demo Book", "Penulis", ["demo"])
    TransactionRepo.add(uid, bid, "borrow")
    print("DB:", DB_PATH)
    print("User demo id:", uid)
    print("Book id:", bid)
