class LibraryItem:
    def __init__(self, title):
        self.title = title


class Book(LibraryItem):
    def __init__(self, title, author):
        super().__init__(title)
        self.author = author

    def __str__(self):
        return f"Book: {self.title} by {self.author}"


class DVD(LibraryItem):
    def __init__(self, title, genre):
        super().__init__(title)
        self.genre = genre

    def __str__(self):
        return f"DVD: {self.title} Genre: {self.genre}"


class Magazine(LibraryItem):
    def __init__(self, title, issue):
        super().__init__(title)
        self.issue = issue

    def __str__(self):
        return f"Magazine: {self.title} Issue: {self.issue}"


class Library:
    def __init__(self, items: list[LibraryItem] = None):
        self.items = items if items is not None else []

    def check_out(self, title: str):
        for item in self.items:
            if item.title == title:
                self.items.remove(item)
                return item
        return None

    def return_item(self, item: LibraryItem):
        self.items.append(item)

    def display(self, title: str):
        for item in self.items:
            if item.title == title:
                print(item)
                return
        print("Item not found")

    def __str__(self):
        output = "The library has the following items:\n"
        for item in self.items:
            output += f"{item}\n"
        return output


book = Book("The Great Gatsby", "F. Scott Fitzgerald")
dvd = DVD("The Godfather", "Crime")
magazine = Magazine("Time", "July 2024")

library = Library([book, dvd, magazine])

print(library)
library.display("The Godfather")
item = library.check_out("Time")

print(library)

library.return_item(item)

print(library)
