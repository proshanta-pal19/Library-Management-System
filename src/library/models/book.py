from library.exceptions import BookNotAvailableError, BookNotBorrowedError
# Declares a blueprint named Book

class Book:
    '''Represents a single book in the library'''

    # It is a constructor which runs automatically whenever we need to create a new book.
    def __init__(self, title: str, author: str, isbn: str) -> None:
        self._title = title
        self._author = author
        self._isbn = isbn
        self._is_available = True # Assume, every new book starts as available

    # Read-only properties
    @property
    def title(self) -> str:
        return self._title

    @property 
    def author(self) -> str:
        return self._author

    @property
    def isbn(self) -> str:
        return self._isbn

    @property
    def is_available(self) -> bool:
        return self._is_available

    # Behaviour
    def mark_as_borrowed(self) -> None:
        '''Mark the book as borrowed. Fails if it is already borrowed'''
        if not self._is_available:
            raise BookNotAvailableError(f'{self} is already borrowed.')
        self._is_available = False

    def mark_as_returned(self) -> None:
        '''Mark the book as returned. Fails if it is already returned'''
        if self._is_available:
            raise BookNotBorrowedError(f'{self} was not borrowed.')
        self._is_available = True

    def to_dict(self) -> dict[str, str]:
        '''Convert the book into a JSON dictionary'''
        return {
            'title': self._title,
            'author': self._author,
            'isbn': self._isbn
        }

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> 'Book':
        '''Build a Book from a dictionary'''
        return cls(data['title'], data['author'], data['isbn'])

    # Defines string representation of an object.
    def __str__(self) -> str:
        return f"'{self.title}' by {self.author}"

    # Defines an unambiguous, and detailed developer-focused description
    def __repr__(self) -> str:
        return f"Book(title={self.title!r}, author={self.author!r}, isbn={self.isbn!r})"