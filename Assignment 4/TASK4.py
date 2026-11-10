# TASK 4: File and Exception Forensics
# 4.1 Flawed demonstration
# Do not use this as the final implementation.
def flawed_log(filename, book_name):
    file = open(filename, "w", encoding="utf-8")
    file.write(book_name)
    file.close()
# 4.2 Corrected implementation
def log_book(filename, book_name):
    try:
        with open(filename, "a", encoding="utf-8") as file:
            file.write(book_name.strip() + "\n")

    except PermissionError:
        print(f"Permission denied: {filename}")

    except OSError as error:
        print(f"Could not write log: {error}")
def read_log(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.read().splitlines()

    except FileNotFoundError:
        print("Log file does not exist yet.")
        return []

    except OSError as error:
        print(f"Could not read log: {error}")
        return []
# 4.3 Demonstration of the flawed version
print("Flawed demonstration:")
flawed_filename = "flawed_books.log"
flawed_log(flawed_filename, "Book-A")
flawed_log(flawed_filename, "Book-B")
flawed_log(flawed_filename, "Book-C")
print("Final flawed file:", read_log(flawed_filename))
# 4.4 Three-run test of the corrected version
print("\nCorrected demonstration:")
filename = "books.log"
log_book(filename, "Book-A")
log_book(filename, "Book-B")
log_book(filename, "Book-C")
print("Corrected file contents:", read_log(filename))
