from flask import Flask, request, send_file
from werkzeug.utils import secure_filename
from PIL import Image
from rembg import remove
import os
import io

app = Flask(__name__)

# Ensure the uploads directory exists
UPLOAD_FOLDER = '/tmp/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return {"message": "Background Remover API is running!"}

@app.route('/remove-background', methods=['POST'])
def remove_background():
    # Check if the request contains a file
    if 'file' not in request.files:
        return {"error": "No file provided"}, 400

    file = request.files['file']

    # Validate file
    if file.filename == '' or not allowed_file(file.filename):
        return {"error": "Invalid file type"}, 400

    # Save the uploaded file
    filename = secure_filename(file.filename)
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(input_path)

    # Read and process the image
    with open(input_path, "rb") as f:
        input_image = f.read()
        output_image = remove(input_image)

    # Save the output image
    output_path = os.path.join(UPLOAD_FOLDER, f"output_{filename}")
    with open(output_path, "wb") as f:
        f.write(output_image)

    # Serve the processed image
    return send_file(output_path, mimetype='image/png')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
