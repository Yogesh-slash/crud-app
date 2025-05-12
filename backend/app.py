from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
db = SQLAlchemy(app)

# Define the Note model
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)

# Initialize database
with app.app_context():
    db.create_all()

# Get all notes or create a new note
@app.route('/api/notes', methods=['GET', 'POST'])
def handle_notes():
    if request.method == 'POST':
        data = request.get_json()
        new_note = Note(content=data['content'])
        db.session.add(new_note)
        db.session.commit()
        return jsonify({'id': new_note.id, 'content': new_note.content})
    else:
        notes = Note.query.all()
        return jsonify([{'id': n.id, 'content': n.content} for n in notes])

# Update or delete a specific note
@app.route('/api/notes/<int:id>', methods=['PUT', 'DELETE'])
def update_delete_note(id):
    note = Note.query.get_or_404(id)

    if request.method == 'PUT':
        data = request.get_json()
        note.content = data['content']
        db.session.commit()
        return jsonify({'id': note.id, 'content': note.content})

    if request.method == 'DELETE':
        db.session.delete(note)
        db.session.commit()
        return jsonify({'message': 'Note deleted'})

if __name__ == '__main__':
    app.run(debug=True)