import tkinter as tk
from tkinter import ttk, messagebox
import datetime


class LibrarySystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Book Management System")
        self.root.geometry("900x700")
        self.root.configure(bg='#f5f5f5')

        # Data structures
        self.book_stack = []  # Recently returned books (LIFO)
        self.waiting_queue = []  # Waiting list for popular books (FIFO)

        # Available books with copies - USING YOUR TITLES
        self.available_books = {
            "BIBLE": 3,
            "SCIENCE": 2,
            "CHEMISTRY": 1,
            "HAPPY": 2,
            "SECRET": 1
        }

        # Simulated member database
        self.members = {
            "MEM001": "Alice Johnson",
            "MEM002": "Bob Smith",
            "MEM003": "Carol Davis",
            "MEM004": "David Wilson",
            "MEM005": "Eva Brown"
        }

        self.borrowed_books = {}
        self.setup_gui()

    def setup_gui(self):
        # Header
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        header_frame.pack_propagate(False)

        title = tk.Label(header_frame, text="📚 Library Book Management System",
                         font=('Arial', 20, 'bold'), bg='#2c3e50', fg='white')
        title.pack(expand=True)

        # Main container
        main_container = tk.Frame(self.root, bg='#f5f5f5')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Left side - Book Operations
        left_frame = tk.Frame(main_container, bg='#ecf0f1',
                              relief=tk.RAISED, bd=2)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Right side - Visualizations
        right_frame = tk.Frame(
            main_container, bg='#ecf0f1', relief=tk.RAISED, bd=2)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH,
                         expand=True, padx=(10, 0))

        self.setup_book_operations(left_frame)
        self.setup_visualizations(right_frame)

        self.update_displays()

    def setup_book_operations(self, parent):
        # Book Operations Title
        tk.Label(parent, text="Book Operations", font=('Arial', 16, 'bold'),
                 bg='#ecf0f1').pack(pady=10)

        # Book selection
        book_frame = tk.Frame(parent, bg='#ecf0f1')
        book_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(book_frame, text="Select Book:", font=('Arial', 12),
                 bg='#ecf0f1').pack(side=tk.LEFT)

        self.book_var = tk.StringVar()
        book_combo = ttk.Combobox(book_frame, textvariable=self.book_var,
                                  values=list(self.available_books.keys()), width=20)
        book_combo.pack(side=tk.LEFT, padx=10)
        book_combo.set("Select a book")

        # Member selection
        member_frame = tk.Frame(parent, bg='#ecf0f1')
        member_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(member_frame, text="Select Member:", font=('Arial', 12),
                 bg='#ecf0f1').pack(side=tk.LEFT)

        self.member_var = tk.StringVar()
        member_combo = ttk.Combobox(member_frame, textvariable=self.member_var,
                                    values=[f"{mid} - {name}" for mid,
                                            name in self.members.items()],
                                    width=20)
        member_combo.pack(side=tk.LEFT, padx=10)
        member_combo.set("Select a member")

        # Quick member info
        info_frame = tk.Frame(parent, bg='#ecf0f1')
        info_frame.pack(fill=tk.X, padx=20, pady=5)

        self.member_info_label = tk.Label(info_frame, text="Select a member to see details",
                                          font=('Arial', 10), bg='#ecf0f1', fg='#666')
        self.member_info_label.pack()

        # Operation buttons
        button_frame = tk.Frame(parent, bg='#ecf0f1')
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="Borrow Book", command=self.borrow_book,
                  bg='#3498db', fg='white', font=('Arial', 12), width=15).pack(pady=5)

        tk.Button(button_frame, text="Return Book", command=self.return_book,
                  bg='#2ecc71', fg='white', font=('Arial', 12), width=15).pack(pady=5)

        tk.Button(button_frame, text="Join Waiting List", command=self.join_waiting_list,
                  bg='#e67e22', fg='white', font=('Arial', 12), width=15).pack(pady=5)

        tk.Button(button_frame, text="Process Next Waiting", command=self.process_waiting,
                  bg='#9b59b6', fg='white', font=('Arial', 12), width=15).pack(pady=5)

        # Available books display
        available_frame = tk.Frame(parent, bg='#ecf0f1')
        available_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        tk.Label(available_frame, text="Available Books:", font=('Arial', 14, 'bold'),
                 bg='#ecf0f1').pack(anchor=tk.W)

        self.available_text = tk.Text(
            available_frame, height=8, width=30, font=('Arial', 10))
        self.available_text.pack(fill=tk.BOTH, expand=True, pady=5)

    def setup_visualizations(self, parent):
        # Visualizations Title
        tk.Label(parent, text="System Status", font=('Arial', 16, 'bold'),
                 bg='#ecf0f1').pack(pady=10)

        # Recently returned books (STACK)
        stack_frame = tk.Frame(parent, bg='#ecf0f1')
        stack_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(stack_frame, text="📚 Recently Returned Books (STACK)",
                 font=('Arial', 12, 'bold'), bg='#ecf0f1', fg='#c0392b').pack(anchor=tk.W)

        self.stack_text = tk.Text(
            stack_frame, height=6, width=35, font=('Arial', 10))
        self.stack_text.pack(fill=tk.X, pady=5)

        # Waiting list (QUEUE)
        queue_frame = tk.Frame(parent, bg='#ecf0f1')
        queue_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(queue_frame, text="👥 Waiting List for Popular Books (QUEUE)",
                 font=('Arial', 12, 'bold'), bg='#ecf0f1', fg='#2980b9').pack(anchor=tk.W)

        self.queue_text = tk.Text(
            queue_frame, height=6, width=35, font=('Arial', 10))
        self.queue_text.pack(fill=tk.X, pady=5)

        # Currently borrowed books
        borrowed_frame = tk.Frame(parent, bg='#ecf0f1')
        borrowed_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        tk.Label(borrowed_frame, text="Currently Borrowed Books:",
                 font=('Arial', 14, 'bold'), bg='#ecf0f1').pack(anchor=tk.W)

        self.borrowed_text = tk.Text(
            borrowed_frame, height=8, width=30, font=('Arial', 10))
        self.borrowed_text.pack(fill=tk.BOTH, expand=True, pady=5)

        # Member list
        member_frame = tk.Frame(parent, bg='#ecf0f1')
        member_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(member_frame, text="Library Members:",
                 font=('Arial', 12, 'bold'), bg='#ecf0f1').pack(anchor=tk.W)

        member_list_text = tk.Text(
            member_frame, height=4, width=35, font=('Arial', 9))
        member_list_text.pack(fill=tk.X, pady=5)

        # Populate member list
        for mid, name in self.members.items():
            member_list_text.insert(tk.END, f"• {mid}: {name}\n")
        member_list_text.config(state=tk.DISABLED)

    def get_selected_member_id(self):
        """Extract member ID from the selection"""
        selection = self.member_var.get()
        if selection and " - " in selection:
            return selection.split(" - ")[0]
        return None

    def get_selected_member_name(self):
        """Extract member name from the selection"""
        selection = self.member_var.get()
        if selection and " - " in selection:
            return selection.split(" - ")[1]
        return None

    def borrow_book(self):
        book = self.book_var.get()
        member_id = self.get_selected_member_id()
        member_name = self.get_selected_member_name()

        if book == "Select a book" or not book:
            messagebox.showwarning("Input Error", "Please select a book!")
            return

        if not member_id:
            messagebox.showwarning("Input Error", "Please select a member!")
            return

        if self.available_books.get(book, 0) > 0:
            # Borrow the book
            self.available_books[book] -= 1
            borrow_date = datetime.datetime.now().strftime("%Y-%m-%d")
            return_date = (datetime.datetime.now() +
                           datetime.timedelta(days=14)).strftime("%Y-%m-%d")

            self.borrowed_books[book] = {
                'member_id': member_id,
                'member_name': member_name,
                'borrow_date': borrow_date,
                'return_date': return_date
            }

            messagebox.showinfo("Success",
                                f"Book '{book}' borrowed successfully!\n"
                                f"Member: {member_name}\n"
                                f"Return by: {return_date}")
            self.update_displays()
        else:
            messagebox.showinfo("Not Available",
                                f"'{book}' is currently not available.\nYou can join the waiting list.")

    def return_book(self):
        book = self.book_var.get()
        member_id = self.get_selected_member_id()
        member_name = self.get_selected_member_name()

        if book == "Select a book" or not book:
            messagebox.showwarning("Input Error", "Please select a book!")
            return

        if not member_id:
            messagebox.showwarning("Input Error", "Please select a member!")
            return

        if book in self.borrowed_books and self.borrowed_books[book]['member_id'] == member_id:
            # Return the book (add to stack)
            del self.borrowed_books[book]
            self.available_books[book] += 1
            self.book_stack.append({
                'book': book,
                'returned_by': member_name,
                'timestamp': datetime.datetime.now().strftime("%m/%d %H:%M")
            })  # Push to stack

            messagebox.showinfo(
                "Success", f"Book '{book}' returned successfully by {member_name}!")
            self.update_displays()
        else:
            messagebox.showwarning(
                "Error", "This book is not currently borrowed by this member.")

    def join_waiting_list(self):
        book = self.book_var.get()
        member_id = self.get_selected_member_id()
        member_name = self.get_selected_member_name()

        if book == "Select a book" or not book:
            messagebox.showwarning("Input Error", "Please select a book!")
            return

        if not member_id:
            messagebox.showwarning("Input Error", "Please select a member!")
            return

        # Add to waiting queue
        self.waiting_queue.append({
            'book': book,
            'member_id': member_id,
            'member_name': member_name,
            'joined_at': datetime.datetime.now().strftime("%m/%d %H:%M")
        })

        messagebox.showinfo("Success",
                            f"Added to waiting list for '{book}'\n"
                            f"Member: {member_name}\n"
                            f"Position in queue: {len(self.waiting_queue)}")
        self.update_displays()

    def process_waiting(self):
        if not self.waiting_queue:
            messagebox.showinfo("Info", "No one in the waiting list.")
            return

        # Get next person from queue
        next_request = self.waiting_queue.pop(0)  # Dequeue
        book = next_request['book']
        member_id = next_request['member_id']
        member_name = next_request['member_name']

        if self.available_books.get(book, 0) > 0:
            # Borrow the book to waiting person
            self.available_books[book] -= 1
            borrow_date = datetime.datetime.now().strftime("%Y-%m-%d")
            return_date = (datetime.datetime.now() +
                           datetime.timedelta(days=14)).strftime("%Y-%m-%d")

            self.borrowed_books[book] = {
                'member_id': member_id,
                'member_name': member_name,
                'borrow_date': borrow_date,
                'return_date': return_date
            }

            messagebox.showinfo("Waiting List Processed",
                                f"Book '{book}' given to {member_name} from waiting list!\n"
                                f"Return by: {return_date}")
        else:
            messagebox.showinfo("Still Not Available",
                                f"Book '{book}' is still not available for {member_name}")

        self.update_displays()

    def update_displays(self):
        # Update available books
        self.available_text.delete(1.0, tk.END)
        for book, count in self.available_books.items():
            status = "✓ Available" if count > 0 else "✗ Not Available"
            self.available_text.insert(tk.END, f"• {book}\n")
            self.available_text.insert(
                tk.END, f"  Copies: {count} ({status})\n\n")

        # Update stack display (recently returned)
        self.stack_text.delete(1.0, tk.END)
        if not self.book_stack:
            self.stack_text.insert(tk.END, "No recently returned books")
        else:
            self.stack_text.insert(tk.END, "Most Recent ↓\n")
            self.stack_text.insert(tk.END, "―" * 30 + "\n")
            # Show last 5
            for i, return_info in enumerate(reversed(self.book_stack[-5:])):
                self.stack_text.insert(
                    tk.END, f"{i+1}. {return_info['book']}\n")
                self.stack_text.insert(
                    tk.END, f"   Returned by: {return_info['returned_by']}\n")
                self.stack_text.insert(
                    tk.END, f"   At: {return_info['timestamp']}\n\n")
            self.stack_text.insert(tk.END, "―" * 30 + "\n")
            self.stack_text.insert(tk.END, "Oldest ↑")

        # Update queue display (waiting list)
        self.queue_text.delete(1.0, tk.END)
        if not self.waiting_queue:
            self.queue_text.insert(tk.END, "No one in waiting list")
        else:
            self.queue_text.insert(tk.END, "Next in Line →\n")
            self.queue_text.insert(tk.END, "―" * 30 + "\n")
            # Show first 5
            for i, request in enumerate(self.waiting_queue[:5]):
                self.queue_text.insert(
                    tk.END, f"{i+1}. {request['member_name']}\n")
                self.queue_text.insert(tk.END, f"   Book: {request['book']}\n")
                self.queue_text.insert(
                    tk.END, f"   Joined: {request['joined_at']}\n\n")
            if len(self.waiting_queue) > 5:
                self.queue_text.insert(
                    tk.END, f"... and {len(self.waiting_queue) - 5} more\n")
            self.queue_text.insert(tk.END, "―" * 30 + "\n")
            self.queue_text.insert(tk.END, "Last in Line →")

        # Update borrowed books
        self.borrowed_text.delete(1.0, tk.END)
        if not self.borrowed_books:
            self.borrowed_text.insert(tk.END, "No books currently borrowed")
        else:
            for book, details in self.borrowed_books.items():
                self.borrowed_text.insert(tk.END, f"• {book}\n")
                self.borrowed_text.insert(
                    tk.END, f"  Member: {details['member_name']}\n")
                self.borrowed_text.insert(
                    tk.END, f"  Return by: {details['return_date']}\n\n")


def main():
    root = tk.Tk()
    app = LibrarySystem(root)
    root.mainloop()


if __name__ == "__main__":
    main()
