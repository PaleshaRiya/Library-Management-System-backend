import sqlite3
from app.models import Section

class SectionRepository:
    def __init__(self):
        self.db_path = 'app/database.db'

    def get_all_sections(self, filters=None):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        
        query = "SELECT id, name, description FROM section WHERE 1=1"
        params = []

        if filters:
            if 'name' in filters:
                name_filter = filters['name']
                query += " AND name LIKE ?"
                params.append(name_filter + '%')
            if 'id' in filters:
                id_filter = filters['id']
                query += " AND id = ?"
                params.append(id_filter)
                
        cursor.execute(query, params)
        rows = cursor.fetchall()
        sections = [Section(*row) for row in rows]
        connection.close()
        return sections

    def create_section(self, section):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO section (name, description) VALUES (?, ?)",
            (section.name, section.description)
        )
        connection.commit()
        section_id = cursor.lastrowid
        connection.close()
        return section_id

    def update_section(self, section):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE section SET name = ?, description = ? WHERE id = ?",
            (section.name, section.description, section.id)
        )
        connection.commit()
        connection.close()

    def delete_section(self, section_id):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM section WHERE id = ?", (section_id,))
        connection.commit()
        connection.close()