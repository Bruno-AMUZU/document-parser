"""Analyseur pour la catégorisation de documents."""

import re
from collections import Counter
from src.analyzers.base_analyzer import BaseAnalyzer
from src.models.document import Document
from src.models.analysis import Analysis


class CategoryAnalyzer(BaseAnalyzer):
    """Analyseur pour catégoriser un document par thème."""
    
    # Mots-clés pour différentes catégories
    CATEGORY_KEYWORDS = {
        'technologie': ['informatique', 'ordinateur', 'logiciel', 'programmation', 'code', 'développement', 
                       'application', 'système', 'réseau', 'internet', 'données', 'algorithme'],
        'santé': ['médecin', 'maladie', 'santé', 'médical', 'traitement', 'patient', 'hôpital', 
                 'médicament', 'symptôme', 'diagnostic', 'thérapie'],
        'économie': ['économie', 'finance', 'argent', 'investissement', 'bourse', 'marché', 
                    'entreprise', 'commerce', 'prix', 'coût', 'revenu', 'profit'],
        'éducation': ['éducation', 'école', 'université', 'apprentissage', 'enseignement', 
                     'étudiant', 'professeur', 'cours', 'formation', 'pédagogie'],
        'sport': ['sport', 'match', 'équipe', 'joueur', 'championnat', 'compétition', 
                 'entraînement', 'athlète', 'victoire', 'défaite'],
        'politique': ['politique', 'gouvernement', 'élection', 'député', 'ministre', 'loi', 
                     'parlement', 'parti', 'vote', 'démocratie'],
        'science': ['science', 'recherche', 'expérience', 'découverte', 'théorie', 'hypothèse', 
                   'laboratoire', 'scientifique', 'étude', 'publication']
    }
    
    def analyze(self, document: Document, analysis: Analysis) -> Analysis:
        """
        Catégorise le document en fonction de son contenu.
        
        Args:
            document: Document à analyser
            analysis: Objet Analysis à mettre à jour
            
        Returns:
            Analysis: Objet Analysis mis à jour avec les catégories
        """
        if not document.content:
            return analysis
        
        content_lower = document.content.lower()
        category_scores = {}
        
        # Calcul du score pour chaque catégorie
        for category, keywords in self.CATEGORY_KEYWORDS.items():
            score = 0
            for keyword in keywords:
                # Compter les occurrences du mot-clé
                count = len(re.findall(r'\b' + re.escape(keyword) + r'\b', content_lower))
                score += count
            
            if score > 0:
                category_scores[category] = score
        
        # Sélection des catégories avec un score significatif
        if category_scores:
            max_score = max(category_scores.values())
            threshold = max_score * 0.3  # Au moins 30% du score maximum
            
            analysis.categories = [
                category for category, score in category_scores.items() 
                if score >= threshold
            ]
            # Trier par score décroissant
            analysis.categories.sort(key=lambda c: category_scores[c], reverse=True)
        else:
            analysis.categories = ['non-catégorisé']
        
        return analysis

