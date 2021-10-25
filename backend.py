from logging import debug
from config import *
from modelo import Produto
from flask import jsonify

@app.route("/")
def inicio():
    return 'Sistema de cadastro de produtos.<br>' +\
           '<a href="/listar_produtos">Listar</a>'

@app.route("/listar_produtos")
def listar_pessoas():
    produtos = db.session.query(Produto).all()
    produtos_json = [x.json() for x in produtos]
    resposta = jsonify(produtos_json)
    resposta.headers.add("Access-Control_Allow_Origin", "*")
    return resposta

app.run(debug=True)