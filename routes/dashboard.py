from flask import Blueprint, render_template
from flask_login import login_required
from models import Produto, Movimentacao
from sqlalchemy import desc

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@dashboard_bp.route('/dashboard')
@login_required
def index():
    """Dashboard principal"""
    # Estatísticas gerais
    total_produtos = Produto.query.count()
    produtos_estoque_baixo = Produto.query.filter(
        Produto.quantidade_estoque <= Produto.estoque_minimo
    ).all()
    
    # Últimas movimentações
    ultimas_movimentacoes = Movimentacao.query.order_by(
        desc(Movimentacao.data_movimentacao)
    ).limit(10).all()
    
    # Valor total em estoque
    produtos = Produto.query.all()
    valor_total_estoque = sum(float(p.valor) * p.quantidade_estoque for p in produtos)
    
    return render_template('dashboard.html',
                         total_produtos=total_produtos,
                         produtos_estoque_baixo=produtos_estoque_baixo,
                         ultimas_movimentacoes=ultimas_movimentacoes,
                         valor_total_estoque=valor_total_estoque)


@dashboard_bp.route('/alertas')
@login_required
def alertas():
    """Página de alertas de estoque baixo"""
    produtos_estoque_baixo = Produto.query.filter(
        Produto.quantidade_estoque <= Produto.estoque_minimo
    ).order_by(Produto.quantidade_estoque).all()
    
    return render_template('alertas.html', produtos=produtos_estoque_baixo)
