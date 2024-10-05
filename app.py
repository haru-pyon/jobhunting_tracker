from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required, get_user_name
"""
reference to connect with sqlite3
https://www.python-beginners.com/entry/20191125/1574687207
"""
import sqlite3
conn = sqlite3.connect(
    "project.db",
    check_same_thread=False
)
db = conn.cursor()

# Below flask setting regarding Session, Cash and login_required is cited from CS50 week9 project "finance"
# Configure application
app = Flask(__name__)
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    name = get_user_name(db, session)
    if request.method == "GET":
        name = get_user_name(db, session)
        # filtering by DATETIME cited from https://stackoverflow.com/questions/65133363/sqlite-select-all-for-last-7-days
        rows = db.execute(
            "SELECT next_date, company_name, next_process, note FROM jobs WHERE user_id = ? AND \
                next_date <= DATETIME('now', '14 days')",
            (session.get("user_id"), )
        ).fetchall()
        return render_template("index.html", name=name, rows=rows)
    else:
        company_name = request.form.get("companyname")
        company_url = request.form.get("companyurl")
        job_title = request.form.get("jobtitle")
        applied_through = request.form.get("appliedthrough")
        current_status = request.form.get("currentstatus")
        next_process = request.form.get("nextprocess")
        next_date = request.form.get("nextdate")
        note = request.form.get("note")

        db.execute(
            "INSERT INTO jobs (user_id, recorded_date, company_name, company_url, job_title, applied_through,\
            current_status, next_process, next_date, note) VALUES (?, CURRENT_TIMESTAMP, ?, ?, ?, ?, ?, ?, ?, ?)",
            (session["user_id"], company_name, company_url, job_title, applied_through, current_status, next_process,
             next_date, note)
        )
        conn.commit()
        rows = db.execute(
            "SELECT next_date, company_name, next_process, note FROM jobs WHERE user_id = ? AND \
                next_date <= DATETIME('now', '14 days')",
            (session.get("user_id"), )
        ).fetchall()
        return render_template("index.html", name=name, rows=rows)


@app.route("/history", methods=["GET", "POST"])
@login_required
def history():
    name = get_user_name(db, session)
    if request.method == "GET":
        rows = db.execute(
            "SELECT job_id, recorded_date, company_name, company_url, job_title, applied_through,\
             current_status, next_process, next_date, note FROM jobs WHERE user_id = ?",
            (session.get("user_id"), )
        ).fetchall()
        return render_template("history.html", name=name, rows=rows)
    else:
        if not request.form.get("search_companyname"):
            job_id = request.form.get("jobid")
            company_name = request.form.get("companyname")
            company_url = request.form.get("companyurl")
            job_title = request.form.get("jobtitle")
            applied_through = request.form.get("appliedthrough")
            current_status = request.form.get("currentstatus")
            next_process = request.form.get("nextprocess")
            next_date = request.form.get("nextdate")
            note = request.form.get("note")

            db.execute(
                "UPDATE jobs SET recorded_date = CURRENT_TIMESTAMP, company_name = ?, company_url = ?, job_title = ?,\
                applied_through = ?, current_status = ?, next_process = ?, next_date = ?, note = ? \
                WHERE job_id = ? AND user_id = ?",
                (company_name, company_url, job_title, applied_through, current_status, next_process, next_date, note,
                 job_id, session.get("user_id"))
            )
            rows = db.execute(
                "SELECT job_id, recorded_date, company_name, company_url, job_title, applied_through,\
                current_status, next_process, next_date, note FROM jobs WHERE user_id = ?",
                (session.get("user_id"), )
            ).fetchall()
            conn.commit()
        # search for company
        else:
            search_companyname = request.form.get("search_companyname")
            rows = db.execute(
                "SELECT job_id, recorded_date, company_name, company_url, job_title, applied_through,\
                current_status, next_process, next_date, note FROM jobs WHERE user_id = ? AND company_name LIKE ?",
                (session.get("user_id"), "%" + search_companyname + "%")
            ).fetchall()
        return render_template("history.html", rows=rows)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    if request.method == "POST":
        if not request.form.get("username") or not request.form.get("password"):
            flash("must provide username and password")
            return redirect("/login")
        rows = db.execute(
            "SELECT * FROM users WHERE user_name = ?", (request.form.get("username"), )
        ).fetchall()

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0][2], request.form.get("password")):
            flash("username or password is invalid")
            return redirect("/login")

        session["user_id"] = rows[0][0]
        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        """
        reference to show message using flash:
        https://qiita.com/MashCannu/items/d30621dc15055babe06c
        """
        if not request.form.get("username"):
            flash("must provide username")
            return redirect("/register")
        if not request.form.get("password"):
            flash("must provide password")
            return redirect("/register")
        if request.form.get("password") != request.form.get("confirmation"):
            flash("password does not match")
            return redirect("/register")

        """Register user"""
        password = request.form.get("password")
        username = request.form.get("username")
        hashed_password = generate_password_hash(password)

        # Ensure there is no same username already registered
        try:
            db.execute(
                "INSERT INTO users (user_name, hash) VALUES (?, ?)", (username, hashed_password)
            )
            conn.commit()
        except Exception:
            flash("Choose another username")
            return redirect("/register")

        # Remember which user has logged in
        rows = db.execute(
            # reference why parameter needs to be a tuple: https://stackoverflow.com/questions/16856647/sqlite3-programmingerror-incorrect-number-of-bindings-supplied-the-current-sta
            "SELECT * FROM users WHERE user_name = ?", (username, )
        ).fetchall()
        session["user_id"] = rows[0][0]
        return render_template("index.html", name=username)

# flask run --debugger --reload
