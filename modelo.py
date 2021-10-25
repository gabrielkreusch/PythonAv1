from os import system
from flask.json import jsonify
from config import *

import json

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(254))
    valor = db.Column(db.Float)
    quantidade = db.Column(db.Integer)

    def json(self): 
        return f"{{ 'id': {self.id}, 'nome': {self.nome}, 'valor': {self.valor}, 'quantidade': {self.quantidade} }}"

    def __str__(self):
        return str(self.id) + ", " +\
               self.nome + ", " +\
               str(self.valor) + ", " +\
               str(self.quantidade)


if __name__ == "__main__":

    if os.path.exists(arquivobd):
        os.remove(arquivobd)
    
    db.create_all()

    p1 = Produto(nome="Bolacha", valor = 1.5, quantidade = 100)

    db.session.add(p1)
    db.session.commit()

    print(p1)