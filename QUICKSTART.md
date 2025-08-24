# 🚀 Guide de Démarrage Rapide - Assistant d'Analyse Radiologique IA

## Pour les Utilisateurs Windows

1. **Exécutez la configuration automatique :**
   ```bash
   start.bat
   ```

2. **Ou manuellement :**
   ```bash
   python start.py
   ```

## Pour les Utilisateurs Linux/Mac

1. **Rendez le script exécutable :**
   ```bash
   chmod +x start.sh
   ```

2. **Exécutez la configuration automatique :**
   ```bash
   ./start.sh
   ```

3. **Ou manuellement :**
   ```bash
   python3 start.py
   ```

## 🔑 Configuration de l'API

1. Obtenez votre clé API Gemini sur : https://makersuite.google.com/app/apikey
2. Ouvrez le fichier `.env` et remplacez `your_gemini_api_key_here` par votre vraie clé

## 🏥 Utilisation de l'Application

1. Ouvrez votre navigateur sur http://localhost:7860
2. Téléchargez une image radiologique (DICOM, PNG, JPG, etc.)
3. Cliquez sur "Analyser l'image"
4. Consultez le rapport médical détaillé

## ⚠️ Notes Importantes

- Ceci est un outil d'assistance IA, PAS un dispositif de diagnostic médical
- Consultez toujours des professionnels de santé qualifiés
- Gardez votre clé API sécurisée et ne la partagez jamais publiquement

## 🆘 Dépannage

- **Port déjà utilisé :** L'application trouvera automatiquement un port disponible
- **Erreurs API :** Vérifiez votre connexion internet et votre clé API
- **Problèmes de format d'image :** Essayez de convertir en PNG ou JPG
- **Problèmes d'installation :** Exécutez `diagnostic.py` pour vérifier votre environnement

Pour plus de détails, consultez le fichier complet `README.md`.
