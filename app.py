from flask import Flask, request, send_file
from werkzeug.utils import secure_filename
from PIL import Image
from rembg import remove
import os

app = Flask(__name__)

# Ensure the uploads directory exists
UPLOAD_FOLDER = '/tmp/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/remove-background', methods=['POST'])
def remove_background():
    # Check if the request contains a file
    if 'file' not in request.files:
        return {"error": "No file provided"}, 400

    file = request.files['file']

    # Check if the file is allowed
    if file.filename == '' or not allowed_file(file.filename):
        return {"error": "Invalid file type"}, 400

    # Save the uploaded file
    filename = secure_filename(file.filename)
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(input_path)

    # Open the image and remove the background
    with open(input_path, "rb") as f:
        input_data = f.read()
    output_data = remove(input_data)

    # Save the output image
    output_path = os.path.join(UPLOAD_FOLDER, f"output_{filename}")
    with open(output_path, "wb") as f:
        f.write(output_data)

    # Return the processed image
    return send_file(output_path, mimetype='image/png')

# Vercel requires a handler function
def handler(request):
    return app.wsgi_app
