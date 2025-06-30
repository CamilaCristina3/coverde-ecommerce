# 🌱 COVERDE - Plataforma Ecológica de Comércio Local

![Django](https://img.shields.io/badge/Django-5.2-green?style=flat&logo=django)
![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![License](https://img.shields.io/badge/license-MIT-brightgreen.svg)
![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)

**COVERDE** é uma aplicação web para unir produtores locais a consumidores conscientes, promovendo o comércio justo, sustentável e direto de hortícolas e frutas.

---

## 🚀 Funcionalidades

- 👤 Registo e login para **produtores** e **consumidores**
- 🛒 Carrinho de compras com verificação de stock
- 📦 Gestão de produtos e pedidos pelos produtores
- 💳 Checkout simples e resumo do pedido
- 📊 Dashboards distintos para cada tipo de utilizador
- 🧾 Validação de dados como NIF, email, telefone
- 📷 Upload de imagens para perfis e produtos
- 💬 Mensagens e notificações com feedback imediato

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia     | Versão  | Descrição                          |
|----------------|---------|------------------------------------|
| Django         | 5.2     | Framework web Python               |
| Python         | 3.11    | Linguagem principal                |
| SQLite         | Padrão  | Base de dados (pode usar PostgreSQL) |
| Bootstrap      | 5       | Estilo e componentes UI            |
| jQuery / AJAX  | Opcional| Para interações assíncronas        |
| Font Awesome   | 6       | Ícones                             |

---

## 📷 Capturas de Ecrã (sugestão)

> *(Adiciona imagens na pasta `docs/images` e referencia aqui com `![desc](docs/images/...)`)*
- `homepage.png` – Página inicial
- `dashboard_produtor.png` – Painel do produtor
- `carrinho.png` – Carrinho de compras
- `checkout.png` – Confirmação de pedido

---

## 📦 Instalação Local

```bash
# Clonar o repositório
git clone https://github.com/seu-usuario/coverde-ecommerce.git
cd coverde-ecommerce

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Criar base de dados e aplicar migrations
python manage.py migrate

# Criar superusuário para acessar o admin
python manage.py createsuperuser

# Iniciar servidor local
python manage.py runserver

🔑 Exemplo de Login


| Tipo       | Email                                                 | Senha        |
| ---------- | ----------------------------------------------------- | ------------ |
| Admin      | [admin@coverde.pt](mailto:admin@coverde.pt)           | \*\*\*\*\*\* |
| Produtor   | [produtor@coverde.pt](mailto:produtor@coverde.pt)     | \*\*\*\*\*\* |
| Consumidor | [consumidor@coverde.pt](mailto:consumidor@coverde.pt) | \*\*\*\*\*\* |


🗂 Estrutura do Projeto


coverde-ecommerce/
│
├── coverde_ecommerce/     # App principal
│   ├── templates/
│   ├── views/
│   ├── models.py
│   └── urls.py
├── static/                # Arquivos estáticos
├── media/                 # Imagens de produtos e perfis
├── manage.py
└── README.md

🧪 Testes
# Rodar testes unitários
python manage.py test

🌍 Deploy
 Pode ser publicado em Render, PythonAnywhere, Heroku ou Railway.app

Configurações recomendadas:

DEBUG=False

ALLOWED_HOSTS=['suaurl.com'

STATIC_ROOT e MEDIA_ROOT configurados

📄 Licença
Distribuído sob a licença MIT. Veja LICENSE para mais detalhes.

👨‍💻 Desenvolvido por
Nome : Camila Cristina Cuambe Esteves - Estudante de Licenciatuara em Informatica de Gestão 
Projeto criado no âmbito de Trabalho da Unidade Curricular DPI ].

⭐ Contribuições
Fique à vontade para abrir uma issue, propor uma feature, ou enviar um pull request.

