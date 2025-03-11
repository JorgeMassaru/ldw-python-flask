from flask_sqlalchemy import SQLAlchemy 

#Criando uma instância do SQLAlchemy
db = SQLAlchemy()

#Classe responsável por criar a entidade "Games" no banco com seus atributos
class Game(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    titulo = db.Column(db.String(150))
    ano = db.Column(db.Integer)
    categoria = db.Column(db.String(150))
    plataforma = db.Column(db.String(150))
    preco = db.Column(db.Float)
    quantidade = db.Column(db.Integer)
    
    #Método contrutor da Classe
    def __init__(self, titulo, ano, categoria, plataforma, preco, quantidade):
        self.titulo = titulo
        self.ano = ano
        self.categoria = categoria
        self.plataforma = plataforma
        self.preco = preco
        self.quantidade = quantidade