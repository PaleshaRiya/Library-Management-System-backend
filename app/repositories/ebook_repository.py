import sqlite3
from app.models import Ebook

class EbookRepository:
    def __init__(self):
        self.db_path = 'app/database.db'

    def get_all_ebooks(self, filters=None):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        if filters and 'sectionId' in filters:
            query = """
                SELECT e.id, e.name, e.content, e.author, e.prologue, e.price, seb.sectionId, s.name
                FROM sectionToeBook seb
                LEFT JOIN eBook e ON seb.eBookId = e.id
                LEFT JOIN section s ON seb.sectionId = s.id
                WHERE 1=1
            """
            
            params = []

            if filters:
                if 'sectionId' in filters:
                    query += " AND seb.sectionId = ?"
                    params.append(filters['sectionId'])
        
        else:
            query = """
            SELECT e.id, e.name, e.content, e.author, e.prologue, e.price,
                   s.id AS sectionId, s.name AS sectionName
            FROM eBook e
            LEFT JOIN sectionToeBook stb ON e.id = stb.eBookId
            LEFT JOIN section s ON stb.sectionId = s.id
            WHERE 1=1
            """
            
            params = []
            
            if filters:
                if 'name' in filters:
                    query += " AND e.name LIKE ?"
                    params.append(filters['name'] + '%')
                if 'id' in filters:
                    query += " AND e.id = ?"
                    params.append(filters['id'])

        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        print(rows)

        ebooks_dict = {}
        for row in rows:
            ebook_id = row[0]
            if ebook_id not in ebooks_dict:
                ebook_data = row[:6]  # Assuming first 6 columns belong to Ebook
                ebooks_dict[ebook_id] = Ebook(*ebook_data)
                ebooks_dict[ebook_id].sections = []
            
            if row[6] is not None:  # Ensure sectionId is not None
                section_id = row[6]
                section_name = row[7] if row[7] is not None else "Unknown"
                ebooks_dict[ebook_id].sections.append({'id': section_id, 'name': section_name})

        connection.close()

        return list(ebooks_dict.values())


    def create_ebook(self, ebook):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO eBook (name, content, author, prologue, price) VALUES (?, ?, ?, ?, ?)",
            (ebook.name, ebook.content, ebook.author, ebook.prologue, ebook.price)
        )
        connection.commit()
        ebook_id = cursor.lastrowid
        connection.close()
        return ebook_id

    def update_ebook(self, ebook):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE eBook SET name = ?, content = ?, author = ?, prologue = ?, price = ?, updatedAt = CURRENT_TIMESTAMP WHERE id = ?",
            (ebook.name, ebook.content, ebook.author, ebook.prologue, ebook.price, ebook.id)
        )
        connection.commit()
        connection.close()

    def delete_ebook(self, ebook_id):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM eBook WHERE id = ?", (ebook_id,))
        cursor.execute("DELETE FROM sectionToeBook WHERE eBookId = ?", (ebook_id,))
        connection.commit()
        connection.close()

    def add_ebook_to_section(self, ebook_id, section_id):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO sectionToeBook (eBookId, sectionId) VALUES (?, ?)",
            (ebook_id, section_id)
        )
        connection.commit()
        connection.close()

    def remove_ebook_from_section(self, ebook_id, section_id):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute(
            "DELETE FROM sectionToeBook WHERE eBookId = ? AND sectionId = ?",
            (ebook_id, section_id)
        )
        connection.commit()
        connection.close()