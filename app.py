from flask import Flask, redirect, url_for
from flask_login import LoginManager
from config import Config
from models import db, Usuario

def create_app(config_class=Config):
    """Factory para criar a aplicação Flask"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Inicializar extensões
    db.init_app(app)
    
    # Configurar Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor, faça login para acessar esta página.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))
    
    # Registrar blueprints
    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.produtos import produtos_bp
    from routes.movimentacoes import movimentacoes_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(produtos_bp)
    app.register_blueprint(movimentacoes_bp)
    
    # Rota raiz
    @app.route('/')
    def index():
        return redirect(url_for('dashboard.index'))
    
    # Criar tabelas e dados iniciais
    with app.app_context():
        db.create_all()
        
        # Criar usuário admin padrão se não existir
        if Usuario.query.count() == 0:
            admin = Usuario(username='admin', role='Administrador')
            admin.set_password('admin123')
            
            operador = Usuario(username='operador', role='Operador')
            operador.set_password('operador123')
            
            db.session.add(admin)
            db.session.add(operador)
            db.session.commit()
            
            print('Usuários padrão criados:')
            print('  Admin - usuário: admin, senha: admin123')
            print('  Operador - usuário: operador, senha: operador123')
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
