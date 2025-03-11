from flask import Flask, render_template
from controllers import routes 
# Importando o model
from models.database import db
#Importando a biblioteca OS (Comandos de sistemas operacionais)
import os


# Criando a instancia do Flask na variavel app
app = Flask(__name__, template_folder='views')  # Representa o nome do arquivo
routes.init_app(app)

dir = os.path.abspath(os.path.dirname(__file__))

#Passando o diretório do banco ao SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(dir, 'models/games.sqlite3')

# Iniciar o servidor
if __name__ == '__main__':
    db.init_app(app = app)
    #Cria o banco de dados quando a aplicação é rodada
    with app.test_request_context():
        db.create_all()
    app.run(host='localhost', port=5000, debug=True)
