"""Classe abstraite de base pour tous les extracteurs."""

from abc import ABC, abstractmethod
from src.models.document import Document


class BaseExtractor(ABC):
    """Interface abstraite pour tous les extracteurs de documents."""
    
    @abstractmethod
    def extract(self, file_path: str) -> Document:
        """
        Extrait le contenu d'un fichier et retourne un objet Document.
        
        Args:
            file_path: Chemin vers le fichier à extraire
            
        Returns:
            Document: Objet Document contenant le contenu et les métadonnées
            
        Raises:
            FileNotFoundError: Si le fichier n'existe pas
            ValueError: Si le fichier ne peut pas être traité
        """
        pass
    
    @staticmethod
    def get_file_type(file_path: str) -> str:
        """
        Détermine le type de fichier à partir de son extension.
        
        Args:
            file_path: Chemin vers le fichier
            
        Returns:
            str: Type de fichier (extension sans le point)
        """
        return file_path.split('.')[-1].lower() if '.' in file_path else ''

