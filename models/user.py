# models/user.py
import itertools

class User:
    """Represents a library user."""
    _id_counter = itertools.count(1)

    def __init__(self, name, contact_info, max_borrow_limit=3):
        self.user_id = next(self._id_counter)
        self.name = name
        self.contact_info = contact_info
        self.borrowed_items = []  # List of item_ids
        self.max_borrow_limit = max_borrow_limit

    def display_info(self):
        """Returns a string with the user's details."""
        return (f"User ID: {self.user_id}\n"
                f"  Name: {self.name}\n"
                f"  Contact: {self.contact_info}\n"
                f"  Borrowed Items: {len(self.borrowed_items)}/{self.max_borrow_limit}")