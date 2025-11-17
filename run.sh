#!/bin/bash

# Script de inicialização do Sistema de Gestão de Estoque

echo "=========================================="
echo "Sistema de Gestão de Estoque"
echo "=========================================="
echo ""

# Verificar se está no diretório correto
if [ ! -f "app.py" ]; then
    echo "Erro: Execute este script no diretório do projeto!"
    exit 1
fi

# Verificar se as dependências estão instaladas
echo "Verificando dependências..."
python3.11 -c "import flask, flask_sqlalchemy, flask_login, flask_wtf" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Instalando dependências..."
    sudo pip3 install -r requirements.txt
fi

echo ""
echo "Iniciando aplicação..."
echo ""
echo "Acesse o sistema em:"
echo "  - Local: http://localhost:5000"
echo "  - Rede: http://$(hostname -I | awk '{print $1}'):5000"
echo ""
echo "Usuários padrão:"
echo "  Admin: admin / admin123"
echo "  Operador: operador / operador123"
echo ""
echo "Pressione CTRL+C para parar o servidor"
echo "=========================================="
echo ""

# Executar aplicação
python3.11 app.py
