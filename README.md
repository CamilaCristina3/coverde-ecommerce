# COVERDE | Agricultura Sustentável

**COVERDE** é uma plataforma de e-commerce focada em agricultura local e sustentável.  
Este projeto foi desenvolvido para conectar consumidores conscientes com produtores locais de forma justa, simples e transparente.

## ✨ Funcionalidades

- Registo e autenticação de utilizadores (consumidores e produtores)
- Publicação de produtos (por produtores)
- Carrinho de compras (para consumidores)
- Simulação de pagamento e checkout
- Filtros por categoria e pesquisa de produtos
- Página institucional, contactos e novidades

## 🎯 Objetivo

Facilitar o consumo responsável e apoiar os pequenos produtores, promovendo uma economia mais sustentável, local e solidária.

## 📦 Tecnologias

- Python + Django
- Bootstrap 5
- HTML5 / CSS3
- SQLite (modo local)
- JavaScript básico (para interações como carrinho)

## 🚀 Como executar localmente

```bash
# Clonar o projeto
git clone https://github.com/CamilaCristina3/coverde-ecommerce.git

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows

# Instalar dependências
pip install -r requirements.txt

# Migrar base de dados
python manage.py migrate

# Executar servidor
python manage.py runserver
