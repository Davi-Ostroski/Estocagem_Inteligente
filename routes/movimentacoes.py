from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, Movimentacao, Produto
from forms import MovimentacaoForm
from sqlalchemy import desc

movimentacoes_bp = Blueprint('movimentacoes', __name__, url_prefix='/movimentacoes')

@movimentacoes_bp.route('/')
@login_required
def historico():
    """Histórico de movimentações"""
    # Filtros
    produto_id = request.args.get('produto_id', type=int)
    tipo = request.args.get('tipo', '')
    
    query = Movimentacao.query
    
    if produto_id:
        query = query.filter_by(id_produto=produto_id)
    
    if tipo:
        query = query.filter_by(tipo_movimentacao=tipo)
    
    movimentacoes = query.order_by(desc(Movimentacao.data_movimentacao)).all()
    produtos = Produto.query.order_by(Produto.descricao).all()
    
    return render_template('movimentacoes/historico.html', 
                         movimentacoes=movimentacoes,
                         produtos=produtos,
                         produto_id_filtro=produto_id,
                         tipo_filtro=tipo)


@movimentacoes_bp.route('/registro', methods=['GET', 'POST'])
@login_required
def registro():
    """Registro de nova movimentação"""
    form = MovimentacaoForm()
    
    # Preencher choices do select de produtos
    produtos = Produto.query.order_by(Produto.descricao).all()
    form.id_produto.choices = [(p.id, f'{p.codigo} - {p.descricao}') for p in produtos]
    
    if form.validate_on_submit():
        produto = Produto.query.get(form.id_produto.data)
        tipo = form.tipo_movimentacao.data
        quantidade = form.quantidade.data
        
        # Validar saída
        if tipo == 'Saída' and produto.quantidade_estoque < quantidade:
            flash(f'Estoque insuficiente! Disponível: {produto.quantidade_estoque}', 'danger')
            return render_template('movimentacoes/registro.html', form=form, produtos=produtos)
        
        # Criar movimentação
        movimentacao = Movimentacao(
            id_produto=produto.id,
            tipo_movimentacao=tipo,
            quantidade=quantidade,
            observacao=form.observacao.data,
            usuario_id=current_user.id
        )
        
        # Atualizar estoque
        if tipo == 'Entrada':
            produto.adicionar_estoque(quantidade)
        else:
            produto.remover_estoque(quantidade)
        
        db.session.add(movimentacao)
        db.session.commit()
        
        # Verificar alerta de estoque baixo
        if produto.esta_abaixo_minimo():
            flash(f'Atenção! O produto "{produto.descricao}" está com estoque abaixo do mínimo!', 'warning')
        
        flash(f'Movimentação de {tipo.lower()} registrada com sucesso!', 'success')
        return redirect(url_for('movimentacoes.historico'))
    
    return render_template('movimentacoes/registro.html', form=form, produtos=produtos)


@movimentacoes_bp.route('/produto/<int:produto_id>')
@login_required
def por_produto(produto_id):
    """Movimentações de um produto específico"""
    produto = Produto.query.get_or_404(produto_id)
    movimentacoes = Movimentacao.query.filter_by(id_produto=produto_id).order_by(
        desc(Movimentacao.data_movimentacao)
    ).all()
    
    return render_template('movimentacoes/por_produto.html', 
                         produto=produto,
                         movimentacoes=movimentacoes)
