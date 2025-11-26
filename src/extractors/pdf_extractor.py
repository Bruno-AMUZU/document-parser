"""Extracteur pour les fichiers PDF."""

import pdfplumber
from pathlib import Path
from src.extractors.base_extractor import BaseExtractor
from src.models.document import Document


class PdfExtractor(BaseExtractor):
    """Extracteur pour les fichiers PDF (.pdf)."""
    
    def extract(self, file_path: str) -> Document:
        """
        Extrait le contenu d'un fichier PDF.
        
        Args:
            file_path: Chemin vers le fichier PDF
            
        Returns:
            Document: Objet Document contenant le contenu extrait
            
        Raises:
            FileNotFoundError: Si le fichier n'existe pas
            Exception: Si le PDF ne peut pas être lu
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"Le fichier {file_path} n'existe pas.")
        
        content_parts = []
        metadata = {}
        
        try:
            with pdfplumber.open(file_path) as pdf:
                # Extraction du texte de toutes les pages
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        content_parts.append(text)
                
                # Extraction des métadonnées
                if pdf.metadata:
                    metadata = {
                        'title': pdf.metadata.get('Title'),
                        'author': pdf.metadata.get('Author'),
                        'subject': pdf.metadata.get('Subject'),
                        'creator': pdf.metadata.get('Creator'),
                        'producer': pdf.metadata.get('Producer'),
                        'creation_date': str(pdf.metadata.get('CreationDate', '')),
                        'modification_date': str(pdf.metadata.get('ModDate', '')),
                        'page_count': len(pdf.pages)
                    }
        except Exception as e:
            raise Exception(f"Erreur lors de la lecture du PDF: {str(e)}")
        
        content = '\n\n'.join(content_parts)
        
        return Document(
            content=content,
            file_path=str(path.absolute()),
            file_type=self.get_file_type(file_path),
            title=metadata.get('title'),
            author=metadata.get('author'),
            metadata=metadata
        )

