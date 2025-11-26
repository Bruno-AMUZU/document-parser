"""Analyseur pour l'extraction de relations entre entités."""

import spacy
from typing import List, Set, Tuple
from src.analyzers.base_analyzer import BaseAnalyzer
from src.models.document import Document
from src.models.analysis import Analysis, Relation


class RelationAnalyzer(BaseAnalyzer):
    """Analyseur pour extraire les relations entre entités."""
    
    def __init__(self, model_name: str = 'fr_core_news_sm'):
        """
        Initialise l'analyseur de relations.
        
        Args:
            model_name: Nom du modèle spaCy à utiliser
        """
        try:
            self.nlp = spacy.load(model_name)
        except OSError:
            try:
                self.nlp = spacy.load('en_core_web_sm')
            except OSError:
                self.nlp = spacy.load('xx_ent_wiki_sm')
    
    def analyze(self, document: Document, analysis: Analysis) -> Analysis:
        """
        Extrait les relations entre entités du document.
        
        Args:
            document: Document à analyser
            analysis: Objet Analysis à mettre à jour
            
        Returns:
            Analysis: Objet Analysis mis à jour avec les relations
        """
        if not document.content or not analysis.entities:
            return analysis
        
        doc = self.nlp(document.content)
        
        # Créer un set des entités pour recherche rapide
        entity_texts = {ent.text.lower() for ent in analysis.entities}
        
        # Extraire les relations basées sur les dépendances syntaxiques
        relations = self._extract_relations_from_doc(doc, entity_texts)
        
        # Ajouter les relations à l'analyse
        for relation in relations:
            analysis.relations.append(relation)
        
        return analysis
    
    def _extract_relations_from_doc(self, doc, entity_texts: Set[str]) -> List[Relation]:
        """
        Extrait les relations depuis le document parsé par spaCy.
        
        Args:
            doc: Document spaCy parsé
            entity_texts: Set des textes d'entités (en minuscules)
            
        Returns:
            List[Relation]: Liste des relations extraites
        """
        relations = []
        seen_relations: Set[Tuple[str, str, str]] = set()
        
        for sent in doc.sents:
            # Trouver les entités dans cette phrase
            sent_entities = [ent for ent in sent.ents if ent.text.lower() in entity_texts]
            
            # Chercher des relations entre entités proches
            for i, ent1 in enumerate(sent_entities):
                for ent2 in sent_entities[i+1:]:
                    # Vérifier si les entités sont proches (dans la même phrase)
                    if abs(ent1.start - ent2.start) < 50:  # Distance maximale de 50 caractères
                        # Déterminer le type de relation basé sur les dépendances
                        relation_type = self._determine_relation_type(ent1, ent2, sent)
                        
                        if relation_type:
                            # Créer une clé unique pour éviter les doublons
                            key = tuple(sorted([ent1.text.lower(), ent2.text.lower()]) + [relation_type])
                            if key not in seen_relations:
                                seen_relations.add(key)
                                relations.append(Relation(
                                    entity1=ent1.text,
                                    entity2=ent2.text,
                                    relation_type=relation_type,
                                    confidence=None
                                ))
        
        return relations
    
    def _determine_relation_type(self, ent1, ent2, sent) -> str:
        """
        Détermine le type de relation entre deux entités.
        
        Args:
            ent1: Première entité
            ent2: Deuxième entité
            sent: Phrase contenant les entités
            
        Returns:
            str: Type de relation ou None
        """
        # Recherche de verbes ou prépositions entre les entités
        start = min(ent1.end, ent2.end)
        end = max(ent1.start, ent2.start)
        
        between_tokens = [token for token in sent if start <= token.i < end]
        
        # Types de relations basiques
        for token in between_tokens:
            if token.pos_ == 'VERB':
                return 'action'
            elif token.text.lower() in ['de', 'du', 'des', 'à', 'au', 'aux', 'pour', 'avec']:
                return 'association'
            elif token.text.lower() in ['et', 'ou']:
                return 'conjonction'
        
        # Relation par défaut
        return 'relation'

