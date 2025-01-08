from flask import Blueprint, jsonify, request
from app.models import Book
from app.models import Author
from app.utils import paginate

bp = Blueprint('books', __name__)

@bp.route('/', methods=['GET'])
def get_books():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    query = Book.objects

    title_filter = request.args.get('title')
    if title_filter:
        query = query.filter(title__icontains=title_filter)

    genre_filter = request.args.get('genre')
    if genre_filter:
        query = query.filter(genre__icontains=genre_filter)

    author_name_filter = request.args.get('author_name')
    if author_name_filter:
        author_ids = [author.id for author in Author.objects(name__icontains=author_name_filter)]
        query = query.filter(author__in=author_ids)

    result = paginate(query, page, per_page)
    books = [{
        'id': str(book.id),
        'title': book.title,
        'genre': book.genre,
        'author': {
            'name': book.author.name,
            'age': book.author.age
        }
    } for book in result['items']]
    return jsonify({
        'total': result['total'],
        'page': result['page'],
        'per_page': result['per_page'],
        'books': books
    })

@bp.route('/', methods=['POST'])
def create_book():
    data = request.json
    author_id = data.get('author_id')
    author = Author.objects(id=author_id).first()
    
    if not author:
        return jsonify({'error': 'Author not found'}), 404

    book = Book(
        title=data.get('title'),
        genre=data.get('genre'),
        author=author
    )
    book.save()

    return jsonify({
        'id': str(book.id),
        'title': book.title,
        'genre': book.genre,
        'author': {
            'name': author.name,
            'age': author.age
        }
    }), 201

@bp.route('/<book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.json
    book = Book.objects(id=book_id).first_or_404()
    book.update(**data)
    return jsonify({'message': 'Book updated successfully'})

@bp.route('/<book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.objects(id=book_id).first_or_404()
    book.delete()
    return jsonify({'message': 'Book deleted successfully'})