
# Student Task Tracker

A web-based task management application designed to help students organize academic tasks, manage deadlines, and track their productivity.

## About the Project

Student Task Tracker is developed using Python Flask, SQLite, HTML, CSS, and JavaScript. It provides a simple interface for managing academic activities in one place.

## Features

- Add, edit, and delete tasks
- Mark tasks as completed
- Set task priorities: High, Medium, and Low
- Search and filter tasks
- Sort tasks
- Track overdue and upcoming deadlines
- View task completion progress
- Analytics dashboard
- Responsive user interface
- SQLite database integration

## Technologies Used

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, Flask
- **Database:** SQLite
- **Development Tool:** Visual Studio Code

## Project Structure

```text
Student-Task-Tracker/
│
├── app.py
├── tasks.db
├── requirements.txt
├── .gitignore
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── tasks.html
│   ├── deadlines.html
│   ├── analytics.html
│   ├── about.html
│   └── edit.html
│
└── static/
    └── style.css
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/Student-Task-Tracker.git
```

### 2. Open the project folder

```bash
cd Student-Task-Tracker
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment (Windows)

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
python app.py
```

Open your browser and visit:

http://127.0.0.1:5000/

## Learning Outcomes

- Understanding Flask web application development
- Implementing CRUD operations
- Connecting Python with an SQLite database
- Designing responsive web interfaces
- Managing academic tasks and deadlines

## Future Enhancements

- User authentication
- Email reminders for deadlines
- Cloud database integration
- Export task reports
- Calendar integration

## Author

Developed as a student web development project.
