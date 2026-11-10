from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import date, timedelta

app = Flask(__name__)


# =========================================================
# DATABASE
# =========================================================

def init_db():

    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            subject TEXT NOT NULL,
            due_date TEXT NOT NULL,
            completed INTEGER DEFAULT 0,
            priority TEXT DEFAULT 'Medium'
        )
    """)

    # Check whether priority column already exists
    cursor.execute("PRAGMA table_info(tasks)")
    columns = [column[1] for column in cursor.fetchall()]

    # Add priority column to old databases
    if "priority" not in columns:

        cursor.execute("""
            ALTER TABLE tasks
            ADD COLUMN priority TEXT DEFAULT 'Medium'
        """)

    conn.commit()
    conn.close()


# =========================================================
# GET ALL TASKS
# =========================================================

def get_tasks():

    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM tasks
        ORDER BY due_date
    """)

    tasks = cursor.fetchall()

    conn.close()

    return tasks


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/")
def home():

    tasks = get_tasks()

    total = len(tasks)

    completed = sum(
        1 for task in tasks
        if task[4] == 1
    )

    pending = total - completed

    if total > 0:
        progress = round((completed / total) * 100)
    else:
        progress = 0

    return render_template(
        "index.html",
        tasks=tasks,
        total=total,
        completed=completed,
        pending=pending,
        progress=progress
    )


# =========================================================
# MY TASKS
# =========================================================

@app.route("/tasks")
def tasks_page():

    tasks = get_tasks()

    total = len(tasks)

    completed = sum(
        1 for task in tasks
        if task[4] == 1
    )

    pending = total - completed

    return render_template(
        "tasks.html",
        tasks=tasks,
        total=total,
        completed=completed,
        pending=pending
    )


# =========================================================
# ADD TASK
# =========================================================

@app.route("/add", methods=["POST"])
def add_task():

    task = request.form["task"]
    subject = request.form["subject"]
    due_date = request.form["due_date"]
    priority = request.form["priority"]

    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tasks
        (task, subject, due_date, priority)
        VALUES (?, ?, ?, ?)
    """, (
        task,
        subject,
        due_date,
        priority
    ))

    conn.commit()
    conn.close()

    return redirect(url_for("tasks_page"))


# =========================================================
# COMPLETE TASK
# =========================================================

@app.route("/complete/<int:task_id>")
def complete_task(task_id):

    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tasks
        SET completed = 1
        WHERE id = ?
    """, (task_id,))

    conn.commit()
    conn.close()

    return redirect(url_for("tasks_page"))


# =========================================================
# EDIT TASK
# =========================================================

@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):

    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    if request.method == "POST":

        task = request.form["task"]
        subject = request.form["subject"]
        due_date = request.form["due_date"]
        priority = request.form["priority"]

        cursor.execute("""
            UPDATE tasks
            SET task = ?,
                subject = ?,
                due_date = ?,
                priority = ?
            WHERE id = ?
        """, (
            task,
            subject,
            due_date,
            priority,
            task_id
        ))

        conn.commit()
        conn.close()

        return redirect(url_for("tasks_page"))

    cursor.execute("""
        SELECT *
        FROM tasks
        WHERE id = ?
    """, (task_id,))

    task = cursor.fetchone()

    conn.close()

    return render_template(
        "edit.html",
        task=task
    )


# =========================================================
# DELETE TASK
# =========================================================

@app.route("/delete/<int:task_id>")
def delete_task(task_id):

    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM tasks
        WHERE id = ?
    """, (task_id,))

    conn.commit()
    conn.close()

    return redirect(url_for("tasks_page"))


# =========================================================
# DEADLINES PAGE
# =========================================================

@app.route("/deadlines")
def deadlines():

    tasks = get_tasks()

    today = date.today()
    tomorrow = today + timedelta(days=1)

    overdue = []
    due_today = []
    due_tomorrow = []
    upcoming = []

    for task in tasks:

        # Skip completed tasks
        if task[4] == 1:
            continue

        try:

            due_date = date.fromisoformat(task[3])

        except ValueError:

            continue

        if due_date < today:

            overdue.append(task)

        elif due_date == today:

            due_today.append(task)

        elif due_date == tomorrow:

            due_tomorrow.append(task)

        elif due_date > tomorrow:

            upcoming.append(task)

    return render_template(
        "deadlines.html",
        overdue=overdue,
        due_today=due_today,
        due_tomorrow=due_tomorrow,
        upcoming=upcoming
    )


# =========================================================
# ANALYTICS PAGE
# =========================================================

@app.route("/analytics")
def analytics():

    tasks = get_tasks()

    total = len(tasks)

    completed = sum(
        1 for task in tasks
        if task[4] == 1
    )

    pending = total - completed

    # Completion percentage
    if total > 0:

        completion_percentage = round(
            (completed / total) * 100
        )

    else:

        completion_percentage = 0

    # Priority statistics
    high = sum(
        1 for task in tasks
        if task[5] == "High"
    )

    medium = sum(
        1 for task in tasks
        if task[5] == "Medium"
    )

    low = sum(
        1 for task in tasks
        if task[5] == "Low"
    )

    # Subject statistics
    subject_counts = {}

    for task in tasks:

        subject = task[2]

        if subject in subject_counts:

            subject_counts[subject] += 1

        else:

            subject_counts[subject] = 1

    return render_template(
        "analytics.html",
        total=total,
        completed=completed,
        pending=pending,
        completion_percentage=completion_percentage,
        high=high,
        medium=medium,
        low=low,
        subject_counts=subject_counts
    )


# =========================================================
# ABOUT PAGE
# =========================================================

@app.route("/about")
def about():

    return render_template("about.html")


# =========================================================
# START APPLICATION
# =========================================================

if __name__ == "__main__":

    init_db()

    app.run(debug=True)