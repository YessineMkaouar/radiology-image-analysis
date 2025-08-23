# Exemples d'Images Radiologiques

Ce dossier est destiné à contenir des images d'exemple pour tester l'assistant d'analyse radiologique.

## Types d'images recommandées

Pour tester l'application, vous pouvez utiliser des images radiologiques de type :

### 1. Radiographies Thoraciques
- **Format** : JPEG, PNG, TIFF
- **Résolution** : Minimum 512x512 pixels
- **Exemple de cas** : 
  - Radiographie pulmonaire normale
  - Suspicion de pneumonie
  - Contrôle post-opératoire

### 2. Mammographies
- **Format** : JPEG, PNG, TIFF, DICOM
- **Résolution** : Haute résolution recommandée
- **Exemple de cas** :
  - Mammographie de dépistage
  - Contrôle de routine
  - Suivi post-traitement

### 3. Radiographies Osseuses
- **Format** : JPEG, PNG, TIFF
- **Résolution** : Minimum 512x512 pixels
- **Exemple de cas** :
  - Fracture du poignet
  - Radiographie du rachis cervical
  - Contrôle orthopédique

### 4. Radiographies Abdominales
- **Format** : JPEG, PNG, TIFF
- **Résolution** : Minimum 512x512 pixels
- **Exemple de cas** :
  - Abdomen sans préparation
  - Recherche d'occlusion
  - Contrôle post-opératoire

## ⚠️ Important

- **Utilisez uniquement des images anonymisées** sans informations patient identifiables
- **Respectez la confidentialité médicale** et les réglementations en vigueur
- **Images de test uniquement** : ces exemples sont à des fins de démonstration

## Sources d'Images de Test

Pour obtenir des images de test appropriées :

1. **Bases de données publiques** :
   - NIH Chest X-ray Dataset
   - MIMIC-CXR Database (accès contrôlé)
   - Open-i biomedical image search

2. **Images simulées** :
   - Créées pour la formation médicale
   - Datasets académiques anonymisés

3. **Propres images** :
   - Images provenant de votre pratique (après anonymisation complète)
   - Accord patient et conformité RGPD requis

## Structure Recommandée

```
examples/
├── chest_xray/
│   ├── normal_case_1.jpg
│   ├── pneumonia_case_1.jpg
│   └── ...
├── mammography/
│   ├── screening_case_1.png
│   └── ...
├── bone/
│   ├── wrist_fracture_1.jpg
│   ├── cervical_spine_1.jpg
│   └── ...
└── abdomen/
    ├── normal_abdomen_1.jpg
    └── ...
```

Pour ajouter vos propres images de test, placez-les dans les sous-dossiers appropriés selon le type d'examen.
