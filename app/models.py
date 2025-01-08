from mongoengine import Document, StringField, IntField, ReferenceField

class Author(Document):
    name = StringField(required=True, max_length=50)
    age = IntField(required=True)

class Book(Document):
    title = StringField(required=True, max_length=100)
    genre = StringField(required=True, max_length=50)
    author = ReferenceField(Author, required=True) 