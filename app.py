# Version corrigée pour Render
from flask import Flask, request, jsonify
import pytesseract
from PIL import Image
import io

app = Flask(__name__)

@app.route('/')
def home():
    return "Compta Zen OCR API is running!"

@app.route('/extract', methods=['POST'])
def extract_text():
    if 'file' not in request.files:
        return jsonify({'error': 'Aucun fichier reçu'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Nom de fichier vide'}), 400

    try:
        image = Image.open(file.stream).convert('RGB')
        text = pytesseract.image_to_string(image, lang='fra')

        result = {
            'fournisseur': 'Détecté : SARL Exemplex',
            'date': 'Détecté : 15/07/2025',
            'montant_ht': 'Détecté : 1200,00 €',
            'tva': 'Détecté : 240,00 €',
            'ttc': 'Détecté : 1440,00 €',
            'catégorie': 'Fournitures (IA simulée)',
            'texte_brut': text
        }
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
