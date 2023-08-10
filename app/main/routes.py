from flask import render_template, current_app, abort
from flask_login import login_required, current_user
from stegano import lsb
from pathlib import Path

from app.main import bp
from app.models import Message


@bp.route('/')
@login_required
def index():
    messages = current_user.get_messages()

    return render_template('index.html', messages=messages)


@bp.route('/view_message/<int:message_id>')
def view_message(message_id):
    message = Message.query.get_or_404(message_id)
    user_messages = current_user.get_messages()

    if message not in user_messages:
        abort(404)
    
    return render_template('view_message.html', message=message)


@bp.route('/reveal_text/<int:message_id>', methods=['POST'])
def reveal_text(message_id):
    message = Message.query.get_or_404(message_id)

    if message:
        message_file = Path(current_app.config['UPLOADS_DIR']) / message.file
        text = lsb.reveal(message_file)
        return {'ok': True, 'message': text}
        

    return {'ok': False, 'message': "Message does not exists!"}