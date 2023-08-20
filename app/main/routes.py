from flask import flash, render_template, current_app, abort, redirect, url_for
from flask_login import login_required, current_user
from stegano import lsb
from pathlib import Path
from werkzeug.utils import secure_filename

from app.main import bp
from app.models import Message, User
from app.main.forms import CreateMessageForm, UploadImageForm


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


@bp.route('/message', methods=['POST', 'GET'])
def send_message():
    """
    Route for sending messages with mandatory image attachments for steganography.

    This route handles the process of sending messages between users. Users are required to
    provide the receiver's username, a title for the message, and the message content. The
    main feature of this route is the secure embedding of the message content within an image
    using steganography.

    Args:
        None

    Returns:
        If the request method is GET:
            Renders the 'message.html' template with a form to compose and send messages.
        
        If the request method is POST and form validation succeeds:
            - Sends the message with the message content securely hidden within the attached image.
            - If successful, redirects to the view_message route for the sent message.
            - If unsuccessful, flashes an appropriate error message and renders the 'message.html' template.
        
        If the request method is POST and form validation fails:
            Flashes validation error messages and renders the 'message.html' template.

    Raises:
        HTTPError(500): If an error occurs during steganographic image embedding.
        
    Note:
        - Uses the CreateMessageForm form for input validation.
        - Relies on the User model for querying receiver details.
        - The file upload is saved to the UPLOADS_DIR specified in the app configuration.

    Examples:
        A user can compose a new message using the 'message.html' form, specifying the receiver's
        username, title, and message content. An image file must be attached, as the text content
        will be hidden within the image using steganography. Upon successful submission, the message
        is sent, and the message text is securely embedded within the attached image.

    """
    form = CreateMessageForm()

    if form.validate_on_submit():
        receiver = User.query.filter_by(username=form.receiver.data).first()

        # Check if the receiver exists else send an error message
        if not receiver:
            flash("Incorrect receiver username")
            return render_template('message.html', form=form)
        
        # Get the message data from the form
        title = form.title.data
        message_text = form.message.data
        file = form.file.data

        # Prepare the file name and destination
        file_name = secure_filename(file.filename.lower())
        file_dest = current_app.config['UPLOADS_DIR'] + f"/{file_name}"

        # Hide the text inside the image
        try:
            image = lsb.hide(file, message_text)
            image.save(file_dest)
        except:
            abort(500)

        
        message = current_user.send_message(
            title=title,
            file=file_name,
            receiver=receiver
        )

        if message:
            flash("Message sent successfully")

            return redirect(url_for('main.view_message', message_id=message.id))
        
        flash("Failed to send message!")
        
    return render_template('send_message.html', form=form)


@bp.route('/messages')
def view_messages():
    messages = current_user.get_messages()

    return render_template('view_messages.html', messages=messages)


@bp.route("/upload", methods=["GET", "POST"])
def upload():
    """
    Route for uploading steganographic image.

    This route enables users to upload pre-prepared steganographic images, where the user is both the sender
    and the receiver of the message. Users can provide a title for the message and the steganographic image
    file to be uploaded.

    Args:
        None

    Returns:
        If the request method is GET:
            Renders the 'upload.html' template with a form to upload steganographic images.
        
        If the request method is POST and form validation succeeds:
            - Uploads the steganographic image as a message.
            - Associates the message with the user as both sender and receiver.
            - If successful, redirects to the view_message route for the uploaded message.
            - If unsuccessful, flashes an appropriate error message and renders the 'upload.html' template.

    Raises:
        None
        
    Note:
        - Uses the UploadImageForm form for input validation.
        - The file upload is saved to the UPLOADS_DIR specified in the app configuration.
        - Users can indicate whether the uploaded image is already encrypted as a steganographic message.

    Examples:
        A user can upload a pre-prepared steganographic image using the 'upload.html' form, providing a title
        for the message and the steganographic image file. The uploaded image will be treated as a message
        where the user is both the sender and the receiver.
    """
    
    form = UploadImageForm()
    if form.validate_on_submit():
          # Get the message data from the form
        title = form.title.data
        image = form.image.data

        # Prepare the file name and destination
        file_name = secure_filename(image.filename.lower())
        file_dest = current_app.config['UPLOADS_DIR'] + f"/{file_name}"

        message = current_user.send_message(
            title=title,
            file=file_name,
            receiver=current_user,
        )
        message.encrypted = form.already_encrypted.data

        if message:
            image.save(file_dest)
            flash("Message uploaded successfully")

            return redirect(url_for('main.view_message', message_id=message.id))
        
        flash("Failed to upload message!")

    return render_template("upload.html", form=form)