from flask import Flask, jsonify, request
from models import db, Book

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET'])
def home():
    return "¡Hola, Mundo! "

@app.get('/Books')
def get_books():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 3, type=int)

        if page < 1:
            page = 1
        if per_page < 1 or per_page > 100:  
            per_page = 3

        books_pagination = Book.query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return jsonify({
            
            'success': True,
            'data': [book.to_dict() for book in books_pagination.items],
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al obtener libros: {str(e)}'
        }), 500
@app.get('/Books/<int:id>')  
def get_book(id):
    try:
        book = Book.query.get(id)
        if book:
            return jsonify({
                'success': True,
                'data': book.to_dict()
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Libro no encontrado'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al obtener el libro: {str(e)}'
        }), 500


@app.post('/Books')
def add_book():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se recibieron datos JSON'
            }), 400
        
        if not data.get('title') or not data.get('author'):
            return jsonify({
                'success': False,
                'error': 'Los campos title y author son obligatorios'
            }), 400
        
        nuevo_libro = Book(
            title=data.get('title'),
            author=data.get('author'),
            editorial=data.get('editorial', ''), 
            edition=data.get('edition')
        )
        
        db.session.add(nuevo_libro)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Libro agregado correctamente',
            'data': nuevo_libro.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Error al crear el libro: {str(e)}'
        }), 500

@app.patch('/Books/<int:id>')
def update_book(id):
    try:
        book = Book.query.get(id)
        if not book:
            return jsonify({
                'success': False,
                'error': 'Libro no encontrado'
            }), 404
        
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se recibieron datos JSON'
            }), 400
        
        if 'title' in data:
            book.title = data['title']
        if 'author' in data:
            book.author = data['author']
        if 'editorial' in data:
            book.editorial = data['editorial']
        if 'edition' in data:
            book.edition = data['edition']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Libro actualizado correctamente',
            'data': book.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Error al actualizar el libro: {str(e)}'
        }), 500

@app.delete('/Books/<int:id>')
def delete_book(id):
    try:
        book = Book.query.get(id)
        if not book:
            return jsonify({
                'success': False,
                'error': 'Libro no encontrado'
            }), 404
        
        deleted_book = book.to_dict()
        
        db.session.delete(book)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Libro eliminado correctamente',
            'deleted_data': deleted_book
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Error al eliminar el libro: {str(e)}'
        }), 500
    
if __name__ == '__main__':
    app.run(debug=True)