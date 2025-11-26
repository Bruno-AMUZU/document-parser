"""Classe abstraite de base pour tous les exportateurs."""

from abc import ABC, abstractmethod
from src.models.document import Document
from src.models.analysis import Analysis


class BaseExporter(ABC):
    """Interface abstraite pour tous les exportateurs."""
    
    @abstractmethod
    def export(self, document: Document, analysis: Analysis, output_path: str) -> str:
        """
        Exporte un document et son analyse dans un fichier.
        
        Args:
            document: Document à exporter
            analysis: Analyse à exporter
            output_path: Chemin du fichier de sortie
            
        Returns:
            str: Chemin du fichier créé
        """
        pass

