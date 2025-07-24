# core/library_manager.py
from datetime import date
from models.loan import Loan


class LibraryManager:
    """Manages all library operations."""

    def __init__(self):
        self.items = {}  # {item_id: item_object}
        self.users = {}  # {user_id: user_object}
        self.loans = {}  # {loan_id: loan_object}

    # --- Item Management ---
    def add_item(self, item):
        self.items[item.item_id] = item
        print(f"✅ Item '{item.title}' added with ID {item.item_id}.")

    def find_item(self, item_id):
        return self.items.get(item_id)

    # --- NEW: update_item method ---
    def update_item(self, item_id, **new_data):
        """Updates an existing item's attributes."""
        item = self.find_item(item_id)
        if not item:
            raise ValueError("❌ Error: Item not found.")

        for key, value in new_data.items():
            if hasattr(item, key):
                setattr(item, key, value)
        print(f"✅ Item ID {item_id} has been updated.")

    def delete_item(self, item_id):
        item = self.find_item(item_id)
        if not item:
            raise ValueError("❌ Error: Item not found.")
        if item.status == "Borrowed":
            raise ValueError("❌ Error: Cannot delete a borrowed item.")
        del self.items[item_id]
        print(f"🗑️ Item with ID {item_id} has been deleted.")

    # --- User Management ---
    def add_user(self, user):
        self.users[user.user_id] = user
        print(f"✅ User '{user.name}' registered with ID {user.user_id}.")

    def find_user(self, user_id):
        return self.users.get(user_id)

    # --- NEW: update_user method ---
    def update_user(self, user_id, **new_data):
        """Updates an existing user's attributes."""
        user = self.find_user(user_id)
        if not user:
            raise ValueError("❌ Error: User not found.")

        for key, value in new_data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        print(f"✅ User ID {user_id} has been updated.")

    def delete_user(self, user_id):
        user = self.find_user(user_id)
        if not user:
            raise ValueError("❌ Error: User not found.")
        if user.borrowed_items:
            raise ValueError("❌ Error: Cannot delete a user with borrowed items.")
        del self.users[user_id]
        print(f"🗑️ User with ID {user_id} has been deleted.")

    # ... (Borrowing & Returning methods are unchanged) ...
    def borrow_item(self, user_id, item_id):
        user = self.find_user(user_id)
        item = self.find_item(item_id)

        if not user: raise ValueError("❌ Error: User not found.")
        if not item: raise ValueError("❌ Error: Item not found.")

        if item.status != "Available":
            raise ValueError("❌ Error: Item is not available for borrowing.")
        if len(user.borrowed_items) >= user.max_borrow_limit:
            raise ValueError("❌ Error: User has reached the maximum borrowing limit.")

        item.status = "Borrowed"
        user.borrowed_items.append(item.item_id)
        new_loan = Loan(item_id=item.item_id, user_id=user.user_id)
        self.loans[new_loan.loan_id] = new_loan

        print(f"✅ Item '{item.title}' borrowed by '{user.name}'. Due: {new_loan.due_date}.")

    def return_item(self, user_id, item_id):
        user = self.find_user(user_id)
        item = self.find_item(item_id)

        if not user: raise ValueError("❌ Error: User not found.")
        if not item: raise ValueError("❌ Error: Item not found.")
        if item.item_id not in user.borrowed_items:
            raise ValueError("❌ Error: This user has not borrowed this item.")

        active_loan = None
        for loan in self.loans.values():
            if loan.user_id == user_id and loan.item_id == item_id and loan.return_date is None:
                active_loan = loan
                break

        if not active_loan:
            raise ValueError("❌ Error: Active loan record not found.")

        item.status = "Available"
        user.borrowed_items.remove(item.item_id)
        active_loan.return_date = date.today()
        fine = active_loan.calculate_fine()

        print(f"✅ Item '{item.title}' returned by '{user.name}'.")
        if fine > 0:
            print(f"🔔 A fine of ${fine:.2f} has been applied for late return.")

    def search_items_by_title(self, title_query):
        return [item for item in self.items.values() if title_query.lower() in item.title.lower()]

    def filter_items_by_status(self, status):
        return [item for item in self.items.values() if item.status.lower() == status.lower()]