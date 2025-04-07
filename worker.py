from pathlib import Path
import sqlite3
import json
import os

# Paths to the database and output file
DB_PATH = (
    Path(os.getenv("INPUT_PATH", "/mnt/input")) / "query_results.db"
)  # Default path to the SQLite database
OUTPUT_PATH = (
    Path(os.getenv("OUTPUT_PATH", "/mnt/output")) / "stats.json"
)  # Default output JSON path


def create_db_connection():
    """Establishes connection to the database with dictionary row factory."""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        raise e


def get_users_data(cursor):
    """Retrieves all data from users table."""
    try:
        cursor.execute("SELECT * FROM users")
        users = [dict(row) for row in cursor.fetchall()]
        return users
    except Exception as e:
        print(f"Error querying users table: {e}")
        raise e


def get_storage_metrics_data(cursor):
    """Retrieves all data from storage_metrics table."""
    try:
        cursor.execute("SELECT * FROM storage_metrics")
        storage_metrics = [dict(row) for row in cursor.fetchall()]
        return storage_metrics
    except Exception as e:
        print(f"Error querying storage_metrics table: {e}")
        raise e


def get_auth_sources_data(cursor):
    """Retrieves all data from auth_sources table."""
    try:
        cursor.execute("SELECT * FROM auth_sources")
        auth_sources = [dict(row) for row in cursor.fetchall()]
        return auth_sources
    except Exception as e:
        print(f"Error querying auth_sources table: {e}")
        raise e


def get_all_data():
    """Retrieves all data from all tables using specialized functions."""
    try:
        # Create a single connection and cursor to be used by all functions
        conn = create_db_connection()
        cursor = conn.cursor()

        # Get data from each table using the specialized functions
        users = get_users_data(cursor)
        storage_metrics = get_storage_metrics_data(cursor)
        auth_sources = get_auth_sources_data(cursor)

        # Close the connection after all queries are done
        conn.close()

        # Create a nested structure with all data
        all_data = {
            "users": users,
            "storage_metrics": storage_metrics,
            "auth_sources": auth_sources,
        }

        return all_data
    except Exception as e:
        print(f"Error compiling all data: {e}")
        raise e


def save_data_to_json(data, output_path):
    """Saves the combined data to a JSON file."""
    try:
        # Ensure the output directory exists
        output_dir = os.path.dirname(output_path)
        os.makedirs(output_dir, exist_ok=True)

        # Save to JSON
        with open(output_path, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Data saved to {output_path}")
    except Exception as e:
        print(f"Error saving JSON: {e}")


def main():
    print(f"Processing query results from {DB_PATH}")
    all_data = get_all_data()
    if all_data:
        print(f"Successfully retrieved data from all tables")
        save_data_to_json(all_data, OUTPUT_PATH)
    else:
        print("No data found in the database")
        # Create an empty stats file to indicate processing completed
        save_data_to_json({}, OUTPUT_PATH)


if __name__ == "__main__":
    main()
