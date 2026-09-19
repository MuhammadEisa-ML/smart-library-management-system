"""Smart Library Management System — a CS50 final project."""
import os
import sqlite3
from datetime import date, timedelta
from functools import wraps
from pathlib import Path
from flask import Flask, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "library.db"
FINE_PER_DAY, LOAN_DAYS = 20, 14
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "development-key-change-before-deployment")

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE); g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db

@app.teardown_appcontext
def close_db(_error=None):
    db = g.pop("db", None)
    if db: db.close()

def init_db():
    db = sqlite3.connect(DATABASE)
    db.executescript("""
    PRAGMA foreign_keys = ON;
    CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT NOT NULL UNIQUE, password_hash TEXT NOT NULL, role TEXT NOT NULL DEFAULT 'member' CHECK(role IN ('member','admin')), created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
    CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, isbn TEXT UNIQUE, title TEXT NOT NULL, author TEXT NOT NULL, category TEXT NOT NULL, publisher TEXT, publication_year INTEGER, quantity INTEGER NOT NULL CHECK(quantity >= 0), available INTEGER NOT NULL CHECK(available >= 0), shelf_location TEXT, description TEXT DEFAULT '');
    CREATE TABLE IF NOT EXISTS loans (id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL, book_id INTEGER NOT NULL, borrow_date TEXT NOT NULL, due_date TEXT NOT NULL, return_date TEXT, status TEXT NOT NULL DEFAULT 'borrowed' CHECK(status IN ('borrowed','returned')), fine INTEGER NOT NULL DEFAULT 0, FOREIGN KEY(user_id) REFERENCES users(id), FOREIGN KEY(book_id) REFERENCES books(id));
    CREATE TABLE IF NOT EXISTS favorites (user_id INTEGER NOT NULL, book_id INTEGER NOT NULL, PRIMARY KEY(user_id,book_id), FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE, FOREIGN KEY(book_id) REFERENCES books(id) ON DELETE CASCADE);
    """)
    if not db.execute("SELECT id FROM users WHERE email=?", ("admin@library.local",)).fetchone():
        db.execute("INSERT INTO users (name,email,password_hash,role) VALUES (?,?,?,'admin')", ("Library Admin", "admin@library.local", generate_password_hash("admin123")))
    if not db.execute("SELECT id FROM books LIMIT 1").fetchone():
        db.executemany("INSERT INTO books (isbn,title,author,category,publisher,publication_year,quantity,available,shelf_location,description) VALUES (?,?,?,?,?,?,?,?,?,?)", [
            ("9780132350884","Clean Code","Robert C. Martin","Computer Science","Prentice Hall",2008,4,4,"CS-A-12","A handbook of agile software craftsmanship."),
            ("9780262033848","Introduction to Algorithms","Thomas H. Cormen","Computer Science","MIT Press",2009,3,3,"CS-A-04","A comprehensive introduction to modern algorithms."),
            ("9780134685991","Effective Python","Brett Slatkin","Programming","Addison-Wesley",2019,5,5,"CS-B-08","Ninety specific ways to write better Python."),
            ("9780747532743","Harry Potter and the Philosopher's Stone","J. K. Rowling","Fiction","Bloomsbury",1997,6,6,"F-A-02","The first story in the Harry Potter series."),
            ("9780061120084","To Kill a Mockingbird","Harper Lee","Fiction","Harper Perennial",1960,3,3,"F-B-06","A classic novel about justice and empathy.")])
    db.commit(); db.close()

def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to continue.", "warning"); return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped

def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if session.get("role") != "admin":
            flash("This page is for librarians only.", "error"); return redirect(url_for("index"))
        return view(*args, **kwargs)
    return wrapped

def overdue_days(due): return max(0, (date.today() - date.fromisoformat(due)).days)
@app.context_processor
def template_globals(): return {"today": date.today().isoformat(), "fine_per_day": FINE_PER_DAY}

@app.route("/")
def index(): return render_template("index.html", books=get_db().execute("SELECT * FROM books ORDER BY title LIMIT 6").fetchall())

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        name=request.form.get("name","").strip(); email=request.form.get("email","").lower().strip(); password=request.form.get("password",""); confirmation=request.form.get("confirmation","")
        if not name or not email or not password: flash("Name, email, and password are required.","error")
        elif password != confirmation: flash("Passwords do not match.","error")
        elif len(password) < 6: flash("Use a password with at least 6 characters.","error")
        else:
            try:
                db=get_db(); db.execute("INSERT INTO users (name,email,password_hash) VALUES (?,?,?)",(name,email,generate_password_hash(password))); db.commit()
                flash("Account created. You can now log in.","success"); return redirect(url_for("login"))
            except sqlite3.IntegrityError: flash("That email address is already registered.","error")
    return render_template("register.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        user=get_db().execute("SELECT * FROM users WHERE email=?",(request.form.get("email","").lower().strip(),)).fetchone()
        if not user or not check_password_hash(user["password_hash"],request.form.get("password","")): flash("Invalid email or password.","error")
        else:
            session.clear(); session.update(user_id=user["id"],user_name=user["name"],role=user["role"]); flash(f"Welcome back, {user['name']}!","success")
            return redirect(url_for("admin_dashboard" if user["role"]=="admin" else "books"))
    return render_template("login.html")
@app.route("/logout")
def logout(): session.clear(); flash("You have been logged out.","success"); return redirect(url_for("index"))

@app.route("/books")
def books():
    q=request.args.get("q","").strip(); cat=request.args.get("category","").strip(); available=request.args.get("availability","")
    sql="SELECT * FROM books WHERE 1=1"; params=[]
    if q: sql+=" AND (title LIKE ? OR author LIKE ? OR isbn LIKE ? OR category LIKE ?)"; params += [f"%{q}%"]*4
    if cat: sql+=" AND category=?"; params.append(cat)
    if available=="available": sql+=" AND available>0"
    db=get_db(); rows=db.execute(sql+" ORDER BY title",params).fetchall(); categories=db.execute("SELECT DISTINCT category FROM books ORDER BY category").fetchall()
    return render_template("books.html",books=rows,categories=categories,query=q,selected_category=cat,availability=available)

@app.route("/books/<int:book_id>")
def book_detail(book_id):
    db=get_db(); book=db.execute("SELECT * FROM books WHERE id=?",(book_id,)).fetchone()
    if not book: return ("Book not found",404)
    fav=session.get("user_id") and db.execute("SELECT 1 FROM favorites WHERE user_id=? AND book_id=?",(session["user_id"],book_id)).fetchone()
    similar=db.execute("SELECT * FROM books WHERE category=? AND id!=? ORDER BY title LIMIT 3",(book["category"],book_id)).fetchall()
    return render_template("book_detail.html",book=book,favorite=fav,similar=similar)

@app.post("/books/<int:book_id>/borrow")
@login_required
def borrow(book_id):
    db=get_db(); book=db.execute("SELECT * FROM books WHERE id=?",(book_id,)).fetchone()
    if not book or book["available"]<1: flash("This book is not currently available.","error")
    elif db.execute("SELECT 1 FROM loans WHERE user_id=? AND book_id=? AND status='borrowed'",(session["user_id"],book_id)).fetchone(): flash("You already have this book on loan.","warning")
    else:
        due=date.today()+timedelta(days=LOAN_DAYS); db.execute("INSERT INTO loans (user_id,book_id,borrow_date,due_date) VALUES (?,?,?,?)",(session["user_id"],book_id,date.today().isoformat(),due.isoformat())); db.execute("UPDATE books SET available=available-1 WHERE id=?",(book_id,)); db.commit(); flash(f"Book borrowed. Return it by {due.strftime('%d %b %Y')}.","success")
    return redirect(url_for("my_loans"))

@app.post("/loans/<int:loan_id>/return")
@login_required
def return_book(loan_id):
    db=get_db(); loan=db.execute("SELECT * FROM loans WHERE id=?",(loan_id,)).fetchone()
    if not loan or (loan["user_id"]!=session["user_id"] and session.get("role")!="admin") or loan["status"]!="borrowed": flash("That active loan was not found.","error")
    else:
        fine=overdue_days(loan["due_date"])*FINE_PER_DAY; db.execute("UPDATE loans SET status='returned',return_date=?,fine=? WHERE id=?",(date.today().isoformat(),fine,loan_id)); db.execute("UPDATE books SET available=available+1 WHERE id=?",(loan["book_id"],)); db.commit(); flash("Book returned."+(f" Fine: Rs. {fine}." if fine else " No fine due."),"success")
    return redirect(request.referrer or url_for("my_loans"))

@app.route("/my-loans")
@login_required
def my_loans():
    rows=get_db().execute("SELECT loans.*,books.title,books.author FROM loans JOIN books ON books.id=loans.book_id WHERE loans.user_id=? ORDER BY status,due_date DESC",(session["user_id"],)).fetchall()
    return render_template("my_loans.html",loans=rows,overdue_days=overdue_days)

@app.post("/books/<int:book_id>/favorite")
@login_required
def favorite(book_id):
    db=get_db(); found=db.execute("SELECT 1 FROM favorites WHERE user_id=? AND book_id=?",(session["user_id"],book_id)).fetchone()
    if found: db.execute("DELETE FROM favorites WHERE user_id=? AND book_id=?",(session["user_id"],book_id)); flash("Removed from favorites.","success")
    else: db.execute("INSERT OR IGNORE INTO favorites (user_id,book_id) VALUES (?,?)",(session["user_id"],book_id)); flash("Added to favorites.","success")
    db.commit(); return redirect(request.referrer or url_for("books"))
@app.route("/favorites")
@login_required
def favorites(): return render_template("favorites.html",books=get_db().execute("SELECT books.* FROM favorites JOIN books ON books.id=favorites.book_id WHERE user_id=? ORDER BY books.title",(session["user_id"],)).fetchall())

@app.route("/admin")
@login_required
@admin_required
def admin_dashboard():
    db=get_db(); stats={"books":db.execute("SELECT COALESCE(SUM(quantity),0) FROM books").fetchone()[0],"members":db.execute("SELECT COUNT(*) FROM users WHERE role='member'").fetchone()[0],"borrowed":db.execute("SELECT COUNT(*) FROM loans WHERE status='borrowed'").fetchone()[0],"overdue":db.execute("SELECT COUNT(*) FROM loans WHERE status='borrowed' AND due_date<?",(date.today().isoformat(),)).fetchone()[0]}
    popular=db.execute("SELECT books.title,COUNT(loans.id) count FROM books LEFT JOIN loans ON books.id=loans.book_id GROUP BY books.id ORDER BY count DESC,books.title LIMIT 5").fetchall(); categories=db.execute("SELECT category,COUNT(*) count FROM books GROUP BY category ORDER BY count DESC").fetchall()
    return render_template("admin_dashboard.html",stats=stats,popular=popular,categories=categories)

def form_data(form): return (form.get("isbn","").strip() or None,form.get("title","").strip(),form.get("author","").strip(),form.get("category","").strip(),form.get("publisher","").strip(),form.get("publication_year",type=int),form.get("quantity",type=int),form.get("shelf_location","").strip(),form.get("description","").strip())
@app.route("/admin/books/new",methods=["GET","POST"])
@login_required
@admin_required
def add_book():
    if request.method=="POST":
        d=form_data(request.form)
        if not d[1] or not d[2] or not d[3] or d[6] is None or d[6]<0: flash("Title, author, category, and a valid quantity are required.","error")
        else:
            try: get_db().execute("INSERT INTO books (isbn,title,author,category,publisher,publication_year,quantity,available,shelf_location,description) VALUES (?,?,?,?,?,?,?,?,?,?)",(*d[:7],d[6],*d[7:])); get_db().commit(); flash("Book added.","success"); return redirect(url_for("books"))
            except sqlite3.IntegrityError: flash("ISBN must be unique.","error")
    return render_template("book_form.html",book=None)
@app.route("/admin/books/<int:book_id>/edit",methods=["GET","POST"])
@login_required
@admin_required
def edit_book(book_id):
    db=get_db(); book=db.execute("SELECT * FROM books WHERE id=?",(book_id,)).fetchone()
    if not book:return("Book not found",404)
    if request.method=="POST":
        d=form_data(request.form); active=db.execute("SELECT COUNT(*) FROM loans WHERE book_id=? AND status='borrowed'",(book_id,)).fetchone()[0]
        if not d[1] or not d[2] or not d[3] or d[6] is None or d[6]<active: flash(f"Use valid details. Quantity cannot be below {active}, the number loaned.","error")
        else:
            try: db.execute("UPDATE books SET isbn=?,title=?,author=?,category=?,publisher=?,publication_year=?,quantity=?,available=?,shelf_location=?,description=? WHERE id=?",(*d[:7],d[6]-active,*d[7:],book_id)); db.commit(); flash("Book updated.","success"); return redirect(url_for("book_detail",book_id=book_id))
            except sqlite3.IntegrityError: flash("ISBN must be unique.","error")
    return render_template("book_form.html",book=book)
@app.post("/admin/books/<int:book_id>/delete")
@login_required
@admin_required
def delete_book(book_id):
    db=get_db()
    if db.execute("SELECT 1 FROM loans WHERE book_id=?",(book_id,)).fetchone(): flash("Books with loan history cannot be deleted.","error")
    else: db.execute("DELETE FROM books WHERE id=?",(book_id,)); db.commit(); flash("Book deleted.","success")
    return redirect(url_for("books"))
@app.route("/admin/loans")
@login_required
@admin_required
def admin_loans():
    rows=get_db().execute("SELECT loans.*,books.title,users.name,users.email FROM loans JOIN books ON books.id=loans.book_id JOIN users ON users.id=loans.user_id WHERE loans.status='borrowed' ORDER BY loans.due_date").fetchall()
    return render_template("admin_loans.html",loans=rows,overdue_days=overdue_days)

if __name__ == "__main__": init_db(); app.run(debug=True)
