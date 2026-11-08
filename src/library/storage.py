import json
from pathlib import Path
from library.exceptions import LibraryError, StorageError
from library.library import Library
from library.models.book import Book
from library.models.member import Member, Student, Teacher


# Maps the member type label
MEMBER_TYPES: dict[str, type[Member]] = {
    Member.MEMBER_TYPE: Member,
    Student.MEMBER_TYPE: Student,
    Teacher.MEMBER_TYPE: Teacher
}

class Storage:
    '''Saves and loads a Library as as JSON file'''

    def __init__(self, file_path: str | Path) -> None:
        self.file_path = Path(file_path)

    def save(self, library: Library) -> None:
        data = {
            'name': library.name,
            'books': [book.to_dict() for book in library.books],
            'members': [member.to_dict() for member in library.members]
        }

        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        # Write to a temporary file, then swap it in.
        # If the program crashes mid-write, the old data file is still intact.
        temp_path = self.file_path.with_suffix('.temp')
        temp_path.write_text(json.dumps(data, indent=2), encoding='utf-8')
        temp_path.replace(self.file_path)

    def load(self) -> Library:
        try:
            raw_text = self.file_path.read_text(encoding='utf-8')
            data = json.loads(raw_text)
        except FileNotFoundError:
            raise StorageError(f'Data file not found: {self.file_path}') from None
        except json.JSONDecodeError:
            raise StorageError(f'Data file is not valid JSON: {self.file_path}') from None

        try:
            library = Library(data['name'])

            for book_data in data['books']:
                library.add_book(Book.from_dict(book_data))

            for member_data in data['members']:
                member_class = MEMBER_TYPES[member_data['type']]
                member = member_class.from_dict(member_data)
                library.register_member(member)

                # Reuse the borrow rules to restore who holds what
                for isbn in member_data['borrowed_isbns']:
                    library.borrow_book(member.member_id, isbn)

        except (KeyError, LibraryError) as error:
            raise StorageError(f'Data file has invalid content: {error}') from error

        return library