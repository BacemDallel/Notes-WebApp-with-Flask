from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
from datetime import datetime
import json


views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    notes = Note.query.filter_by(user_id=current_user.id).all()

    if request.method == 'POST':
        note_text = request.form.get('note')
        if len(note_text) < 1:
            flash("Can't add an empty note!", category='error')
        else:
            new_note = Note(data=note_text, date=datetime.now(), user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user, notes=notes)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note_data = json.loads(request.data)
    note_id = note_data['noteId']

    note = Note.query.get(note_id)
    if note and note.user_id == current_user.id:
        db.session.delete(note)
        db.session.commit()
        return jsonify({})

    return jsonify({'error': 'Note not found or unauthorized'})
