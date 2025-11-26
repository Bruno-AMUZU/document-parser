"""Modèle de données pour représenter les résultats d'analyse NLP."""

from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class Entity:
    """Représente une entité nommée extraite du texte."""
    
    text: str
    label: str
    start: int
    end: int
    confidence: Optional[float] = None


@dataclass
class Relation:
    """Représente une relation entre deux entités."""
    
    entity1: str
    entity2: str
    relation_type: str
    confidence: Optional[float] = None


@dataclass
class Analysis:
    """Stocke tous les résultats d'analyse NLP d'un document."""
    
    entities: List[Entity] = field(default_factory=list)
    sentiment: Optional[Dict[str, float]] = None
    categories: List[str] = field(default_factory=list)
    relations: List[Relation] = field(default_factory=list)
    language: Optional[str] = None
    word_count: Optional[int] = None
    sentence_count: Optional[int] = None
    
    def to_dict(self) -> Dict:
        """Convertit l'analyse en dictionnaire pour l'export."""
        return {
            'entities': [
                {
                    'text': e.text,
                    'label': e.label,
                    'start': e.start,
                    'end': e.end,
                    'confidence': e.confidence
                }
                for e in self.entities
            ],
            'sentiment': self.sentiment,
            'categories': self.categories,
            'relations': [
                {
                    'entity1': r.entity1,
                    'entity2': r.entity2,
                    'relation_type': r.relation_type,
                    'confidence': r.confidence
                }
                for r in self.relations
            ],
            'language': self.language,
            'word_count': self.word_count,
            'sentence_count': self.sentence_count
        }

