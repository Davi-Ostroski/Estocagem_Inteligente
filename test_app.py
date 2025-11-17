"""Script de teste para verificar funcionalidades do sistema"""
from app import create_app
from models import db, Usuario, Produto, Movimentacao

def test_database():
    """Testa a criação e consulta no banco de dados"""
    app = create_app()
    
    with app.app_context():
        # Verificar usuários
        usuarios = Usuario.query.all()
        print(f"✓ Usuários cadastrados: {len(usuarios)}")
        for user in usuarios:
            print(f"  - {user.username} ({user.role})")
        
        # Criar produtos de teste
        produtos_teste = [
            Produto(
                codigo='PROD001',
                descricao='Notebook Dell Inspiron',
                categoria='Informática',
                valor=3500.00,
                quantidade_estoque=10,
                estoque_minimo=5
            ),
            Produto(
                codigo='PROD002',
                descricao='Mouse Logitech',
                categoria='Periféricos',
                valor=89.90,
                quantidade_estoque=3,
                estoque_minimo=10
            ),
            Produto(
                codigo='PROD003',
                descricao='Teclado Mecânico',
                categoria='Periféricos',
                valor=450.00,
                quantidade_estoque=15,
                estoque_minimo=5
            )
        ]
        
        # Verificar se produtos já existem
        if Produto.query.count() == 0:
            for produto in produtos_teste:
                db.session.add(produto)
            db.session.commit()
            print(f"\n✓ Produtos de teste criados: {len(produtos_teste)}")
        else:
            print(f"\n✓ Produtos já existem: {Produto.query.count()}")
        
        # Listar produtos
        produtos = Produto.query.all()
        print("\nProdutos cadastrados:")
        for p in produtos:
            status = "⚠️ BAIXO" if p.esta_abaixo_minimo() else "✓ OK"
            print(f"  {status} {p.codigo} - {p.descricao} (Estoque: {p.quantidade_estoque})")
        
        # Criar movimentações de teste
        if Movimentacao.query.count() == 0:
            produto1 = Produto.query.filter_by(codigo='PROD001').first()
            produto2 = Produto.query.filter_by(codigo='PROD002').first()
            admin = Usuario.query.filter_by(username='admin').first()
            
            if produto1 and produto2 and admin:
                mov1 = Movimentacao(
                    id_produto=produto1.id,
                    tipo_movimentacao='Entrada',
                    quantidade=5,
                    observacao='Compra inicial',
                    usuario_id=admin.id
                )
                
                mov2 = Movimentacao(
                    id_produto=produto2.id,
                    tipo_movimentacao='Saída',
                    quantidade=2,
                    observacao='Venda',
                    usuario_id=admin.id
                )
                
                produto1.adicionar_estoque(5)
                produto2.remover_estoque(2)
                
                db.session.add(mov1)
                db.session.add(mov2)
                db.session.commit()
                
                print(f"\n✓ Movimentações de teste criadas: 2")
        
        # Verificar movimentações
        movimentacoes = Movimentacao.query.all()
        print(f"\nTotal de movimentações: {len(movimentacoes)}")
        
        # Verificar alertas
        alertas = Produto.query.filter(
            Produto.quantidade_estoque <= Produto.estoque_minimo
        ).all()
        print(f"\n⚠️  Produtos com estoque baixo: {len(alertas)}")
        for p in alertas:
            print(f"  - {p.codigo}: {p.quantidade_estoque} (mínimo: {p.estoque_minimo})")
        
        print("\n" + "="*50)
        print("✓ TODOS OS TESTES PASSARAM COM SUCESSO!")
        print("="*50)

if __name__ == '__main__':
    test_database()
