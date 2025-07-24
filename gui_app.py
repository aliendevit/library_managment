# gui_app.py

import tkinter as tk
from tkinter import ttk, messagebox

from core.library_manager import LibraryManager
from dialogs import ItemDialog, UserDialog
from models.book import Book
from models.user import User
from models.magazine import Magazine
from models.multimedia_item import MultimediaItem

# --- NEW: Dark Theme Color Palette ---
BG_COLOR = "#2E2E2E"
FRAME_COLOR = "#3C3C3C"
TEXT_COLOR = "#EAEAEA"
ACCENT_COLOR = "#00BFFF"  # A brighter blue for dark backgrounds
ACCENT_TEXT_COLOR = "#2E2E2E"
HEADER_COLOR = "#4A4A4A"
ENTRY_BG_COLOR = "#4F4F4F"
ODD_ROW_COLOR = "#363636"
EVEN_ROW_COLOR = "#3C3C3C"

FONT_NORMAL = ("Segoe UI", 10)
FONT_BOLD = ("Segoe UI", 10, "bold")
FONT_TITLE = ("Segoe UI", 16, "bold")
DETAIL_LABEL_COLOR = "#AAAAAA"


class LibraryApp(tk.Tk):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager

        self.title("📚 Library Management System")
        self.geometry("1200x700")
        self.configure(bg=BG_COLOR)

        self.setup_styles()

        title_label = ttk.Label(self, text="Library Management System", font=FONT_TITLE, style='Title.TLabel')
        title_label.pack(pady=(10, 20))

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(pady=10, padx=10, expand=True, fill="both")

        self.create_items_tab()
        self.create_users_tab()
        self.create_borrow_return_tab()

        self.refresh_all_lists()

    def setup_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        # --- Configure all widgets for the Dark Theme ---
        style.configure('.', background=BG_COLOR, foreground=TEXT_COLOR, font=FONT_NORMAL)
        style.configure('TFrame', background=FRAME_COLOR)
        style.configure('Title.TLabel', font=FONT_TITLE, foreground=ACCENT_COLOR, background=BG_COLOR)
        style.configure('TLabel', background=FRAME_COLOR)
        style.configure('Detail.TLabel', foreground=TEXT_COLOR, background=FRAME_COLOR)
        style.configure('DetailHeader.TLabel', font=FONT_BOLD, foreground=DETAIL_LABEL_COLOR, background=FRAME_COLOR)
        style.configure('Accent.TLabel', font=FONT_BOLD, foreground=ACCENT_COLOR, background=FRAME_COLOR)

        # --- Buttons ---
        style.configure('TButton', font=FONT_BOLD, padding=6, background=HEADER_COLOR, foreground=TEXT_COLOR)
        style.map('TButton', background=[('active', '#6A6A6A')])
        style.configure('Accent.TButton', foreground=ACCENT_TEXT_COLOR, background=ACCENT_COLOR)
        style.map('Accent.TButton', background=[('active', '#009ACD')])

        # --- Notebook (Tabs) ---
        style.configure('TNotebook', background=BG_COLOR, borderwidth=0)
        style.configure('TNotebook.Tab', font=FONT_BOLD, padding=[10, 5], background=BG_COLOR,
                        foreground=DETAIL_LABEL_COLOR)
        style.map('TNotebook.Tab', background=[('selected', FRAME_COLOR)], foreground=[('selected', ACCENT_COLOR)])

        # --- Treeview (Lists) ---
        style.configure('Treeview', rowheight=25, fieldbackground=FRAME_COLOR, background=FRAME_COLOR,
                        foreground=TEXT_COLOR)
        style.configure('Treeview.Heading', font=FONT_BOLD, background=HEADER_COLOR, foreground=TEXT_COLOR, padding=5)
        style.map('Treeview.Heading', background=[('active', '#6A6A6A')])

        # --- Entry and Combobox ---
        style.configure('TEntry', fieldbackground=ENTRY_BG_COLOR, foreground=TEXT_COLOR, insertcolor=TEXT_COLOR,
                        borderwidth=1, relief='flat')
        style.map('TCombobox', fieldbackground=[('readonly', ENTRY_BG_COLOR)], foreground=[('readonly', TEXT_COLOR)],
                  selectbackground=[('readonly', ENTRY_BG_COLOR)])

        # --- LabelFrame ---
        style.configure('TLabelFrame', background=FRAME_COLOR, borderwidth=1, relief="solid")
        style.configure('TLabelFrame.Label', foreground=ACCENT_COLOR, background=FRAME_COLOR, font=FONT_BOLD)

    def create_items_tab(self):
        items_frame = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(items_frame, text="  Items  ")

        paned_window = ttk.PanedWindow(items_frame, orient='horizontal')
        paned_window.pack(expand=True, fill="both", padx=10, pady=10)

        list_frame = ttk.Frame(paned_window, padding=10)

        search_frame = ttk.Frame(list_frame)
        search_frame.pack(fill='x', pady=(0, 10))

        ttk.Label(search_frame, text="Search Title:", font=FONT_BOLD).pack(side='left', padx=(0, 5))
        self.item_search_var = tk.StringVar()
        item_search_entry = ttk.Entry(search_frame, textvariable=self.item_search_var, width=30)
        item_search_entry.pack(side='left', padx=5)

        ttk.Label(search_frame, text="Status:", font=FONT_BOLD).pack(side='left', padx=(10, 5))
        self.item_status_var = tk.StringVar()
        status_filter_combo = ttk.Combobox(search_frame, textvariable=self.item_status_var,
                                           values=["All", "Available", "Borrowed"], state="readonly")
        status_filter_combo.pack(side='left', padx=5)
        status_filter_combo.set("All")

        ttk.Button(search_frame, text="🔍 Search", command=self._perform_item_search, style='Accent.TButton').pack(
            side='left', padx=5)
        ttk.Button(search_frame, text="Clear", command=self._clear_item_search).pack(side='left', padx=5)

        cols = ("ID", "Title", "Type", "Status")
        self.items_tree = ttk.Treeview(list_frame, columns=cols, show='headings', selectmode='browse')
        for col in cols: self.items_tree.heading(col, text=col)
        self.items_tree.column("ID", width=50, anchor='center');
        self.items_tree.column("Title", width=300)
        self.items_tree.pack(expand=True, fill="both")
        self.items_tree.tag_configure('oddrow', background=ODD_ROW_COLOR)
        self.items_tree.tag_configure('evenrow', background=EVEN_ROW_COLOR)

        btn_frame = ttk.Frame(list_frame)
        btn_frame.pack(fill='x', pady=(10, 0))
        ttk.Button(btn_frame, text="➕ Add", command=self.add_item_window, style='Accent.TButton').pack(side='left',
                                                                                                       padx=5)
        ttk.Button(btn_frame, text="✏️ Update Selected", command=self.update_item_window).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="🗑️ Delete", command=self.delete_item).pack(side='left', padx=5)

        paned_window.add(list_frame, weight=2)

        details_frame_container = ttk.Frame(paned_window, padding=10)
        details_frame = ttk.LabelFrame(details_frame_container, text="Item Details", padding=15)
        details_frame.pack(expand=True, fill="both")
        self.detail_vars = {}
        detail_labels = ["ID", "Title", "Author/Creator", "Genre", "Publication Year", "Publisher", "Status",
                         "Item Type", "ISBN", "Edition", "Page Count", "Issue Number", "Publication Date", "Media Type",
                         "Director/Narrator", "Duration (mins)"]
        for i, label_text in enumerate(detail_labels):
            ttk.Label(details_frame, text=f"{label_text}:", style='DetailHeader.TLabel').grid(row=i, column=0,
                                                                                              sticky='w', padx=5,
                                                                                              pady=2)
            self.detail_vars[label_text] = tk.StringVar(value="N/A")
            ttk.Label(details_frame, textvariable=self.detail_vars[label_text], style='Detail.TLabel',
                      wraplength=250).grid(row=i, column=1, sticky='w', padx=5, pady=2)

        paned_window.add(details_frame_container, weight=1)
        self.items_tree.bind('<<TreeviewSelect>>', self._show_item_details)

    # All other methods are unchanged
    def create_users_tab(self):
        users_frame = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(users_frame, text="  Users  ")
        content_frame = ttk.Frame(users_frame, padding=10)
        content_frame.pack(expand=True, fill="both", padx=10, pady=10)

        user_search_frame = ttk.Frame(content_frame)
        user_search_frame.pack(fill='x', pady=(0, 10))
        ttk.Label(user_search_frame, text="Search Name/ID:", font=FONT_BOLD).pack(side='left', padx=(0, 5))
        self.user_search_var = tk.StringVar()
        user_search_entry = ttk.Entry(user_search_frame, textvariable=self.user_search_var, width=30)
        user_search_entry.pack(side='left', padx=5)
        ttk.Button(user_search_frame, text="🔍 Search", command=self._perform_user_search, style='Accent.TButton').pack(
            side='left', padx=5)
        ttk.Button(user_search_frame, text="Clear", command=self._clear_user_search).pack(side='left', padx=5)

        cols = ("ID", "Name", "Contact", "Borrowed")
        self.users_tree = ttk.Treeview(content_frame, columns=cols, show='headings', selectmode='browse')
        for col in cols: self.users_tree.heading(col, text=col)
        self.users_tree.column("ID", width=50, anchor='center');
        self.users_tree.column("Name", width=200)
        self.users_tree.pack(expand=True, fill="both")
        self.users_tree.tag_configure('oddrow', background=ODD_ROW_COLOR);
        self.users_tree.tag_configure('evenrow', background=EVEN_ROW_COLOR)
        btn_frame = ttk.Frame(content_frame)
        btn_frame.pack(fill='x', pady=(10, 0))
        ttk.Button(btn_frame, text="➕ Register", command=self.add_user_window, style='Accent.TButton').pack(side='left',
                                                                                                            padx=5)
        ttk.Button(btn_frame, text="✏️ Update Selected", command=self.update_user_window).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="🗑️ Delete", command=self.delete_user).pack(side='left', padx=5)

    def create_borrow_return_tab(self):
        br_frame = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(br_frame, text="  Borrow / Return  ")
        borrow_lf = ttk.LabelFrame(br_frame, text="Borrow an Item", padding=15)
        borrow_lf.pack(fill='x', padx=20, pady=20)
        ttk.Label(borrow_lf, text="User ID:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.borrow_user_id = ttk.Entry(borrow_lf, width=30)
        self.borrow_user_id.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(borrow_lf, text="Item ID:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.borrow_item_id = ttk.Entry(borrow_lf, width=30)
        self.borrow_item_id.grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(borrow_lf, text="Borrow Item", style='Accent.TButton', command=self.borrow_item).grid(row=2,
                                                                                                         column=1,
                                                                                                         padx=5,
                                                                                                         pady=10,
                                                                                                         sticky='e')
        return_lf = ttk.LabelFrame(br_frame, text="Return an Item", padding=15)
        return_lf.pack(fill='x', padx=20, pady=10)
        ttk.Label(return_lf, text="User ID:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.return_user_id = ttk.Entry(return_lf, width=30)
        self.return_user_id.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(return_lf, text="Item ID:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.return_item_id = ttk.Entry(return_lf, width=30)
        self.return_item_id.grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(return_lf, text="Return Item", style='Accent.TButton', command=self.return_item).grid(row=2,
                                                                                                         column=1,
                                                                                                         padx=5,
                                                                                                         pady=10,
                                                                                                         sticky='e')

    def refresh_items_list(self, title_query=None, status_filter=None):
        for i in self.items_tree.get_children(): self.items_tree.delete(i)
        items_to_display = list(self.manager.items.values())
        if title_query: items_to_display = [item for item in items_to_display if
                                            title_query.lower() in item.title.lower()]
        if status_filter and status_filter != "All": items_to_display = [item for item in items_to_display if
                                                                         item.status == status_filter]
        for i, item in enumerate(items_to_display):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.items_tree.insert("", "end", values=(item.item_id, item.title, item.__class__.__name__, item.status),
                                   tags=(tag,))

    def _perform_item_search(self):
        self.refresh_items_list(self.item_search_var.get().strip(), self.item_status_var.get())

    def _clear_item_search(self):
        self.item_search_var.set(""); self.item_status_var.set("All"); self.refresh_items_list()

    def refresh_users_list(self, query=None):
        for i in self.users_tree.get_children(): self.users_tree.delete(i)
        users_to_display = list(self.manager.users.values())
        if query: q = query.lower(); users_to_display = [user for user in users_to_display if
                                                         q in user.name.lower() or q == str(user.user_id)]
        for i, user in enumerate(users_to_display):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            borrowed_count = f"{len(user.borrowed_items)}/{user.max_borrow_limit}"
            self.users_tree.insert("", "end", values=(user.user_id, user.name, user.contact_info, borrowed_count),
                                   tags=(tag,))

    def _perform_user_search(self):
        self.refresh_users_list(self.user_search_var.get().strip())

    def _clear_user_search(self):
        self.user_search_var.set(""); self.refresh_users_list()

    def refresh_all_lists(self):
        self._clear_item_search(); self._clear_user_search(); [self.detail_vars[key].set("N/A") for key in
                                                               self.detail_vars]

    def _show_item_details(self, event):
        selected_items = self.items_tree.selection()
        if not selected_items: return
        item_id = int(self.items_tree.item(selected_items[0], 'values')[0])
        item = self.manager.find_item(item_id)
        if not item: return
        for key in self.detail_vars: self.detail_vars[key].set("N/A")
        self.detail_vars["ID"].set(item.item_id)
        self.detail_vars["Title"].set(item.title)
        self.detail_vars["Author/Creator"].set(item.author_or_creator)
        self.detail_vars["Genre"].set(item.genre)
        self.detail_vars["Publication Year"].set(item.publication_year)
        self.detail_vars["Publisher"].set(item.publisher)
        self.detail_vars["Status"].set(item.status)
        self.detail_vars["Item Type"].set(item.__class__.__name__)
        if hasattr(item, 'isbn'): self.detail_vars["ISBN"].set(item.isbn)
        if hasattr(item, 'edition'): self.detail_vars["Edition"].set(item.edition)
        if hasattr(item, 'page_count'): self.detail_vars["Page Count"].set(item.page_count)
        if hasattr(item, 'issue_number'): self.detail_vars["Issue Number"].set(item.issue_number)
        if hasattr(item, 'publication_date'): self.detail_vars["Publication Date"].set(item.publication_date)
        if hasattr(item, 'media_type'): self.detail_vars["Media Type"].set(item.media_type)
        if hasattr(item, 'director_or_narrator'): self.detail_vars["Director/Narrator"].set(item.director_or_narrator)
        if hasattr(item, 'duration_minutes'): self.detail_vars["Duration (mins)"].set(item.duration_minutes)

    def add_item_window(self):
        dialog = ItemDialog(self, title="Add New Library Item")
        if dialog.result: self.manager.add_item(dialog.result); self.refresh_all_lists(); messagebox.showinfo("Success",
                                                                                                              "Item added successfully!")

    def update_item_window(self):
        selected = self.items_tree.focus()
        if not selected: return messagebox.showwarning("Selection Error", "Please select an item to update.")
        item_id = int(self.items_tree.item(selected, 'values')[0])
        item_to_update = self.manager.find_item(item_id)
        dialog = ItemDialog(self, title="Update Item", item_to_update=item_to_update)
        if dialog.result: self.manager.update_item(item_id,
                                                   **dialog.result); self.refresh_all_lists(); messagebox.showinfo(
            "Success", "Item updated successfully!")

    def add_user_window(self):
        dialog = UserDialog(self, title="Register New User")
        if dialog.result: self.manager.add_user(dialog.result); self.refresh_all_lists(); messagebox.showinfo("Success",
                                                                                                              f"User '{dialog.result.name}' registered!")

    def update_user_window(self):
        selected = self.users_tree.focus()
        if not selected: return messagebox.showwarning("Selection Error", "Please select a user to update.")
        user_id = int(self.users_tree.item(selected, 'values')[0])
        user_to_update = self.manager.find_user(user_id)
        dialog = UserDialog(self, title="Update User", user_to_update=user_to_update)
        if dialog.result: self.manager.update_user(user_id,
                                                   **dialog.result); self.refresh_all_lists(); messagebox.showinfo(
            "Success", "User updated successfully!")

    def delete_item(self):
        selected = self.items_tree.focus()
        if not selected: return messagebox.showwarning("Selection Error", "Please select an item to delete.")
        item_id = int(self.items_tree.item(selected, 'values')[0])
        if messagebox.askyesno("Confirm", f"Are you sure you want to delete item ID {item_id}?"):
            try:
                self.manager.delete_item(item_id); self.refresh_all_lists()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def delete_user(self):
        selected = self.users_tree.focus()
        if not selected: return messagebox.showwarning("Selection Error", "Please select a user to delete.")
        user_id = int(self.users_tree.item(selected, 'values')[0])
        if messagebox.askyesno("Confirm", f"Are you sure you want to delete user ID {user_id}?"):
            try:
                self.manager.delete_user(user_id); self.refresh_all_lists()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def borrow_item(self):
        try:
            user_id = int(self.borrow_user_id.get())
            item_id = int(self.borrow_item_id.get())
            self.manager.borrow_item(user_id, item_id)
            self.refresh_all_lists()
            messagebox.showinfo("Success", "Item borrowed successfully!")
            self.borrow_user_id.delete(0, 'end');
            self.borrow_item_id.delete(0, 'end')
        except ValueError as e:
            messagebox.showerror("Error", f"Could not borrow item: {e}")

    def return_item(self):
        try:
            user_id = int(self.return_user_id.get())
            item_id = int(self.return_item_id.get())
            self.manager.return_item(user_id, item_id)
            self.refresh_all_lists()
            messagebox.showinfo("Success", "Item returned successfully!")
            self.return_user_id.delete(0, 'end');
            self.return_item_id.delete(0, 'end')
        except ValueError as e:
            messagebox.showerror("Error", f"Could not return item: {e}")


def main():
    manager = LibraryManager()
    manager.add_item(Book(title="The Hitchhiker's Guide", author_or_creator="Douglas Adams", publication_year=1979,
                          publisher="Pan Books", genre="Sci-Fi", page_count=224, edition="1st", isbn="0-345-39180-2"))
    manager.add_item(
        Magazine(title="National Geographic", author_or_creator="NGS", publication_year=2023, publisher="NGS",
                 genre="Science", issue_number=145, publication_date="July 2023"))
    manager.add_item(MultimediaItem(title="The Matrix", author_or_creator="Wachowskis", publication_year=1999,
                                    publisher="Warner Bros.", genre="Sci-Fi", media_type="DVD",
                                    director_or_narrator="Lana & Lilly Wachowski", duration_minutes=136))
    manager.add_user(User(name="Alice Wonder", contact_info="alice@example.com"))
    manager.add_user(User(name="Bob Builder", contact_info="bob@example.com"))

    app = LibraryApp(manager)
    app.mainloop()


if __name__ == "__main__":
    main()