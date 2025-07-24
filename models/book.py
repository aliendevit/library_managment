# models/book.py
from models.library_item import LibraryItem

class Book(LibraryItem):
    """Represents a book, inheriting from LibraryItem."""
    def __init__(self, title, author_or_creator, publication_year, publisher, genre, page_count, edition, isbn):
        super().__init__(title, author_or_creator, publication_year, publisher, genre)
        self.page_count = page_count
        self.edition = edition
        self.isbn = isbn

    def display_info(self):
        """Extends the base display_info with book-specific details."""
        base_info = super().display_info()
        return (f"{base_info}\n"
                f"  Type: Book\n"
                f"  ISBN: {self.isbn}\n"
                f"  Pages: {self.page_count}\n"
                f"  Edition: {self.edition}")