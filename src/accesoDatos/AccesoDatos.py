import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
from pathlib import Path

ruta_actual=Path(__file__).resolve()
ruta_proyecto = ruta_actual.parent.parent.parent
ruta_env=ruta_proyecto/'.env'

load_dotenv(dotenv_path=ruta_env)

URL = os.getenv("SHOPIFY_URL")
TOKEN = os.getenv("SHOPIFY_TOKEN")

def obtener_ventas_mensuales():
    if not URL or not TOKEN:
        raise ValueError("Error: Faltan variables en el .env")
    
    fecha_corte = (datetime.now() - timedelta(days=30)).isoformat()
    query = f"""
        {{
        orders(first: 250, query: "created_at:>{fecha_corte}") {{
            edges {{
            node {{
                lineItems(first: 10) {{
                edges {{
                    node {{
                    title
                    quantity
                    }}
                }}
                }}
            }}
            }}
        }}
        }}
        """
    headers = {"X-Shopify-Access-Token": TOKEN}

    print("Conectando con Shopify...")

    response= requests.post(URL, json={'query': query}, headers= headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise ConnectionError(f"Error Shopify: {response.text}")
