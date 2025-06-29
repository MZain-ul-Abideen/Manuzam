import sqlite3
from typing import List, Tuple

def get_tables_and_columns(db_path: str) -> List[Tuple[str, List[str]]]:
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        
        result = []
        
        for table in tables:
            cursor.execute(f"PRAGMA table_info({table});")
            columns = [row[1] for row in cursor.fetchall()]
            result.append((table, columns))
            
        return result
    
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
    
    finally:
        if conn:
            conn.close()

def print_database_schema(db_path: str) -> None:
    tables_info = get_tables_and_columns(db_path)
    
    if not tables_info:
        print("No tables found or error occurred")
        return
        
    for table_name, columns in tables_info:
        print(f"\nTable: {table_name}")
        print("Columns:")
        for column in columns:
            print(f"  - {column}")

if __name__ == "__main__":
    database_path = "../backend/app.db"
    print_database_schema(database_path)