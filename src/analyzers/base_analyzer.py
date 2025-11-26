"""Classe abstraite de base pour tous les analyseurs."""

from abc import ABC, abstractmethod
from src.models.document import Document
from src.models.analysis import Analysis


class BaseAnalyzer(ABC):
    """Interface abstraite pour tous les analyseurs NLP."""
    
    @abstractmethod
    def analyze(self, document: Document, analysis: Analysis) -> Analysis:
        """
        Analyse un document et met à jour l'objet Analysis.
        
        Args:
            document: Document à analyser
            analysis: Objet Analysis à mettre à jour
            
        Returns:
            Analysis: Objet Analysis mis à jour avec les résultats
        """
        pass

