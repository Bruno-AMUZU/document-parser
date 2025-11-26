"""Factory pour sélectionner automatiquement le bon extracteur."""

from pathlib import Path
from src.extractors.txt_extractor import TxtExtractor
from src.extractors.pdf_extractor import PdfExtractor
from src.extractors.epub_extractor import EpubExtractor
from src.extractors.html_extractor import HtmlExtractor
from src.extractors.docx_extractor import DocxExtractor
from src.extractors.base_extractor import BaseExtractor


class ExtractorFactory:
    """Factory pour créer le bon extracteur selon le type de fichier."""
    
    # Mapping des extensions vers les classes d'extracteurs
    _extractors = {
        'txt': TxtExtractor,
        'pdf': PdfExtractor,
        'epub': EpubExtractor,
        'html': HtmlExtractor,
        'htm': HtmlExtractor,
        'docx': DocxExtractor
    }
    
    @classmethod
    def get_extractor(cls, file_path: str) -> BaseExtractor:
        """
        Retourne l'extracteur approprié pour le fichier donné.
        
        Args:
            file_path: Chemin vers le fichier
            
        Returns:
            BaseExtractor: Instance de l'extracteur approprié
            
        Raises:
            ValueError: Si le format de fichier n'est pas supporté
        """
        path = Path(file_path)
        extension = path.suffix.lower().lstrip('.')
        
        if extension not in cls._extractors:
            supported_formats = ', '.join(cls._extractors.keys())
            raise ValueError(
                f"Format de fichier '{extension}' non supporté. "
                f"Formats supportés: {supported_formats}"
            )
        
        extractor_class = cls._extractors[extension]
        return extractor_class()
    
    @classmethod
    def is_supported(cls, file_path: str) -> bool:
        """
        Vérifie si le format de fichier est supporté.
        
        Args:
            file_path: Chemin vers le fichier
            
        Returns:
            bool: True si le format est supporté, False sinon
        """
        path = Path(file_path)
        extension = path.suffix.lower().lstrip('.')
        return extension in cls._extractors
    
    @classmethod
    def get_supported_formats(cls) -> list:
        """
        Retourne la liste des formats supportés.
        
        Returns:
            list: Liste des extensions de fichiers supportées
        """
        return list(cls._extractors.keys())

