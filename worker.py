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


def get_all_data():
    """Retrieves all data from all tables using specialized functions."""
    try:
        # Create a single connection and cursor to be used by all functions
        conn = create_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM results")
        results = [dict(row) for row in cursor.fetchall()]
        # Close the connection after all queries are done
        conn.close()

        return results
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
