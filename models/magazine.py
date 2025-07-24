# models/magazine.py
from models.library_item import LibraryItem

class Magazine(LibraryItem):
    """Represents a magazine."""
    def __init__(self, title, author_or_creator, publication_year, publisher, genre, issue_number, publication_date):
        super().__init__(title, author_or_creator, publication_year, publisher, genre)
        self.issue_number = issue_number
        self.publication_date = publication_date

    def display_info(self):
        base_info = super().display_info()
        return (f"{base_info}\n"
                f"  Type: Magazine\n"
                f"  Issue: {self.issue_number} ({self.publication_date})")