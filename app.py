from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
import uuid
from werkzeug.utils import secure_filename
from src.document_processor import DocumentProcessor
from src.metadata_generator import MetadataGenerator

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx', 'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        # Generate unique filename
        original_filename = secure_filename(file.filename)
        file_extension = original_filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{str(uuid.uuid4())}.{file_extension}"
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        # Process document and generate metadata
        doc_processor = DocumentProcessor()
        metadata_generator = MetadataGenerator()
        
        extracted_text = doc_processor.extract_text(filepath, file_extension)
        metadata = metadata_generator.generate_metadata(extracted_text, original_filename)
        
        return jsonify({
            'success': True,
            'original_filename': original_filename,
            'metadata': metadata
        })
    
    return jsonify({'error': 'File type not allowed'}), 400

@app.route('/analyze', methods=['GET'])
def analyze():
    # For demonstration, this would show statistics on processed documents
    return render_template('analyze.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
