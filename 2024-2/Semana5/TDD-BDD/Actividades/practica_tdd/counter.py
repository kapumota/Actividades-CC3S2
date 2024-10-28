from flask import Flask
import status

app = Flask(__name__)

COUNTERS = {}

@app.route("/counters/<name>", methods=["POST"])
def create_counter(name):
    """Crea un contador"""
    app.logger.info(f"Solicitud para crear el contador: {name}")
    global COUNTERS

    # Verifica si el contador ya existe
    if name in COUNTERS:
        return {"message": f"El contador {name} ya existe"}, status.HTTP_409_CONFLICT

    # Si no existe, inicializa el contador en 0
    COUNTERS[name] = 0
    return {name: COUNTERS[name]}, status.HTTP_201_CREATED
