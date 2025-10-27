"""
operations.py

Core functions for the Mini Library Management System.
Uses only functions, dictionaries, lists and tuples (no OOP) as required.
"""

from typing import List, Dict

# Global data structures
GENRES = ("Fiction", "Non-Fiction", "Sci-Fi", "Biography", "Mystery", "Romance")

books: Dict[str, Dict] = {}   # ISBN -> book info dict
members: List[Dict] = []     # list of member dicts

# -------------------------
# Create
# -------------------------
def add_book(isbn: str, title: str, author: str, genre: str, total_copies: int) -> bool:
    """Add a new book to the books dictionary.
    Returns True if successful, False otherwise (ISBN exists or invalid genre or bad copies).
    """
    isbn = str(isbn).strip()
    if not isbn:
        return False
    if isbn in books:
        return False
    if genre not in GENRES:
        return False
    if not isinstance(total_copies, int) or total_copies < 1:
        return False

    books[isbn] = {
        "title": title.strip(),
        "author": author.strip(),
        "genre": genre,
        "initial_copies": total_copies,    # original number of copies
        "available_copies": total_copies,  # copies available for borrowing
    }
    return True


def add_member(member_id: str, name: str, email: str) -> bool:
    """Add a new member if member_id is unique.
    Initializes borrowed_books as empty list.
    """
    member_id = str(member_id).strip()
    if not member_id:
        return False
    for m in members:
        if m["member_id"] == member_id:
            return False
    members.append({
        "member_id": member_id,
        "name": name.strip(),
        "email": email.strip(),
        "borrowed_books": []
    })
    return True


# -------------------------
# Read
# -------------------------
def search_books(query: str, by: str = "title") -> List[Dict]:
    """Search books by title or author (case-insensitive, partial matches).
    Returns a list of matching book dicts (each includes 'isbn').
    """
    q = str(query).lower().strip()
    if not q:
        return []
    results = []
    by = by.lower()
    for isbn, b in books.items():
        target = b["author"].lower() if by == "author" else b["title"].lower()
        if q in target:
            entry = b.copy()
            entry["isbn"] = isbn
            results.append(entry)
    return results


# -------------------------
# Update
# -------------------------
def update_book(isbn: str, title: str = None, author: str = None, genre: str = None, total_copies: int = None) -> bool:
    """Update specified fields of a book.
    If total_copies is provided, ensure it is not less than borrowed copies.
    """
    isbn = str(isbn).strip()
    if isbn not in books:
        return False
    book = books[isbn]

    if genre is not None:
        if genre not in GENRES:
            return False
        book["genre"] = genre

    if title is not None:
        book["title"] = title.strip()
    if author is not None:
        book["author"] = author.strip()

    if total_copies is not None:
        if not isinstance(total_copies, int) or total_copies < 0:
            return False
        borrowed = book["initial_copies"] - book["available_copies"]
        if total_copies < borrowed:
            return False
        book["initial_copies"] = total_copies
        book["available_copies"] = total_copies - borrowed

    return True


def update_member(member_id: str, name: str = None, email: str = None) -> bool:
    """Update member details if member exists."""
    member_id = str(member_id).strip()
    for m in members:
        if m["member_id"] == member_id:
            if name is not None:
                m["name"] = name.strip()
            if email is not None:
                m["email"] = email.strip()
            return True
    return False


# -------------------------
# Delete
# -------------------------
def delete_book(isbn: str) -> bool:
    """Remove a book if no copies are currently borrowed."""
    isbn = str(isbn).strip()
    if isbn not in books:
        return False
    book = books[isbn]
    if book["available_copies"] != book["initial_copies"]:
        return False
    del books[isbn]
    return True


def delete_member(member_id: str) -> bool:
    """Remove a member if they have no borrowed books."""
    member_id = str(member_id).strip()
    for i, m in enumerate(members):
        if m["member_id"] == member_id:
            if m["borrowed_books"]:
                return False
            members.pop(i)
            return True
    return False


# -------------------------
# Borrow / Return
# -------------------------
def borrow_book(isbn: str, member_id: str) -> bool:
    """Borrow a book if available and member under limit (3)."""
    isbn = str(isbn).strip()
    member_id = str(member_id).strip()

    if isbn not in books:
        return False
    book = books[isbn]
    if book["available_copies"] <= 0:
        return False

    member = next((m for m in members if m["member_id"] == member_id), None)
    if member is None:
        return False

    if len(member["borrowed_books"]) >= 3:
        return False

    if isbn in member["borrowed_books"]:
        return False

    book["available_copies"] -= 1
    member["borrowed_books"].append(isbn)
    return True


def return_book(isbn: str, member_id: str) -> bool:
    """Return a borrowed book."""
    isbn = str(isbn).strip()
    member_id = str(member_id).strip()

    if isbn not in books:
        return False
    book = books[isbn]

    member = next((m for m in members if m["member_id"] == member_id), None)
    if member is None:
        return False

    if isbn not in member["borrowed_books"]:
        return False

    member["borrowed_books"].remove(isbn)
    # Defensive: do not exceed initial copies
    if book["available_copies"] < book["initial_copies"]:
        book["available_copies"] += 1
    else:
        book["available_copies"] += 1
    return True
