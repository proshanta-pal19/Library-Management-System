# Custom exceptions

class LibraryError(Exception):
    '''Base class for all errors raised by the library system'''


class BookNotFoundError(LibraryError):
    '''Raised when no book matches the given ISBN'''


class MemberNotFoundError(LibraryError):
    '''Raised when no member matches the given ID'''


class DuplicateBookError(LibraryError):
    '''Raised when adding a book whose ISBN already exists'''


class DuplicateMemberError(LibraryError):
    '''Raised when registering a member ID that already exists'''


class BookNotAvailableError(LibraryError):
    '''Raised when borrowing a book that is already borrowed'''


class BookNotBorrowedError(LibraryError):
    '''Raised when returning a book that was not borrowed'''


class BorrowLimitReachedError(LibraryError):
    '''Raised when a member tries to exceed the borrowing limit'''


class StorageError(LibraryError):
    '''Raised when the data file cannot be read, written, or understood'''
