import os
import requests
from bs4 import BeautifulSoup
from googlesearch import search

def search_pdfs(keywords, num_results=3):
    query = f"{keywords} filetype:pdf"
    urls = []
    for url in search(query, num_results=num_results):
        if url.endswith(".pdf"):
            urls.append(url)
    return urls

def download_pdf(url, output_dir, file_index):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        filename = os.path.join(output_dir, f"pdfp5_{file_index}.pdf")
        with open(filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        print(f"Descargado: {filename}")
    except requests.RequestException as e:
        print(f"Error al descargar {url}: {e}")

if __name__ == "__main__":
    output_dir = "D:\Proyectos\IA_TrabajosActualicado\Trabajos_IA\Proyecto4\PDFs"
    os.makedirs(output_dir, exist_ok=True)
    print("Buscando PDFs...")
    pdf_urls = search_pdfs("Impacto desaparición organismos autónomos sociedad civil México", num_results=5)
    
    if pdf_urls:
        print(f"Se encontraron {len(pdf_urls)} PDFs. Descargando...")
        for index, pdf_url in enumerate(pdf_urls, start=1):
            download_pdf(pdf_url, output_dir, index)
    else:
        print("No se encontraron PDFs.")
