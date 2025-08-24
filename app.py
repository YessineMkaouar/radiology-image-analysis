import os

import gradio as gr
from dotenv import load_dotenv
from PIL import Image

from radiology_analyzer import load_analyzer

# Charger les variables d'environnement
load_dotenv()

# Initialiser l'analyseur
analyzer = None

def initialize_analyzer():
    """Initialise l'analyseur radiologique"""
    global analyzer
    if analyzer is None:
        analyzer = load_analyzer()
    return analyzer is not None

def analyze_radiology_image(image, clinical_info, patient_name="", birth_date="", doctor_name=""):
    """
    Fonction principale pour analyser une image radiologique
    
    Args:
        image: Image uploadée par l'utilisateur
        clinical_info: Renseignements cliniques
        patient_name: Nom du patient (optionnel)
        birth_date: Date de naissance (optionnel)
        doctor_name: Nom du médecin prescripteur (optionnel)
        
    Returns:
        Rapport d'analyse ou message d'erreur
    """
    global analyzer
    
    # Vérifier que l'analyseur est initialisé
    if not initialize_analyzer():
        return """
        ❌ **Erreur de configuration**
        
        La clé API Google Gemini n'est pas configurée. 
        
        **Pour configurer :**
        1. Obtenez une clé API sur https://makersuite.google.com/app/apikey
        2. Ajoutez-la dans le fichier .env : `GOOGLE_API_KEY=votre_cle_api`
        3. Redémarrez l'application
        """
    
    # Test de connexion API (optionnel mais recommandé)
    try:
        api_test_success, api_test_message = analyzer.test_api_connection()
        if not api_test_success:
            return f"""
            ❌ **Problème de connexion API**
            
            {api_test_message}
            
            **Vérifications suggérées :**
            • Clé API valide et active
            • Quota API disponible
            • Connexion internet stable
            """
    except Exception as e:
        # Continue même si le test échoue (pour éviter de bloquer l'analyse)
        pass
    
    # Vérifier que l'image est fournie
    if image is None:
        return "❌ **Veuillez uploader une image radiologique**"
    
    # Vérifier que les renseignements cliniques sont fournis
    if not clinical_info.strip():
        return "❌ **Veuillez fournir les renseignements cliniques**"
    
    try:
        # Convertir l'image si nécessaire - Gradio fournit directement une PIL Image
        if isinstance(image, str):
            # Si c'est un chemin de fichier
            pil_image = Image.open(image)
        elif hasattr(image, 'shape'):
            # Si c'est un array numpy
            pil_image = Image.fromarray(image)
        elif isinstance(image, Image.Image):
            # Si c'est déjà une PIL Image (cas normal avec Gradio)
            pil_image = image
        else:
            return "❌ **Format d'image non reconnu**"
        
        # Assurer que l'image est en mode RGB pour Gemini
        if pil_image.mode not in ['RGB', 'RGBA']:
            pil_image = pil_image.convert('RGB')
        
        # Valider l'image
        is_valid, message = analyzer.validate_image(pil_image)
        if not is_valid:
            return f"❌ **Image invalide :** {message}"
        
        # Analyser l'image
        analysis = analyzer.analyze_image(
            pil_image, clinical_info, patient_name, birth_date, doctor_name
        )
        
        # Nettoyer le rapport pour éliminer les commentaires inutiles
        cleaned_analysis = clean_medical_report(analysis)
        
        return cleaned_analysis
        
    except Exception as e:
        return f"❌ **Erreur lors de l'analyse :** {str(e)}"

def clean_medical_report(report: str) -> str:
    """
    Nettoie le rapport médical en éliminant les commentaires introductifs
    
    Args:
        report: Rapport brut généré par l'IA
        
    Returns:
        Rapport nettoyé
    """
    # Liste des phrases introductives à supprimer
    unwanted_phrases = [
        "Absolument.",
        "Voici le rapport de radiologie",
        "Voici le rapport médical",
        "Je vais analyser",
        "Après analyse de l'image",
        "Suite à l'analyse",
        "En analysant cette image",
        "rédigé en suivant scrupuleusement",
        "la méthodologie et la structure demandées",
        "Voici l'analyse",
        "Voici donc",
        "Comme demandé",
        "Selon la structure demandée"
    ]
    
    # Supprimer les phrases introductives
    lines = report.split('\n')
    cleaned_lines = []
    skip_line = False
    
    for line in lines:
        # Vérifier si la ligne contient une phrase indésirable
        line_lower = line.lower().strip()
        contains_unwanted = any(phrase.lower() in line_lower for phrase in unwanted_phrases)
        
        # Si on trouve "# EN-TÊTE" ou "# TYPE D'EXAMEN", on commence à garder les lignes
        if line.strip().startswith("# "):
            skip_line = False
            
        # Ignorer les lignes vides au début et les phrases introductives
        if not skip_line or line.strip():
            if not contains_unwanted and line.strip():
                cleaned_lines.append(line)
            elif line.strip().startswith("#"):
                cleaned_lines.append(line)
        
        # Une fois qu'on a du contenu structuré, arrêter de skip
        if line.strip().startswith("# "):
            skip_line = False
    
    # Rejoindre et nettoyer
    cleaned_report = '\n'.join(cleaned_lines)
    
    # Supprimer les lignes vides excessives
    while '\n\n\n' in cleaned_report:
        cleaned_report = cleaned_report.replace('\n\n\n', '\n\n')
    
    return cleaned_report.strip()

def create_demo():
    """Crée l'interface Gradio pour la démonstration"""
    
    # CSS personnalisé pour un style médical professionnel
    css = """
    .gradio-container {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        max-width: 1200px !important;
        margin: auto;
        padding: 20px;
    }
    .gr-button-primary {
        background: linear-gradient(90deg, #1e40af, #3b82f6) !important;
        border: none !important;
        color: white !important;
        font-weight: 600 !important;
    }
    .gr-button-primary:hover {
        background: linear-gradient(90deg, #1e3a8a, #2563eb) !important;
    }
    
    /* Styles pour le rapport médical */
    .medical-report {
        background: #fafafa !important;
        border: 1px solid #e0e0e0 !important;
        border-radius: 8px !important;
        padding: 20px !important;
        margin: 10px 0 !important;
        font-family: 'Georgia', serif !important;
        line-height: 1.6 !important;
        max-height: 600px !important;
        overflow-y: auto !important;
    }
    
    .medical-report h1 {
        color: #1e40af !important;
        border-bottom: 2px solid #3b82f6 !important;
        padding-bottom: 8px !important;
        margin-bottom: 15px !important;
        font-size: 1.4em !important;
    }
    
    .medical-report h2 {
        color: #2563eb !important;
        margin-top: 20px !important;
        margin-bottom: 10px !important;
        font-size: 1.2em !important;
    }
    
    .medical-report h3 {
        color: #3b82f6 !important;
        margin-top: 15px !important;
        margin-bottom: 8px !important;
        font-size: 1.1em !important;
    }
    
    .medical-report p {
        margin-bottom: 12px !important;
        text-align: justify !important;
    }
    
    .medical-report strong {
        color: #1e40af !important;
        font-weight: 600 !important;
    }
    
    .medical-report ol, .medical-report ul {
        margin-left: 20px !important;
        margin-bottom: 15px !important;
    }
    
    .medical-report li {
        margin-bottom: 5px !important;
    }
    
    .medical-report hr {
        border: none !important;
        border-top: 1px solid #d1d5db !important;
        margin: 20px 0 !important;
    }
    
    .gr-textbox textarea {
        font-family: 'Courier New', monospace !important;
        font-size: 14px !important;
    }
    .medical-header {
        text-align: center;
        background: linear-gradient(135deg, #1e40af, #3b82f6);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .medical-info {
        background: #f8fafc;
        border-left: 4px solid #3b82f6;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }
    """
    
    with gr.Blocks(css=css, title="Assistant d'Analyse Radiologique") as demo:
        # En-tête
        gr.HTML("""
        <div class="medical-header">
            <h1>🏥 Assistant d'Analyse Radiologique IA</h1>
            <h3>Analyse automatisée d'images médicales</h3>
            <p>Radiographies • Mammographies • Scanners 2D • IRM</p>
        </div>
        """)
        
        with gr.Row():
            # Colonne gauche - Entrées
            with gr.Column(scale=1):
                gr.HTML("<h3>📋 Informations Patient & Examen</h3>")
                
                # Informations patient (optionnelles)
                with gr.Group():
                    gr.HTML("<h4>Informations Patient (Optionnel)</h4>")
                    patient_name = gr.Textbox(
                        label="Nom du Patient",
                        placeholder="Ex: Dupont Jean",
                        value=""
                    )
                    birth_date = gr.Textbox(
                        label="Date de Naissance", 
                        placeholder="JJ/MM/AAAA",
                        value=""
                    )
                    doctor_name = gr.Textbox(
                        label="Médecin Prescripteur",
                        placeholder="Ex: Dr. Martin",
                        value=""
                    )
                
                # Renseignements cliniques (obligatoire)
                clinical_info = gr.Textbox(
                    label="🩺 Renseignements Cliniques (Obligatoire)",
                    placeholder="Ex: Patient de 53 ans, fumeur, adressé pour majoration d'une névralgie cervicobrachiale C8-T1. Présente une douleur du membre supérieur gauche et une légère atrophie musculaire de l'épaule.",
                    lines=4,
                    value="Patient de 53 ans, fumeur, adressé pour majoration d'une névralgie cervicobrachiale C8-T1. Présente une douleur du membre supérieur gauche et une légère atrophie musculaire de l'épaule."
                )
                
                # Upload d'image
                image_input = gr.Image(
                    label="📷 Image Radiologique",
                    type="pil",
                    height=300
                )
                
                # Bouton d'analyse
                analyze_btn = gr.Button(
                    "🔍 Analyser l'Image Radiologique",
                    variant="primary",
                    size="lg"
                )
            
            # Colonne droite - Résultats
            with gr.Column(scale=1):
                gr.HTML("<h3>📄 Rapport d'Analyse Radiologique</h3>")
                
                output = gr.Markdown(
                    value="Le rapport d'analyse apparaîtra ici après soumission...",
                    label="Rapport Médical Généré",
                    elem_classes=["medical-report"]
                )
        
        # Exemples d'utilisation
        gr.HTML("""
        <div class="medical-info" style="margin-top: 20px;">
            <h4>💡 Conseils d'utilisation</h4>
            <ul>
                <li><strong>Formats supportés :</strong> JPEG, PNG, TIFF, BMP, DICOM</li>
                <li><strong>Qualité d'image :</strong> Utilisez des images de haute résolution pour de meilleurs résultats</li>
                <li><strong>Renseignements cliniques :</strong> Plus vous fournissez d'informations contextuelles, plus l'analyse sera précise</li>
                <li><strong>Types d'examens :</strong> Radiographies thoraciques, abdominales, osseuses, mammographies, etc.</li>
            </ul>
        </div>
        """)
        
        # Configuration des événements
        analyze_btn.click(
            fn=analyze_radiology_image,
            inputs=[image_input, clinical_info, patient_name, birth_date, doctor_name],
            outputs=output,
            show_progress=True
        )
        
        # Exemples prédéfinis
        gr.HTML("<h3>📚 Exemples de Renseignements Cliniques</h3>")
        
        examples_data = [
            [
                "Patient de 45 ans, non-fumeur, consulte pour une toux persistante depuis 3 semaines avec légère dyspnée d'effort. Antécédents familiaux de cancer pulmonaire.",
                "Radiographie thoracique de face"
            ],
            [
                "Patiente de 52 ans en suivi post-thérapeutique pour cancer du sein gauche traité il y a 2 ans. Contrôle de routine.",
                "Mammographie bilatérale"
            ],
            [
                "Patient de 35 ans, ouvrier du bâtiment, chute d'échafaudage il y a 2 heures. Douleur intense poignet droit, impotence fonctionnelle.",
                "Radiographie poignet droit"
            ]
        ]
        
        for i, (clinical, exam_type) in enumerate(examples_data, 1):
            with gr.Row():
                gr.HTML(f"""
                <div style="background: #f1f5f9; padding: 10px; border-radius: 5px; margin: 5px 0;">
                    <strong>Exemple {i} - {exam_type} :</strong><br>
                    <em>"{clinical}"</em>
                </div>
                """)
        
        # Pied de page
        gr.HTML("""
        <div style="text-align: center; margin-top: 30px; padding: 20px; background: #f8fafc; border-radius: 10px;">
            <p><strong>🤖 Assistant IA d'Analyse Radiologique</strong></p>
            <p>Développé avec Gemini 2.5 Pro • Interface Gradio</p>
            <p style="font-size: 12px; color: #666;">
                Version 1.0 • Pour un usage éducatif et d'assistance uniquement
            </p>
        </div>
        """)
    
    return demo

if __name__ == "__main__":
    # Créer et lancer la démonstration
    demo = create_demo()
    
    # Configuration du lancement
    demo.launch()
