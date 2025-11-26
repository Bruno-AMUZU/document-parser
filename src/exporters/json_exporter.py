"""Exportateur pour le format JSON."""

import json
from pathlib import Path
from datetime import datetime
from src.exporters.base_exporter import BaseExporter
from src.models.document import Document
from src.models.analysis import Analysis


class JsonExporter(BaseExporter):
    """Exportateur pour exporter les résultats en JSON."""
    
    def export(self, document: Document, analysis: Analysis, output_path: str) -> str:
        """
        Exporte un document et son analyse en JSON.
        
        Args:
            document: Document à exporter
            analysis: Analyse à exporter
            output_path: Chemin du fichier de sortie JSON
            
        Returns:
            str: Chemin du fichier créé
        """
        output_path = Path(output_path)
        
        # Créer le répertoire parent si nécessaire
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Préparer les données à exporter
        export_data = {
            'document': {
                'file_path': document.file_path,
                'file_type': document.file_type,
                'title': document.title,
                'author': document.author,
                'date': document.date.isoformat() if document.date else None,
                'metadata': document.metadata,
                'content_length': len(document.content),
                'content_preview': document.content[:500] if document.content else None  # Aperçu des 500 premiers caractères
            },
            'analysis': analysis.to_dict(),
            'export_date': datetime.now().isoformat()
        }
        
        # Écrire le fichier JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        return str(output_path.absolute())

