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
    
    # Vérifier que l'image est fournie
    if image is None:
        return "❌ **Veuillez uploader une image radiologique**"
    
    # Vérifier que les renseignements cliniques sont fournis
    if not clinical_info.strip():
        return "❌ **Veuillez fournir les renseignements cliniques**"
    
    try:
        # Convertir l'image si nécessaire
        if isinstance(image, str):
            pil_image = Image.open(image)
        else:
            pil_image = Image.fromarray(image) if hasattr(image, 'shape') else image
        
        # Valider l'image
        is_valid, message = analyzer.validate_image(pil_image)
        if not is_valid:
            return f"❌ **Image invalide :** {message}"
        
        # Analyser l'image
        analysis = analyzer.analyze_image(
            pil_image, clinical_info, patient_name, birth_date, doctor_name
        )
        
        return analysis
        
    except Exception as e:
        return f"❌ **Erreur lors de l'analyse :** {str(e)}"

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
            <h3>Analyse automatisée d'images médicales avec Gemini 2.5 Pro</h3>
            <p>Radiographies • Mammographies • Scanners 2D • IRM</p>
        </div>
        """)
        
        # Information importante
        gr.HTML("""
        <div class="medical-info">
            <h4>⚠️ AVERTISSEMENT MÉDICAL IMPORTANT</h4>
            <p><strong>Cet outil est destiné à des fins éducatives et d'assistance uniquement.</strong></p>
            <p>• Les résultats ne remplacent PAS un diagnostic médical professionnel</p>
            <p>• Toujours consulter un radiologue qualifié pour un diagnostic définitif</p>
            <p>• Ne pas utiliser pour des décisions médicales critiques</p>
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
                
                output = gr.Textbox(
                    label="Rapport Médical Généré",
                    lines=25,
                    max_lines=30,
                    placeholder="Le rapport d'analyse apparaîtra ici après soumission...",
                    show_copy_button=True
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
    demo.launch(
        server_name="0.0.0.0",  # Permettre l'accès externe
        server_port=7860,       # Port par défaut Gradio
        share=False,            # Ne pas créer de lien public automatiquement
        debug=True,             # Mode debug pour le développement
        show_error=True,        # Afficher les erreurs détaillées
        favicon_path=None,      # Pas d'icône personnalisée
        ssl_verify=False        # Désactiver la vérification SSL en dev
    )
