import sqlite3
from app.models import Request

class RequestRepository:
    def __init__(self):
        self.db_path = 'app/database.db'

    def get_all_requests(self, filters=None):
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
                br.isApproved, 
                br.isRejected, 
                br.isReturned, 
                br.isRevoked, 
                br.isBought, 
                br.isDeleted,
                br.rejectionReason, 
                br.issueDate, 
                br.returnDate, 
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
            if 'isApproved' in filters:
                query += " AND br.isApproved = ?"
                params.append(filters['isApproved'])
            if 'isRejected' in filters:
                query += " AND br.isRejected = ?"
                params.append(filters['isRejected'])
            if 'isReturned' in filters:
                query += " AND br.isReturned = ?"
                params.append(filters['isReturned'])
            if 'isRevoked' in filters:
                query += " AND br.isRevoked = ?"
                params.append(filters['isRevoked'])
            if 'isBought' in filters:
                query += " AND br.isBought = ?"
                params.append(filters['isBought'])
            if 'isDeleted' in filters:
                query += " AND br.isDeleted = ?"
                params.append(filters['isDeleted'])
            if 'issueDateFrom' in filters:
                query += " AND br.issueDate >= ?"
                params.append(filters['issueDateFrom'])
            if 'issueDateTo' in filters:
                query += " AND br.issueDate <= ?"
                params.append(filters['issueDateTo'])
            if 'returnDateFrom' in filters:
                query += " AND br.returnDate >= ?"
                params.append(filters['returnDateFrom'])
            if 'returnDateTo' in filters:
                query += " AND br.returnDate <= ?"
                params.append(filters['returnDateTo'])
            if 'id' in filters:
                query += " AND br.id = ?"
                params.append(filters['id'])
                
        cursor.execute(query, params)
        rows = cursor.fetchall()
        requests = []
        
        print(rows)
        
        for row in rows:
            request = Request(*row)
            requests.append(request)
        connection.close()
        return requests

    def create_request(self, request):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO bookRequest (userId, bookId, isApproved, isRejected, isReturned, isRevoked, isBought, rejectionReason, issueDate, returnDate, feedback, rating) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (request.userId, request.bookId, request.isApproved, request.isRejected, request.isReturned, request.isRevoked, request.isBought, request.rejectionReason, request.issueDate, request.returnDate, request.feedback, request.rating)
        )
        connection.commit()
        request_id = cursor.lastrowid
        connection.close()
        return request_id

    def update_request(self, request):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE bookRequest SET userId = ?, bookId = ?, isApproved = ?, isRejected = ?, isReturned = ?, isRevoked = ?, isBought = ?, isDeleted = ?, rejectionReason = ?, issueDate = ?, returnDate = ?, feedback = ?, rating = ? WHERE id = ?",
            (request.userId, request.bookId, request.isApproved, request.isRejected, request.isReturned, request.isRevoked, request.isBought,request.isDeleted,  request.rejectionReason, request.issueDate, request.returnDate, request.feedback, request.rating, request.id)
        )
        connection.commit()
        connection.close()

    def delete_request(self, request_id):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE bookRequest SET isDeleted = ? WHERE id = ?",
            (True, request_id)
        )
        connection.commit()
        connection.close()
