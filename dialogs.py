# dialogs.py

import tkinter as tk
from tkinter import ttk, messagebox
from models.book import Book
from models.magazine import Magazine
from models.multimedia_item import MultimediaItem
from models.user import User

# --- NEW: Dark Theme Color Palette for Dialogs ---
BG_COLOR = "#3C3C3C"
TEXT_COLOR = "#EAEAEA"
ACCENT_COLOR = "#00BFFF"
ENTRY_BG_COLOR = "#4F4F4F"
FONT_NORMAL = ("Segoe UI", 10)
FONT_BOLD = ("Segoe UI", 10, "bold")


class CustomDialog(tk.Toplevel):
    """A base class for custom dialog windows."""

    def __init__(self, parent, title=None):
        super().__init__(parent)
        self.transient(parent)
        self.title(title)

        # --- Apply Dark Theme to Dialog Window ---
        self.configure(bg=BG_COLOR)
        self.setup_dialog_styles()

        self.parent = parent
        self.result = None

        body = ttk.Frame(self, style='Dialog.TFrame')
        body.pack(padx=10, pady=10, expand=True, fill="both")
        self.initial_focus = self.body(body)

        self.buttonbox()
        self.grab_set()

        if not self.initial_focus: self.initial_focus = self
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.geometry(f"+{parent.winfo_rootx() + 50}+{parent.winfo_rooty() + 50}")
        self.initial_focus.focus_set()
        self.wait_window(self)

    def setup_dialog_styles(self):
        s = ttk.Style(self)
        s.configure('Dialog.TFrame', background=BG_COLOR)
        s.configure('TLabel', background=BG_COLOR, foreground=TEXT_COLOR)
        s.configure('TLabelFrame', background=BG_COLOR, foreground=TEXT_COLOR)
        s.configure('TLabelFrame.Label', background=BG_COLOR, foreground=ACCENT_COLOR, font=FONT_BOLD)
        s.configure('TButton', font=FONT_BOLD, padding=6, background="#4A4A4A", foreground=TEXT_COLOR)
        s.map('TButton', background=[('active', '#6A6A6A')])
        s.configure('TEntry', fieldbackground=ENTRY_BG_COLOR, foreground=TEXT_COLOR, insertcolor=TEXT_COLOR)
        s.map('TCombobox', fieldbackground=[('readonly', ENTRY_BG_COLOR)], foreground=[('readonly', TEXT_COLOR)])

    # ... (Rest of the CustomDialog class is unchanged) ...
    def body(self, master):
        pass

    def buttonbox(self):
        box = ttk.Frame(self, style='Dialog.TFrame')
        ttk.Button(box, text="OK", width=10, command=self.ok).pack(side="left", padx=5, pady=5)
        ttk.Button(box, text="Cancel", width=10, command=self.cancel).pack(side="left", padx=5, pady=5)
        self.bind("<Return>", self.ok);
        self.bind("<Escape>", self.cancel)
        box.pack(pady=5)

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
    # This class logic is the same, but it will now inherit the dark theme styling
    # ... (No logical changes needed in ItemDialog or UserDialog) ...
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
        common_fields = ["Title", "Author/Creator", "Publication Year", "Publisher", "Genre"]
        for i, field in enumerate(common_fields):
            label = ttk.Label(self.common_fields_frame, text=f"{field}:", font=FONT_NORMAL)
            label.grid(row=i, column=0, padx=5, pady=5, sticky="w")
            entry = ttk.Entry(self.common_fields_frame)
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
        if hasattr(self.item_to_update, 'page_count'): self.entries['specifics']["Page Count"].insert(0,
                                                                                                      self.item_to_update.page_count)
        if hasattr(self.item_to_update, 'edition'): self.entries['specifics']["Edition"].insert(0,
                                                                                                self.item_to_update.edition)
        if hasattr(self.item_to_update, 'isbn'): self.entries['specifics']["ISBN"].insert(0, self.item_to_update.isbn)

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
            entry = ttk.Entry(self.specific_fields_frame)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
            self.entries['specifics'][field] = entry

    def validate(self):
        for key, entry in self.entries.items():
            if key == 'specifics': continue
            if not entry.get().strip(): messagebox.showerror("Validation Error",
                                                             f"Common field '{key}' cannot be empty.",
                                                             parent=self); return False
        for key, entry in self.entries['specifics'].items():
            if not entry.get().strip(): messagebox.showerror("Validation Error",
                                                             f"Specific field '{key}' cannot be empty.",
                                                             parent=self); return False
        return True

    def apply(self):
        try:
            data = {'author_or_creator': self.entries["Author/Creator"].get(),
                    'publication_year': int(self.entries["Publication Year"].get()),
                    'publisher': self.entries["Publisher"].get(), 'genre': self.entries["Genre"].get(),
                    'title': self.entries["Title"].get()}
            specific_args = {k.lower().replace(' ', '_').replace('(mins)', '_minutes'): v.get() for k, v in
                             self.entries['specifics'].items()}
            data.update(specific_args)
            if self.item_to_update:
                self.result = data
            else:
                item_type = self.item_type.get()
                if item_type == "Book":
                    data['page_count'] = int(data['page_count']); self.result = Book(**data)
                elif item_type == "Magazine":
                    self.result = Magazine(**data)
                elif item_type == "Multimedia":
                    data['duration_minutes'] = int(data['duration_minutes']); self.result = MultimediaItem(**data)
        except (ValueError, TypeError) as e:
            messagebox.showerror("Input Error", f"Please check your input values.\nDetails: {e}",
                                 parent=self); self.result = None


class UserDialog(CustomDialog):
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
        if self.user_to_update: self.entries["Name"].insert(0, self.user_to_update.name); self.entries[
            "Contact Info"].insert(0, self.user_to_update.contact_info)
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