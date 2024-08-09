import sqlite3
from app.models import Feedback

class FeedbackRepository:
    def __init__(self):
        self.db_path = 'app/database.db'

    def get_all_feedbacks(self, filters=None):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        
        query = """
            SELECT 
                br.id, 
                br.userId, 
                u.username, 
                u.email,
                br.bookId, 
                e.name AS bookName,
                br.feedback, 
                br.rating
            FROM bookRequest br
            LEFT JOIN eBook e ON br.bookId = e.id
            LEFT JOIN user u ON br.userId = u.id
            WHERE 1=1
        """
        params = []

        if filters:
            if 'userId' in filters:
                query += " AND br.userId = ?"
                params.append(filters['userId'])
            if 'bookId' in filters:
                query += " AND br.bookId = ?"
                params.append(filters['bookId'])
            if 'id' in filters:
                query += " AND br.id = ?"
                params.append(filters['id'])
                
        cursor.execute(query, params)
        rows = cursor.fetchall()
        feedbacks = []
        
        print(rows)
        
        for row in rows:
            feedback = Feedback(*row)
            feedbacks.append(feedback)
        connection.close()
        return feedbacks

    def update_feedback(self, feedback):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE bookRequest SET feedback = ?, rating = ? WHERE id = ?",
            (feedback.feedback, feedback.rating, feedback.id)
        )
        connection.commit()
        connection.close()

    def delete_feedback(self, feedback_id):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE bookRequest SET feedback = ?, rating = ? WHERE id = ?",
            (None, None, feedback_id)
        )
        connection.commit()
        connection.close()
