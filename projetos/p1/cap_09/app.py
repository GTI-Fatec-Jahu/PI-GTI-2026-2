from flask import Flask, render_template, abort, request, redirect, url_for, session, flash
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

# Chave provisória, só para o projeto de sala. Ela assina o cookie da session.
# Num sistema de verdade, a chave fica fora do código (o .env aparece no Capítulo 11).
app.secret_key = 'chave-provisoria-fatec-2026'

CSRFProtect(app)

categorias = ['Papelaria', 'Informática', 'Casa', 'Acessórios']

produtos_iniciais = [
    {'id': 1, 'nome': 'Caneta esferográfica azul', 'categoria': 'Papelaria', 'preco': 2.50},
    {'id': 2, 'nome': 'Caderno universitário 96 folhas', 'categoria': 'Papelaria', 'preco': 18.90},
    {'id': 3, 'nome': 'Mouse sem fio', 'categoria': 'Informática', 'preco': 59.90},
    {'id': 4, 'nome': 'Teclado USB', 'categoria': 'Informática', 'preco': 89.90},
    {'id': 5, 'nome': 'Garrafa térmica 500 ml', 'categoria': 'Casa', 'preco': 49.90},
    {'id': 6, 'nome': 'Mochila escolar', 'categoria': 'Acessórios', 'preco': 129.00},
    {'id': 7, 'nome': 'Fone de ouvido', 'categoria': 'Informática', 'preco': 79.90},
]


def produtos_da_sessao():
    if 'produtos' not in session:
        session['produtos'] = produtos_iniciais.copy()

    return session['produtos']


def validar_nome(nome):
    if nome == '':
        return 'Informe o nome do produto.'

    if len(nome) < 3:
        return 'O nome deve ter pelo menos 3 caracteres.'

    if len(nome) > 100:
        return 'O nome deve ter no máximo 100 caracteres.'

    return None


def validar_categoria(categoria):
    if categoria not in categorias:
        return 'Escolha uma das categorias da lista.'

    return None


def validar_preco(texto):
    if texto == '':
        return 'Informe o preço.'

    try:
        preco = float(texto)
    except ValueError:
        return 'O preço deve ser um número, como 2.50.'

    if preco > 0 and preco <= 99999.99:
        return None

    return 'O preço deve ser maior que zero e no máximo 99999.99.'


@app.route('/')
def index():
    busca = request.args.get('busca', '').strip()

    encontrados = []
    for item in produtos_da_sessao():
        if busca.lower() in item['nome'].lower():
            encontrados.append(item)

    return render_template('index.html', titulo='Catálogo de Produtos',
                           produtos=encontrados, categorias=categorias, busca=busca)


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    nome = ''
    categoria = ''
    preco_texto = ''

    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        categoria = request.form.get('categoria', '')
        preco_texto = request.form.get('preco', '').strip()

        erros = []

        erro = validar_nome(nome)
        if erro:
            erros.append(erro)

        erro = validar_categoria(categoria)
        if erro:
            erros.append(erro)

        erro = validar_preco(preco_texto)
        if erro:
            erros.append(erro)

        if erros:
            for mensagem in erros:
                flash(mensagem, 'danger')
        else:
            preco = float(preco_texto)
            produtos = produtos_da_sessao()

            maior_id = 0
            for item in produtos:
                if item['id'] > maior_id:
                    maior_id = item['id']

            novo = {'id': maior_id + 1, 'nome': nome, 'categoria': categoria, 'preco': preco}
            produtos.append(novo)
            session.modified = True

            flash(f'Produto "{nome}" cadastrado.', 'success')
            return redirect(url_for('index'))

    return render_template('cadastro.html', categorias=categorias,
                           nome=nome, categoria=categoria, preco=preco_texto)


@app.route('/contato', methods=['GET', 'POST'])
def contato():
    dados = None

    if request.method == 'POST':
        if request.form.get('novidades') == 'sim':
            novidades = 'Sim'
        else:
            novidades = 'Não'

        dados = {
            'nome': request.form['nome'],
            'email': request.form['email'],
            'retorno': request.form['retorno'],
            'assunto': request.form.get('assunto', 'Não informado'),
            'mensagem': request.form['mensagem'],
            'novidades': novidades,
        }

    return render_template('contato.html', dados=dados)


@app.route('/produto/<int:produto_id>')
def produto(produto_id):
    produto_encontrado = None
    for item in produtos_da_sessao():
        if item['id'] == produto_id:
            produto_encontrado = item

    if produto_encontrado is None:
        abort(404)

    return render_template('produto.html', produto=produto_encontrado)


@app.route('/produto/<int:produto_id>/excluir', methods=['POST'])
def produto_excluir(produto_id):
    excluido = None
    restantes = []
    for item in produtos_da_sessao():
        if item['id'] == produto_id:
            excluido = item
        else:
            restantes.append(item)

    if excluido is None:
        abort(404)

    nome = excluido['nome']

    session['produtos'] = restantes
    flash(f'Produto "{nome}" excluído.', 'success')
    return redirect(url_for('index'))


@app.errorhandler(404)
def pagina_nao_encontrada(erro):
    return render_template('404.html'), 404


@app.errorhandler(500)
def erro_no_servidor(erro):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
