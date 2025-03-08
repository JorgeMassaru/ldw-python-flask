from flask import Flask, render_template
from controllers import routes

# Criando a instância do Flask na variável app
app = Flask(__name__, template_folder='views')  # Representa o nome do arquivo
routes.init_app(app)
# Criando a primeira rota da aplicação

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
