from flask import Flask, render_template, request, redirect, url_for
import urllib.request
import json
from urllib.error import HTTPError, URLError

app = Flask(__name__)

# Lista para armazenar Pokémon
pokemon_list = []

# Dicionário para armazenar Pokémon
pokemon_dict = {}

def init_app(app):
    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/pokemon_list', methods=['GET', 'POST'])
    def pokemon_list_route():
        if request.method == 'POST':
            pokemon_name = request.form.get('pokemon_name')
            if pokemon_name:
                pokemon_list.append(pokemon_name)
                return redirect(url_for('pokemon_list_route'))
        
        return render_template('pokemon_list.html', pokemon_list=pokemon_list)

    @app.route('/pokemon_table', methods=['GET', 'POST'])
    def pokemon_table():
        if request.method == 'POST':
            pokemon_name = request.form.get('pokemon_name')
            pokemon_type = request.form.get('pokemon_type')
            if pokemon_name and pokemon_type:
                pokemon_dict[pokemon_name] = pokemon_type
                return redirect(url_for('pokemon_table'))
        
        return render_template('pokemon_table.html', pokemon_dict=pokemon_dict)

    @app.route('/api_pokemon', methods=['GET'])
    def api_pokemon():
        try:
            # Parâmetros de paginação
            limit = 12  # Número de Pokémon por página
            offset = int(request.args.get('offset', 0))  # Offset inicial (0 por padrão)

            # URL da PokeAPI com paginação
            url = f'https://pokeapi.co/api/v2/pokemon?limit={limit}&offset={offset}'

            # Criar uma requisição com cabeçalhos
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})

            # Abrir a URL e ler os dados
            res = urllib.request.urlopen(req)
            data = res.read()
            pokemon_data = json.loads(data)

            # Extrair os detalhes de cada Pokémon
            pokemons = []
            for pokemon in pokemon_data['results']:
                pokemon_url = pokemon['url']
                try:
                    # Criar uma requisição com cabeçalhos para os detalhes do Pokémon
                    pokemon_req = urllib.request.Request(pokemon_url, headers={'User-Agent': 'Mozilla/5.0'})
                    pokemon_res = urllib.request.urlopen(pokemon_req)
                    pokemon_info = json.loads(pokemon_res.read())
                    
                    # Extrair dados extras
                    types = [t['type']['name'] for t in pokemon_info['types']]  # Tipos do Pokémon
                    height = pokemon_info['height'] / 10  # Altura em metros
                    weight = pokemon_info['weight'] / 10  # Peso em quilogramas
                  
                    pokemons.append({
                    'name': pokemon_info['name'],
                    'image': pokemon_info['sprites']['front_default'],
                    'types': types,
                    'height': height,
                    'weight': weight,
                    })
                except (HTTPError, URLError) as e:
                    print(f"Erro ao buscar detalhes do Pokémon {pokemon['name']}: {e}")
                    continue  # Ignora esse Pokémon e continua para o próximo

            # Verificar se há mais páginas
            next_offset = offset + limit if pokemon_data['next'] else None
            prev_offset = offset - limit if offset > 0 else None

            return render_template('api_pokemon.html', pokemons=pokemons, next_offset=next_offset, prev_offset=prev_offset)
        
        except (HTTPError, URLError) as e:
            return f"Erro ao acessar a PokeAPI: {e}", 500
        except json.JSONDecodeError as e:
            return f"Erro ao decodificar JSON: {e}", 500
        except Exception as e:
            return f"Erro inesperado: {e}", 500

    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=4000, debug=True)