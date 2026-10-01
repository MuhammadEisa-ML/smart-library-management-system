# ShelfWise: Smart Library Management System

#### Video Demo: <PASTE-YOUR-UNLISTED-YOUTUBE-VIDEO-URL-HERE>

#### Description:

ShelfWise is a web-based Library Management System built as my CS50x final project. The purpose of the application is to make a small library's everyday work simpler: members can discover books and manage their own borrowing, while a librarian can maintain the collection and monitor loans. A paper-based library register or a collection of separate spreadsheets makes it difficult to know which copies are available, when books are due, and who has borrowed them. ShelfWise stores that information in one SQLite database and presents it through a responsive Flask web application.

The project has two types of accounts. A member can register with a name, email address, and password. Passwords are never stored directly: Werkzeug generates a password hash before the account is saved. After logging in, a member can search the catalogue by title, author, ISBN, or category; filter for books currently available; open a book's detail page; borrow an available copy; return a book; see current and previous loans; and save or remove favorites. A member cannot borrow the same book twice at the same time. Each loan lasts fourteen days by default.

A librarian signs in using an administrator account. The admin dashboard shows total physical copies, registered members, active loans, and overdue loans. It also displays the most borrowed books and the number of books in each category. The librarian can add a book, edit its metadata and quantity, delete a book that has no loan history, inspect all active loans, and return a book on a member's behalf. The project seeds the database with a small starter collection, which makes the app immediately usable after its first run.

Borrowing and returning are the central business rules in ShelfWise. When a member borrows a book, the application first confirms that a copy is available and that the member has no existing active loan for the same title. It then creates a loan record with the borrowing date and a due date fourteen days later, and decreases the book's available-copy count. When a book is returned, the loan record is marked returned, the return date is stored, and the available-copy count is increased. If the return date is after the due date, ShelfWise calculates a fine of Rs. 20 per late day. The system displays overdue loans and late-day counts in both member and librarian pages.

The recommendation feature is intentionally lightweight. On each book-detail page, ShelfWise suggests up to three other books from the same category. I chose this approach instead of a heavy machine-learning dependency because it produces useful related reading suggestions, keeps the project easy to run on ordinary hardware, and allows the main focus to remain on Flask, SQL, authentication, and data relationships learned in CS50.

## Technologies

- Python and Flask for routing, templates, sessions, validation, and server-side logic
- SQLite for persistent relational data
- HTML, Jinja, and CSS for the responsive interface
- Werkzeug security helpers for password hashing and validation
- Gunicorn for an optional production host such as Render

## Files and directories

- `app.py` is the application's entry point. It creates the Flask app, initializes the SQLite schema and starter data, opens database connections, defines authentication decorators, calculates late days, and contains every route. It also contains the business logic for loans, returns, favorites, search, statistics, and administrator tools.
- `requirements.txt` lists Flask and Gunicorn. Flask is needed locally; Gunicorn is only useful when deploying to a Linux web host.
- `templates/base.html` provides the shared page structure, navigation bar, flash-message area, and footer.
- `templates/index.html` is the public landing page, while `_book_card.html` is a reusable component for book cards.
- `templates/books.html` renders the searchable catalogue. `book_detail.html` displays a book, its availability, related recommendations, and its borrow/favorite controls.
- `templates/login.html` and `register.html` provide the two authentication forms.
- `templates/my_loans.html` and `favorites.html` show member-specific information.
- `templates/admin_dashboard.html`, `admin_loans.html`, and `book_form.html` are restricted librarian views for analytics, active loans, and book management.
- `static/styles.css` contains the visual design, card layout, responsive mobile rules, forms, tables, status colors, and dashboard charts.

## Database design

The database has four tables. `users` stores member and administrator identity, a password hash, and a role. `books` stores bibliographic data, total quantity, available quantity, shelf location, and description. `loans` joins one user to one book and records the borrowing, due, return, status, and fine information. `favorites` is a many-to-many table that lets a member save multiple books and lets a book be favorited by multiple members. SQLite foreign keys protect these relationships.

## Design decisions

I used SQLite because the project runs without requiring a database server and is appropriate for a small demonstration library. I used server-rendered Jinja templates rather than a separate JavaScript frontend because Flask templates keep the project smaller and easier to explain. The role is stored in the user record and checked by decorators so that members cannot access librarian routes by typing an admin URL manually. For deletion, books with any loan history cannot be removed; this preserves historical records and avoids broken references. Available copies are stored directly in `books` so the catalogue can show availability quickly, while the application updates that number together with each loan transaction.

## Installation and use

Install Python 3, then open PowerShell in this folder and run:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
py app.py
```

Open `http://127.0.0.1:5000`. On the first run, the application creates `library.db`, the demonstration books, and this librarian account:

```text
Email: admin@library.local
Password: admin123
```

For a real deployment, change the administrator password and set a strong `FLASK_SECRET_KEY`. Local SQLite storage is appropriate for the project demonstration but should be replaced by a managed database for a public production deployment.

## Academic honesty and AI assistance

AI assistance was used to help draft the initial Flask structure and explain concepts. I reviewed the code, tested the application, and will be able to explain its design, database relationships, routes, and business rules. This acknowledgement is included to comply with the CS50 final-project policy.
