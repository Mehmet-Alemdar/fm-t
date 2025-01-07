from flask import Blueprint, jsonify, request
from app.models import Author
from app.utils import paginate

bp = Blueprint('authors', __name__)

@bp.route('/', methods=['GET'])
def get_authors():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    query = Author.objects

    name_filter = request.args.get('name')
    if name_filter:
        query = query.filter(name__icontains=name_filter)

    result = paginate(query, page, per_page)
    authors = [{'id': str(author.id), 'name': author.name, 'age': author.age} for author in result['items']]
    return jsonify({
        'total': result['total'],
        'page': result['page'],
        'per_page': result['per_page'],
        'authors': authors
    })

@bp.route('/', methods=['POST'])
def create_author():
    data = request.json
    author = Author(**data).save()
    return jsonify({'id': str(author.id), 'name': author.name, 'age': author.age}), 201

@bp.route('/<author_id>', methods=['PUT'])
def update_author(author_id):
    print(author_id) 
    data = request.json
    author = Author.objects(id=author_id).first()
    author.update(**data)
    return jsonify({'message': 'Author updated successfully'})

@bp.route('/<author_id>', methods=['DELETE'])
def delete_author(author_id):
    author = Author.objects(id=author_id).first()
    author.delete()
    return jsonify({'message': 'Author deleted successfully'})