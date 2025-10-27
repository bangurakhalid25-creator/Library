# tests.py
""""
Simple unit tests using assert statements.
Run: python tests.py
"""
from operations import (
    books, members, GENRES,
    add_book, add_member, search_books,
    update_book, update_member, delete_book, delete_member,
    borrow_book, return_book
)

# Reset state (in case tests run repeatedly)
books.clear()
members.clear()

# 1) Add books and members
assert add_book("B001", "Python Basics", "John Doe", "Non-Fiction", 3) == True, "Failed to add B001"
assert add_book("B002", "Advanced Python", "Jane Roe", "Non-Fiction", 2) == True, "Failed to add B002"
assert add_member("M001", "Alice", "alice@example.com") == True, "Failed to add member M001"
assert add_member("M002", "Bob", "bob@example.com") == True, "Failed to add member M002"

# 2) Borrowing: normal case
assert borrow_book("B001", "M001") == True, "Alice should borrow B001"
# available copies updated
assert books["B001"]["available_copies"] == 2, "available copies should be 2 after borrow"

# 3) Edge case: borrow when no copies left
assert borrow_book("B002", "M001") == True
assert borrow_book("B002", "M002") == True
assert borrow_book("B002", "M001") == False, "Should not borrow when no copies left"

# 4) Edge case: member exceeding 3-loan limit
assert add_book("B003", "Clean Code", "R. Martin", "Non-Fiction", 1) == True
assert add_book("B004", "Django Unleashed", "April", "Non-Fiction", 1) == True
assert borrow_book("B003", "M002") == True
assert borrow_book("B004", "M002") == True
assert add_book("B005", "Algorithms", "CLRS", "Non-Fiction", 1) == True
assert borrow_book("B005", "M002") == False, "Member M002 should not borrow more than 3 books"

# 5) Return book not borrowed -> should fail
assert return_book("B005", "M001") == False, "Cannot return book not borrowed"

# 6) Update member and book
assert update_member("M001", name="Alice Smith") == True
assert update_book("B001", title="Python Basics 2nd Edition") == True

# 7) Delete member with borrowed books should fail
assert delete_member("M001") == False, "Should not delete member with borrowed books"

# 8) Return a book and then delete member
assert return_book("B001", "M001") == True
# Return any remaining borrowed by M001
for isbn in list([b for b in members[0]["borrowed_books"]]) if members else []:
    return_book(isbn, "M001")
assert delete_member("M001") == True, "Member M001 should be deletable after returning books"

# 9) Delete book that has no borrowed copies
assert return_book("B003", "M002") == True
assert delete_book("B003") == True

print("All tests passed.")
