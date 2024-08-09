from app.repositories import RequestRepository
from app.models import Request
from app.services import UserService

user_service = UserService()

class RequestService:
    def __init__(self):
        self.request_repository = RequestRepository()

    def get_all_requests(self, filters=None):
        return self.request_repository.get_all_requests(filters)

    def create_request(self, request_data):
        
        user = user_service.get_all_users({
            'id': request_data['userId']
        })[0]
        
        if not user:
            raise ValueError("User not found")
        
        if user and user.currentBooks >= 5:
            raise ValueError("User already has 5 books issued")
        
        request = Request(None, request_data['userId'],None, None, request_data['bookId'],None, False, False, False, False,False, False, None, request_data['issueDate'], request_data['returnDate'], None, None)
        
        if 'isBought' in request_data:
            request.isBought = request_data['isBought']
        
        bookRequest = self.request_repository.create_request(request)     
        user.currentBooks += 1
        updated = user_service.update_user(user.id, {
            'currentBooks': user.currentBooks
        })
        return bookRequest

    def update_request(self, request_id, request_data):
        existing_request = self.get_all_requests({
            'id': request_id
        })[0]
        
        if not existing_request:
            raise ValueError("Request not found")

        # Update only provided fields
        if 'isApproved' in request_data:
            existing_request.isApproved = request_data['isApproved']
        if 'isRejected' in request_data:
            existing_request.isRejected = request_data['isRejected']
        if 'isReturned' in request_data:
            existing_request.isReturned = request_data['isReturned']
        if 'isRevoked' in request_data:
            existing_request.isRevoked = request_data['isRevoked']
        if 'isBought' in request_data:
            existing_request.isBought = request_data['isBought']
        if 'isDeleted' in request_data:
            existing_request.isDeleted = request_data['isDeleted']
        if 'rejectionReason' in request_data:
            existing_request.rejectionReason = request_data['rejectionReason']
        if 'feedback' in request_data:
            existing_request.feedback = request_data['feedback']
        if 'rating' in request_data:
            existing_request.rating = request_data['rating']
        if 'issueDate' in request_data:
            existing_request.issueDate = request_data['issueDate']
        if 'returnDate' in request_data:
            existing_request.returnDate = request_data['returnDate']

        self.request_repository.update_request(existing_request)
        
        if existing_request.isReturned or existing_request.isRevoked or existing_request.isDeleted:
            user = user_service.get_all_users({
                'id': existing_request.userId
            })[0]
            user.currentBooks -= 1
            updated = user_service.update_user(user.id, {
                'currentBooks': user.currentBooks
            })

    def delete_request(self, request_id):
        self.request_repository.delete_request(request_id)

    def return_book(self, request_id, request_data):
        existing_request = self.get_all_requests({
            'id': request_id
        })[0]
        
        if not existing_request:
            raise ValueError("Request not found")

        if 'isReturned' in request_data:
            existing_request.isReturned = request_data['isReturned']
        if 'isBought' in request_data:
            existing_request.isBought = request_data['isBought']
        if 'feedback' in request_data:
            existing_request.feedback = request_data['feedback']
        if 'rating' in request_data:
            existing_request.rating = request_data['rating']
        if 'issueDate' in request_data:
            existing_request.issueDate = request_data['issueDate']
        if 'returnDate' in request_data:
            existing_request.returnDate = request_data['returnDate']

        self.request_repository.update_request(existing_request)
        
        if existing_request.isReturned or existing_request.isRevoked or existing_request.isDeleted:
            user = user_service.get_all_users({
                'id': existing_request.userId
            })[0]
            user.currentBooks -= 1
            updated = user_service.update_user(user.id, {
                'currentBooks': user.currentBooks
            })
