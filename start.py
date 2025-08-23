#!/usr/bin/env python3
"""
Script de démarrage pour l'Assistant d'Analyse Radiologique
"""

import os
import subprocess
import sys
from pathlib import Path


def check_python_version():
    """Vérification de la version Python"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 ou supérieur est requis.")
        print(f"Version actuelle: {sys.version}")
        return False
    return True

def install_requirements():
    """Installation des dépendances"""
    requirements_file = Path(__file__).parent / "requirements.txt"
    
    if not requirements_file.exists():
        print("❌ Fichier requirements.txt introuvable")
        return False
    
    print("📦 Installation des dépendances...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
        ])
        print("✅ Dépendances installées avec succès")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'installation des dépendances: {e}")
        return False

def check_env_file():
    """Vérification du fichier .env"""
    env_file = Path(__file__).parent / ".env"
    
    if not env_file.exists():
        print("⚠️  Fichier .env introuvable")
        print("Création d'un fichier .env par défaut...")
        
        with open(env_file, 'w') as f:
            f.write("# Configuration\n")
            f.write("GOOGLE_API_KEY=your_gemini_api_key_here\n")
        
        print("📝 Fichier .env créé.")
        print("🔑 Veuillez ajouter votre clé API Gemini dans le fichier .env")
        print("   Obtenez votre clé sur: https://makersuite.google.com/app/apikey")
        return False
    
    # Vérifier si la clé API est configurée
    with open(env_file, 'r') as f:
        content = f.read()
        if "your_gemini_api_key_here" in content:
            print("⚠️  Clé API Gemini non configurée dans .env")
            print("🔑 Veuillez remplacer 'your_gemini_api_key_here' par votre vraie clé API")
            return False
    
    return True

def main():
    """Fonction principale de démarrage"""
    print("🏥 Assistant d'Analyse Radiologique - Démarrage")
    print("=" * 50)
    
    # Vérifications préalables
    if not check_python_version():
        return
    
    # Installation des dépendances
    if not install_requirements():
        print("❌ Impossible d'installer les dépendances")
        return
    
    # Vérification de la configuration
    env_configured = check_env_file()
    
    print("\n" + "=" * 50)
    print("🚀 Lancement de l'application...")
    
    if not env_configured:
        print("⚠️  Application lancée SANS clé API configurée")
        print("   L'analyse ne fonctionnera pas tant que la clé n'est pas ajoutée")
    
    # Lancement de l'application Gradio
    try:
        # Import des modules après installation des dépendances
        from app import create_demo
        
        demo = create_demo()
        demo.launch(
            server_name="127.0.0.1",
            server_port=7860,
            share=False,
            debug=False,
            show_error=True
        )
        
    except ImportError as e:
        print(f"❌ Erreur d'importation: {e}")
        print("Assurez-vous que toutes les dépendances sont installées")
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")

if __name__ == "__main__":
    main()
