import re
import pandas as pd
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

class NLPEngine:
    def __init__(self):
        factory = StemmerFactory()
        self.stemmer = factory.create_stemmer()
        # Words often found in clickbait/hoax titles
        self.provocative_words = [
            "viral", "heboh", "gemparkan", "menjerit", "awas", 
            "terbongkar", "ternyata", "mengejutkan", "ngeri", 
            "sadis", "azab", "subhanallah", "konspirasi", "diam-diam"
        ]

    def clean_text(self, text):
        """Basic text cleaning."""
        # Check for empty input
        if not text or not isinstance(text, str):
            return ""
        return text.strip()

    def count_caps_ratio(self, text):
        """Calculates percentage of uppercase letters."""
        if not text: return 0.0
        # Count only letters, ignore spaces/numbers for ratio
        letters = [c for c in text if c.isalpha()]
        if not letters: return 0.0
        
        caps_count = sum(1 for c in letters if c.isupper())
        return (caps_count / len(letters)) * 100

    def count_provocative_score(self, text):
        """Calculates a score based on provocative words and punctuation."""
        if not text: return 0.0
        
        score = 0
        lower_text = text.lower()
        
        # Check for provocative words
        for word in self.provocative_words:
            if word in lower_text:
                score += 20 # Add significant score for trigger words
                
        # Check for excessive punctuation
        exclamation_count = text.count('!')
        score += (exclamation_count * 10)
        
        # Check for excessive question marks
        question_count = text.count('?')
        if question_count > 1:
            score += 10
            
        return min(score, 100) # Cap at 100

    def analyze(self, text):
        """Main analysis function returning crisp values."""
        clean = self.clean_text(text)
        
        return {
            "caps_ratio": self.count_caps_ratio(clean),
            "provocative_score": self.count_provocative_score(clean),
            "original_text": text
        }

if __name__ == "__main__":
    # Test block
    nlp = NLPEngine()
    test_text = "VIRAL!! Babi Ngepet Ditemukan?"
    print(nlp.analyze(test_text))
