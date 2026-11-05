# Library is the manager who owns the collections of books and members, and it decides whether a borrow or return is allowed

from library.models.book import Book
from library.models.member import Member

class Library:
    '''Manage books and members, and enforce the borrowing rules'''

    def __init__(self, name: str) -> None:
        self.name = name
        self._books: dict[str, Book] = {}
        self._members: dict[str, Member] = {}

    # Resister a member to the library
    def register_member(self, member: Member) -> None:
        if member.member_id in self._members:
            raise ValueError(f'Member ID {member.member_id} is already registered.')
        self._members[member.member_id] = member

    # Add new books to the library
    def add_book(self, book: Book) -> None:
        if book.isbn in self._books:
            raise ValueError(f'A book with ISBN {book.isbn} already exists.')
        self._books[book.isbn] = book


    # Search books in the library
    def search_books(self, keyword: str) -> list[Book]:
        keyword = keyword.lower()

        return [book for book in self._books.values() if keyword in book.title.lower() or keyword in book.author.lower()]

    # Get all avaiable books in the library
    def get_available_books(self) -> list[Book]:
        return [book for book in self._books.values() if book.is_available]

    # Get the book using isbn number which a member wants to borrow
    def _get_book(self, isbn: str) -> Book:
        try:
            return self._books[isbn]
        except KeyError:
            raise ValueError(f'No book found with ISBN {isbn}.') from None

    # Find the member who want to borrow books 
    def _get_member(self, member_id: str) -> Member:
        try:
            return self._members[member_id]
        except KeyError:
            raise ValueError(f'No member found with ID {member_id}.') from None

    # Borrow books from the library
    def borrow_book(self, member_id: str, isbn: str) -> None:
        # Search the member and the book from the library
        member = self._get_member(member_id)
        book = self._get_book(isbn)

        if not book.is_available:
            raise ValueError(f'{book} is not available at that time.')
        if member.has_reached_limit():
            raise ValueError(f'{member.name} has reached the borrowing limit.')

        book.mark_as_borrowed() 
        member.add_book(book)

    # Return books to the library
    def return_book(self, member_id: str, isbn: str) -> None:
        member = self._get_member(member_id)
        book = self._get_book(isbn)

        if book not in member.borrowed_books:
            raise ValueError(f'{member.name} has not borrowed {book}.')

        book.mark_as_returned()
        member.remove_book(book)