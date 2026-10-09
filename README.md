# Mini SOC Security Monitoring Dashboard

A lightweight Security Operations Center (SOC) dashboard built with Python and Flask to demonstrate security monitoring concepts through a web-based interface.

## Overview

The Mini SOC Dashboard is a beginner-friendly cybersecurity project designed to explore security monitoring, event visibility, and dashboard development. It uses Flask for the web application and SQLite for local data storage.

## Features

* Web-based security monitoring dashboard
* Python Flask backend
* HTML, CSS, and JavaScript frontend
* SQLite database for local data storage
* Simple project structure for learning and customization

## Technologies Used

* **Python** — Backend development
* **Flask** — Web framework
* **HTML5** — Page structure
* **CSS3** — Dashboard styling
* **JavaScript** — Frontend interactions
* **SQLite** — Local database

## Project Structure

```text
mini-soc-dashboard/
├── app.py
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── script.js
├── data/
│   └── soc.db
├── .gitignore
└── README.md
```

*Note: The local database and Python virtual environment are excluded from Git.*

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/aryanvish126/mini-soc-dashboard.git
cd mini-soc-dashboard
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install Flask

```bash
python -m pip install flask
```

### 5. Run the application

```bash
python app.py
```

Open the local address shown in the terminal in your browser. For a typical Flask development server, this is `http://127.0.0.1:5000/`.

## Learning Objectives

* Understand the basics of SOC dashboards.
* Practice Python and Flask web development.
* Work with local SQLite data storage.
* Build a foundation for further cybersecurity monitoring projects.

## Future Improvements

* Integrate real security log sources.
* Add log filtering and search.
* Implement alert severity classification.
* Add authentication and role-based access.
* Explore integration with SIEM tools.

## Disclaimer

This project is intended for educational purposes and cybersecurity learning. It is not a replacement for a production-grade Security Information and Event Management (SIEM) platform.
