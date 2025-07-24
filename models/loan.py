# models/loan.py
import itertools
from datetime import date, timedelta

class Loan:
    """Represents a loan transaction."""
    _id_counter = itertools.count(1)

    def __init__(self, item_id, user_id):
        self.loan_id = next(self._id_counter)
        self.item_id = item_id
        self.user_id = user_id
        self.borrow_date = date.today()
        self.due_date = self.borrow_date + timedelta(days=14) # 14-day loan period
        self.return_date = None
        self.fine_amount = 0.0

    def calculate_fine(self, fine_per_day=1.0):
        """Calculates fine if the item is returned late."""
        if self.return_date and self.return_date > self.due_date:
            days_overdue = (self.return_date - self.due_date).days
            self.fine_amount = days_overdue * fine_per_day
        return self.fine_amount