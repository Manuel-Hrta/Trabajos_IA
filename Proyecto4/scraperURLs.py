from googlesearch import search
import random
import time
import json
import urllib3

# Deshabilitar advertencias SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# palabras clave
KEYWORDS = [
    "como impactara el costo económico con la promocion con la nueva reforma al poder judicial", 
    "como compatibilizar la incorporacion de medidas para preservar la identitdad de los jueces con los estandares internacionales con la nueva reforma al poder judicial", "como asegurar la carrera judicial con la nueva reforma al poder judicial", 
    "como se conforman los comites de postulacion con la nueva reforma al poder judicial",
    "medias acorde a la reforma al poder judicial para evitar la captacion del crimen organizado y violencia en el contexto electoral",
    "porque la reforma no incluye a las fiscalias y a la defensoria, limitandose solo al poder judicial", 
    "Estudios para llevar acabo la Reforma al Poder Judicial de la Federacion México", 
]

# Retrasar alatoramiente entre solicitudes
def delay_request():
    delay = random.randint(10, 15)
    print(f"Esperando {delay} sgnds antes de la siguiente solicitud")
    time.sleep(delay)

# busquedador en Google
def search_google(keyword, num_results=5):
    urls = []
    try:
        for result in search(keyword, num_results=num_results):
            urls.append(result)
    except Exception as e:
        print(f"Error en busqueda hacia: '{keyword}': {e}")
    return urls


def main():
    print("Buscando en Google...")
    resultados = {}

    for keyword in KEYWORDS:
        print(f"Buscando: {keyword}")
        urls = search_google(keyword)
        print(f"Se encontraron {len(urls)} resultados para '{keyword}':")
        
        # Guardar los enlaces en el diccionario
        resultados[keyword] = urls
        
        delay_request()

    # Guardar resultados en un archivo JSON
    with open("Urls/LPJ.json", "a", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=4)

    print("\nBúsqueda completada. Enlaces guardados en 'enlaces.json'.")

if __name__ == "__main__":
    main()