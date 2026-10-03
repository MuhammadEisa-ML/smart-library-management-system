# ShelfWise: Smart Library Management System

#### Video Demo: https://youtu.be/OuX62ZH5FdI

#### Description:

ShelfWise is a web-based Smart Library Management System created for my CS50x final project. It is designed for a small library that needs one simple place to manage its book collection, members, borrowing records, due dates, returns, and fines. Instead of relying on paper registers or separate spreadsheets, ShelfWise uses a relational SQLite database and a Flask web application to keep this information accurate and easy to use.

The project has two user roles: member and librarian. A member can create an account, log in, search for books, filter the catalogue by availability or category, open a book-detail page, borrow an available book, return a borrowed book, see current and past loans, and save favorite books. A librarian has additional protected administration tools. The librarian can add books, edit book information, delete books that have no loan history, monitor active loans, return books for members, and view a dashboard containing library statistics.

The application was built with Python and Flask for the backend, SQLite for the database, and HTML, Jinja templates, and CSS for the user interface. It uses Werkzeug's password-hashing functions so that passwords are not stored as plain text. The interface is responsive, so it can be used on both desktop and mobile-sized screens.

## Problem being solved

Small libraries often need to answer basic questions quickly: Which books are available? Who borrowed a particular book? When is it due? Which books are popular? Manual systems can make these questions slow and can cause errors in availability counts. ShelfWise solves this by connecting each book, user, and loan record in a single database. The system automatically updates availability when a member borrows or returns a book.

## Main features

### Member features

- Register and log in with an email address and password.
- Search books by title, author, ISBN, or category.
- Filter the catalogue to show only available books.
- Open detailed pages showing the book description, publisher, publication year, shelf location, and available copies.
- Borrow one available copy for fourteen days.
- Return a book from the My Loans page.
- View active loans, borrowing history, overdue status, and fines.
- Save books to a personal favorites list.
- Receive lightweight book recommendations based on the category of the current book.

### Librarian features

- Log in to a protected administrator dashboard.
- View total copies, registered members, books currently on loan, and overdue loans.
- View the most borrowed books and collection totals by category.
- Add new books to the catalogue.
- Edit book metadata, shelf location, descriptions, and quantities.
- Delete a book only when it has no loan history, protecting historical data.
- View all active loans and return a book for a member.

## Borrowing, returns, and fines

The loan system is the main business feature of ShelfWise. Before creating a loan, the application checks that the requested book exists, that at least one copy is available, and that the member does not already have the same book on an active loan. If the request is valid, ShelfWise creates a new loan row containing the user ID, book ID, borrow date, and due date. The due date is automatically set to fourteen days after borrowing. At the same time, the available-copy count for that book is reduced by one.

When a book is returned, the application marks the loan as returned, saves the return date, and increases the available-copy count by one. If the return date is after the due date, ShelfWise calculates a fine of Rs. 20 for each overdue day. The member's loan page and the librarian's active-loan page both clearly identify overdue books.

## Recommendation feature

ShelfWise includes a lightweight recommendation feature. When a user views a book, the book-detail page lists up to three other books from the same category under “You may also like.” I chose category-based recommendations rather than a large machine-learning model because it gives useful suggestions without requiring heavy dependencies or complex deployment. It also keeps the project focused on the Flask, SQL, authentication, and database-design skills learned in CS50.

## Database design

The SQLite database is stored in `library.db` and contains four related tables:

- `users` stores each user's name, email, password hash, account role, and creation time. Roles are either `member` or `admin`.
- `books` stores ISBN, title, author, category, publisher, publication year, quantity, available copies, shelf location, and description.
- `loans` connects a user to a book and stores borrowing, due, and return dates, current status, and any calculated fine.
- `favorites` is a many-to-many relationship table that allows a user to save many books and allows a book to be saved by many users.

Foreign-key constraints keep the relationships valid. For example, a loan cannot point to a user or book that does not exist. The application also prevents a librarian from deleting a book that already has loan history.

## Files and directories

- `app.py` is the main Flask application. It defines the database schema, creates starter data, handles sessions and authentication, calculates fines, and contains every member and administrator route.
- `requirements.txt` lists the Python packages used by the project: Flask for the application and Gunicorn for optional deployment.
- `templates/base.html` contains the shared navigation, messages, and footer used by the standard application pages.
- `templates/index.html` is the home page. `_book_card.html` is a reusable template for a book card.
- `templates/books.html` displays the searchable and filterable book catalogue.
- `templates/book_detail.html` displays one book, its information, availability, recommendations, and member actions.
- `templates/login.html` and `templates/register.html` contain the authentication forms.
- `templates/my_loans.html` and `templates/favorites.html` display member-specific data.
- `templates/admin_dashboard.html`, `templates/admin_loans.html`, and `templates/book_form.html` provide the librarian dashboard, active-loan management, and book-management forms.
- `templates/video_intro.html` is the opening title card used in my project demonstration video.
- `static/styles.css` contains the responsive visual design, layout, cards, forms, tables, dashboard statistics, and video-intro styling.
- `DEMO_SCRIPT.md` contains the narration plan used to record the video demonstration.

## Design decisions

I chose Flask because it provides a clear way to build web routes, templates, forms, sessions, and database access in Python. I chose SQLite because it is lightweight, requires no separate database server, and is suitable for a small library demonstration. Jinja templates were used instead of a separate frontend framework because they keep the project structure smaller and easier to understand.

The application stores both `quantity` and `available` copies for each book. This allows the catalogue to display availability quickly while retaining the total number of copies owned by the library. On a book edit, the system ensures that total quantity cannot become lower than the number of copies currently on loan. The app uses role-based decorators to ensure that ordinary members cannot access librarian routes simply by entering an administrator URL in the browser.

## Installation and use

Install Python 3. Then open PowerShell in the `project` directory and run:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
py app.py
```

Open `http://127.0.0.1:5000` in a web browser. On its first run, ShelfWise automatically creates `library.db`, a small demonstration collection, and the following librarian account:

```text
Email: admin@library.local
Password: admin123
```

The video title card can be opened at `http://127.0.0.1:5000/video-intro`.

## Author

Created by Muhammad Eisa

- GitHub: `MuhammadEisa-ML`
- edX: `MuhammadEisa628068`
- Location: Islamabad, Pakistan
- Recorded: 1 October 2026

## Academic honesty and AI assistance

AI assistance was used to help draft the initial Flask project structure and explain Flask and SQLite concepts. I reviewed the project, tested it, and can explain its routes, database relationships, authentication, business rules, and design decisions. This acknowledgement is included in accordance with the CS50 final-project policy.
