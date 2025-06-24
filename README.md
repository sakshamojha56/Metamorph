# Metagen: Automated Metadata Generation System

## Overview

Metagen is a comprehensive automated metadata generation system designed to enhance document discoverability, classification, and analysis. The system processes various document formats, extracts meaningful content, and generates structured metadata that can be used for better document management and insights.

## Key Features

- **Multi-format Support**: Process documents in PDF, DOCX, TXT, and image formats
- **Automatic Content Extraction**: Extract text using specialized parsers for each format
- **OCR Capabilities**: Convert text in images to machine-readable content
- **Semantic Analysis**: Identify meaningful sections and key information in documents
- **Named Entity Recognition**: Extract people, organizations, locations, and dates
- **Keyword Extraction**: Generate relevant keywords using TF-IDF analysis
- **Readability Assessment**: Calculate document complexity scores
- **Document Summarization**: Generate concise summaries of document content
- **Intuitive Web Interface**: Upload documents and view generated metadata
- **Analytics Dashboard**: View insights across processed documents

## Technical Architecture

Metamorph is built with a modern tech stack:

- **Backend**: Python/Flask RESTful API
- **Frontend**: HTML5, CSS3, JavaScript with Bootstrap 5
- **Text Processing**: NLTK, spaCy, scikit-learn
- **Document Parsing**: PyPDF2, python-docx, Pillow, pytesseract
- **Data Analysis**: pandas, NumPy
- **Visualization**: Chart.js

## Installation and Setup

### Prerequisites

- Python 3.8+
- Tesseract OCR (for image processing)
- Required Python packages (see requirements.txt)

### Steps

1. Clone the repository:
   ```
   git clone https://github.com/sakshamojha56/Metagen.git
   cd Metamorph
   ```

2. Create and activate a virtual environment (recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Install additional requirements for OCR:
   - For Ubuntu/Debian:
     ```
     sudo apt-get install tesseract-ocr
     ```
   - For macOS:
     ```
     brew install tesseract
     ```
   - For Windows: Download and install from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)

5. Download spaCy model:
   ```
   python -m spacy download en_core_web_sm
   ```

6. Run the application:
   ```
   python app.py
   ```

7. Access the web interface at http://localhost:5000

## Using the Jupyter Notebook

For data scientists and developers who want to use the core functionality in a notebook environment, we provide a comprehensive Jupyter Notebook that demonstrates:

1. Document loading and text extraction
2. Text preprocessing and cleaning
3. Feature extraction and metadata generation
4. Visualization of results
5. Examples of advanced usage

The notebook can be found at `notebooks/metadata_generation.ipynb`.

## Project Structure

```
Metagen/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
├── notebooks/              # Jupyter notebooks
│   └── metadata_generation.ipynb
├── src/                    # Source code
│   ├── document_processor.py  # Document text extraction
│   └── metadata_generator.py  # Metadata generation logic
├── static/                 # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── img/
├── templates/              # HTML templates
│   ├── index.html
│   └── analyze.html
└── uploads/                # Temporary document storage
```

## API Reference

Metamorph provides a simple RESTful API for programmatic access:

- `POST /upload`: Upload and process a document
  - Returns: JSON with generated metadata

- `GET /analyze`: Get analytics data across all processed documents
  - Returns: JSON with aggregate statistics

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- NLTK and spaCy for natural language processing
- PyPDF2 and python-docx for document parsing
- Flask for the web framework
- Bootstrap for the UI components
