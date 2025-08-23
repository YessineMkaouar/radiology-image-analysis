"""
Utilitaires pour l'assistant d'analyse radiologique
"""

import base64
import io
import os
from typing import Any, Dict, List

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter


class ImageProcessor:
    """Classe pour le prétraitement d'images radiologiques"""
    
    @staticmethod
    def enhance_contrast(image: Image.Image, factor: float = 1.5) -> Image.Image:
        """
        Améliore le contraste d'une image radiologique
        
        Args:
            image: Image PIL à traiter
            factor: Facteur d'amélioration du contraste (1.0 = inchangé)
            
        Returns:
            Image avec contraste amélioré
        """
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(factor)
    
    @staticmethod
    def adjust_brightness(image: Image.Image, factor: float = 1.2) -> Image.Image:
        """
        Ajuste la luminosité d'une image
        
        Args:
            image: Image PIL à traiter
            factor: Facteur d'ajustement de la luminosité
            
        Returns:
            Image avec luminosité ajustée
        """
        enhancer = ImageEnhance.Brightness(image)
        return enhancer.enhance(factor)
    
    @staticmethod
    def sharpen_image(image: Image.Image, factor: float = 1.5) -> Image.Image:
        """
        Applique un filtre de netteté à l'image
        
        Args:
            image: Image PIL à traiter
            factor: Facteur de netteté
            
        Returns:
            Image plus nette
        """
        enhancer = ImageEnhance.Sharpness(image)
        return enhancer.enhance(factor)
    
    @staticmethod
    def preprocess_radiology_image(image: Image.Image) -> Image.Image:
        """
        Pipeline complet de prétraitement pour images radiologiques
        
        Args:
            image: Image radiologique brute
            
        Returns:
            Image prétraitée et optimisée
        """
        # Conversion en RGB si nécessaire
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Amélioration du contraste
        image = ImageProcessor.enhance_contrast(image, 1.3)
        
        # Légère amélioration de la netteté
        image = ImageProcessor.sharpen_image(image, 1.2)
        
        # Ajustement de la luminosité si nécessaire
        image = ImageProcessor.adjust_brightness(image, 1.1)
        
        return image


class ReportFormatter:
    """Classe pour formater les rapports médicaux"""
    
    @staticmethod
    def format_medical_report(report_text: str) -> str:
        """
        Formate un rapport médical avec des améliorations typographiques
        
        Args:
            report_text: Texte brut du rapport
            
        Returns:
            Rapport formaté avec markdown
        """
        # Remplacer les sections en gras
        sections = [
            "EN-TÊTE", "TYPE D'EXAMEN", "DESCRIPTION ANALYTIQUE", 
            "SYNTHÈSE ET DIAGNOSTIC", "IMPRESSION", "CONCLUSION"
        ]
        
        formatted_text = report_text
        
        for section in sections:
            formatted_text = formatted_text.replace(
                f"**{section}**", 
                f"\n## 📋 {section}\n"
            )
        
        # Améliorer la lisibilité des listes
        lines = formatted_text.split('\n')
        formatted_lines = []
        
        for line in lines:
            line = line.strip()
            if line.startswith('•'):
                formatted_lines.append(f"  {line}")
            elif line.startswith('*'):
                formatted_lines.append(f"**{line[1:].strip()}**")
            else:
                formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)
    
    @staticmethod
    def add_disclaimer(report: str) -> str:
        """
        Ajoute un avertissement médical au rapport
        
        Args:
            report: Rapport médical
            
        Returns:
            Rapport avec avertissement
        """
        disclaimer = """
---
⚠️ **AVERTISSEMENT MÉDICAL**

Ce rapport a été généré par une intelligence artificielle à des fins d'assistance et d'éducation uniquement. 
Il ne remplace en aucun cas l'expertise d'un radiologue qualifié ou un diagnostic médical professionnel.

**Veuillez consulter un professionnel de santé pour toute décision médicale.**
---
"""
        return report + disclaimer


class ValidationUtils:
    """Utilitaires de validation pour l'application"""
    
    @staticmethod
    def validate_clinical_info(clinical_info: str) -> tuple[bool, str]:
        """
        Valide les renseignements cliniques fournis
        
        Args:
            clinical_info: Texte des renseignements cliniques
            
        Returns:
            Tuple (est_valide, message)
        """
        if not clinical_info or not clinical_info.strip():
            return False, "Les renseignements cliniques sont obligatoires"
        
        if len(clinical_info.strip()) < 10:
            return False, "Les renseignements cliniques sont trop courts (minimum 10 caractères)"
        
        if len(clinical_info) > 2000:
            return False, "Les renseignements cliniques sont trop longs (maximum 2000 caractères)"
        
        return True, "Renseignements cliniques valides"
    
    @staticmethod
    def validate_patient_info(name: str, birth_date: str) -> tuple[bool, str]:
        """
        Valide les informations patient (optionnelles)
        
        Args:
            name: Nom du patient
            birth_date: Date de naissance
            
        Returns:
            Tuple (est_valide, message)
        """
        # Validation du nom (si fourni)
        if name and len(name.strip()) < 2:
            return False, "Le nom du patient doit contenir au moins 2 caractères"
        
        # Validation de la date de naissance (si fournie)
        if birth_date:
            # Format attendu : JJ/MM/AAAA
            import re
            date_pattern = r'^\d{2}/\d{2}/\d{4}$'
            if not re.match(date_pattern, birth_date):
                return False, "Format de date invalide. Utilisez JJ/MM/AAAA"
        
        return True, "Informations patient valides"


def create_example_clinical_cases() -> List[Dict[str, Any]]:
    """
    Crée une liste de cas cliniques d'exemple pour la démonstration
    
    Returns:
        Liste de dictionnaires contenant les cas d'exemple
    """
    examples = [
        {
            "title": "Radiographie Thoracique - Toux Persistante",
            "clinical_info": "Patient de 45 ans, non-fumeur, consulte pour une toux persistante depuis 3 semaines avec légère dyspnée d'effort. Antécédents familiaux de cancer pulmonaire. Auscultation révèle des râles crépitants en base droite.",
            "exam_type": "Radiographie thoracique de face et profil",
            "specialty": "Pneumologie"
        },
        {
            "title": "Mammographie - Dépistage de Routine",
            "clinical_info": "Patiente de 52 ans en suivi post-thérapeutique pour cancer du sein gauche traité il y a 2 ans par tumorectomie et radiothérapie. Contrôle de routine dans le cadre de la surveillance oncologique. Aucun signe clinique suspect à l'examen.",
            "exam_type": "Mammographie bilatérale avec tomosynthèse",
            "specialty": "Sénologie"
        },
        {
            "title": "Radiographie Osseuse - Traumatisme",
            "clinical_info": "Patient de 35 ans, ouvrier du bâtiment, chute d'échafaudage il y a 2 heures. Douleur intense poignet droit, impotence fonctionnelle totale, déformation visible. Pas de troubles vasculo-nerveux distaux. Recherche de fracture.",
            "exam_type": "Radiographie poignet droit face et profil",
            "specialty": "Orthopédie"
        },
        {
            "title": "Radiographie Cervicale - Névralgie",
            "clinical_info": "Patient de 53 ans, fumeur, adressé pour majoration d'une névralgie cervicobrachiale C8-T1. Présente une douleur du membre supérieur gauche et une légère atrophie musculaire de l'épaule. Paresthésies dans le territoire cubital.",
            "exam_type": "Radiographie rachis cervical face et profil",
            "specialty": "Neurologie"
        },
        {
            "title": "Radiographie Abdominale - Douleurs Abdominales",
            "clinical_info": "Patiente de 67 ans, diabétique, présente depuis 48h des douleurs abdominales diffuses avec arrêt des matières et des gaz. Vomissements bilieux. Abdomen distendu, tympanique. Suspicion d'occlusion intestinale.",
            "exam_type": "Radiographie abdomen sans préparation debout et couché",
            "specialty": "Gastroentérologie"
        }
    ]
    
    return examples


def get_supported_formats() -> List[str]:
    """
    Retourne la liste des formats d'image supportés
    
    Returns:
        Liste des extensions de fichiers supportées
    """
    return ['.jpg', '.jpeg', '.png', '.tiff', '.tif', '.bmp', '.dcm', '.dicom']


def get_max_file_size() -> int:
    """
    Retourne la taille maximale de fichier supportée en bytes
    
    Returns:
        Taille max en bytes (10 MB par défaut)
    """
    return 10 * 1024 * 1024  # 10 MB
