import json
from flask import Flask, render_template, request, abort, redirect, url_for

app = Flask(__name__)

# Cargar los datos del archivo JSON con manejo de errores
try:
    with open('juegos.json', 'r', encoding='utf-8') as file:
        juegos = json.load(file)
except FileNotFoundError:
    print("Error: El archivo 'juegos.json' no se encuentra en el directorio.")
    juegos = []
except json.JSONDecodeError:
    print("Error: El archivo 'juegos.json' tiene un formato JSON inválido.")
    juegos = []
except Exception as e:
    print(f"Error inesperado al cargar 'juegos.json': {e}")
    juegos = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/juegos')
def buscar_juegos():
    return render_template('buscar_juegos.html')

@app.route('/listajuegos', methods=['POST'])
def lista_juegos():
    # Obtener el término de búsqueda del formulario
    termino = request.form.get('termino', '').strip().lower()
    
    # Filtrar juegos según el término de búsqueda
    if termino:
        juegos_filtrados = [juego for juego in juegos if juego['titulo'].lower().startswith(termino)]
    else:
        juegos_filtrados = juegos
    
    return render_template('lista_juegos.html', juegos=juegos_filtrados)

@app.route('/juego/<id>')
def detalle_juego(id):
    # Buscar el juego por ID
    juego = next((j for j in juegos if j['_id'] == id), None)
    if juego is None:
        abort(404)  # Devolver 404 si el juego no existe
    return render_template('detalle_juego.html', juego=juego)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)