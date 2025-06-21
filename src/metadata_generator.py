import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from datetime import datetime
import logging
from collections import Counter
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import os

# Download necessary NLTK resources
try:
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt', quiet=True)
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

class MetadataGenerator:
    """Class for generating metadata from document text"""
    
    def __init__(self):
        try:
            self.stop_words = set(stopwords.words('english'))
        except:
            self.stop_words = set()
            logging.warning("Stopwords not available")
    
    def generate_metadata(self, text, filename):
        """
        Generate metadata from document text
        
        Args:
            text (str): Extracted text from document
            filename (str): Original filename of the document
            
        Returns:
            dict: Generated metadata
        """
        if not text or text.strip() == "":
            return self._generate_empty_metadata(filename)
        
        # Basic text statistics
        word_count = len(word_tokenize(text))
        
        # Extract keywords using TF-IDF
        keywords = self._extract_keywords(text)
        
        # Extract named entities
        entities = self._extract_entities(text)
        
        # Detect document language
        language = self._detect_language(text)
        
        # Try to extract title
        title = self._extract_title(text, filename)
        
        # Generate summary
        summary = self._generate_summary(text)
        
        # Calculate readability
        readability_score = self._calculate_readability(text)
        
        # Final metadata object
        metadata = {
            "title": title,
            "filename": filename,
            "file_size": len(text),
            "word_count": word_count,
            "processing_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "language": language,
            "keywords": keywords,
            "entities": entities,
            "summary": summary,
            "readability_score": readability_score
        }
        
        return metadata
    
    def _generate_empty_metadata(self, filename):
        """Generate metadata for empty document"""
        return {
            "title": filename,
            "filename": filename,
            "file_size": 0,
            "word_count": 0,
            "processing_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "language": "unknown",
            "keywords": [],
            "entities": {},
            "summary": "Empty document",
            "readability_score": 0
        }
    
    def _extract_keywords(self, text, max_keywords=10):
        """Extract keywords using TF-IDF"""
        try:
            # If text is too short, extract frequent words instead
            if len(text.split()) < 100:
                return self._extract_frequent_words(text, max_keywords)
            
            vectorizer = TfidfVectorizer(
                max_df=0.85,
                min_df=2,
                stop_words='english',
                use_idf=True,
                ngram_range=(1, 2)
            )
            
            # Ensure we have enough text
            documents = [text]
            if len(text.split()) > 200:
                # Create artificial documents by splitting text
                sentences = nltk.sent_tokenize(text)
                # Group sentences into chunks
                chunk_size = max(5, len(sentences) // 5)
                for i in range(0, len(sentences), chunk_size):
                    chunk = " ".join(sentences[i:i+chunk_size])
                    if chunk:
                        documents.append(chunk)
            
            tfidf_matrix = vectorizer.fit_transform(documents)
            feature_names = vectorizer.get_feature_names_out()
            
            # Get scores from the first document (the full text)
            tfidf_scores = zip(feature_names, tfidf_matrix[0].toarray()[0])
            sorted_keywords = sorted(tfidf_scores, key=lambda x: x[1], reverse=True)
            
            # Filter keywords to ensure they are meaningful
            keywords = []
            for keyword, score in sorted_keywords:
                if score > 0.01 and len(keyword) > 2:
                    keywords.append({
                        "text": keyword,
                        "score": float(score)
                    })
                if len(keywords) >= max_keywords:
                    break
            
            return keywords
        except Exception as e:
            logging.error(f"Error extracting keywords: {e}")
            return self._extract_frequent_words(text, max_keywords)
    
    def _extract_frequent_words(self, text, max_words=10):
        """Extract most frequent words"""
        try:
            # Tokenize and clean
            tokens = word_tokenize(text.lower())
            tokens = [word for word in tokens if word.isalpha() and word not in self.stop_words and len(word) > 2]
            
            # Count frequency
            freq_dist = Counter(tokens)
            
            # Get top words
            top_words = freq_dist.most_common(max_words)
            
            # Format as keywords
            keywords = []
            for word, count in top_words:
                # Normalize score between 0 and 1
                score = count / max(freq_dist.values())
                keywords.append({
                    "text": word,
                    "score": float(score)
                })
            
            return keywords
        except Exception as e:
            logging.error(f"Error extracting frequent words: {e}")
            return []
    
    def _extract_entities(self, text):
        """Extract named entities using spaCy"""
        entity_groups = {
            "PERSON": [],
            "ORG": [],
            "GPE": [],  # Countries, cities, states
            "DATE": [],
            "MISC": []
        }
        
        if not nlp:
            return entity_groups
        
        try:
            # Limit text length to avoid memory issues
            limited_text = text[:100000]
            doc = nlp(limited_text)
            
            for ent in doc.ents:
                # Map entity label to our groups
                if ent.label_ in ["PERSON"]:
                    entity_groups["PERSON"].append(ent.text)
                elif ent.label_ in ["ORG"]:
                    entity_groups["ORG"].append(ent.text)
                elif ent.label_ in ["GPE", "LOC"]:
                    entity_groups["GPE"].append(ent.text)
                elif ent.label_ in ["DATE", "TIME"]:
                    entity_groups["DATE"].append(ent.text)
                else:
                    entity_groups["MISC"].append(ent.text)
            
            # Remove duplicates and limit length
            for key in entity_groups:
                entity_groups[key] = list(set(entity_groups[key]))[:10]
        
        except Exception as e:
            logging.error(f"Error extracting entities: {e}")
        
        return entity_groups
    
    def _detect_language(self, text):
        """Detect document language - simplified version"""
        # For now, we'll assume English
        # In a production system, use a language detection library
        return "English"
    
    def _extract_title(self, text, filename):
        """Try to extract a title from the document"""
        # First try: Take the first line if it's reasonably short
        lines = text.split('\n')
        if lines and lines[0].strip() and len(lines[0].strip()) < 100 and len(lines[0].strip().split()) < 15:
            return lines[0].strip()
        
        # Second try: Look for patterns that might indicate titles
        title_patterns = [
            r'^#\s+(.+)$',  # Markdown title
            r'^Title:\s*(.+)$',  # Explicit title
            r'^Subject:\s*(.+)$'  # Document subject
        ]
        
        for pattern in title_patterns:
            match = re.search(pattern, text, re.MULTILINE | re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        # Fallback: Use filename without extension
        filename_parts = filename.rsplit('.', 1)
        if len(filename_parts) > 1:
            return filename_parts[0]
        return filename
    
    def _generate_summary(self, text, max_length=200):
        """Generate a brief summary of the document"""
        # Simple extractive summarization
        try:
            # Split into sentences
            sentences = nltk.sent_tokenize(text)
            
            if len(sentences) <= 2:
                # If very short document, return the text itself
                if len(text) <= max_length:
                    return text
                return text[:max_length] + "..."
            
            # Use first and last sentence as summary
            first_sentence = sentences[0]
            last_sentence = sentences[-1]
            
            # If they're too long, truncate
            if len(first_sentence) > max_length // 2:
                first_sentence = first_sentence[:max_length // 2] + "..."
            
            if len(last_sentence) > max_length // 2:
                last_sentence = last_sentence[:max_length // 2] + "..."
            
            return first_sentence + " [...] " + last_sentence
        
        except Exception as e:
            logging.error(f"Error generating summary: {e}")
            # Fallback to simple truncation
            if len(text) <= max_length:
                return text
            return text[:max_length] + "..."
    
    def _calculate_readability(self, text):
        """Calculate simple readability score based on sentence and word length"""
        try:
            sentences = nltk.sent_tokenize(text)
            words = nltk.word_tokenize(text)
            
            if not sentences or not words:
                return 0
            
            # Average sentence length
            avg_sentence_length = len(words) / len(sentences)
            
            # Average word length
            avg_word_length = sum(len(word) for word in words) / len(words)
            
            # Simple readability score (higher is more complex)
            # Scale between 0-100 for easier interpretation
            readability = (avg_sentence_length * 0.6 + avg_word_length * 5) * 5
            
            # Cap the score at 100
            return min(100, readability)
        
        except Exception as e:
            logging.error(f"Error calculating readability: {e}")
            return 0
