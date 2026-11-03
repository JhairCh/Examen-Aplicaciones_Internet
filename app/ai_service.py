
import os
import json
from groq import Groq


def analizar_ticket(titulo, descripcion, categorias, prioridades):
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return {"error": "No se encontró la API Key de Groq."}

    try:
        client = Groq(api_key=api_key)

        respuesta = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": f"""
                    Eres un asistente experto en soporte técnico.

                    Analiza el ticket y responde exclusivamente en JSON
                    con estas tres propiedades:
                    - categoria
                    - prioridad
                    - solucion

                    Categorías disponibles: {categorias}
                    Prioridades disponibles: {prioridades}

                    Selecciona exactamente una categoría y una prioridad
                    de las listas proporcionadas.
                    La solución debe ser breve y estar en español.
                    """
                },
                {
                    "role": "user",
                    "content": f"Título: {titulo}\nDescripción: {descripcion}"
                }
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )

        contenido = respuesta.choices[0].message.content
        resultado = json.loads(contenido)

        return {
            "categoria": resultado["categoria"],
            "prioridad": resultado["prioridad"],
            "solucion": resultado["solucion"]
        }

    except Exception as e:
        return {"error": f"Error al analizar el ticket: {str(e)}"}
