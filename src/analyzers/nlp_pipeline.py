"""Pipeline NLP orchestrant tous les analyseurs."""

from typing import List
from src.analyzers.base_analyzer import BaseAnalyzer
from src.analyzers.entity_analyzer import EntityAnalyzer
from src.analyzers.sentiment_analyzer import SentimentAnalyzer
from src.analyzers.category_analyzer import CategoryAnalyzer
from src.analyzers.relation_analyzer import RelationAnalyzer
from src.models.document import Document
from src.models.analysis import Analysis


class NLPPipeline:
    """Pipeline pour orchestrer tous les analyseurs NLP."""
    
    def __init__(self, model_name: str = 'fr_core_news_sm'):
        """
        Initialise le pipeline NLP avec tous les analyseurs.
        
        Args:
            model_name: Nom du modèle spaCy à utiliser
        """
        self.analyzers: List[BaseAnalyzer] = [
            EntityAnalyzer(model_name),
            SentimentAnalyzer(),
            CategoryAnalyzer(),
            RelationAnalyzer(model_name)
        ]
    
    def analyze(self, document: Document) -> Analysis:
        """
        Analyse un document avec tous les analyseurs configurés.
        
        Args:
            document: Document à analyser
            
        Returns:
            Analysis: Objet Analysis contenant tous les résultats
        """
        analysis = Analysis()
        
        # Appliquer chaque analyseur dans l'ordre
        for analyzer in self.analyzers:
            try:
                analysis = analyzer.analyze(document, analysis)
            except Exception as e:
                print(f"Erreur lors de l'analyse avec {analyzer.__class__.__name__}: {str(e)}")
                # Continuer avec les autres analyseurs même en cas d'erreur
        
        return analysis
    
    def add_analyzer(self, analyzer: BaseAnalyzer):
        """
        Ajoute un analyseur personnalisé au pipeline.
        
        Args:
            analyzer: Instance d'un analyseur à ajouter
        """
        self.analyzers.append(analyzer)
    
    def remove_analyzer(self, analyzer_class: type):
        """
        Retire un analyseur du pipeline.
        
        Args:
            analyzer_class: Classe de l'analyseur à retirer
        """
        self.analyzers = [a for a in self.analyzers if not isinstance(a, analyzer_class)]

