"""Modèle de données pour représenter un document."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Document:
    """Représente un document avec ses métadonnées et son contenu."""
    
    content: str
    file_path: str
    file_type: str
    title: Optional[str] = None
    author: Optional[str] = None
    date: Optional[datetime] = None
    metadata: Optional[dict] = None
    
    def __post_init__(self):
        """Initialise les valeurs par défaut."""
        if self.metadata is None:
            self.metadata = {}
        if self.title is None:
            self.title = self.file_path.split('/')[-1].split('\\')[-1]

