from app.repositories import EbookRepository
from app.models import Ebook

class EbookService:
    def __init__(self):
        self.ebook_repository = EbookRepository()

    def get_all_ebooks(self, filters=None):
        return self.ebook_repository.get_all_ebooks(filters)

    def create_ebook(self, ebook_data):
        ebook = Ebook(None, ebook_data['name'], ebook_data['content'], ebook_data['author'], ebook_data['prologue'], None)
        
        if 'price' in ebook_data:
            ebook.price = ebook_data['price']
                    
        ebook_id = self.ebook_repository.create_ebook(ebook)
        
        if 'sectionId' in ebook_data:
            section_id = ebook_data['sectionId']
            self.ebook_repository.add_ebook_to_section(ebook_id, section_id)
            
        return ebook_id

    def update_ebook(self, ebook_id, ebook_data):
        existing_ebook = self.get_all_ebooks({
            'id': ebook_id
        })[0]
        
        if not existing_ebook:
            raise ValueError("ebook not found")

        # Update only provided fields
        if 'name' in ebook_data:
            existing_ebook.name = ebook_data['name']
        if 'content' in ebook_data:
            existing_ebook.content = ebook_data['content']
        if 'author' in ebook_data:
            existing_ebook.author = ebook_data['author']
        if 'prologue' in ebook_data:
            existing_ebook.prologue = ebook_data['prologue']
        if 'price' in ebook_data:
            existing_ebook.price = ebook_data['price']

        self.ebook_repository.update_ebook(existing_ebook)

    def delete_ebook(self, ebook_id):
        self.ebook_repository.delete_ebook(ebook_id)

    def add_ebook_to_section(self, ebook_id, section_id):
        self.ebook_repository.add_ebook_to_section(ebook_id, section_id)

    def remove_ebook_from_section(self, ebook_id, section_id):
        self.ebook_repository.remove_ebook_from_section(ebook_id, section_id)