import os
import PyPDF2
import docx
import pytesseract
from PIL import Image
import nltk
from nltk.tokenize import sent_tokenize
import spacy
import logging

# Download necessary NLTK resources
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
except Exception as e:
    logging.warning(f"Failed to download NLTK resources: {e}")

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except:
    logging.warning("Spacy model not found. Running spacy download")
    os.system("python -m spacy download en_core_web_sm")
    try:
        nlp = spacy.load("en_core_web_sm")
    except Exception as e:
        logging.error(f"Failed to load spaCy model: {e}")
        nlp = None

class DocumentProcessor:
    """Class for processing various document types and extracting text"""
    
    def extract_text(self, file_path, file_extension):
        """
        Extract text from document based on file type
        
        Args:
            file_path (str): Path to the document
            file_extension (str): Extension of the file
            
        Returns:
            str: Extracted text from the document
        """
        if file_extension in ['pdf']:
            return self._extract_from_pdf(file_path)
        elif file_extension in ['docx']:
            return self._extract_from_docx(file_path)
        elif file_extension in ['txt']:
            return self._extract_from_txt(file_path)
        elif file_extension in ['png', 'jpg', 'jpeg']:
            return self._extract_from_image(file_path)
        else:
            return ""
    
    def _extract_from_pdf(self, file_path):
        """Extract text from PDF files"""
        text = ""
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    text += page.extract_text() + "\n"
        except Exception as e:
            logging.error(f"Error extracting text from PDF: {e}")
        return text
    
    def _extract_from_docx(self, file_path):
        """Extract text from DOCX files"""
        text = ""
        try:
            doc = docx.Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"
        except Exception as e:
            logging.error(f"Error extracting text from DOCX: {e}")
        return text
    
    def _extract_from_txt(self, file_path):
        """Extract text from TXT files"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='latin-1') as file:
                    return file.read()
            except Exception as e:
                logging.error(f"Error extracting text from TXT: {e}")
                return ""
        except Exception as e:
            logging.error(f"Error extracting text from TXT: {e}")
            return ""
    
    def _extract_from_image(self, file_path):
        """Extract text from image files using OCR"""
        try:
            img = Image.open(file_path)
            text = pytesseract.image_to_string(img)
            return text
        except Exception as e:
            logging.error(f"Error extracting text from image: {e}")
            return ""
    
    def clean_text(self, text):
        """
        Clean and preprocess the extracted text
        
        Args:
            text (str): Extracted text from document
            
        Returns:
            str: Cleaned text
        """
        # Basic cleaning - remove excess whitespace
        text = " ".join(text.split())
        
        # More advanced cleaning could be implemented here
        return text
    
    def extract_sentences(self, text):
        """Extract sentences from text"""
        return sent_tokenize(text)
    
    def extract_entities(self, text):
        """Extract named entities from text using spaCy"""
        if not nlp:
            return []
        
        entities = []
        try:
            doc = nlp(text[:100000])  # Limit text length to avoid memory issues
            for ent in doc.ents:
                entities.append({
                    "text": ent.text,
                    "label": ent.label_,
                    "start": ent.start_char,
                    "end": ent.end_char
                })
        except Exception as e:
            logging.error(f"Error extracting entities: {e}")
        
        return entities
