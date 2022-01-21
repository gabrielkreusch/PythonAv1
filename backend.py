import flask
from flask import request
from config import *
from modelo import Cliente, Endereco

@app.route("/")
def inicio():
    return 'Sistema de cadastro de produtos.<br>' +\
           '<a href="/listar_clientes">Listar</a>'

@app.route("/listar_clientes")
def listar_clientes():
    return flask.render_template('listar_clientes.html')

@app.route("/listar_clientes_json")
def listar_clientes_json():
    clientes = db.session.query(Cliente).all()
    clientes_json = [x.json() for x in clientes]
    resposta = jsonify(clientes_json)
    resposta.headers.add("Access-Control-Allow-Origin", "*")
    return resposta

@app.route("/cadastrar_cliente")
def cadastrar_cliente():
    return flask.render_template('cadastrar_cliente.html')

@app.route("/inserir_cliente", methods=['post'])
def inserir_cliente():
    resposta = jsonify({ "resultado": "ok"})
    cliente_json = request.get_json()
    try:
        cliente = Cliente(**cliente_json)
        db.session.add(cliente)
        db.session.commit()
    except Exception as ex:
        resposta = jsonify({ "resultado": "erro"})
    resposta.headers.add("Access-Control-Allow-Origin", "*")
    return resposta

@app.route("/listar_enderecos_json")
def listar_enderecos_json():
    enderecos = db.session.query(Endereco).all()
    enderecos_json = [x.json() for x in enderecos]
    resposta = jsonify(enderecos_json)
    resposta.headers.add("Access-Control-Allow-Origin", "*")
    return resposta

app.run(debug=True)