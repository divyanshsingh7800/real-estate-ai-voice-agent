import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE_DIR / "real_estate.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def create_tables():

    connection = get_connection()
    cursor = connection.cursor()

    # Main leads table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            location TEXT,
            property_type TEXT,
            bhk TEXT,
            budget_min INTEGER,
            budget_max INTEGER,
            timeline TEXT,
            purpose TEXT,
            requirements TEXT,
            recommended_properties TEXT,
            conversation_summary TEXT,
            qualification_score INTEGER
        )
    """)

    connection.commit()

    # ---------------------------------------------------------
    # Check existing columns
    # ---------------------------------------------------------

    cursor.execute("PRAGMA table_info(leads)")
    existing_columns = {
        row["name"] for row in cursor.fetchall()
    }

    # ---------------------------------------------------------
    # Add missing columns
    # ---------------------------------------------------------

    required_columns = {

        "name": "TEXT",
        "phone": "TEXT",
        "location": "TEXT",
        "property_type": "TEXT",
        "bhk": "TEXT",
        "budget_min": "INTEGER",
        "budget_max": "INTEGER",
        "timeline": "TEXT",
        "purpose": "TEXT",
        "requirements": "TEXT",
        "recommended_properties": "TEXT",
        "conversation_summary": "TEXT",
        "qualification_score": "INTEGER"
    }

    for column_name, column_type in required_columns.items():

        if column_name not in existing_columns:

            cursor.execute(
                f"ALTER TABLE leads ADD COLUMN "
                f"{column_name} {column_type}"
            )

    connection.commit()
    connection.close()


def save_leads(lead_data):

    # Make sure database/table is updated
    create_tables()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO leads (
            name,
            phone,
            location,
            property_type,
            bhk,
            budget_min,
            budget_max,
            timeline,
            purpose,
            requirements,
            recommended_properties,
            conversation_summary,
            qualification_score
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        lead_data.get("name"),
        lead_data.get("phone"),
        lead_data.get("location"),
        lead_data.get("property_type"),
        lead_data.get("bhk"),
        lead_data.get("budget_min"),
        lead_data.get("budget_max"),
        lead_data.get("timeline"),
        lead_data.get("purpose"),
        lead_data.get("requirements"),
        lead_data.get("recommended_properties"),
        lead_data.get("conversation_summary"),
        lead_data.get("qualification_score")
    ))

    connection.commit()

    lead_id = cursor.lastrowid

    connection.close()

    return lead_id


def get_all_leads():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM leads ORDER BY id DESC"
    )

    leads = cursor.fetchall()

    connection.close()

    return leads


# Create/update database automatically
create_tables()