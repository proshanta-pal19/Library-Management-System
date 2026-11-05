from library.models.book import Book

class Member:
    '''Represents a library member who can borrow books'''

    # class attribute
    MAX_BOOKS = 3

    def __init__(self, member_id: str, name: str) -> None:
        self.member_id = member_id
        self.name = name
        self._borrowed_books: list[Book] = []

    # Helper function
    @property
    def borrowed_books(self) -> list[Book]:
        return list(self._borrowed_books)

    def has_reached_limit(self) -> bool:
        '''Return True if the member cannont borrow more books'''
        return len(self._borrowed_books) >= self.MAX_BOOKS

    def add_book(self, book: Book) -> None:
        '''Record a book as borrowed by this member'''
        self._borrowed_books.append(book)

    def remove_book(self, book: Book) -> None:
        '''Remove a returned book from this member's list'''
        self._borrowed_books.remove(book)

    def __str__(self) -> str:
        return f"{self.name} (ID: {self.member_id})"

    def __repr__(self) -> str:
        return f"Member(member_id={self.member_id!r}, name={self.name!r})"