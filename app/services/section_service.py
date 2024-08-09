from app.repositories.section_repository import SectionRepository
from app.models import Section

class SectionService:
    def __init__(self):
        self.section_repository = SectionRepository()

    def get_all_sections(self, filters=None):
        return self.section_repository.get_all_sections(filters)

    def create_section(self, section_data):
        section = Section(None, section_data['name'], section_data['description'])
        return self.section_repository.create_section(section)

    def update_section(self, section_id, section_data):
        existing_section = self.get_all_sections({
            'id': section_id
        })[0]
        
        if not existing_section:
            raise ValueError("section not found")

        # Update only provided fields
        if 'name' in section_data:
            existing_section.name = section_data['name']
        if 'description' in section_data:
            existing_section.description = section_data['description']

        self.section_repository.update_section(existing_section)

    def delete_section(self, section_id):
        self.section_repository.delete_section(section_id)
