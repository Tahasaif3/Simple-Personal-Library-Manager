import os
import json
from datetime import datetime

class LibraryManager:
    def __init__(self):
        self.books = []
        self.filename = "library.txt"
        self.load_library()

    def load_library(self):
        """Load the library from a file if it exists."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as file:
                    self.books = json.load(file)
                print(f"Library loaded from {self.filename}.")
            except (json.JSONDecodeError, Exception) as e:
                print(f"Error loading library: {e}")
                self.books = []
        else:
            print("No saved library found. Starting with an empty library.")

    def save_library(self):
        """Save the library to a file."""
        try:
            with open(self.filename, 'w') as file:
                json.dump(self.books, file, indent=4)
            print(f"Library saved to {self.filename}.")
        except Exception as e:
            print(f"Error saving library: {e}")

    def add_book(self):
        """Add a book to the library."""
        title = input("Enter the book title: ")
        author = input("Enter the author: ")
        
        # Validate publication year
        while True:
            try:
                pub_year = int(input("Enter the publication year: "))
                current_year = datetime.now().year
                if 0 <= pub_year <= current_year:
                    break
                else:
                    print(f"Please enter a valid year between 0 and {current_year}.")
            except ValueError:
                print("Please enter a valid year (numbers only).")
        
        genre = input("Enter the genre: ")
        
        # Validate read status
        while True:
            read_status = input("Have you read this book? (yes/no): ").lower()
            if read_status in ['yes', 'y']:
                read_status = True
                break
            elif read_status in ['no', 'n']:
                read_status = False
                break
            else:
                print("Please enter 'yes' or 'no'.")
        
        book = {
            "title": title,
            "author": author,
            "publication_year": pub_year,
            "genre": genre,
            "read": read_status
        }
        
        self.books.append(book)
        print("Book added successfully!")

    def remove_book(self):
        """Remove a book from the library."""
        if not self.books:
            print("Your library is empty.")
            return
            
        title = input("Enter the title of the book to remove: ")
        
        # Find books with matching there titles
        matching_books = [book for book in self.books if book["title"].lower() == title.lower()]
        
        if not matching_books:
            print(f"No book found with title '{title}'.")
            return
        
        if len(matching_books) == 1:
            self.books.remove(matching_books[0])
            print("Book removed successfully!")
        else:
            print(f"Found {len(matching_books)} books with the title '{title}':")
            for i, book in enumerate(matching_books, 1):
                print(f"{i}. {book['title']} by {book['author']} ({book['publication_year']})")
            
            while True:
                try:
                    choice = int(input("Enter the number of the book to remove (0 to cancel): "))
                    if choice == 0:
                        print("Removal cancelled.")
                        return
                    if 1 <= choice <= len(matching_books):
                        self.books.remove(matching_books[choice-1])
                        print("Book removed successfully!")
                        return
                    else:
                        print(f"Please enter a number between 1 and {len(matching_books)}.")
                except ValueError:
                    print("Please enter a valid number.")

    def search_book(self):
        """Search for a book by title or author."""
        if not self.books:
            print("Your library is empty.")
            return
            
        print("Search by:")
        print("1. Title")
        print("2. Author")
        
        while True:
            try:
                choice = int(input("Enter your choice: "))
                if choice in [1, 2]:
                    break
                else:
                    print("Please enter 1 or 2.")
            except ValueError:
                print("Please enter a valid number.")
        
        if choice == 1:
            search_term = input("Enter the title: ").lower()
            matching_books = [book for book in self.books if search_term in book["title"].lower()]
            search_type = "title"
        else:
            search_term = input("Enter the author: ").lower()
            matching_books = [book for book in self.books if search_term in book["author"].lower()]
            search_type = "author"
        
        if matching_books:
            print(f"Matching Books (search term: '{search_term}' in {search_type}):")
            self.display_books(matching_books)
        else:
            print(f"No books found with {search_type} containing '{search_term}'.")

    def display_books(self, books_to_display=None):
        """Display all books or a specified subset."""
        if books_to_display is None:
            books_to_display = self.books
            
        if not books_to_display:
            print("No books to display.")
            return
            
        print("\nYour Library:")
        for i, book in enumerate(books_to_display, 1):
            read_status = "Read" if book["read"] else "Unread"
            print(f"{i}. {book['title']} by {book['author']} ({book['publication_year']}) - {book['genre']} - {read_status}")
        print()

    def display_statistics(self):
        """Display statistics about the library."""
        if not self.books:
            print("Your library is empty.")
            return
            
        total_books = len(self.books)
        read_books = sum(1 for book in self.books if book["read"])
        
        percentage_read = (read_books / total_books) * 100 if total_books > 0 else 0
        
        # Count books by genre 
        genres = {}
        for book in self.books:
            genre = book["genre"]
            genres[genre] = genres.get(genre, 0) + 1
        
        # Find the oldest and newest books
        sorted_books = sorted(self.books, key=lambda x: x["publication_year"])
        oldest_book = sorted_books[0] if sorted_books else None
        newest_book = sorted_books[-1] if sorted_books else None
        
        print("\nLibrary Statistics:")
        print(f"Total books: {total_books}")
        print(f"Books read: {read_books} ({percentage_read:.1f}%)")
        print(f"Books unread: {total_books - read_books} ({100 - percentage_read:.1f}%)")
        
        if genres:
            print("\nBooks by genre:")
            for genre, count in sorted(genres.items(), key=lambda x: x[1], reverse=True):
                print(f"  {genre}: {count} ({(count / total_books) * 100:.1f}%)")
        
        if oldest_book:
            print(f"\nOldest book: {oldest_book['title']} ({oldest_book['publication_year']})")
        if newest_book:
            print(f"Newest book: {newest_book['title']} ({newest_book['publication_year']})")
        print()  # Extra newline for readability

    def display_menu(self):
        """Display the main menu."""
        print("\nWelcome to your Personal Library Manager!")
        print("1. Add a book")
        print("2. Remove a book")
        print("3. Search for a book")
        print("4. Display all books")
        print("5. Display statistics")
        print("6. Exit")

    def run(self):
        """Run the library manager program."""
        while True:
            self.display_menu()
            
            try:
                choice = input("Enter your choice: ")
                
                if choice == '1':
                    self.add_book()
                elif choice == '2':
                    self.remove_book()
                elif choice == '3':
                    self.search_book()
                elif choice == '4':
                    self.display_books()
                elif choice == '5':
                    self.display_statistics()
                elif choice == '6':
                    self.save_library()
                    print("Goodbye!")
                    break
                else:
                    print("Invalid choice. Please try again.")
            except KeyboardInterrupt:
                print("\nProgram interrupted. Saving library...")
                self.save_library()
                print("Goodbye!")
                break
            except Exception as e:
                print(f"An error occurred: {e}")


if __name__ == "__main__":
    library = LibraryManager()
    library.run()