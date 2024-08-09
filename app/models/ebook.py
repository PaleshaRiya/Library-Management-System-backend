class Ebook:
    def __init__(self, id, name, content, author, prologue, price):
        self.id = id
        self.name = name
        self.content = content
        self.author = author
        self.prologue = prologue
        self.price = price
        self.sections = [] 

    def to_dict(self):
        ebook_dict = {
            'id': self.id,
            'name': self.name,
            'content': self.content,
            'author': self.author,
            'prologue': self.prologue,
            'price': self.price
        }
        
        if self.sections:
            ebook_dict['sections'] = self.sections
        
        return ebook_dict
