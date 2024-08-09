import sqlite3
from datetime import datetime, timezone, timedelta

class CeleryRepository:
    def __init__(self):
        self.db_path = 'app/database.db'
    
    def revoke_access(self):
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            
            current_time = datetime.now(timezone.utc)
            
            print(f"Revoking access for book requests with return date before {current_time}")
            
            cursor.execute(
                "SELECT id, returnDate FROM bookRequest WHERE isRevoked = 0"
            )
            rows = cursor.fetchall()
            
            for row in rows:
                book_request_id = row[0]
                return_date_str = row[1]
                return_date = datetime.fromisoformat(return_date_str)
                
                if return_date < current_time:
                    cursor.execute(
                        "UPDATE bookRequest SET isRevoked = 1 WHERE id = ? AND isRevoked = 0 AND isBought = 0",
                        (book_request_id,)
                    )
                    print(f"Revoked access for book request id {book_request_id}")
        
            connection.commit()
            connection.close()
            return True
        
        except Exception as e:
            print(f"Error revoking access: {str(e)}")
            return False
    
    def send_daily_reminder(self):
        connection = sqlite3.connect('app/database.db')
        cursor = connection.cursor()
        
        current_time = datetime.now(timezone.utc)
        next_day = current_time + timedelta(days=1)
        
        print(f"Sending daily reminders for book requests with return date {next_day}")
        print(f"Current time: {current_time}")
        
        cursor.execute(
            """
            SELECT u.email, u.username, b.name, br.returnDate
            FROM bookRequest br
            JOIN user u ON br.userId = u.id
            JOIN eBook b ON br.bookId = b.id
            WHERE br.isRevoked = 0 AND date(br.returnDate) = date(?) AND br.isBought = 0 AND br.isReturned = 0 AND br.isDeleted = 0 AND br.isRejected = 0
            """, (next_day.date(),)
        )
        
        rows = cursor.fetchall()
        connection.close()
        return rows

    def get_monthly_report_data(self):
        connection = sqlite3.connect('app/database.db')
        cursor = connection.cursor()
        
        # Calculate the date range for the last month
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        # Query to get issued eBooks, return dates, and ratings
        query = """
            SELECT br.userId, u.username AS username, u.email, eb.name AS bookName, br.issueDate, br.returnDate, br.rating, br.feedback, br.isReturned, br.isRevoked, br.isBought, br.isApproved
            FROM bookRequest br
            JOIN user u ON br.userId = u.id
            JOIN eBook eb ON br.bookId = eb.id
            WHERE br.createdAt BETWEEN ? AND ?
        """
        cursor.execute(query, (start_date, end_date))
        result = cursor.fetchall()
        
        connection.close()
        return result

    def get_ebooks_data(self):
        connection = sqlite3.connect('app/database.db')
        cursor = connection.cursor()

        # Calculate the date range for the last month
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)

        # Query to get issued eBooks, return dates, and additional fields
        query = """
        SELECT u.id AS userId, u.name AS username, u.email, eb.name AS bookName, eb.content, eb.author, br.issueDate, br.returnDate
        FROM bookRequest br
        JOIN user u ON br.userId = u.id
        JOIN eBook eb ON br.bookId = eb.id
        WHERE br.createdAt BETWEEN ? AND ?
        """
        cursor.execute(query, (start_date, end_date))
        result = cursor.fetchall()

        connection.close()
        return result

