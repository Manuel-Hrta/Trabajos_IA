import os
from PyPDF2 import PdfReader

# Archivo donde se guardará el corpus en formato TXT
CORPUS_FILE = "PDFs\corpus.txt"

# Guardar texto en el archivo TXT
def save_to_corpus(article_text, score=5):  # Calificación predeterminada de 5
    try:
        with open(CORPUS_FILE, "a", encoding="utf-8") as file:
            file.write(f"Calificación: {score}\n")
            file.write(article_text.strip())
            file.write("\n---\n")  # Separador entre artículos
        print("Texto guardado en el corpus.txt exitosamente.")
    except Exception as e:
        print(f"Error al guardar el texto en el corpus: {e}")

# Procesar un PDF y agregarlo directamente
def add_pdf_to_corpus(file_path):
    try:
        # Leer el PDF
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:  # Evitar páginas vacías
                text += page_text.strip() + "\n"

        if not text.strip():
            print(f"El PDF {file_path} no contiene texto extraíble.")
            return

        # Agregar al corpus con formato legible
        save_to_corpus(text, score=5)
    except Exception as e:
        print(f"Error al procesar el archivo PDF {file_path}: {e}")

# Procesar un grupo de PDFs en una carpeta
def process_pdfs_in_folder(folder_path):
    try:
        for filename in os.listdir(folder_path):
            if filename.endswith(".pdf"):
                file_path = os.path.join(folder_path, filename)
                print(f"Procesando archivo: {file_path}")
                add_pdf_to_corpus(file_path)
        print("Todos los PDFs han sido procesados.")
    except Exception as e:
        print(f"Error al procesar la carpeta: {e}")

# Uso del método
if __name__ == "__main__":
    folder_path = "PDFs"  # Ruta de la carpeta con los PDFs
    os.makedirs("PDFs", exist_ok=True)  # Asegura que la carpeta exista
    process_pdfs_in_folder(folder_path)

