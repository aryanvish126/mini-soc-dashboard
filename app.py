
from flask import Flask, render_template, jsonify
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data" / "soc.db"


def connect_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_db():
    with connect_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                source_ip TEXT NOT NULL,
                event_type TEXT NOT NULL,
                username TEXT NOT NULL,
                status TEXT NOT NULL,
                details TEXT NOT NULL
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                severity TEXT NOT NULL,
                title TEXT NOT NULL,
                source_ip TEXT NOT NULL,
                description TEXT NOT NULL
            )
        """)


def seed_events():
    with connect_db() as conn:
        count = conn.execute(
            "SELECT COUNT(*) FROM events"
        ).fetchone()[0]

        if count > 0:
            return

        now = datetime.now()
        sample_events = []

        # Simulated failed logins from a documentation-only IP.
        for minutes_ago in [2, 3, 4, 5, 6]:
            timestamp = (
                now - timedelta(minutes=minutes_ago)
            ).isoformat(timespec="seconds")

            sample_events.append((
                timestamp,
                "203.0.113.42",
                "LOGIN",
                "admin",
                "FAILED",
                "Simulated failed login attempt"
            ))

        sample_events.extend([
            (
                now.isoformat(timespec="seconds"),
                "192.0.2.10",
                "LOGIN",
                "analyst",
                "SUCCESS",
                "Successful simulated login"
            ),
            (
                (now - timedelta(minutes=8)).isoformat(
                    timespec="seconds"
                ),
                "198.51.100.23",
                "LOGIN",
                "guest",
                "FAILED",
                "Invalid password"
            ),
            (
                (now - timedelta(minutes=12)).isoformat(
                    timespec="seconds"
                ),
                "192.0.2.15",
                "LOGIN",
                "analyst",
                "SUCCESS",
                "Successful simulated login"
            ),
            (
                (now - timedelta(minutes=15)).isoformat(
                    timespec="seconds"
                ),
                "198.51.100.23",
                "LOGIN",
                "guest",
                "FAILED",
                "Invalid password"
            ),
            (
                (now - timedelta(minutes=20)).isoformat(
                    timespec="seconds"
                ),
                "192.0.2.18",
                "LOGIN",
                "operator",
                "SUCCESS",
                "Successful simulated login"
            ),
        ])

        conn.executemany("""
            INSERT INTO events
            (timestamp, source_ip, event_type, username,
             status, details)
            VALUES (?, ?, ?, ?, ?, ?)
        """, sample_events)

    detect_brute_force()


def detect_brute_force():
    cutoff = (
        datetime.now() - timedelta(minutes=10)
    ).isoformat(timespec="seconds")

    with connect_db() as conn:
        suspicious_sources = conn.execute("""
            SELECT source_ip, COUNT(*) AS attempts
            FROM events
            WHERE status = 'FAILED'
              AND timestamp >= ?
            GROUP BY source_ip
            HAVING COUNT(*) >= 5
        """, (cutoff,)).fetchall()

        for source in suspicious_sources:
            existing = conn.execute("""
                SELECT id FROM alerts
                WHERE source_ip = ?
                  AND title = ?
            """, (
                source["source_ip"],
                "Possible brute-force login"
            )).fetchone()

            if existing is None:
                conn.execute("""
                    INSERT INTO alerts
                    (timestamp, severity, title, source_ip,
                     description)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    datetime.now().isoformat(
                        timespec="seconds"
                    ),
                    "HIGH",
                    "Possible brute-force login",
                    source["source_ip"],
                    f"{source['attempts']} failed logins "
                    "detected within 10 minutes."
                ))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/dashboard")
def dashboard_data():
    detect_brute_force()

    with connect_db() as conn:
        events = conn.execute("""
            SELECT * FROM events
            ORDER BY timestamp DESC
            LIMIT 100
        """).fetchall()

        alerts = conn.execute("""
            SELECT * FROM alerts
            ORDER BY timestamp DESC
            LIMIT 50
        """).fetchall()

        total_events = conn.execute(
            "SELECT COUNT(*) FROM events"
        ).fetchone()[0]

        failed_logins = conn.execute("""
            SELECT COUNT(*) FROM events
            WHERE status = 'FAILED'
        """).fetchone()[0]

        successful_logins = conn.execute("""
            SELECT COUNT(*) FROM events
            WHERE status = 'SUCCESS'
        """).fetchone()[0]

        high_alerts = conn.execute("""
            SELECT COUNT(*) FROM alerts
            WHERE severity = 'HIGH'
        """).fetchone()[0]

    return jsonify({
        "total_events": total_events,
        "failed_logins": failed_logins,
        "successful_logins": successful_logins,
        "high_alerts": high_alerts,
        "events": [dict(row) for row in events],
        "alerts": [dict(row) for row in alerts]
    })


if __name__ == "__main__":
    initialize_db()
    seed_events()
    print("Mini SOC dashboard starting...")
    print("Open http://127.0.0.1:5000 in your browser")
    app.run(host="127.0.0.1", port=5000, debug=False)