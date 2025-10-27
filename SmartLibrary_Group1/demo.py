"""
demo.py

Sequential demo script demonstrating the Mini Library Management System.
Follows assignment requirements: add 5 books, 3 members, CRUD, borrow/return flows.
"""

from operations import books, members, GENRES, add_book, add_member, search_books, update_book, update_member, delete_book, delete_member, borrow_book, return_book
from pprint import pprint

def print_state(note=""):
    print("="*60)
    print(f"STATE: {note}")
    print("- Books -")
    pprint(books)
    print("- Members -")
    pprint(members)
    print("="*60)
    print()

def run_demo():
    # Initialize/clear in case of re-run
    books.clear()
    members.clear()
    print("Demo starting. Valid genres:", GENRES)
    print_state("Initial empty state")

    # Add 5 books
    add_book("ISBN001", "Python Basics", "John Doe", "Non-Fiction", 5)
    add_book("ISBN002", "Learn Java", "Jane Roe", "Non-Fiction", 3)
    add_book("ISBN003", "Space Odyssey", "Arthur C", "Sci-Fi", 2)
    add_book("ISBN004", "Love in Time", "Romance Author", "Romance", 4)
    add_book("ISBN005", "Mystery Manor", "Detective X", "Mystery", 2)
    print_state("After adding 5 books")

    # Add 3 members
    add_member("MM001", "Alice Smith", "alice.smith@example.com")
    add_member("MM002", "Bob Brown", "bob.brown@example.com")
    add_member("MM003", "Clara Oswald", "clara.o@example.com")
    print_state("After adding 3 members")

    # Search books by title
    print("Search for 'python' by title:")
    p = search_books("python", by="title")
    pprint(p)
    print()

    # Borrow flow
    print("Borrowing ISBN001 for MM001:", borrow_book("ISBN001", "MM001"))
    print("Borrowing ISBN001 for MM002:", borrow_book("ISBN001", "MM002"))
    print("Borrowing ISBN003 for MM001:", borrow_book("ISBN003", "MM001"))
    print_state("After some borrows")

    # Attempt to borrow when unavailable
    print("Attempt to borrow ISBN003 for MM002 (should succeed if copies available):", borrow_book("ISBN003", "MM002"))
    print("Attempt to borrow ISBN003 for MM003 (should fail if none left):", borrow_book("ISBN003", "MM003"))
    print_state("After attempts on ISBN003")

    # Return a book
    print("MM001 returns ISBN001:", return_book("ISBN001", "MM001"))
    print_state("After return")

    # Update operations
    print("Update book ISBN002 title -> 'Java: From Zero' :", update_book("ISBN002", title="Java: From Zero"))
    print("Update member MM003 name -> 'Clara O' :", update_member("MM003", name="Clara O"))
    print_state("After updates")

    # Delete attempts
    print("Attempt to delete book ISBN001 (should fail if borrowed):", delete_book("ISBN001"))
    # Ensure all borrowed copies returned for ISBN001
    for m in list(members):
        while "ISBN001" in m["borrowed_books"]:
            return_book("ISBN001", m["member_id"])
    print("Now delete book ISBN001 (should succeed):", delete_book("ISBN001"))
    print_state("Final state")

if __name__ == '__main__':
    run_demo()
