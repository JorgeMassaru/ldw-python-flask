from flask import render_template, request, redirect, url_for
#Importando o Model
from models.database import db, Game
# Essa biblioteca serve para ler uma determinada url
import urllib
import json

jogadores = []

gamelist = [{'titulo': 'CS-GO',
             'ano': 2012,
             'categoria': 'FPS Online'}]
  
def init_app(app):
    @app.route('/')
    # View Function -> Função de visualização
    def home():
        return render_template('index.html')

    @app.route('/games', methods=['GET', 'POST'])
    def games():
         # criando um dicionario = lista q nao pode ser mudada com varios atributos
        game = gamelist[0]
        if request.method == 'POST':
            if request.form.get('jogador'):
                jogadores.append(request.form.get('jogador'))
                return redirect(url_for('games'))
            
        return render_template('games.html', game=game, jogadores=jogadores)
    
    @app.route('/cadgames', methods=['GET', 'POST'])
    def cadgames():
        if request.method == 'POST':
            form_data = request.form.to_dict()
            gamelist.append(form_data)
            return(redirect(url_for('cadgames')))
            
        return render_template('cadgames.html', gamelist=gamelist)
    
    @app.route('/apigames', methods=['GET', 'POST'])
    # Passando parâmetros para a rota
    @app.route('/apigames/<int:id>', methods=['GET', 'POST'])
    #Definindo que o parâmetro é opcional
    def apigames(id=None):
        url = 'http://www.freetogame.com/api/games'
        res = urllib.request.urlopen(url)
        # print(res)
        data = res.read()
        gamesjson = json.loads(data)
        
        if id:
            ginfo = []
            for g in gamesjson:
                if g['id'] == id:
                    ginfo = g
                    break
            if ginfo:
                return render_template('gameinfo.html', ginfo=ginfo)
            else:
                return f'Game com a ID {id} não foi encontrado.'
        
        return render_template('apigames.html', gamesjson=gamesjson)
    
    #Rota com CRUD de jogos
    @app.route('/estoque', methods=['GET', 'POST'])
    def estoque():
        if request.method == 'POST':
            # Cadastra um novo jogo 
            newgame = Game(request.form['titulo'], request.form['ano'], request.form['categoria'], request.form['plataforma'], request.form['preco'], request.form['quantidade'])
            db.session.add(newgame)
            db.session.commit()
            return redirect(url_for('estoque'))
        
        # Método do SQLAlchemy que faz um select no banco na tabela Games
        gamesestoque = Game.query.all()
        return render_template('estoque.html', gamesestoque=gamesestoque)
    

    
    