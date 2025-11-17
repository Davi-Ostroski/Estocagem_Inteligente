from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DecimalField, IntegerField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError, Optional
from models import Produto

class LoginForm(FlaskForm):
    """Formulário de login"""
    username = StringField('Usuário', validators=[
        DataRequired(message='Campo obrigatório'),
        Length(min=3, max=80, message='O usuário deve ter entre 3 e 80 caracteres')
    ])
    password = PasswordField('Senha', validators=[
        DataRequired(message='Campo obrigatório'),
        Length(min=4, message='A senha deve ter no mínimo 4 caracteres')
    ])


class ProdutoForm(FlaskForm):
    """Formulário de cadastro/edição de produto"""
    codigo = StringField('Código', validators=[
        DataRequired(message='Campo obrigatório'),
        Length(max=50, message='O código deve ter no máximo 50 caracteres')
    ])
    descricao = StringField('Descrição', validators=[
        DataRequired(message='Campo obrigatório'),
        Length(max=200, message='A descrição deve ter no máximo 200 caracteres')
    ])
    categoria = StringField('Categoria', validators=[
        Optional(),
        Length(max=100, message='A categoria deve ter no máximo 100 caracteres')
    ])
    valor = DecimalField('Valor (R$)', validators=[
        DataRequired(message='Campo obrigatório'),
        NumberRange(min=0.01, message='O valor deve ser maior que zero')
    ], places=2)
    quantidade_estoque = IntegerField('Quantidade em Estoque', validators=[
        DataRequired(message='Campo obrigatório'),
        NumberRange(min=0, message='A quantidade não pode ser negativa')
    ])
    estoque_minimo = IntegerField('Estoque Mínimo', validators=[
        DataRequired(message='Campo obrigatório'),
        NumberRange(min=0, message='O estoque mínimo não pode ser negativo')
    ])
    
    def __init__(self, produto_id=None, *args, **kwargs):
        super(ProdutoForm, self).__init__(*args, **kwargs)
        self.produto_id = produto_id
    
    def validate_codigo(self, field):
        """Valida se o código já existe"""
        produto = Produto.query.filter_by(codigo=field.data).first()
        if produto and (self.produto_id is None or produto.id != self.produto_id):
            raise ValidationError('Este código já está cadastrado.')


class MovimentacaoForm(FlaskForm):
    """Formulário de registro de movimentação"""
    id_produto = SelectField('Produto', coerce=int, validators=[
        DataRequired(message='Selecione um produto')
    ])
    tipo_movimentacao = SelectField('Tipo de Movimentação', 
        choices=[('Entrada', 'Entrada'), ('Saída', 'Saída')],
        validators=[DataRequired(message='Campo obrigatório')]
    )
    quantidade = IntegerField('Quantidade', validators=[
        DataRequired(message='Campo obrigatório'),
        NumberRange(min=1, message='A quantidade deve ser maior que zero')
    ])
    observacao = TextAreaField('Observação', validators=[
        Optional(),
        Length(max=500, message='A observação deve ter no máximo 500 caracteres')
    ])
