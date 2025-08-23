import base64
import io
import os
from datetime import datetime
from typing import Optional, Tuple

import cv2
import google.generativeai as genai
import numpy as np
from PIL import Image


class RadiologyAnalyzer:
    """Analyseur d'images radiologiques utilisant Gemini 2.5 Pro"""
    
    def __init__(self, api_key: str):
        """
        Initialise l'analyseur avec la clé API Gemini
        
        Args:
            api_key: Clé API Google Gemini
        """
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
    def create_analysis_prompt(self, clinical_info: str, patient_name: str = "", 
                             birth_date: str = "", doctor_name: str = "") -> str:
        """
        Crée le prompt d'analyse structuré en français
        
        Args:
            clinical_info: Renseignements cliniques fournis par le médecin
            patient_name: Nom du patient (optionnel)
            birth_date: Date de naissance (optionnel) 
            doctor_name: Nom du médecin prescripteur (optionnel)
            
        Returns:
            Prompt structuré pour l'analyse radiologique
        """
        current_date = datetime.now().strftime("%d/%m/%Y")
        
        prompt = f"""
# RÔLE ET OBJECTIF

Tu es un assistant IA expert en imagerie médicale, agissant comme un radiologue chevronné et un excellent diagnostiqueur. Ta mission n'est pas seulement de décrire une image, mais de réaliser une synthèse clinico-radiologique complète. Tu dois éviter les biais cognitifs courants comme la "satisfaction de recherche" (s'arrêter à la première anomalie trouvée) et toujours te demander : "Qu'est-ce qui pourrait expliquer l'ensemble du tableau clinique et radiologique ?"

---

# INSTRUCTIONS FONDAMENTALES DE RAISONNEMENT

Avant de rédiger le rapport, tu dois suivre ces principes directeurs :

1. *Analyse Systématique Obligatoire :* Ne te concentre pas uniquement sur la lésion évidente. Examine méthodiquement TOUTES les structures, en accordant une attention particulière aux zones "cachées" ou difficiles.

2. *Corrélation Clinico-Radiologique Stricte :* Le contexte clinique n'est pas une information secondaire, c'est la clé de l'interprétation. Tu dois activement chercher comment les signes radiologiques peuvent expliquer *chaque détail* des renseignements cliniques fournis.

3. *Élaboration d'un Diagnostic Différentiel :* Pour toute anomalie significative, tu dois d'abord établir une liste de diagnostics différentiels possibles.

---

# STRUCTURE DU RAPPORT

Tu dois impérativement générer le rapport en suivant la structure ci-dessous, qui force une analyse par étapes.

**1. EN-TÊTE**
• *Patient :* {patient_name if patient_name else "[Nom du Patient]"}
• *Date de Naissance :* {birth_date if birth_date else "[JJ/MM/AAAA]"}
• *Date de l'examen :* {current_date}
• *Médecin prescripteur :* Dr. {doctor_name if doctor_name else "[Nom du Médecin]"}

**2. TYPE D'EXAMEN ET RENSEIGNEMENTS CLINIQUES**
• *Examen :* [Précise ici le type d'examen que tu identifies]
• *Renseignements cliniques :* {clinical_info}

**3. DESCRIPTION ANALYTIQUE DES SIGNES RADIOLOGIQUES**
• Décris de manière objective et systématique ce qui est visible sur l'image, SANS interprétation à ce stade.

**4. SYNTHÈSE ET DIAGNOSTIC DIFFÉRENTIEL**
• En te basant sur la description ci-dessus, liste les anomalies principales.
• Pour l'anomalie la plus significative, propose un diagnostic différentiel.
• Maintenant, réalise la *synthèse clinico-radiologique* : mets en corrélation les signes radiologiques avec les renseignements cliniques. Explique quel diagnostic du différentiel est le plus probable et pourquoi.

**5. IMPRESSION / CONCLUSION**
• Résume en une liste numérotée et concise la conclusion finale issue de ta synthèse. Le diagnostic le plus probable doit être clairement énoncé.

---

# MA DEMANDE

Maintenant, applique cette méthodologie rigoureuse pour générer le rapport de radiologie pour l'image ci-jointe.

*Renseignements cliniques à utiliser :* {clinical_info}
"""
        return prompt
    
    def preprocess_image(self, image: Image.Image) -> Image.Image:
        """
        Prétraite l'image pour optimiser l'analyse
        
        Args:
            image: Image PIL à prétraiter
            
        Returns:
            Image prétraitée
        """
        # Convertir en niveaux de gris si nécessaire pour les images radiologiques
        if image.mode != 'RGB':
            image = image.convert('RGB')
            
        # Redimensionner si l'image est très grande (pour optimiser l'API)
        max_size = 1024
        if max(image.size) > max_size:
            ratio = max_size / max(image.size)
            new_size = tuple(int(dim * ratio) for dim in image.size)
            image = image.resize(new_size, Image.Resampling.LANCZOS)
            
        return image
    
    def analyze_image(self, image: Image.Image, clinical_info: str, 
                     patient_name: str = "", birth_date: str = "", 
                     doctor_name: str = "") -> str:
        """
        Analyse une image radiologique avec Gemini 2.5 Pro
        
        Args:
            image: Image radiologique à analyser
            clinical_info: Renseignements cliniques
            patient_name: Nom du patient (optionnel)
            birth_date: Date de naissance (optionnel)
            doctor_name: Nom du médecin (optionnel)
            
        Returns:
            Rapport d'analyse radiologique structuré
        """
        try:
            # Prétraiter l'image
            processed_image = self.preprocess_image(image)
            
            # Créer le prompt structuré
            prompt = self.create_analysis_prompt(
                clinical_info, patient_name, birth_date, doctor_name
            )
            
            # Générer l'analyse avec Gemini
            response = self.model.generate_content([prompt, processed_image])
            
            return response.text
            
        except Exception as e:
            return f"Erreur lors de l'analyse : {str(e)}"
    
    def validate_image(self, image: Image.Image) -> Tuple[bool, str]:
        """
        Valide qu'une image est appropriée pour l'analyse radiologique
        
        Args:
            image: Image à valider
            
        Returns:
            Tuple (est_valide, message)
        """
        if image is None:
            return False, "Aucune image fournie"
            
        # Vérifier la taille minimale
        if min(image.size) < 100:
            return False, "Image trop petite pour l'analyse"
            
        # Vérifier le format
        if image.format not in ['JPEG', 'PNG', 'TIFF', 'BMP', 'DICOM']:
            return False, "Format d'image non supporté"
            
        return True, "Image valide"


def load_analyzer() -> Optional[RadiologyAnalyzer]:
    """
    Charge l'analyseur avec la clé API depuis les variables d'environnement
    
    Returns:
        Instance de RadiologyAnalyzer ou None si erreur
    """
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        return None
    
    try:
        return RadiologyAnalyzer(api_key)
    except Exception as e:
        print(f"Erreur lors de l'initialisation de l'analyseur : {e}")
        return None
