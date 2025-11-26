#!/usr/bin/env python3
"""Point d'entrée principal du parseur de documents."""

import argparse
import sys
from pathlib import Path
from src.extractors.extractor_factory import ExtractorFactory
from src.analyzers.nlp_pipeline import NLPPipeline
from src.exporters.json_exporter import JsonExporter


def main():
    """Fonction principale du programme."""
    parser = argparse.ArgumentParser(
        description='Parseur de documents avec analyse NLP',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  python main.py document.pdf
  python main.py document.txt -o resultat.json
  python main.py document.pdf --no-export
        """
    )
    
    parser.add_argument(
        'file',
        type=str,
        help='Chemin vers le fichier à analyser'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        default=None,
        help='Chemin du fichier de sortie JSON (par défaut: nom_du_fichier_analyse.json)'
    )
    
    parser.add_argument(
        '--no-export',
        action='store_true',
        help='Ne pas exporter les résultats, les afficher uniquement'
    )
    
    parser.add_argument(
        '--model',
        type=str,
        default='fr_core_news_sm',
        help='Modèle spaCy à utiliser (par défaut: fr_core_news_sm)'
    )
    
    args = parser.parse_args()
    
    # Vérifier que le fichier existe
    file_path = Path(args.file)
    if not file_path.exists():
        print(f"Erreur: Le fichier '{args.file}' n'existe pas.", file=sys.stderr)
        sys.exit(1)
    
    # Vérifier que le format est supporté
    if not ExtractorFactory.is_supported(str(file_path)):
        supported = ', '.join(ExtractorFactory.get_supported_formats())
        print(f"Erreur: Format non supporté. Formats supportés: {supported}", file=sys.stderr)
        sys.exit(1)
    
    try:
        # 1. Extraction du contenu
        print(f"Extraction du contenu depuis {file_path.name}...")
        extractor = ExtractorFactory.get_extractor(str(file_path))
        document = extractor.extract(str(file_path))
        print(f"✓ Contenu extrait ({len(document.content)} caractères)")
        
        # 2. Analyse NLP
        print("Analyse NLP en cours...")
        pipeline = NLPPipeline(model_name=args.model)
        analysis = pipeline.analyze(document)
        print("✓ Analyse terminée")
        
        # 3. Affichage des résultats
        print("\n" + "="*60)
        print("RÉSULTATS DE L'ANALYSE")
        print("="*60)
        print(f"Document: {document.title}")
        if document.author:
            print(f"Auteur: {document.author}")
        print(f"Type: {document.file_type}")
        print(f"Langue détectée: {analysis.language or 'Non détectée'}")
        print(f"Nombre de mots: {analysis.word_count or 'N/A'}")
        print(f"Nombre de phrases: {analysis.sentence_count or 'N/A'}")
        
        if analysis.sentiment:
            print(f"\nSentiment: {analysis.sentiment.get('label', 'N/A')} "
                  f"(polarité: {analysis.sentiment.get('polarity', 0):.2f})")
        
        if analysis.categories:
            print(f"\nCatégories: {', '.join(analysis.categories)}")
        
        if analysis.entities:
            print(f"\nEntités trouvées: {len(analysis.entities)}")
            entity_types = {}
            for entity in analysis.entities[:10]:  # Afficher les 10 premières
                entity_types[entity.label] = entity_types.get(entity.label, 0) + 1
            for label, count in sorted(entity_types.items(), key=lambda x: x[1], reverse=True):
                print(f"  - {label}: {count}")
            if len(analysis.entities) > 10:
                print(f"  ... et {len(analysis.entities) - 10} autres")
        
        if analysis.relations:
            print(f"\nRelations trouvées: {len(analysis.relations)}")
            for relation in analysis.relations[:5]:  # Afficher les 5 premières
                print(f"  - {relation.entity1} --[{relation.relation_type}]--> {relation.entity2}")
            if len(analysis.relations) > 5:
                print(f"  ... et {len(analysis.relations) - 5} autres")
        
        print("="*60 + "\n")
        
        # 4. Export JSON
        if not args.no_export:
            if args.output:
                output_path = args.output
            else:
                output_path = file_path.with_suffix('.json')
            
            exporter = JsonExporter()
            exported_file = exporter.export(document, analysis, str(output_path))
            print(f"✓ Résultats exportés dans: {exported_file}")
        
    except Exception as e:
        print(f"Erreur: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

