"""Extracteur pour les fichiers HTML."""

from pathlib import Path
from bs4 import BeautifulSoup
from src.extractors.base_extractor import BaseExtractor
from src.models.document import Document


class HtmlExtractor(BaseExtractor):
    """Extracteur pour les fichiers HTML (.html, .htm)."""
    
    def extract(self, file_path: str) -> Document:
        """
        Extrait le contenu textuel d'un fichier HTML.
        
        Args:
            file_path: Chemin vers le fichier HTML
            
        Returns:
            Document: Objet Document contenant le contenu extrait
            
        Raises:
            FileNotFoundError: Si le fichier n'existe pas
            Exception: Si le HTML ne peut pas être lu
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"Le fichier {file_path} n'existe pas.")
        
        metadata = {}
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                html_content = f.read()
            
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Extraction du titre
            title_tag = soup.find('title')
            title = title_tag.get_text(strip=True) if title_tag else None
            
            # Extraction des métadonnées meta
            meta_tags = soup.find_all('meta')
            for meta in meta_tags:
                name = meta.get('name') or meta.get('property')
                content = meta.get('content')
                if name and content:
                    metadata[name] = content
            
            # Suppression des scripts et styles
            for script in soup(['script', 'style', 'nav', 'header', 'footer']):
                script.decompose()
            
            # Extraction du texte principal
            content = soup.get_text(separator=' ', strip=True)
            
            # Nettoyage des espaces multiples
            content = ' '.join(content.split())
        
        except Exception as e:
            raise Exception(f"Erreur lors de la lecture du HTML: {str(e)}")
        
        return Document(
            content=content,
            file_path=str(path.absolute()),
            file_type=self.get_file_type(file_path),
            title=title,
            metadata=metadata
        )

