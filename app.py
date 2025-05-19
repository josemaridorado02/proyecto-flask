import json
import os
from flask import Flask, render_template, request, abort, redirect, url_for

app = Flask(__name__)

# Función para cargar los datos del archivo JSON
def load_juegos():
    try:
        with open('juegos.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print("Error: El archivo 'juegos.json' no se encuentra en el directorio.")
        return []
    except json.JSONDecodeError:
        print("Error: El archivo 'juegos.json' tiene un formato JSON inválido.")
        return []
    except Exception as e:
        print(f"Error inesperado al cargar 'juegos.json': {e}")
        return []

juegos = load_juegos()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/juegos')
def buscar_juegos():
    return render_template('buscar_juegos.html')

@app.route('/listajuegos', methods=['POST'])
def lista_juegos():
    termino = request.form.get('termino', '').strip().lower()
    if termino:
        juegos_filtrados = [juego for juego in juegos if juego['titulo'].lower().startswith(termino)]
    else:
        juegos_filtrados = juegos
    return render_template('lista_juegos.html', juegos=juegos_filtrados)

@app.route('/juego/<id>')
def detalle_juego(id):
    juego = next((j for j in juegos if j['_id'] == id), None)
    if juego is None:
        abort(404)
    return render_template('detalle_juego.html', juego=juego)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
