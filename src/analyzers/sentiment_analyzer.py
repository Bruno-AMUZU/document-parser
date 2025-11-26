"""Analyseur pour l'analyse de sentiment."""

from textblob import TextBlob
from src.analyzers.base_analyzer import BaseAnalyzer
from src.models.document import Document
from src.models.analysis import Analysis


class SentimentAnalyzer(BaseAnalyzer):
    """Analyseur pour déterminer le sentiment d'un document."""
    
    def analyze(self, document: Document, analysis: Analysis) -> Analysis:
        """
        Analyse le sentiment du document.
        
        Args:
            document: Document à analyser
            analysis: Objet Analysis à mettre à jour
            
        Returns:
            Analysis: Objet Analysis mis à jour avec le sentiment
        """
        if not document.content:
            return analysis
        
        try:
            blob = TextBlob(document.content)
            polarity = blob.sentiment.polarity  # -1 (négatif) à 1 (positif)
            subjectivity = blob.sentiment.subjectivity  # 0 (objectif) à 1 (subjectif)
            
            # Détermination du label de sentiment
            if polarity > 0.1:
                sentiment_label = 'positif'
            elif polarity < -0.1:
                sentiment_label = 'négatif'
            else:
                sentiment_label = 'neutre'
            
            analysis.sentiment = {
                'polarity': float(polarity),
                'subjectivity': float(subjectivity),
                'label': sentiment_label
            }
        except Exception as e:
            # En cas d'erreur, on continue sans sentiment
            print(f"Erreur lors de l'analyse de sentiment: {str(e)}")
        
        return analysis

