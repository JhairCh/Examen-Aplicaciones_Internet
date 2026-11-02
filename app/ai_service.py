import os
from groq import Groq


def analizar_ticket(titulo, descripcion):
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return "Error: no se encontró la API Key de Groq."

    try:
        client = Groq(api_key=api_key)

        respuesta = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": """
                    Eres un asistente experto en soporte técnico.
                    Analiza los tickets y proporciona:
                    1. Categoría sugerida.
                    2. Prioridad: Baja, Media, Alta o Crítica.
                    3. Posible solución.
                    Responde en español de forma clara y breve.
                    """
                },
                {
                    "role": "user",
                    "content": f"Título: {titulo}\nDescripción: {descripcion}"
                }
            ],
            temperature=0.3
        )

        return respuesta.choices[0].message.content

    except Exception as e:
        return f"Error al analizar el ticket: {str(e)}"