"""Extracteur pour les fichiers texte."""

import chardet
from pathlib import Path
from src.extractors.base_extractor import BaseExtractor
from src.models.document import Document


class TxtExtractor(BaseExtractor):
    """Extracteur pour les fichiers texte (.txt)."""
    
    def extract(self, file_path: str) -> Document:
        """
        Extrait le contenu d'un fichier texte.
        
        Args:
            file_path: Chemin vers le fichier texte
            
        Returns:
            Document: Objet Document contenant le contenu extrait
            
        Raises:
            FileNotFoundError: Si le fichier n'existe pas
            UnicodeDecodeError: Si l'encodage ne peut pas être détecté
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"Le fichier {file_path} n'existe pas.")
        
        # Détection de l'encodage
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            encoding_result = chardet.detect(raw_data)
            encoding = encoding_result.get('encoding', 'utf-8')
        
        # Lecture du contenu avec l'encodage détecté
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
        except (UnicodeDecodeError, LookupError):
            # Fallback sur UTF-8 si la détection échoue
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
        
        return Document(
            content=content,
            file_path=str(path.absolute()),
            file_type=self.get_file_type(file_path),
            metadata={
                'encoding': encoding,
                'encoding_confidence': encoding_result.get('confidence', 0.0)
            }
        )

