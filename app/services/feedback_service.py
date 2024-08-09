from app.repositories import FeedbackRepository
from app.models import Feedback

class FeedbackService:
    def __init__(self):
        self.feedback_repository = FeedbackRepository()

    def get_all_feedbacks(self, filters=None):
        return self.feedback_repository.get_all_feedbacks(filters)

    def create_feedback(self, feedback_data):
        existing_feedback = self.get_all_feedbacks({
            'id': feedback_data['id']
        })[0]
        
        if not existing_feedback:
            raise ValueError("feedback not found")

        if 'feedback' in feedback_data:
            existing_feedback.feedback = feedback_data['feedback']
        if 'rating' in feedback_data:
            existing_feedback.rating = feedback_data['rating']

        self.feedback_repository.update_feedback(existing_feedback)

    def update_feedback(self, feedback_id, feedback_data):
        existing_feedback = self.get_all_feedbacks({
            'id': feedback_id
        })[0]
        
        if not existing_feedback:
            raise ValueError("feedback not found")

        if 'feedback' in feedback_data:
            existing_feedback.feedback = feedback_data['feedback']
        if 'rating' in feedback_data:
            existing_feedback.rating = feedback_data['rating']

        self.feedback_repository.update_feedback(existing_feedback)

    def delete_feedback(self, feedback_id):
        self.feedback_repository.delete_feedback(feedback_id)
