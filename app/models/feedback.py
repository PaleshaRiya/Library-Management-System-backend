class Feedback:
    def __init__(self, id, userId, username,email,  bookId, bookName, feedback, rating):
        self.id = id
        self.userId = userId
        self.username = username
        self.email = email
        self.bookId = bookId
        self.bookName = bookName
        self.feedback = feedback
        self.rating = rating

    def to_dict(self):
        return {
            'id': self.id,
            'userId': self.userId,
            'username': self.username,
            'email': self.email,
            'bookId': self.bookId,
            'bookName': self.bookName,
            'feedback': self.feedback,
            'rating': self.rating
        }
