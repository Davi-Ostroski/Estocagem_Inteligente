from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, Produto
from forms import ProdutoForm
from sqlalchemy import or_

produtos_bp = Blueprint('produtos', __name__, url_prefix='/produtos')

@produtos_bp.route('/')
@login_required
def lista():
    """Lista todos os produtos"""
    # Busca
    query = request.args.get('q', '')
    
    if query:
        produtos = Produto.query.filter(
            or_(
                Produto.codigo.contains(query),
                Produto.descricao.contains(query),
                Produto.categoria.contains(query)
            )
        ).all()
    else:
        produtos = Produto.query.order_by(Produto.descricao).all()
    
    return render_template('produtos/lista.html', produtos=produtos, query=query)


@produtos_bp.route('/cadastro', methods=['GET', 'POST'])
@login_required
def cadastro():
    """Cadastro de novo produto"""
    if not current_user.is_admin():
        flash('Acesso negado. Apenas administradores podem cadastrar produtos.', 'danger')
        return redirect(url_for('produtos.lista'))
    
    form = ProdutoForm()
    
    if form.validate_on_submit():
        produto = Produto(
            codigo=form.codigo.data,
            descricao=form.descricao.data,
            categoria=form.categoria.data,
            valor=form.valor.data,
            quantidade_estoque=form.quantidade_estoque.data,
            estoque_minimo=form.estoque_minimo.data
        )
        
        db.session.add(produto)
        db.session.commit()
        
        flash(f'Produto "{produto.descricao}" cadastrado com sucesso!', 'success')
        return redirect(url_for('produtos.lista'))
    
    return render_template('produtos/cadastro.html', form=form, titulo='Cadastrar Produto')


@produtos_bp.route('/<int:id>')
@login_required
def detalhes(id):
    """Detalhes de um produto"""
    produto = Produto.query.get_or_404(id)
    return render_template('produtos/detalhes.html', produto=produto)


@produtos_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar(id):
    """Editar produto existente"""
    if not current_user.is_admin():
        flash('Acesso negado. Apenas administradores podem editar produtos.', 'danger')
        return redirect(url_for('produtos.lista'))
    
    produto = Produto.query.get_or_404(id)
    form = ProdutoForm(produto_id=produto.id, obj=produto)
    
    if form.validate_on_submit():
        produto.codigo = form.codigo.data
        produto.descricao = form.descricao.data
        produto.categoria = form.categoria.data
        produto.valor = form.valor.data
        produto.quantidade_estoque = form.quantidade_estoque.data
        produto.estoque_minimo = form.estoque_minimo.data
        
        db.session.commit()
        
        flash(f'Produto "{produto.descricao}" atualizado com sucesso!', 'success')
        return redirect(url_for('produtos.detalhes', id=produto.id))
    
    return render_template('produtos/cadastro.html', form=form, titulo='Editar Produto', produto=produto)


@produtos_bp.route('/<int:id>/excluir', methods=['POST'])
@login_required
def excluir(id):
    """Excluir produto"""
    if not current_user.is_admin():
        flash('Acesso negado. Apenas administradores podem excluir produtos.', 'danger')
        return redirect(url_for('produtos.lista'))
    
    produto = Produto.query.get_or_404(id)
    descricao = produto.descricao
    
    db.session.delete(produto)
    db.session.commit()
    
    flash(f'Produto "{descricao}" excluído com sucesso!', 'success')
    return redirect(url_for('produtos.lista'))
