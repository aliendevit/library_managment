# dialogs.py

import tkinter as tk
from tkinter import ttk, messagebox
from models.book import Book
from models.magazine import Magazine
from models.multimedia_item import MultimediaItem
from models.user import User

FONT_NORMAL = ("Segoe UI", 10)
FONT_BOLD = ("Segoe UI", 10, "bold")


class CustomDialog(tk.Toplevel):
    # This base class is unchanged
    def __init__(self, parent, title=None):
        super().__init__(parent)
        self.transient(parent)
        self.title(title)
        self.configure(bg=parent.colors["FRAME_COLOR"])
        self.parent = parent
        self.result = None
        body = ttk.Frame(self, padding=10)
        body.pack(expand=True, fill="both")
        self.initial_focus = self.body(body)
        self.buttonbox()
        self.grab_set()
        if not self.initial_focus: self.initial_focus = self
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.geometry(f"+{parent.winfo_rootx() + 50}+{parent.winfo_rooty() + 50}")
        self.initial_focus.focus_set()
        self.wait_window(self)

    def body(self, master):
        pass

    def buttonbox(self):
        box = ttk.Frame(self, padding=(0, 5))
        ttk.Button(box, text="OK", width=10, style='Accent.TButton', command=self.ok).pack(side="left", padx=5)
        ttk.Button(box, text="Cancel", width=10, command=self.cancel).pack(side="left", padx=5)
        self.bind("<Return>", self.ok);
        self.bind("<Escape>", self.cancel)
        box.pack()

    def ok(self, event=None):
        if not self.validate(): self.initial_focus.focus_set(); return
        self.withdraw();
        self.update_idletasks();
        self.apply();
        self.cancel()

    def cancel(self, event=None):
        self.parent.focus_set(); self.destroy()

    def validate(self):
        return True

    def apply(self):
        pass


class ItemDialog(CustomDialog):
    def __init__(self, parent, title, item_to_update=None):
        self.item_to_update = item_to_update
        super().__init__(parent, title)

    def body(self, master):
        self.entries = {}
        ttk.Label(master, text="Select Item Type:", font=FONT_BOLD).grid(row=0, column=0, columnspan=2, pady=(0, 10))
        self.item_type = ttk.Combobox(master, values=["Book", "Magazine", "Multimedia"], state="readonly")
        self.item_type.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        if self.item_to_update:
            self.item_type.set(self.item_to_update.__class__.__name__); self.item_type.config(state="disabled")
        else:
            self.item_type.set("Book")
        self.item_type.bind("<<ComboboxSelected>>", self.toggle_fields)
        self.common_fields_frame = ttk.LabelFrame(master, text="Common Details", padding=10)
        self.common_fields_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")
        common_fields = ["Title", "Author/Creator", "Publication Year", "Publisher", "Genre", "Status"]
        for i, field in enumerate(common_fields):
            label = ttk.Label(self.common_fields_frame, text=f"{field}:", font=FONT_NORMAL)
            label.grid(row=i, column=0, padx=5, pady=5, sticky="w")
            if field == "Status":
                self.status_var = tk.StringVar()
                entry = ttk.Combobox(self.common_fields_frame, textvariable=self.status_var,
                                     values=["Available", "Borrowed", "Lost"], state="readonly")
                if not self.item_to_update:
                    self.status_var.set("Available")
                    entry.config(state="disabled")
            else:
                entry = ttk.Entry(self.common_fields_frame, width=40)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
            self.entries[field] = entry
        self.specific_fields_frame = ttk.LabelFrame(master, text="Specific Details", padding=10)
        self.specific_fields_frame.grid(row=3, column=0, columnspan=2, pady=5, sticky="ew")
        self.toggle_fields()
        self.prefill_form()
        return self.item_type

    def prefill_form(self):
        if not self.item_to_update: return
        self.entries["Title"].insert(0, self.item_to_update.title)
        self.entries["Author/Creator"].insert(0, self.item_to_update.author_or_creator)
        self.entries["Publication Year"].insert(0, self.item_to_update.publication_year)
        self.entries["Publisher"].insert(0, self.item_to_update.publisher)
        self.entries["Genre"].insert(0, self.item_to_update.genre)
        self.status_var.set(self.item_to_update.status)
        if isinstance(self.item_to_update, Book):
            self.entries['specifics']["Page Count"].insert(0, self.item_to_update.page_count)
            self.entries['specifics']["Edition"].insert(0, self.item_to_update.edition)
            self.entries['specifics']["ISBN"].insert(0, self.item_to_update.isbn)
        elif isinstance(self.item_to_update, Magazine):
            self.entries['specifics']["Issue Number"].insert(0, self.item_to_update.issue_number)
            self.entries['specifics']["Publication Date"].insert(0, self.item_to_update.publication_date)
        elif isinstance(self.item_to_update, MultimediaItem):
            self.entries['specifics']["Media Type"].insert(0, self.item_to_update.media_type)
            self.entries['specifics']["Director/Narrator"].insert(0, self.item_to_update.director_or_narrator)
            self.entries['specifics']["Duration (mins)"].insert(0, self.item_to_update.duration_minutes)

    def toggle_fields(self, event=None):
        for widget in self.specific_fields_frame.winfo_children(): widget.destroy()
        self.entries['specifics'] = {}
        item_type = self.item_type.get()
        self.specific_fields_frame.config(text=f"{item_type} Specifics")
        specific_fields = []
        if item_type == "Book":
            specific_fields = ["Page Count", "Edition", "ISBN"]
        elif item_type == "Magazine":
            specific_fields = ["Issue Number", "Publication Date"]
        elif item_type == "Multimedia":
            specific_fields = ["Media Type", "Director/Narrator", "Duration (mins)"]
        for i, field in enumerate(specific_fields):
            ttk.Label(self.specific_fields_frame, text=f"{field}:", font=FONT_NORMAL).grid(row=i, column=0, padx=5,
                                                                                           pady=5, sticky="w")
            entry = ttk.Entry(self.specific_fields_frame, width=40)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
            self.entries['specifics'][field] = entry

    def validate(self):
        for key, entry in self.entries.items():
            if key == 'specifics': continue
            if key == 'Status':
                if not self.status_var.get(): messagebox.showerror("Validation Error", "Status cannot be empty.",
                                                                   parent=self); return False
            elif not entry.get().strip():
                messagebox.showerror("Validation Error", f"Common field '{key}' cannot be empty.",
                                     parent=self); return False
        for key, entry in self.entries['specifics'].items():
            if not entry.get().strip(): messagebox.showerror("Validation Error",
                                                             f"Specific field '{key}' cannot be empty.",
                                                             parent=self); return False
        return True

    def apply(self):
        try:
            # --- THIS IS THE CORRECTION ---
            # Save the item type before the window is destroyed
            self.item_type_result = self.item_type.get()

            common_args = {
                'title': self.entries["Title"].get(), 'author_or_creator': self.entries["Author/Creator"].get(),
                'publication_year': self.entries["Publication Year"].get(),
                'publisher': self.entries["Publisher"].get(),
                'genre': self.entries["Genre"].get(), 'status': self.status_var.get()
            }
            specific_args = {}
            specific_entries = self.entries['specifics']
            if self.item_type_result == "Book":
                specific_args['page_count'] = specific_entries["Page Count"].get()
                specific_args['edition'] = specific_entries["Edition"].get()
                specific_args['isbn'] = specific_entries["ISBN"].get()
            elif self.item_type_result == "Magazine":
                specific_args['issue_number'] = specific_entries["Issue Number"].get()
                specific_args['publication_date'] = specific_entries["Publication Date"].get()
            elif self.item_type_result == "Multimedia":
                specific_args['media_type'] = specific_entries["Media Type"].get()
                specific_args['director_or_narrator'] = specific_entries["Director/Narrator"].get()
                specific_args['duration_minutes'] = specific_entries["Duration (mins)"].get()

            final_data = {**common_args, **specific_args}

            if self.item_to_update:
                self.result = final_data
            else:
                del final_data['status']
                final_data['publication_year'] = int(final_data['publication_year'])
                if self.item_type_result == "Book":
                    final_data['page_count'] = int(final_data['page_count'])
                    self.result = Book(**final_data)
                elif self.item_type_result == "Magazine":
                    self.result = Magazine(**final_data)
                elif self.item_type_result == "Multimedia":
                    final_data['duration_minutes'] = int(final_data['duration_minutes'])
                    self.result = MultimediaItem(**final_data)
        except (ValueError, TypeError, KeyError) as e:
            messagebox.showerror("Input Error",
                                 f"Please check your input values.\n(e.g., Year must be a number).\n\nDetails: {e}",
                                 parent=self)
            self.result = None


class UserDialog(CustomDialog):
    # This class is unchanged
    def __init__(self, parent, title, user_to_update=None):
        self.user_to_update = user_to_update
        super().__init__(parent, title)

    def body(self, master):
        self.entries = {}
        fields = ["Name", "Contact Info"]
        for i, field in enumerate(fields):
            ttk.Label(master, text=f"{field}:", font=FONT_NORMAL).grid(row=i, column=0, padx=5, pady=5, sticky="w")
            entry = ttk.Entry(master, width=40)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
            self.entries[field] = entry
        if self.user_to_update:
            self.entries["Name"].insert(0, self.user_to_update.name)
            self.entries["Contact Info"].insert(0, self.user_to_update.contact_info)
        return self.entries["Name"]

    def validate(self):
        for key, entry in self.entries.items():
            if not entry.get().strip(): messagebox.showerror("Validation Error", f"Field '{key}' cannot be empty.",
                                                             parent=self); return False
        return True

    def apply(self):
        data = {'name': self.entries["Name"].get(), 'contact_info': self.entries["Contact Info"].get()}
        if self.user_to_update:
            self.result = data
        else:
            self.result = User(**data)