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
        self.model = genai.GenerativeModel('gemini-2.5-pro')
        
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
Tu es un radiologue expert. Analyse cette image radiologique avec rigueur scientifique et génère UNIQUEMENT le rapport structuré, sans aucun commentaire introductif.

INSTRUCTIONS CRITIQUES :
- Ne commence PAS par "Voici le rapport", "Absolument", ou toute phrase introductive
- Commence DIRECTEMENT par "# EN-TÊTE"
- Suis EXACTEMENT la structure demandée
- Utilise le format Markdown pour un meilleur affichage

MÉTHODOLOGIE D'ANALYSE OBLIGATOIRE :
1. **RÉFLEXION SYSTÉMATIQUE** : Examine méthodiquement chaque région anatomique visible
2. **JUSTIFICATION CONCRÈTE** : Base chaque observation sur des signes radiologiques précis et visibles
3. **INTERDICTION DE MESURES** : Ne fournis JAMAIS de mesures chiffrées, dimensions ou tailles
4. **DIFFÉRENCIATION NORMALE/PATHOLOGIQUE** : Distingue clairement entre :
   - Examen NORMAL : "Aucune anomalie radiologique décelée"
   - Examen PATHOLOGIQUE : Décris précisément les anomalies observées

PRINCIPES DE DESCRIPTION :
- Justifie chaque observation par des signes radiologiques concrets
- Si l'image est normale, affirme clairement l'absence d'anomalie
- Si pathologique, décris les anomalies avec précision sans spéculer

STRUCTURE OBLIGATOIRE :

# EN-TÊTE
**Patient :** {patient_name if patient_name else "[Nom du Patient]"}  
**Date de Naissance :** {birth_date if birth_date else "[JJ/MM/AAAA]"}  
**Date de l'examen :** {current_date}  
**Médecin prescripteur :** Dr. {doctor_name if doctor_name else "[Nom du Médecin]"}

---

# TYPE D'EXAMEN ET RENSEIGNEMENTS CLINIQUES
**Examen :** [Précise le type d'examen identifié]  
**Renseignements cliniques :** {clinical_info}

---

# DESCRIPTION ANALYTIQUE DES SIGNES RADIOLOGIQUES
[MÉTHODOLOGIE : Examine systématiquement chaque région anatomique visible]
[IMPÉRATIF : Décris UNIQUEMENT ce qui est objectivement visible, avec justifications concrètes]
[INTERDICTION : Aucune mesure chiffrée, aucune spéculation]
[FORMAT : Pour chaque observation, explique le signe radiologique qui la justifie]

**Analyse systématique :**
- **Structures osseuses :** [Décris l'aspect des os visibles avec justification radiologique]
- **Tissus mous :** [Décris les tissus mous avec justification radiologique]  
- **Organes visibles :** [Décris les organes avec justification radiologique]
- **Symétrie/Asymétrie :** [Note toute asymétrie avec justification]

**Conclusion de la description :**
- Si NORMAL : "Aucune anomalie radiologique objectivement décelée"
- Si PATHOLOGIQUE : "Anomalies identifiées nécessitant interprétation"

---

# SYNTHÈSE ET DIAGNOSTIC DIFFÉRENTIEL

## Anomalies principales
[OBLIGATOIRE : Si AUCUNE anomalie → "Aucune anomalie radiologique identifiée"]
[Si anomalies présentes → Liste avec justification radiologique précise pour chacune]

## Diagnostic différentiel
[SEULEMENT si anomalies identifiées :]
[Pour chaque anomalie principale, liste les diagnostics possibles avec argumentation radiologique]
[Si examen normal → "Non applicable - examen sans anomalie"]

## Synthèse clinico-radiologique
[Corrélation entre :]
- **Signes radiologiques objectifs** (avec justification)
- **Renseignements cliniques fournis**
- **Cohérence diagnostique** entre clinique et imagerie

**Conclusion analytique :**
[Diagnostic le plus probable avec argumentation basée sur les signes observés]

---

# IMPRESSION / CONCLUSION

**RÉFLEXION DIAGNOSTIQUE :**
[Synthèse du raisonnement basé sur les signes radiologiques observés]

**CONCLUSION FINALE :**

**CAS NORMAL :**
1. Examen radiologique sans anomalie décelée
2. Structures anatomiques d'aspect normal
3. Absence de signe pathologique objectif

**CAS PATHOLOGIQUE :**
1. [Premier diagnostic avec justification radiologique précise]
2. [Deuxième élément diagnostique avec argumentation]
3. [Diagnostic final le plus probable avec synthèse des arguments]

**RECOMMANDATIONS :**
[Suggestions de suivi ou examens complémentaires si nécessaire, basées sur les observations]

RENSEIGNEMENTS CLINIQUES : {clinical_info}
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
        # Convertir en RGB (requis par Gemini)
        if image.mode != 'RGB':
            image = image.convert('RGB')
            
        # Redimensionner si l'image est très grande (pour optimiser l'API)
        max_size = 1024
        if max(image.size) > max_size:
            ratio = max_size / max(image.size)
            new_size = tuple(int(dim * ratio) for dim in image.size)
            image = image.resize(new_size, Image.Resampling.LANCZOS)
        
        # Vérifier la taille minimale pour Gemini
        min_size = 32
        if min(image.size) < min_size:
            # Redimensionner vers la taille minimale
            new_size = (max(min_size, image.width), max(min_size, image.height))
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
            
            # Configuration de sécurité pour les images médicales
            safety_settings = [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            ]
            
            # Générer l'analyse avec Gemini
            response = self.model.generate_content(
                [prompt, processed_image],
                safety_settings=safety_settings
            )
            
            # Vérifier si la réponse est valide
            if response.candidates and len(response.candidates) > 0:
                candidate = response.candidates[0]
                
                # Vérifier le statut de fin
                if hasattr(candidate, 'finish_reason'):
                    finish_reason = candidate.finish_reason
                    if finish_reason == 1:  # STOP - normal
                        pass
                    elif finish_reason == 2:  # MAX_TOKENS
                        return "⚠️ Réponse tronquée : Le rapport est trop long. Veuillez essayer avec des renseignements cliniques plus concis."
                    elif finish_reason == 3:  # SAFETY
                        return "⚠️ Contenu bloqué pour des raisons de sécurité. Veuillez vérifier que l'image est appropriée pour l'analyse médicale."
                    elif finish_reason == 4:  # RECITATION
                        return "⚠️ Contenu bloqué pour récitation. Veuillez essayer avec une image différente."
                    else:
                        return f"⚠️ Génération arrêtée (raison: {finish_reason}). Veuillez réessayer."
                
                # Extraire le texte
                if hasattr(candidate.content, 'parts') and candidate.content.parts:
                    text_parts = []
                    for part in candidate.content.parts:
                        if hasattr(part, 'text') and part.text:
                            text_parts.append(part.text)
                    
                    if text_parts:
                        return '\n'.join(text_parts)
                    else:
                        return "❌ Aucun contenu textuel généré. Veuillez réessayer avec une image différente."
                else:
                    return "❌ Structure de réponse inattendue. Veuillez réessayer."
            else:
                return "❌ Aucune réponse générée. Veuillez vérifier votre clé API et réessayer."
            
        except Exception as e:
            error_msg = str(e)
            if "finish_reason" in error_msg:
                return f"⚠️ Génération interrompue par Gemini. Cela peut être dû à:\n• Image trop complexe ou peu claire\n• Contenu considéré comme sensible\n• Problème temporaire du service\n\nDétails: {error_msg}"
            elif "INVALID_ARGUMENT" in error_msg:
                return "❌ Image invalide ou format non supporté par Gemini. Veuillez essayer avec une image JPEG ou PNG."
            elif "PERMISSION_DENIED" in error_msg:
                return "❌ Problème d'authentification. Vérifiez votre clé API Gemini."
            elif "QUOTA_EXCEEDED" in error_msg:
                return "⚠️ Quota API dépassé. Veuillez attendre ou vérifier votre plan Gemini."
            else:
                return f"❌ Erreur lors de l'analyse: {error_msg}"
    
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
            
        # Vérifier le format - être plus permissif pour les images Gradio
        # Si le format est None (cas fréquent avec Gradio), on accepte l'image
        if image.format is not None:
            supported_formats = ['JPEG', 'PNG', 'TIFF', 'BMP', 'DICOM']
            if image.format not in supported_formats:
                return False, f"Format d'image non supporté: {image.format}"
        
        # Vérification additionnelle : l'image doit avoir des canaux de couleur valides
        if not hasattr(image, 'mode') or image.mode not in ['RGB', 'RGBA', 'L', 'P']:
            return False, "Mode d'image non supporté"
            
        return True, "Image valide"
    
    def test_api_connection(self) -> Tuple[bool, str]:
        """
        Teste la connexion à l'API Gemini
        
        Returns:
            Tuple (succès, message)
        """
        try:
            # Test simple avec du texte
            test_response = self.model.generate_content("Répondez simplement 'OK' si vous recevez ce message.")
            
            if test_response.candidates and len(test_response.candidates) > 0:
                return True, "✅ Connexion API Gemini réussie"
            else:
                return False, "❌ Pas de réponse de l'API Gemini"
                
        except Exception as e:
            return False, f"❌ Erreur de connexion API: {str(e)}"


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
