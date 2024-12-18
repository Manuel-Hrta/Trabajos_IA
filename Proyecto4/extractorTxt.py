import requests
from bs4 import BeautifulSoup

# def extraer_texto_relevante(url):

def extraer_texto_relevante(url):
    try:
        # Deshabilita la verificación SSL
        response = requests.get(url, verify=False)  
        response.raise_for_status()  
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Buscar el contenedor principal del artículo (ajustar según el sitio web)
        articulo = soup.find('article')  
        if not articulo:
            articulo = soup.find('div', class_='main-content')  
        if not articulo:
            articulo = soup  # Si no se encuentra, usar todo el HTML
        
        # Eliminar datos irrelevantes
        for sidebar in articulo.find_all(['aside', 'nav', 'footer']):
            sidebar.decompose()  # Elimina estos elementos del DOM
        
        for no_relevante in articulo.find_all('div', class_=['sidebar', 'related', 'ads', 'promo', 'banner']):
            no_relevante.decompose()
        
        # Extraer encabezados y párrafos
        contenido = []
        for encabezado in articulo.find_all(['h1', 'h2', 'h3']):
            contenido.append(encabezado.get_text(strip=True))
        for parrafo in articulo.find_all('p'):
            contenido.append(parrafo.get_text(strip=True))
        
        texto_relevante = "\n".join(contenido)
        
        return texto_relevante

    except requests.RequestException as e:
        print(f"Error al acceder a la URL: {e}")
        return None

    
def main():
    
    urls = [
        "http://www.scjn.gob.mx/relaciones-institucionales/que-se-ha-dicho-sobre-la-reforma-judicial/estudios-articulos"
    
            ]
    

    for i,url in enumerate(urls, start=1):
        print("Extrayendo contenido:")
        texto = extraer_texto_relevante(url)
        
        if texto:
            print(f"art {i}")
            print("\nSe extrajo el texto:")
            print(texto)
            
            archivo = "URLs/corpus.txt"
            with open(archivo, "a", encoding="utf-8") as f:
                f.write(f"{texto}\nNewPage\n")
            print(f"\nAe fuardo el texto en: {archivo}")
        else:
            print("No se pudo extraer el texto.")
        

if __name__ == "__main__":
    main()