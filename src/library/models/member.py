from library.models.book import Book

class Member:
    '''Represents a library member who can borrow books'''

    # class attribute
    MAX_BOOKS = 3
    MEMBER_TYPE = 'member' 

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

    def to_dict(self) -> dict:
        '''Convert the member into a JSON dictionary'''
        return {
            'type': self.MEMBER_TYPE,
            'memeber_id': self.member_id,
            'name': self.name,
            'borrowed_isbns': [book.isbn for book in self._borrowed_books]
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Member':
        '''Build a member from a dictionary'''
        return cls(data['member_id'], data['name'])

    def __str__(self) -> str:
        return f"{self.name} (ID: {self.member_id})"

    def __repr__(self) -> str:
        return f"Member(member_id={self.member_id!r}, name={self.name!r})"


class Student(Member):
    '''A student member with a lower borrowing limit'''

    MAX_BOOKS = 3
    MEMBER_TYPE = 'student'

    def __init__(self, member_id: str, name: str, semester: str) -> None:
        super().__init__(member_id, name)
        self.semester = semester

    def to_dict(self) -> dict:
        data = super().to_dict()
        data['semester'] = self.semester
        return data

    @classmethod
    def from_dict(cls, data: dict) -> 'Student':
        return cls(data['member_id'], data['name'], data['semester'])


class Teacher(Member):
    '''A teacher member with a higher borrowing limit'''

    MAX_BOOKS = 5
    MEMBER_TYPE = 'teacher'

    def __init__(self, member_id: str, name: str, department: str) -> None:
        super().__init__(member_id, name)
        self.department = department

    def to_dict(self) -> dict:
        data = super().to_dict()
        data['department'] = self.department
        return data

    @classmethod
    def from_dict(cls, data: dict) -> 'Teacher':
        return cls(data['member_id'], data['name'], data['department'])