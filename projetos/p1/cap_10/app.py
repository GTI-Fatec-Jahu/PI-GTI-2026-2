from flask import Flask, render_template, abort, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect

from db import execute_query, execute_one

app = Flask(__name__)

# Chave provisória, só para o projeto de sala. Ela assina o cookie da session.
# Num sistema de verdade, a chave fica fora do código (o .env aparece no Capítulo 11).
app.secret_key = 'chave-provisoria-fatec-2026'

CSRFProtect(app)

categorias = ['Papelaria', 'Informática', 'Casa', 'Acessórios']


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

    produtos = execute_query(
        'SELECT id_produto, nome, categoria, preco FROM produtos WHERE nome LIKE %s ORDER BY id_produto',
        ('%' + busca + '%',),
        fetch=True,
    )

    return render_template('index.html', titulo='Catálogo de Produtos',
                           produtos=produtos, categorias=categorias, busca=busca)


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

            execute_query(
                'INSERT INTO produtos (nome, categoria, preco) VALUES (%s, %s, %s)',
                (nome, categoria, preco),
            )

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


@app.route('/produto/<int:id_produto>')
def produto(id_produto):
    produto_encontrado = execute_one(
        'SELECT id_produto, nome, categoria, preco FROM produtos WHERE id_produto = %s',
        (id_produto,),
    )

    if produto_encontrado is None:
        abort(404)

    return render_template('produto.html', produto=produto_encontrado)


@app.route('/produto/<int:id_produto>/excluir', methods=['POST'])
def excluir_produto(id_produto):
    excluido = execute_one('SELECT id_produto, nome FROM produtos WHERE id_produto = %s', (id_produto,))

    if excluido is None:
        abort(404)

    execute_query('DELETE FROM produtos WHERE id_produto = %s', (id_produto,))

    nome = excluido['nome']
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
