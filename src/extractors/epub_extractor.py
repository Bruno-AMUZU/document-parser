"""Extracteur pour les fichiers EPUB."""

import ebooklib
from ebooklib import epub
from pathlib import Path
from bs4 import BeautifulSoup
from src.extractors.base_extractor import BaseExtractor
from src.models.document import Document


class EpubExtractor(BaseExtractor):
    """Extracteur pour les fichiers EPUB (.epub)."""
    
    def extract(self, file_path: str) -> Document:
        """
        Extrait le contenu d'un fichier EPUB.
        
        Args:
            file_path: Chemin vers le fichier EPUB
            
        Returns:
            Document: Objet Document contenant le contenu extrait
            
        Raises:
            FileNotFoundError: Si le fichier n'existe pas
            Exception: Si l'EPUB ne peut pas être lu
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"Le fichier {file_path} n'existe pas.")
        
        content_parts = []
        metadata = {}
        
        try:
            book = epub.read_epub(file_path)
            
            # Extraction des métadonnées
            metadata = {
                'title': book.get_metadata('DC', 'title'),
                'author': book.get_metadata('DC', 'creator'),
                'language': book.get_metadata('DC', 'language'),
                'publisher': book.get_metadata('DC', 'publisher'),
                'date': book.get_metadata('DC', 'date'),
                'description': book.get_metadata('DC', 'description')
            }
            
            # Nettoyage des métadonnées (retirer les listes)
            for key, value in metadata.items():
                if value and isinstance(value, list) and len(value) > 0:
                    metadata[key] = value[0][0] if isinstance(value[0], tuple) else value[0]
            
            # Extraction du contenu de tous les chapitres
            for item in book.get_items():
                if item.get_type() == ebooklib.ITEM_DOCUMENT:
                    soup = BeautifulSoup(item.get_content(), 'html.parser')
                    text = soup.get_text(separator=' ', strip=True)
                    if text:
                        content_parts.append(text)
        
        except Exception as e:
            raise Exception(f"Erreur lors de la lecture de l'EPUB: {str(e)}")
        
        content = '\n\n'.join(content_parts)
        
        return Document(
            content=content,
            file_path=str(path.absolute()),
            file_type=self.get_file_type(file_path),
            title=metadata.get('title'),
            author=metadata.get('author'),
            metadata=metadata
        )

