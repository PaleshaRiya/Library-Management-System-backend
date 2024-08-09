class Request:
    def __init__(self, id, userId, username,email,  bookId, bookName, isApproved, isRejected, isReturned, isRevoked, isBought, isDeleted, rejectionReason, issueDate, returnDate, feedback, rating):
        self.id = id
        self.userId = userId
        self.username = username
        self.email = email
        self.bookId = bookId
        self.bookName = bookName
        self.isApproved = isApproved
        self.isRejected = isRejected
        self.isReturned = isReturned
        self.isRevoked = isRevoked
        self.isBought = isBought
        self.isDeleted = isDeleted
        self.rejectionReason = rejectionReason
        self.issueDate = issueDate
        self.returnDate = returnDate
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
            'isApproved': self.isApproved,
            'isRejected': self.isRejected,
            'isReturned': self.isReturned,
            'isRevoked': self.isRevoked,
            'isBought': self.isBought,
            'isDeleted': self.isDeleted,
            'rejectionReason': self.rejectionReason,
            'issueDate': self.issueDate,
            'returnDate': self.returnDate,
            'feedback': self.feedback,
            'rating': self.rating
        }
