# models/library_item.py
import itertools

class LibraryItem:
    """Base class for all library items."""
    _id_counter = itertools.count(1)

    def __init__(self, title, author_or_creator, publication_year, publisher, genre):
        self.item_id = next(self._id_counter)
        self.title = title
        self.author_or_creator = author_or_creator
        self.publication_year = publication_year
        self.publisher = publisher
        self.genre = genre
        self.status = "Available"  # "Available", "Borrowed", "Lost"

    def display_info(self):
        """Returns a string with the item's details."""
        return (f"ID: {self.item_id}\n"
                f"  Title: {self.title}\n"
                f"  Creator: {self.author_or_creator}\n"
                f"  Published: {self.publication_year} by {self.publisher}\n"
                f"  Genre: {self.genre}\n"
                f"  Status: {self.status}")