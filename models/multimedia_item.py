# models/multimedia_item.py
from models.library_item import LibraryItem

class MultimediaItem(LibraryItem):
    """Represents a multimedia item like a DVD or CD."""
    def __init__(self, title, author_or_creator, publication_year, publisher, genre, media_type, director_or_narrator, duration_minutes):
        super().__init__(title, author_or_creator, publication_year, publisher, genre)
        self.media_type = media_type
        self.director_or_narrator = director_or_narrator
        self.duration_minutes = duration_minutes

    def display_info(self):
        base_info = super().display_info()
        return (f"{base_info}\n"
                f"  Type: {self.media_type}\n"
                f"  Director/Narrator: {self.director_or_narrator}\n"
                f"  Duration: {self.duration_minutes} minutes")