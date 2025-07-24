# gui_app.py

import tkinter as tk
from tkinter import ttk, messagebox
from core.library_manager import LibraryManager
from dialogs import ItemDialog, UserDialog
from models.book import Book
from models.magazine import Magazine
from models.multimedia_item import MultimediaItem
from models.user import User

THEMES = {
    "Dark": {"BG_COLOR": "#2E2E2E", "FRAME_COLOR": "#3C3C3C", "TEXT_COLOR": "#EAEAEA", "ACCENT_COLOR": "#00BFFF",
             "ACCENT_TEXT_COLOR": "#2E2E2E", "HEADER_COLOR": "#4A4A4A", "ENTRY_BG_COLOR": "#4F4F4F",
             "ODD_ROW_COLOR": "#363636", "EVEN_ROW_COLOR": "#3C3C3C", "DETAIL_LABEL_COLOR": "#AAAAAA"},
    "Light": {"BG_COLOR": "#F5F5F5", "FRAME_COLOR": "#FFFFFF", "TEXT_COLOR": "#333333", "ACCENT_COLOR": "#007ACC",
              "ACCENT_TEXT_COLOR": "#FFFFFF", "HEADER_COLOR": "#E0E0E0", "ENTRY_BG_COLOR": "#FFFFFF",
              "ODD_ROW_COLOR": "#E8F0F9", "EVEN_ROW_COLOR": "#FFFFFF", "DETAIL_LABEL_COLOR": "#555555"}
}
FONT_NORMAL = ("Segoe UI", 10)
FONT_BOLD = ("Segoe UI", 10, "bold")
FONT_TITLE = ("Segoe UI", 16, "bold")


class LibraryApp(tk.Tk):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.title("📚 Library Management System")
        self.geometry("1200x700")
        self.theme_var = tk.StringVar(value="Dark")
        self.create_menu()
        self.apply_theme()
        title_label = ttk.Label(self, text="Library Management System", font=FONT_TITLE, style='Title.TLabel')
        title_label.pack(pady=(10, 20))
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(pady=10, padx=10, expand=True, fill="both")
        self.create_items_tab()
        self.create_users_tab()
        self.create_borrow_return_tab()
        self.create_loans_tab()
        self.refresh_all_lists()

    def create_menu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        theme_menu = tk.Menu(settings_menu, tearoff=0)
        settings_menu.add_cascade(label="Theme", menu=theme_menu)
        theme_menu.add_radiobutton(label="Dark", variable=self.theme_var, value="Dark", command=self.apply_theme)
        theme_menu.add_radiobutton(label="Light", variable=self.theme_var, value="Light", command=self.apply_theme)

    def apply_theme(self):
        self.colors = THEMES[self.theme_var.get()]
        self.configure(bg=self.colors["BG_COLOR"])
        self.setup_styles()
        if hasattr(self, 'items_tree'):
            self.refresh_all_lists()

    def setup_styles(self):
        colors = self.colors;
        style = ttk.Style(self);
        style.theme_use("clam")
        style.configure('.', background=colors["BG_COLOR"], foreground=colors["TEXT_COLOR"], font=FONT_NORMAL)
        style.configure('TFrame', background=colors["FRAME_COLOR"])
        style.configure('Title.TLabel', font=FONT_TITLE, foreground=colors["ACCENT_COLOR"],
                        background=colors["BG_COLOR"])
        style.configure('TLabel', background=colors["FRAME_COLOR"], foreground=colors["TEXT_COLOR"])
        style.configure('Detail.TLabel', foreground=colors["TEXT_COLOR"], background=colors["FRAME_COLOR"])
        style.configure('DetailHeader.TLabel', font=FONT_BOLD, foreground=colors["DETAIL_LABEL_COLOR"],
                        background=colors["FRAME_COLOR"])
        style.configure('Accent.TLabel', font=FONT_BOLD, foreground=colors["ACCENT_COLOR"],
                        background=colors["FRAME_COLOR"])
        style.configure('TButton', font=FONT_BOLD, padding=6, background=colors["HEADER_COLOR"],
                        foreground=colors["TEXT_COLOR"]);
        style.map('TButton', background=[('active', '#6A6A6A')])
        style.configure('Accent.TButton', foreground=colors["ACCENT_TEXT_COLOR"], background=colors["ACCENT_COLOR"]);
        style.map('Accent.TButton', background=[('active', '#009ACD')])
        style.configure('TNotebook', background=colors["BG_COLOR"], borderwidth=0)
        style.configure('TNotebook.Tab', font=FONT_BOLD, padding=[10, 5], background=colors["BG_COLOR"],
                        foreground=colors["DETAIL_LABEL_COLOR"]);
        style.map('TNotebook.Tab', background=[('selected', colors["FRAME_COLOR"])],
                  foreground=[('selected', colors["ACCENT_COLOR"])])
        style.configure('Treeview', rowheight=25, fieldbackground=colors["FRAME_COLOR"],
                        background=colors["FRAME_COLOR"], foreground=colors["TEXT_COLOR"])
        style.configure('Treeview.Heading', font=FONT_BOLD, background=colors["HEADER_COLOR"],
                        foreground=colors["TEXT_COLOR"], padding=5);
        style.map('Treeview.Heading', background=[('active', '#6A6A6A')])
        style.configure('TEntry', fieldbackground=colors["ENTRY_BG_COLOR"], foreground=colors["TEXT_COLOR"],
                        insertcolor=colors["TEXT_COLOR"], borderwidth=1, relief='flat')
        style.map('TCombobox', fieldbackground=[('readonly', colors["ENTRY_BG_COLOR"])],
                  foreground=[('readonly', colors["TEXT_COLOR"])],
                  selectbackground=[('readonly', colors["ENTRY_BG_COLOR"])])
        style.configure('TLabelFrame', background=colors["FRAME_COLOR"], borderwidth=1, relief="solid")
        style.configure('TLabelFrame.Label', foreground=colors["ACCENT_COLOR"], background=colors["FRAME_COLOR"],
                        font=FONT_BOLD)

    def create_items_tab(self):
        items_frame = ttk.Frame(self.notebook, style='TFrame');
        self.notebook.add(items_frame, text="  Items  ")
        paned_window = ttk.PanedWindow(items_frame, orient='horizontal');
        paned_window.pack(expand=True, fill="both", padx=10, pady=10)
        list_frame = ttk.Frame(paned_window, padding=10)
        search_frame = ttk.Frame(list_frame);
        search_frame.pack(fill='x', pady=(0, 10))
        ttk.Label(search_frame, text="Search Title:", font=FONT_BOLD).pack(side='left', padx=(0, 5))
        self.item_search_var = tk.StringVar();
        ttk.Entry(search_frame, textvariable=self.item_search_var, width=30).pack(side='left', padx=5)
        ttk.Label(search_frame, text="Status:", font=FONT_BOLD).pack(side='left', padx=(10, 5))
        self.item_status_var = tk.StringVar()
        status_filter_combo = ttk.Combobox(search_frame, textvariable=self.item_status_var,
                                           values=["All", "Available", "Borrowed", "Lost"], state="readonly");
        status_filter_combo.pack(side='left', padx=5);
        status_filter_combo.set("All")
        ttk.Button(search_frame, text="🔍 Search", command=self._perform_item_search, style='Accent.TButton').pack(
            side='left', padx=5)
        ttk.Button(search_frame, text="Clear", command=self._clear_item_search).pack(side='left', padx=5)
        cols = ("ID", "Title", "Type", "Status");
        self.items_tree = ttk.Treeview(list_frame, columns=cols, show='headings', selectmode='browse')
        for col in cols: self.items_tree.heading(col, text=col)
        self.items_tree.column("ID", width=50, anchor='center');
        self.items_tree.column("Title", width=300)
        self.items_tree.pack(expand=True, fill="both")
        btn_frame = ttk.Frame(list_frame);
        btn_frame.pack(fill='x', pady=(10, 0))
        ttk.Button(btn_frame, text="➕ Add", command=self.add_item_window, style='Accent.TButton').pack(side='left',
                                                                                                       padx=5)
        ttk.Button(btn_frame, text="✏️ Update Selected", command=self.update_item_window).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="🗑️ Delete", command=self.delete_item).pack(side='left', padx=5)
        paned_window.add(list_frame, weight=2)
        details_frame_container = ttk.Frame(paned_window, padding=10)
        details_frame = ttk.LabelFrame(details_frame_container, text="Item Details", padding=15);
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
        paned_window.add(details_frame_container, weight=1);
        self.items_tree.bind('<<TreeviewSelect>>', self._show_item_details)

    def create_users_tab(self):
        users_frame = ttk.Frame(self.notebook, style='TFrame');
        self.notebook.add(users_frame, text="  Users  ")
        content_frame = ttk.Frame(users_frame, padding=10);
        content_frame.pack(expand=True, fill="both", padx=10, pady=10)
        user_search_frame = ttk.Frame(content_frame);
        user_search_frame.pack(fill='x', pady=(0, 10))
        ttk.Label(user_search_frame, text="Search Name/ID:", font=FONT_BOLD).pack(side='left', padx=(0, 5))
        self.user_search_var = tk.StringVar();
        ttk.Entry(user_search_frame, textvariable=self.user_search_var, width=30).pack(side='left', padx=5)
        ttk.Button(user_search_frame, text="🔍 Search", command=self._perform_user_search, style='Accent.TButton').pack(
            side='left', padx=5)
        ttk.Button(user_search_frame, text="Clear", command=self._clear_user_search).pack(side='left', padx=5)
        cols = ("ID", "Name", "Contact", "Borrowed");
        self.users_tree = ttk.Treeview(content_frame, columns=cols, show='headings', selectmode='browse')
        for col in cols: self.users_tree.heading(col, text=col)
        self.users_tree.column("ID", width=50, anchor='center');
        self.users_tree.column("Name", width=200)
        self.users_tree.pack(expand=True, fill="both")
        btn_frame = ttk.Frame(content_frame);
        btn_frame.pack(fill='x', pady=(10, 0))
        ttk.Button(btn_frame, text="➕ Register", command=self.add_user_window, style='Accent.TButton').pack(side='left',
                                                                                                            padx=5)
        ttk.Button(btn_frame, text="✏️ Update Selected", command=self.update_user_window).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="🗑️ Delete", command=self.delete_user).pack(side='left', padx=5)

    def create_borrow_return_tab(self):
        br_frame = ttk.Frame(self.notebook, style='TFrame');
        self.notebook.add(br_frame, text="  Borrow / Return  ")
        borrow_lf = ttk.LabelFrame(br_frame, text="Borrow an Item", padding=15);
        borrow_lf.pack(fill='x', padx=20, pady=20)
        ttk.Label(borrow_lf, text="User ID:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.borrow_user_id = ttk.Entry(borrow_lf, width=30);
        self.borrow_user_id.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(borrow_lf, text="Item ID:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.borrow_item_id = ttk.Entry(borrow_lf, width=30);
        self.borrow_item_id.grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(borrow_lf, text="Borrow Item", style='Accent.TButton', command=self.borrow_item).grid(row=2,
                                                                                                         column=1,
                                                                                                         padx=5,
                                                                                                         pady=10,
                                                                                                         sticky='e')
        return_lf = ttk.LabelFrame(br_frame, text="Return an Item", padding=15);
        return_lf.pack(fill='x', padx=20, pady=10)
        ttk.Label(return_lf, text="User ID:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.return_user_id = ttk.Entry(return_lf, width=30);
        self.return_user_id.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(return_lf, text="Item ID:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.return_item_id = ttk.Entry(return_lf, width=30);
        self.return_item_id.grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(return_lf, text="Return Item", style='Accent.TButton', command=self.return_item).grid(row=2,
                                                                                                         column=1,
                                                                                                         padx=5,
                                                                                                         pady=10,
                                                                                                         sticky='e')

    def create_loans_tab(self):
        loans_frame = ttk.Frame(self.notebook, style='TFrame');
        self.notebook.add(loans_frame, text="  Loan Records  ")
        content_frame = ttk.Frame(loans_frame, padding=10);
        content_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        cols = ("Loan ID", "Item Title", "User Name", "Borrowed", "Due", "Returned", "Fine");
        self.loans_tree = ttk.Treeview(content_frame, columns=cols, show='headings', selectmode='browse')
        for col in cols: self.loans_tree.heading(col, text=col)
        self.loans_tree.column("Loan ID", width=60, anchor='center');
        self.loans_tree.column("Item Title", width=250);
        self.loans_tree.column("User Name", width=150);
        self.loans_tree.column("Fine", width=80, anchor='e')
        self.loans_tree.pack(expand=True, fill='both')
        btn_frame = ttk.Frame(content_frame);
        btn_frame.pack(fill='x', pady=(10, 0))
        ttk.Button(btn_frame, text="🔄 Refresh", command=self.refresh_loans_list).pack(side='left', padx=5)

    def refresh_loans_list(self):
        self.loans_tree.tag_configure('oddrow', background=self.colors["ODD_ROW_COLOR"]);
        self.loans_tree.tag_configure('evenrow', background=self.colors["EVEN_ROW_COLOR"])
        for i in self.loans_tree.get_children(): self.loans_tree.delete(i)
        sorted_loans = sorted(self.manager.loans.values(), key=lambda loan: loan.borrow_date, reverse=True)
        for i, loan in enumerate(sorted_loans):
            item = self.manager.find_item(loan.item_id);
            user = self.manager.find_user(loan.user_id)
            item_title = item.title if item else f"Deleted Item (ID: {loan.item_id})";
            user_name = user.name if user else f"Deleted User (ID: {loan.user_id})"
            return_date = loan.return_date if loan.return_date else "Not Returned";
            fine_str = f"${loan.fine_amount:.2f}" if loan.fine_amount > 0 else "$0.00"
            self.loans_tree.insert("", "end", values=(
            loan.loan_id, item_title, user_name, loan.borrow_date, loan.due_date, return_date, fine_str),
                                   tags=('evenrow' if i % 2 == 0 else 'oddrow',))

    def refresh_items_list(self, title_query=None, status_filter=None):
        self.items_tree.tag_configure('oddrow', background=self.colors["ODD_ROW_COLOR"]);
        self.items_tree.tag_configure('evenrow', background=self.colors["EVEN_ROW_COLOR"])
        for i in self.items_tree.get_children(): self.items_tree.delete(i)
        items_to_display = list(self.manager.items.values())
        if title_query: items_to_display = [item for item in items_to_display if
                                            title_query.lower() in item.title.lower()]
        if status_filter and status_filter != "All": items_to_display = [item for item in items_to_display if
                                                                         item.status == status_filter]
        for i, item in enumerate(items_to_display):
            self.items_tree.insert("", "end", values=(item.item_id, item.title, item.__class__.__name__, item.status),
                                   tags=('evenrow' if i % 2 == 0 else 'oddrow',))

    def _perform_item_search(self):
        self.refresh_items_list(self.item_search_var.get().strip(), self.item_status_var.get())

    def _clear_item_search(self):
        self.item_search_var.set(""); self.item_status_var.set("All"); self.refresh_items_list()

    def refresh_users_list(self, query=None):
        self.users_tree.tag_configure('oddrow', background=self.colors["ODD_ROW_COLOR"]);
        self.users_tree.tag_configure('evenrow', background=self.colors["EVEN_ROW_COLOR"])
        for i in self.users_tree.get_children(): self.users_tree.delete(i)
        users_to_display = list(self.manager.users.values())
        if query: q = query.lower(); users_to_display = [user for user in users_to_display if
                                                         q in user.name.lower() or q == str(user.user_id)]
        for i, user in enumerate(users_to_display):
            self.users_tree.insert("", "end", values=(
            user.user_id, user.name, user.contact_info, f"{len(user.borrowed_items)}/{user.max_borrow_limit}"),
                                   tags=('evenrow' if i % 2 == 0 else 'oddrow',))

    def _perform_user_search(self):
        self.refresh_users_list(self.user_search_var.get().strip())

    def _clear_user_search(self):
        self.user_search_var.set(""); self.refresh_users_list()

    def refresh_all_lists(self):
        self._clear_item_search(); self._clear_user_search(); self.refresh_loans_list(); [
            self.detail_vars[key].set("N/A") for key in self.detail_vars]

    def _show_item_details(self, event):
        selected_items = self.items_tree.selection()
        if not selected_items: return
        item_id = int(self.items_tree.item(selected_items[0], 'values')[0]);
        item = self.manager.find_item(item_id)
        if not item: return
        for key in self.detail_vars: self.detail_vars[key].set("N/A")
        self.detail_vars["ID"].set(item.item_id);
        self.detail_vars["Title"].set(item.title);
        self.detail_vars["Author/Creator"].set(item.author_or_creator);
        self.detail_vars["Genre"].set(item.genre);
        self.detail_vars["Publication Year"].set(item.publication_year);
        self.detail_vars["Publisher"].set(item.publisher);
        self.detail_vars["Status"].set(item.status);
        self.detail_vars["Item Type"].set(item.__class__.__name__)
        if hasattr(item, 'isbn'): self.detail_vars["ISBN"].set(item.isbn)
        if hasattr(item, 'edition'): self.detail_vars["Edition"].set(item.edition)
        if hasattr(item, 'page_count'): self.detail_vars["Page Count"].set(item.page_count)
        if hasattr(item, 'issue_number'): self.detail_vars["Issue Number"].set(item.issue_number)
        if hasattr(item, 'publication_date'): self.detail_vars["Publication Date"].set(item.publication_date)
        if hasattr(item, 'media_type'): self.detail_vars["Media Type"].set(item.media_type)
        if hasattr(item, 'director_or_narrator'): self.detail_vars["Director/Narrator"].set(item.director_or_narrator)
        if hasattr(item, 'duration_minutes'): self.detail_vars["Duration (mins)"].set(item.duration_minutes)

    # --- THIS IS THE CORRECTED METHOD ---
    def add_item_window(self):
        dialog = ItemDialog(self, title="Add New Library Item")
        if dialog.result:
            # The dialog.result is already a fully formed object.
            # We just need to pass it to the manager.
            self.manager.add_item(dialog.result)
            self.refresh_all_lists()
            messagebox.showinfo("Success", "Item added successfully!")

    def update_item_window(self):
        selected = self.items_tree.focus()
        if not selected: return messagebox.showwarning("Selection Error", "Please select an item to update.")
        item_id = int(self.items_tree.item(selected, 'values')[0]);
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
        user_id = int(self.users_tree.item(selected, 'values')[0]);
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
            user_id = int(self.borrow_user_id.get());
            item_id = int(self.borrow_item_id.get())
            self.manager.borrow_item(user_id, item_id);
            self.refresh_all_lists();
            messagebox.showinfo("Success", "Item borrowed successfully!")
            self.borrow_user_id.delete(0, 'end');
            self.borrow_item_id.delete(0, 'end')
        except ValueError as e:
            messagebox.showerror("Error", f"Could not borrow item: {e}")

    def return_item(self):
        try:
            user_id = int(self.return_user_id.get());
            item_id = int(self.return_item_id.get())
            self.manager.return_item(user_id, item_id);
            self.refresh_all_lists();
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
    manager.add_user(User(name="Alice Wonder", contact_info="alice@example.com"))
    app = LibraryApp(manager)
    app.mainloop()


if __name__ == "__main__":
    main()