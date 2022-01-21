from markupsafe import string
from sqlalchemy import Integer, false
from config import *

class Endereco(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rua = db.Column(db.String(254))
    numero = db.Column(db.Integer)
    cep = db.Column(db.String(30))
    complemento = db.Column(db.String(50))
    cidade = db.Column(db.String(30))
    bairro = db.Column(db.String(30))

    def json(self):
        return {
            'id': self.id,
            'rua': self.rua,
            'numero': self.numero,
            'cep': self.cep,
            'complemento': self.complemento,
            'cidade': self.cidade,
            'bairro': self.bairro
        }

    def __str__(self):
        return str(self.id) + ", " +\
            self.rua + ", " +\
            str(self.numero) + ", " +\
            self.cep + ", " +\
            self.complemento + ", " +\
            self.cidade + ", " +\
            self.bairro

class Pessoa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    cpf = db.Column(db.String(20))

    discriminator = db.Column('type', db.String(20), nullable=False)
    __tablename__ = 'pessoa'
    __mapper_args__ = {
        'polymorphic_on': discriminator,
        'polymorphic_identity': 'pessoa',
    }

    def __init__(self, nome="", cpf=""):
        self.nome = nome
        self.cpf = cpf

    def json(self):
        return {
            'id' : self.id,
            'nome' : self.nome,
            'cpf' : self.cpf
        }
    
    def __str__(self):
        return str(self.id) + ", " +\
            self.nome + ", " +\
            self.cpf

class Funcionario(Pessoa):
    cargo = db.Column(db.String(254))
    __tablename__ = 'funcionario'
    __mapper_args__ = {
        'polymorphic_identity': 'funcionario',
    }

    def __init__(self, nome="", cpf="", cargo=""):
        super().__init__(nome, cpf)
        self.cargo = cargo

    def json(self):
        jsonPai = super().json()
        jsonPai.update({"cargo", self.cargo})
        return jsonPai
    
    def __str__(self):
        return str(self.id) + ", " +\
            self.nome + ", " +\
            self.cpf + ", " +\
            self.cargo

class Cliente(Pessoa):
    telefone = db.Column(db.String(50))
    endereco_id = db.Column(
        db.Integer, db.ForeignKey(Endereco.id), nullable=True)
    endereco = db.relationship("Endereco")
   
    __tablename__ = 'cliente'
    __mapper_args__ = {
        'polymorphic_identity': 'cliente',
    }
    def __init__(self, nome="", cpf="", telefone="", endereco_id=0):
        super().__init__(nome, cpf)
        self.telefone = telefone
        self.endereco_id = endereco_id

    def json(self):
        jsonPai = super().json()
        jsonPai.update({'telefone' : self.telefone, 
                        'endereco_id': self.endereco_id,
                        'endereco': self.endereco.json()})
        return jsonPai
    
    def __str__(self):
        return str(self.id) + ", " +\
            self.nome + ", " +\
            self.cpf + ", " +\
            self.telefone + ", " +\
            str(self.endereco_id) + ", " +\
            str(self.endereco)

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(254))
    valor = db.Column(db.Float)
    estoque = db.Column(db.Integer)

    def json(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'valor': self.valor,
            'estoque': self.estoque
        }

    def __str__(self):
        return str(self.id) + ", " +\
            self.nome + ", " +\
            str(self.valor) + ", " +\
            str(self.estoque)

class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(254))
    cliente_id = db.Column(
        db.Integer, db.ForeignKey(Cliente.id), nullable=False)
    cliente = db.relationship("Cliente", foreign_keys=[cliente_id])

    def __init__(self, data="", cliente_id=0):
        self.data = data
        self.cliente_id = cliente_id    

    def json(self):
        return {
            "id": self.id,
            "data": self.data,
            "cliente_id": self.cliente_id,
            "cliente": self.cliente.json()
        }

    def __str__(self):
        return str(self.id) + ", " +\
            self.data + ", " +\
            str(self.cliente_id) + ", " +\
            str(self.cliente)

class PedidoDelivery(Pedido):

    def __init__(self, data="", cliente_id=0):
        super().__init__(data, cliente_id)

    def json(self):
        return super().json()

    def __str__(self):
        return super().__str__()

class PedidoEmLoja(Pedido):
    vendedor_id = db.Column(
        db.Integer, db.ForeignKey(Funcionario.id), nullable=True)
    vendedor = db.relationship("Funcionario", foreign_keys=[vendedor_id])

    def __init__(self, data="", cliente_id=0, vendedor_id=0):
        super().__init__(data, cliente_id)
        self.vendedor_id = vendedor_id

    def json(self):
        return {
            "id": self.id,
            "data": self.data,
            "cliente_id": self.cliente_id,
            "cliente": self.cliente.json(),
            'vendedor_id': self.vendedor_id,
            "vendedor": self.vendedor.json(),
        }

class Item_Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantidade = db.Column(db.Integer)

    produto_id = db.Column(
        db.Integer, db.ForeignKey(Produto.id), nullable=False)
    produto = db.relationship("Produto")

    def json(self):
        return {
            "id": self.id,
            "produto_id": self.produto_id,
            "produto": self.produto.json(),
            "quantidade": self.quantidade
        }

    def __str__(self):
        return str(self.id) + ", " +\
            str(self.produto) + ", " +\
            str(self.quantidade)  

# Testes
if __name__ == "__main__":

    if os.path.exists(arquivobd):
        os.remove(arquivobd)

    db.create_all()

    endereco = Endereco(
        rua = "Rua dos Caçadores", 
        numero = 200, 
        cep = "89040-000", 
        complemento = "Apartamento", 
        cidade = "Blumenau",
        bairro = "Velha")

    db.session.add(endereco)
    db.session.commit()

    print(endereco)

    pessoa = Pessoa(
        nome = "Gabriel", 
        cpf = "123.456.789-00")

    db.session.add(pessoa)
    db.session.commit()

    print(pessoa)

    funcionario = Funcionario(
        nome = "Pedro", 
        cpf = "987.654.321-01", 
        cargo = "Vendedor")

    db.session.add(funcionario)
    db.session.commit()

    print(funcionario)

    cliente = Cliente(
        nome = "Claudio", 
        cpf = "123.234.345-10", 
        telefone = "+55 (47) 9 9995-4545",
        endereco_id = endereco.id)

    db.session.add(cliente)
    db.session.commit()

    print(cliente)

    produto = Produto(
        nome = "Bolacha", 
        valor = 1.5, 
        estoque = 100)

    db.session.add(produto)
    db.session.commit()

    print(produto)

    pedido = Pedido(
        data = "20/01/2022", 
        cliente_id = cliente.id)

    db.session.add(pedido)
    db.session.commit()

    print(pedido)

    delivery = PedidoDelivery(
        data = "21/01/2022", 
        cliente_id = cliente.id)

    db.session.add(delivery)
    db.session.commit()

    print(delivery)

    em_loja = PedidoEmLoja(
        data = "22/01/2022", 
        cliente_id = cliente.id)

    db.session.add(em_loja)
    db.session.commit()

    print(em_loja)

    item_pedido = Item_Pedido(
        quantidade = 5, 
        produto = produto)

    db.session.add(item_pedido)
    db.session.commit()

    print(item_pedido)