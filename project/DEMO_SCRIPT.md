# ShelfWise CS50x Demo Video Script

Replace every item in square brackets before recording. Keep the complete recording under three minutes. Record your browser while the Flask application is running locally.

## 0:00–0:12 — Required opening screen

Open `http://127.0.0.1:5000/video-intro` in the browser and display it for 5–8 seconds. Do not narrate it too quickly.

```text
ShelfWise: Smart Library Management System
Created by: [YOUR FULL NAME]
GitHub: MuhammadEisa-ML
edX: [YOUR EDX USERNAME]
[YOUR CITY], Pakistan
Recorded: [DAY MONTH YEAR]
```

Say: “Hello. My name is [YOUR NAME], and this is ShelfWise, my CS50x final project.”

## 0:12–0:32 — Problem and solution

Open the ShelfWise home page.

Say: “ShelfWise is a Flask and SQLite web application for a small library. It solves the problem of tracking books, availability, members, and due dates in one place. Members can find and borrow books, while librarians can manage the collection and active loans.”

## 0:32–0:56 — Catalogue search

Click **Browse books**. Search for `Python`, then clear the search and choose **Available now**.

Say: “The catalogue supports searching by title, author, ISBN, and category. It also has an availability filter. Each result shows the category and the number of copies currently available.”

## 0:56–1:16 — Book page and recommendation

Open **Effective Python** or another book. Point out the book information and recommendation section.

Say: “The detail page displays the book's bibliographic information, shelf location, and availability. The recommendation feature suggests related books from the same category. I chose category-based recommendations because they are lightweight and useful without adding a complex machine-learning dependency.”

## 1:16–1:44 — Member workflow

Log out, register a new member account, log in, open an available book, and click **Borrow for 14 days**. Then open **My loans**.

Say: “Members register with a secure password hash. After signing in, they can borrow one available copy. The application creates a loan, reduces the available count, and sets the due date fourteen days ahead. My Loans shows current loans, returns, and any late status. A return automatically restores the available copy and calculates a fine of twenty rupees per overdue day.”

## 1:44–2:09 — Favorites

Return to a book detail page, click **Save favorite**, then open **Favorites**.

Say: “Members can also save books to a favorites list. This uses a separate many-to-many favorites table, so one member can save many books and each book can be saved by many members.”

## 2:09–2:40 — Librarian tools

Log out and sign in with the administrator account. Open **Admin**, then **Manage active loans**, and optionally **Add a book**.

Say: “Librarian routes are protected by a role check. The dashboard summarizes total copies, members, active loans, overdue loans, popular books, and categories. From here, a librarian can add or edit books, view active loans, and return a book for a member. The application prevents members from accessing these pages directly.”

## 2:40–2:55 — Technical close

Keep the admin dashboard visible.

Say: “ShelfWise uses Python and Flask for the server, SQLite for the relational database, Jinja templates for the pages, and CSS for its responsive interface. The database has users, books, loans, and favorites tables. Thank you for watching.”

## Recording checklist

- Start the Flask server first: `py app.py`
- Keep the video under 3:00.
- Verify that the opening slide includes every required detail.
- Upload the video as **Unlisted**, not Private.
- Copy its URL into `README.md`.
- Never show passwords other than the deliberately created demo account.
