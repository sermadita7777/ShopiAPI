from src.accesoDatos import AccesoDatos
import os
import pandas as pd
from pathlib import Path
from src.ia import Analista

def procesar_datos(json_respuesta):
    """
    Recibe el JSON crudo de Shopify y devuelve una lista ordenada con el Top 5.
    """
    if not json_respuesta or 'data' not in json_respuesta:
        return []

    try:
        lista_pedidos = json_respuesta.get('data', {}).get('orders', {}).get('edges', [])
    except AttributeError:
        return []

    contador_ventas = {}

    for pedido in lista_pedidos:
        lineas = pedido['node']['lineItems']['edges']
        
        for linea in lineas:
            producto = linea['node']
            nombre = producto['title']
            cantidad = producto['quantity']
            
            contador_ventas[nombre] = contador_ventas.get(nombre, 0) + cantidad

    ranking = sorted(contador_ventas.items(), key=lambda x: x[1], reverse=True)

    return ranking[:10]

def json_CSV(lista_datos):
    ruta_proyecto = Path(__file__).resolve().parent.parent
    rutaCSV = ruta_proyecto / "reporte_ventas.csv"

    try:
        df=pd.DataFrame(lista_datos,columns=['Producto','Cantidad'])
        df.to_csv(rutaCSV,index=False)

        print(f"Registro guardado en {rutaCSV}")
    except Exception as e:
        print(f"Error: {e}")

def iniciar_programa():
    print("Iniciando sistema de reportes Garza...")
    
    try:
        datos_crudos = AccesoDatos.obtener_ventas_mensuales()
    
        top_ventas = procesar_datos(datos_crudos)

        if not top_ventas:
            print("No hay ventas registradas en el último mes.")
        else:
            print("\n--- TOP 10 VENTAS MENSUALES ---")
            for posicion, (producto, cantidad) in enumerate(top_ventas, 1):
                print(f"#{posicion} | {cantidad} uds. | {producto}")
                
        print("Guardando Registro...")
        json_CSV(top_ventas)

        print("\n Análisis Inteligente:")
        conclusion=Analista.generar_resumen_ventas(top_ventas)

        print(conclusion)
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")