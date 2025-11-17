from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class Usuario(UserMixin, db.Model):
    """Modelo de usuário do sistema"""
    __tablename__ = 'usuario'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='Operador')
    
    def set_password(self, password):
        """Gera hash da senha"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verifica se a senha está correta"""
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        """Verifica se o usuário é administrador"""
        return self.role == 'Administrador'
    
    def __repr__(self):
        return f'<Usuario {self.username}>'


class Produto(db.Model):
    """Modelo de produto"""
    __tablename__ = 'produto'
    
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True, nullable=False, index=True)
    descricao = db.Column(db.String(200), nullable=False)
    categoria = db.Column(db.String(100), index=True)
    valor = db.Column(db.Numeric(10, 2), nullable=False)
    quantidade_estoque = db.Column(db.Integer, nullable=False, default=0)
    estoque_minimo = db.Column(db.Integer, nullable=False, default=0)
    data_cadastro = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relacionamento com movimentações
    movimentacoes = db.relationship('Movimentacao', backref='produto', lazy=True, cascade='all, delete-orphan')
    
    def esta_abaixo_minimo(self):
        """Verifica se o estoque está abaixo do mínimo"""
        return self.quantidade_estoque <= self.estoque_minimo
    
    def adicionar_estoque(self, quantidade):
        """Adiciona quantidade ao estoque"""
        self.quantidade_estoque += quantidade
    
    def remover_estoque(self, quantidade):
        """Remove quantidade do estoque"""
        if self.quantidade_estoque >= quantidade:
            self.quantidade_estoque -= quantidade
            return True
        return False
    
    def __repr__(self):
        return f'<Produto {self.codigo} - {self.descricao}>'


class Movimentacao(db.Model):
    """Modelo de movimentação de estoque"""
    __tablename__ = 'movimentacao'
    
    id = db.Column(db.Integer, primary_key=True)
    id_produto = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False, index=True)
    tipo_movimentacao = db.Column(db.String(20), nullable=False)  # 'Entrada' ou 'Saída'
    quantidade = db.Column(db.Integer, nullable=False)
    data_movimentacao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)
    observacao = db.Column(db.Text)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    
    # Relacionamento com usuário
    usuario = db.relationship('Usuario', backref='movimentacoes')
    
    def __repr__(self):
        return f'<Movimentacao {self.tipo_movimentacao} - Produto {self.id_produto} - Qtd {self.quantidade}>'
