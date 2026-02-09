import os
import PyPDF2
from pdf2image import convert_from_path
import pytesseract
from gtts import gTTS

# Configuration Tesseract - chemin vers les données de langue
os.environ['TESSDATA_PREFIX'] = '/usr/share/tesseract-ocr/5/tessdata'

# === À ADAPTER ===
PDF_PATH = "pdfs/02_Tissu osseux.pdf"
OUTPUT_AUDIO = "02_Tissu osseux.mp3"
LANG = "fr"  # langue pour gTTS et Tesseract

# Si tu es sous Windows, décommente et mets le bon chemin :
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_pdf(pdf_path):
    """Texte 'normal' du PDF (non OCR)."""
    text = ""
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for i, page in enumerate(reader.pages, start=1):
            page_text = page.extract_text()
            if page_text:
                text += f"\n\n--- Page {i} (texte) ---\n"
                text += page_text
    return text

def extract_text_from_images(pdf_path, lang="fra"):
    """
    OCR page par page pour éviter de saturer la RAM.
    lang='fra' pour français, 'eng' pour anglais, etc.
    """
    text = ""
    # Obtenir le nombre de pages sans tout charger
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        num_pages = len(reader.pages)

    for page_number in range(1, num_pages + 1):
        print(f"  OCR page {page_number}/{num_pages}...")
        # Ne charge qu'une seule page à la fois
        images = convert_from_path(
            pdf_path,
            first_page=page_number,
            last_page=page_number,
            dpi=150  # Réduire le DPI pour économiser la RAM (200-300 par défaut)
        )
        page_image = images[0]
        
        ocr_text = pytesseract.image_to_string(page_image, lang=lang)
        if ocr_text.strip():
            text += f"\n\n--- Page {page_number} (OCR) ---\n"
            text += ocr_text
        
        # Libérer la mémoire explicitement
        del page_image
        del images

    return text

def main():
    print("Extraction du texte 'normal' du PDF...")
    text_pdf = extract_text_from_pdf(PDF_PATH)

    print("Extraction du texte dans les images (OCR)...")
    # Pour le français, le code langue Tesseract est 'fra'
    text_ocr = extract_text_from_images(PDF_PATH, lang="fra")

    full_text = (text_pdf + "\n\n" + text_ocr).strip()

    if not full_text:
        print("Aucun texte trouvé (ni normal, ni OCR).")
        return

    # Optionnel : limiter ou nettoyer le texte
    print("Longueur du texte final :", len(full_text), "caractères")

    print("Génération de l'audio avec gTTS...")
    tts = gTTS(text=full_text, lang=LANG)
    tts.save(OUTPUT_AUDIO)

    print("Audio généré dans :", OUTPUT_AUDIO)

if __name__ == "__main__":
    main()
