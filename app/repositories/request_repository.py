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

    # New functon to handle the transactional creation of a request with atomicity guarantees
    def create_request_transactional(self, request):
        """
        Executes the checkout limit verification, book counter increment,
        and request insertion inside a single ACID atomic transaction.
        """
        connection = sqlite3.connect(self.db_path, timeout=10.0, isolation_level="EXCLUSIVE")
        cursor = connection.cursor()
        try:
            # 1. ATOMIC CHECK & INCREMENT (Row-level invariant guard)
            # This only increments if the user currently has LESS than 5 books.
            cursor.execute(
                "UPDATE user SET currentBooks = currentBooks + 1 WHERE id = ? AND currentBooks < 5",
                (request.userId,)
            )

            # If 0 rows were updated, either the user doesn't exist or already has 5 books!
            if cursor.rowcount == 0:
                cursor.execute("SELECT id, currentBooks FROM user WHERE id = ?", (request.userId,))
                user_row = cursor.fetchone()
                if not user_row:
                    raise ValueError("User not found")
                else:
                    raise ValueError("User already has 5 books issued (concurrent checkout limit reached)")

            # 2. INSERT THE CHECKOUT REQUEST (In the exact same transaction)
            cursor.execute(
                """INSERT INTO bookRequest 
                   (userId, bookId, isApproved, isRejected, isReturned, isRevoked, isBought, rejectionReason, issueDate, returnDate, feedback, rating) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (request.userId, request.bookId, request.isApproved, request.isRejected, 
                 request.isReturned, request.isRevoked, request.isBought, request.rejectionReason, 
                 request.issueDate, request.returnDate, request.feedback, request.rating)
            )
            request_id = cursor.lastrowid

            # 3. COMMIT BOTH SIMULTANEOUSLY (Atomicity guaranteed: All or Nothing)
            connection.commit()
            return request_id

        except Exception as e:
            # If any failure occurs, rollback completely!
            connection.rollback()
            raise e
        finally:
            connection.close()

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
