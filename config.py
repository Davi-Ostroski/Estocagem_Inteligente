import os

class Config:
    """Configurações da aplicação Flask"""
    
    # Chave secreta para sessões e CSRF
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Configuração do banco de dados SQLite
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'estoque.db')
    
    # Desabilitar rastreamento de modificações (economiza memória)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configurações adicionais
    ITEMS_PER_PAGE = 20
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload
