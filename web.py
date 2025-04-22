from flask import Flask, request, render_template, url_for, jsonify
from flask_socketio import SocketIO, emit
import subprocess
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
socketio = SocketIO(app)

# Función para procesar una tarjeta con el backend seleccionado
def process_card(card, backend):
    try:
        script = "authnet-.py" if backend == "auth" else "globalpay-multisites.py"  # Corrige el nombre del script
        # Ejecutar el script correspondiente y pasar los datos
        process = subprocess.run(
            ["python", script],
            input=card.strip(),
            text=True,
            capture_output=True
        )
        # Capturar la salida del script
        result = process.stdout.strip()
        # Filtrar el resultado para eliminar cualquier texto adicional
        if "=>" in result:
            filtered_result = result.split("=>", 1)  # Dividir en dos partes: tarjeta y respuesta
            response = filtered_result[1].strip()
            # Remover "CC|EXP|CVV:" de la respuesta si está presente
            response = response.replace("CC|EXP|CVV:", "").strip()
            return {"card": filtered_result[0].strip(), "result": response}
        elif not result:
            return {"card": card.strip(), "result": "Sin respuesta del script."}
        else:
            # Remover "CC|EXP|CVV:" de la respuesta si está presente
            response = result.strip().replace("CC|EXP|CVV:", "").strip()
            return {"card": card.strip(), "result": response}
    except Exception as e:
        return {"card": card.strip(), "result": f"Error al procesar: {str(e)}"}

# Página principal con el formulario
@app.route("/", methods=["GET", "POST"])
def index():
    approved_results = []
    declined_results = []
    unknown_results = []
    card_data = None

    if request.method == "POST":
        if "process" in request.form:
            # Obtener los datos del formulario
            card_data = request.form.get("card_data")
            backend = request.form.get("backend", "auth")  # Obtener el backend seleccionado
            if card_data:
                # Dividir las tarjetas por líneas y procesar cada una
                cards = card_data.strip().split("\n")
                with ThreadPoolExecutor() as executor:
                    for card in cards[:10]:  # Limitar a 10 tarjetas
                        future = executor.submit(process_card, card, backend)
                        result = future.result()
                        # Emitir el resultado dinámicamente
                        socketio.emit("card_processed", result)
                        # Clasificar el resultado
                        if "APPROVED" in result["result"]:
                            approved_results.append(result)
                        elif "DECLINED" in result["result"]:
                            declined_results.append(result)
                        else:
                            unknown_results.append(result)
        elif "clear" in request.form:
            # Limpiar los resultados
            approved_results = []
            declined_results = []
            unknown_results = []

        # Emitir evento de finalización
        socketio.emit("processing_finished")

    # Renderizar la plantilla HTML con conteo de resultados
    return render_template(
        "index.html",
        card_data=card_data,
        approved_results=approved_results,
        declined_results=declined_results,
        unknown_results=unknown_results,
        approved_count=len(approved_results),
        declined_count=len(declined_results),
        unknown_count=len(unknown_results)
    )

@app.route("/clear_results", methods=["POST"])
def clear_results():
    # Endpoint para limpiar resultados sin recargar la página
    return jsonify({"message": "Resultados limpiados"})

@app.route("/process_cards", methods=["POST"])
def process_cards():
    # Endpoint para procesar tarjetas sin recargar la página
    card_data = request.json.get("card_data", "")
    backend = request.json.get("backend", "auth")
    approved_results = []
    declined_results = []
    unknown_results = []

    if card_data:
        cards = card_data.strip().split("\n")
        with ThreadPoolExecutor() as executor:
            for card in cards[:10]:
                future = executor.submit(process_card, card, backend)
                result = future.result()
                # Emitir el resultado dinámicamente
                socketio.emit("card_processed", result)
                if "APPROVED" in result["result"]:
                    approved_results.append(result)
                elif "DECLINED" in result["result"]:
                    declined_results.append(result)
                else:
                    unknown_results.append(result)

    return jsonify({
        "approved_results": approved_results,
        "declined_results": declined_results,
        "unknown_results": unknown_results,
        "approved_count": len(approved_results),
        "declined_count": len(declined_results),
        "unknown_count": len(unknown_results)
    })

if __name__ == "__main__":
    socketio.run(app, debug=True)