import torch
import transformers
from typing import List, Dict, Union
import logging
from tqdm import tqdm

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    def __init__(self):
        self.tokenizer = transformers.AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
        self.model = transformers.AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.model.eval()
        
        self.sentiment_mapping = {
            1: "Very Negative",
            2: "Negative",
            3: "Neutral",
            4: "Positive",
            5: "Very Positive"
        }
        
        # Travel-specific aspects
        self.aspects = [
            "hotel", "accommodation", "room",
            "food", "restaurant", "dining",
            "transport", "travel", "flight",
            "service", "staff", "customer service",
            "location", "place", "destination",
            "price", "cost", "value",
            "cleanliness", "hygiene", "maintenance",
            "activities", "entertainment", "attractions"
        ]
    
    def analyze(self, text: str, include_aspects: bool = False) -> Dict[str, Union[str, float, Dict]]:
        """
        Analyze sentiment of a single text.
        
        Args:
            text: The text to analyze
            include_aspects: Whether to include aspect-based sentiment analysis
            
        Returns:
            Dictionary containing sentiment analysis results
        """
        try:
            inputs = self.tokenizer(text, 
                                  return_tensors="pt", 
                                  truncation=True, 
                                  max_length=512)
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = self.model(**inputs)
                predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
            
            score = torch.argmax(predictions).item() + 1
            confidence = predictions[0][score-1].item()
            
            result = {
                "text": text,
                "sentiment": self.sentiment_mapping[score],
                "score": score,
                "confidence": confidence
            }
            
            # Add aspect-based analysis if requested
            if include_aspects:
                result["aspects"] = self._analyze_aspects(text)
            
            return result
            
        except Exception as e:
            logger.error(f"Error in sentiment analysis: {str(e)}")
            return {"error": str(e)}
    
    def analyze_batch(self, texts: List[str], 
                     batch_size: int = 16, 
                     include_aspects: bool = False,
                     show_progress: bool = True) -> List[Dict[str, Union[str, float, Dict]]]:
        """
        Analyze sentiment of multiple texts in batches.
        
        Args:
            texts: List of texts to analyze
            batch_size: Size of batches for processing
            include_aspects: Whether to include aspect-based sentiment analysis
            show_progress: Whether to show progress bar
            
        Returns:
            List of dictionaries containing sentiment analysis results
        """
        results = []
        iterator = tqdm(range(0, len(texts), batch_size)) if show_progress else range(0, len(texts), batch_size)
        
        try:
            for i in iterator:
                batch = texts[i:i + batch_size]
                inputs = self.tokenizer(batch, 
                                      return_tensors="pt", 
                                      truncation=True, 
                                      max_length=512, 
                                      padding=True)
                inputs = {k: v.to(self.device) for k, v in inputs.items()}
                
                with torch.no_grad():
                    outputs = self.model(**inputs)
                    predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
                
                scores = torch.argmax(predictions, dim=1) + 1
                confidences = torch.gather(predictions, 1, (scores - 1).unsqueeze(1)).squeeze()
                
                for text, score, confidence in zip(batch, scores, confidences):
                    result = {
                        "text": text,
                        "sentiment": self.sentiment_mapping[score.item()],
                        "score": score.item(),
                        "confidence": confidence.item()
                    }
                    
                    if include_aspects:
                        result["aspects"] = self._analyze_aspects(text)
                    
                    results.append(result)
            
            return results
            
        except Exception as e:
            logger.error(f"Error in batch sentiment analysis: {str(e)}")
            return [{"error": str(e)}]
    
    def _analyze_aspects(self, text: str) -> Dict[str, Dict[str, Union[str, float]]]:
        """
        Analyze sentiment for specific aspects in the text.
        
        Args:
            text: The text to analyze
            
        Returns:
            Dictionary containing aspect-based sentiment analysis
        """
        aspects_found = {}
        text_lower = text.lower()
        
        # Group related aspects
        aspect_groups = {
            "accommodation": ["hotel", "accommodation", "room"],
            "dining": ["food", "restaurant", "dining"],
            "transportation": ["transport", "travel", "flight"],
            "service": ["service", "staff", "customer service"],
            "location": ["location", "place", "destination"],
            "value": ["price", "cost", "value"],
            "cleanliness": ["cleanliness", "hygiene", "maintenance"],
            "activities": ["activities", "entertainment", "attractions"]
        }
        
        for group, terms in aspect_groups.items():
            # Find sentences containing aspect terms
            sentences = [s for s in text.split('.') if any(term in s.lower() for term in terms)]
            
            if sentences:
                # Analyze sentiment for each relevant sentence
                sentiments = []
                for sentence in sentences:
                    result = self.analyze(sentence)
                    if "error" not in result:
                        sentiments.append(result["score"])
                
                if sentiments:
                    avg_sentiment = sum(sentiments) / len(sentiments)
                    aspects_found[group] = {
                        "sentiment": self.sentiment_mapping[round(avg_sentiment)],
                        "score": avg_sentiment
                    }
        
        return aspects_found

class LanguageDetector:
    def __init__(self):
        self.model = transformers.AutoModelForSequenceClassification.from_pretrained('papluca/xlm-roberta-base-language-detection')
        self.tokenizer = transformers.AutoTokenizer.from_pretrained('papluca/xlm-roberta-base-language-detection')
        self.model.eval()
        
        self.id2label = {
            0: "Arabic",
            1: "Chinese",
            2: "English",
            3: "French",
            4: "German",
            5: "Hindi",
            6: "Italian",
            7: "Japanese",
            8: "Korean",
            9: "Spanish"
        }
    
    def detect(self, text: str) -> Dict[str, Union[str, float]]:
        try:
            inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
            
            with torch.no_grad():
                outputs = self.model(**inputs)
                predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
            
            score = torch.argmax(predictions).item()
            confidence = predictions[0][score].item()
            
            return {
                "language": self.id2label[score],
                "confidence": confidence
            }
        except Exception as e:
            logger.error(f"Error in language detection: {str(e)}")
            return {"error": str(e)} 