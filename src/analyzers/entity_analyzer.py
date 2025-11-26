"""Analyseur pour l'extraction d'entités nommées."""

import spacy
from typing import Optional
from src.analyzers.base_analyzer import BaseAnalyzer
from src.models.document import Document
from src.models.analysis import Analysis, Entity


class EntityAnalyzer(BaseAnalyzer):
    """Analyseur pour extraire les entités nommées d'un document."""
    
    def __init__(self, model_name: str = 'fr_core_news_sm'):
        """
        Initialise l'analyseur d'entités.
        
        Args:
            model_name: Nom du modèle spaCy à utiliser (par défaut: fr_core_news_sm)
        """
        try:
            self.nlp = spacy.load(model_name)
        except OSError:
            # Fallback sur le modèle anglais si le modèle français n'est pas disponible
            try:
                self.nlp = spacy.load('en_core_web_sm')
            except OSError:
                # Si aucun modèle n'est disponible, on utilisera un modèle minimal
                self.nlp = spacy.load('xx_ent_wiki_sm')
    
    def analyze(self, document: Document, analysis: Analysis) -> Analysis:
        """
        Extrait les entités nommées du document.
        
        Args:
            document: Document à analyser
            analysis: Objet Analysis à mettre à jour
            
        Returns:
            Analysis: Objet Analysis mis à jour avec les entités extraites
        """
        if not document.content:
            return analysis
        
        doc = self.nlp(document.content)
        
        # Extraction des entités nommées
        for ent in doc.ents:
            entity = Entity(
                text=ent.text,
                label=ent.label_,
                start=ent.start_char,
                end=ent.end_char,
                confidence=None  # spaCy ne fournit pas de score de confiance par défaut
            )
            analysis.entities.append(entity)
        
        # Détection de la langue
        if hasattr(doc, 'lang_'):
            analysis.language = doc.lang_
        
        # Comptage des mots et phrases
        analysis.word_count = len([token for token in doc if not token.is_punct and not token.is_space])
        analysis.sentence_count = len(list(doc.sents))
        
        return analysis

