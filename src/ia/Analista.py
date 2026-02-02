import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "llama3" 

def generar_resumen_ventas(top_ventas):
    """
    Recibe la lista de ventas, crea un texto para la IA y devuelve su opinión.
    """
    # 1. Preparamos el texto que leerá la IA (El Prompt)
    texto_ventas = ", ".join([f"{prod} ({cant} uds)" for prod, cant in top_ventas])
    
    prompt = f"""
    Eres un experto analista de negocios. Tengo estos datos de ventas del último mes:
    {texto_ventas}
    
    Por favor, dame una conclusión muy breve (máximo 2 frases) sobre qué se está vendiendo mejor y qué estrategia me recomiendas.
    Responde en español profesional.
    """

    # 2. Preparamos el paquete para enviar
    payload = {
        "model": MODELO,
        "prompt": prompt,
        "stream": False 
    }

    print("La IA está pensando...")
    
    try:
        # 3. Llamada al servidor 
        response = requests.post(OLLAMA_URL, json=payload)
        
        if response.status_code == 200:
            respuesta_json = response.json()
            return respuesta_json['response']
        else:
            return f"Error IA: {response.text}"
            
    except Exception as e:
        return f"No se pudo conectar con Ollama: {e}"