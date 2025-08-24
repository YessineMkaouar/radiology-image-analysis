# Assistant d'Analyse Radiologique IA / AI Radiology Analysis Assistant

> 🇫🇷 **Version française** | 🇬🇧 **[English version](README_EN.md)**

Un assistant intelligent pour l'analyse d'images radiologiques utilisant Gemini 2.5 Pro et une interface Gradio moderne.

*An intelligent assistant for radiological image analysis using Gemini 2.5 Pro and a modern Gradio interface.*

## 🎯 Fonctionnalités

- **Analyse automatisée** d'images radiologiques (rayons X, mammographies, scanners 2D)
- **Interface utilisateur intuitive** développée avec Gradio
- **Rapports structurés** en français suivant les standards médicaux
- **Support multi-formats** : JPEG, PNG, TIFF, BMP, DICOM
- **Corrélation clinico-radiologique** avancée

## ⚠️ Avertissement Médical

**Cet outil est destiné à des fins éducatives et d'assistance uniquement.**

- Les résultats ne remplacent PAS un diagnostic médical professionnel
- Toujours consulter un radiologue qualifié pour un diagnostic définitif
- Ne pas utiliser pour des décisions médicales critiques

## 🚀 Installation Rapide

### Prérequis

- Python 3.8 ou supérieur
- Clé API Google Gemini ([Obtenir ici](https://makersuite.google.com/app/apikey))

### Installation

1. **Cloner ou télécharger le projet**
   ```bash
   git clone <repository-url>
   cd radiology-image-analysis
   ```

2. **Exécuter le script de démarrage**
   ```bash
   python start.py
   ```

   Le script va automatiquement :
   - Vérifier la version Python
   - Installer toutes les dépendances
   - Créer le fichier de configuration
   - Lancer l'application

3. **Configurer la clé API**
   - Ouvrez le fichier `.env` créé
   - Remplacez `your_gemini_api_key_here` par votre vraie clé API Gemini
   - Redémarrez l'application

4. **Accéder à l'interface**
   - Ouvrez votre navigateur sur : http://localhost:7860

## 🛠️ Installation Manuelle

Si vous préférez installer manuellement :

```bash
# Installer les dépendances
pip install -r requirements.txt

# Configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec votre clé API

# Lancer l'application
python app.py
```

## 📋 Utilisation

### 1. Interface Web

1. **Uploadez une image radiologique** (formats supportés : JPEG, PNG, TIFF, BMP, DICOM)
2. **Saisissez les renseignements cliniques** (obligatoire)
3. **Complétez les informations patient** (optionnel)
4. **Cliquez sur "Analyser l'Image Radiologique"**
5. **Consultez le rapport généré**

### 2. Structure du Rapport

Le rapport généré suit une structure médicale standardisée :

- **En-tête** : Informations patient et examen
- **Renseignements cliniques** : Contexte médical fourni
- **Description analytique** : Observation objective des signes radiologiques
- **Synthèse et diagnostic différentiel** : Corrélation clinico-radiologique
- **Impression/Conclusion** : Diagnostic probable et recommandations

### 3. Exemples de Renseignements Cliniques

```
Patient de 53 ans, fumeur, adressé pour majoration d'une névralgie 
cervicobrachiale C8-T1. Présente une douleur du membre supérieur 
gauche et une légère atrophie musculaire de l'épaule.
```

```
Patiente de 45 ans, non-fumeuse, consulte pour une toux persistante 
depuis 3 semaines avec légère dyspnée d'effort. Antécédents familiaux 
de cancer pulmonaire.
```

## 🔧 Configuration Avancée

### Variables d'Environnement

Fichier `.env` :
```
GOOGLE_API_KEY=your_actual_gemini_api_key
```

### Personnalisation du Prompt

Le prompt d'analyse peut être personnalisé dans `radiology_analyzer.py` dans la méthode `create_analysis_prompt()`.

## 📁 Structure du Projet

```
radiology-image-analysis/
├── app.py                 # Application Gradio principale
├── radiology_analyzer.py  # Moteur d'analyse avec Gemini
├── start.py              # Script de démarrage automatique
├── requirements.txt      # Dépendances Python
├── .env                  # Configuration (créé automatiquement)
├── README.md            # Documentation
└── examples/            # Images d'exemple (optionnel)
```

## 🐛 Résolution de Problèmes

### Erreur : "Import could not be resolved"

C'est normal avant l'installation des dépendances. Exécutez `python start.py` pour installer automatiquement tous les packages requis.

### Erreur : "Clé API non configurée"

1. Vérifiez que le fichier `.env` existe
2. Assurez-vous que votre clé API Gemini est correctement configurée
3. Redémarrez l'application

### Erreur : "Image invalide"

- Vérifiez que le format d'image est supporté (JPEG, PNG, TIFF, BMP, DICOM)
- Assurez-vous que l'image n'est pas corrompue
- Vérifiez que la taille de l'image est suffisante (minimum 100x100 pixels)

### Problèmes de Performance

- Utilisez des images de résolution raisonnable (max 1024x1024)
- Vérifiez votre connexion internet pour les appels API
- Les images DICOM peuvent prendre plus de temps à traiter

## 🔐 Sécurité et Confidentialité

- **Données locales** : Les images sont traitées localement avant envoi à l'API
- **Pas de stockage** : Aucune image n'est sauvegardée sur nos serveurs
- **API Gemini** : Les données transitent par les serveurs Google selon leurs conditions
- **Responsabilité** : L'utilisateur est responsable de la conformité RGPD/HIPAA

## 🤝 Contribution

Les contributions sont les bienvenues ! Veuillez :

1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🆘 Support

Pour obtenir de l'aide :

1. Consultez cette documentation
2. Vérifiez les [Issues GitHub](issues)
3. Créez une nouvelle issue si nécessaire

## 🔮 Roadmap

- [ ] Support des images DICOM avancé
- [ ] Intégration de modèles spécialisés par type d'examen
- [ ] Export PDF des rapports
- [ ] API REST pour intégration
- [ ] Mode batch pour traitement de plusieurs images
- [ ] Support multilingue (anglais, espagnol)

---

**Développé avec ❤️ pour la communauté médicale**

*Dernière mise à jour : Août 2025*