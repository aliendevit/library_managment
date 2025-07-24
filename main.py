# main.py
from core.library_manager import LibraryManager
from models.book import Book
from models.magazine import Magazine
from models.multimedia_item import MultimediaItem
from models.user import User


def main_menu():
    """Displays the main menu and handles user input."""
    manager = LibraryManager()

    # --- Pre-populate with some data for demonstration ---
    book1 = Book("The Hitchhiker's Guide to the Galaxy", "Douglas Adams", 1979, "Pan Books", "Sci-Fi", 224, "1st",
                 "0-345-39180-2")
    mag1 = Magazine("National Geographic", "National Geographic Society", 2023, "NGS", "Science", 145, "July 2023")
    mm1 = MultimediaItem("The Matrix", "Wachowskis", 1999, "Warner Bros.", "Sci-Fi", "DVD", "Lana & Lilly Wachowski",
                         136)
    manager.add_item(book1)
    manager.add_item(mag1)
    manager.add_item(mm1)

    user1 = User("Alice Wonder", "alice@example.com")
    user2 = User("Bob Builder", "bob@example.com")
    manager.add_user(user1)
    manager.add_user(user2)
    print("\n--- Welcome to the Library Management System! ---")
    # --------------------------------------------------------

    while True:
        print("\n==================== MENU ====================")
        print("1.  List All Items")
        print("2.  List All Users")
        print("3.  Borrow an Item")
        print("4.  Return an Item")
        print("5.  Search Items by Title")
        print("6.  Filter Items by Status")
        print("7.  Add New Item")
        print("8.  Register New User")
        print("0.  Exit")
        print("============================================")

        choice = input("Enter your choice: ")

        try:
            if choice == '1':
                print("\n--- All Library Items ---")
                if not manager.items:
                    print("No items in the library.")
                for item in manager.items.values():
                    print("-" * 20)
                    print(item.display_info())

            elif choice == '2':
                print("\n--- All Registered Users ---")
                if not manager.users:
                    print("No users registered.")
                for user in manager.users.values():
                    print("-" * 20)
                    print(user.display_info())

            elif choice == '3':
                user_id = int(input("Enter your User ID: "))
                item_id = int(input("Enter the Item ID to borrow: "))
                manager.borrow_item(user_id, item_id)

            elif choice == '4':
                user_id = int(input("Enter your User ID: "))
                item_id = int(input("Enter the Item ID to return: "))
                manager.return_item(user_id, item_id)

            elif choice == '5':
                query = input("Enter title to search for: ")
                results = manager.search_items_by_title(query)
                print(f"\n--- Search Results for '{query}' ---")
                if not results:
                    print("No items found.")
                for item in results:
                    print("-" * 20)
                    print(item.display_info())

            elif choice == '6':
                status = input("Enter status to filter by (Available/Borrowed): ")
                results = manager.filter_items_by_status(status)
                print(f"\n--- Items with Status '{status}' ---")
                if not results:
                    print("No items found with that status.")
                for item in results:
                    print("-" * 20)
                    print(item.display_info())

            elif choice == '7':
                # Simplified add new item for CLI
                print("Select item type to add:")
                print("  a. Book")
                print("  b. Magazine")
                item_type = input("Choice: ").lower()
                title = input("Enter Title: ")
                author = input("Enter Author/Creator: ")
                year = int(input("Enter Publication Year: "))
                publisher = input("Enter Publisher: ")
                genre = input("Enter Genre: ")

                if item_type == 'a':
                    pages = int(input("Enter Page Count: "))
                    edition = input("Enter Edition: ")
                    isbn = input("Enter ISBN: ")
                    new_item = Book(title, author, year, publisher, genre, pages, edition, isbn)
                    manager.add_item(new_item)
                elif item_type == 'b':
                    # Add similar inputs for Magazine
                    print("Magazine adding not fully implemented in this demo.")
                else:
                    print("Invalid item type.")

            elif choice == '8':
                name = input("Enter User Name: ")
                contact = input("Enter Contact Info (email/phone): ")
                new_user = User(name, contact)
                manager.add_user(new_user)

            elif choice == '0':
                print("👋 Exiting the system. Goodbye!")
                break
            else:
                print("❌ Invalid choice, please try again.")

        except ValueError as e:
            print(f"\n{e}")
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")


if __name__ == "__main__":
    main_menu()