import math
import os

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from mysql.connector import Error

from db import execute_query, execute_one, execute_insert
from validacoes import validar_nome_perfil, validar_descricao_perfil

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

CSRFProtect(app)

POR_PAGINA = 10

# Ordenações permitidas: a chave vem do endereço, o valor é o SQL fixo escrito por nós
ORDENACOES = {
    'nome': 'nome ASC',
    'recentes': 'criado_em DESC, id_perfil DESC',
}


@app.route('/')
def index():
    perfis = execute_one('SELECT COUNT(*) AS total FROM perfis')
    usuarios = execute_one('SELECT COUNT(*) AS total FROM usuarios')
    produtos = execute_one('SELECT COUNT(*) AS total FROM produtos')

    return render_template('index.html', titulo='Sistema de Gestão',
                           total_perfis=perfis['total'],
                           total_usuarios=usuarios['total'],
                           total_produtos=produtos['total'])


@app.route('/perfis')
def lista_perfis():
    busca = request.args.get('busca', '').strip()
    descricao = request.args.get('descricao', '')
    ordem = request.args.get('ordem', 'nome')
    pagina = request.args.get('pagina', 1, type=int)

    if descricao not in ('com', 'sem'):
        descricao = ''

    if ordem not in ORDENACOES:
        ordem = 'nome'

    # WHERE 1=1 é sempre verdadeiro: todo filtro preenchido entra com AND
    condicoes = ' WHERE 1=1'
    params = []

    if busca:
        condicoes += ' AND (nome LIKE %s OR descricao LIKE %s)'
        params.append('%' + busca + '%')
        params.append('%' + busca + '%')

    if descricao == 'com':
        condicoes += ' AND descricao IS NOT NULL'
    elif descricao == 'sem':
        condicoes += ' AND descricao IS NULL'

    contagem = execute_one('SELECT COUNT(*) AS total FROM perfis' + condicoes, params)
    total = contagem['total']

    total_paginas = math.ceil(total / POR_PAGINA)
    if total_paginas < 1:
        total_paginas = 1

    if pagina < 1:
        pagina = 1
    if pagina > total_paginas:
        pagina = total_paginas

    deslocamento = (pagina - 1) * POR_PAGINA

    sql = ('SELECT id_perfil, nome, descricao, criado_em FROM perfis' + condicoes
           + ' ORDER BY ' + ORDENACOES[ordem] + ' LIMIT %s OFFSET %s')
    perfis = execute_query(sql, params + [POR_PAGINA, deslocamento], fetch=True)

    return render_template('perfis.html', titulo='Perfis', perfis=perfis, total=total,
                           busca=busca, descricao=descricao, ordem=ordem,
                           pagina=pagina, total_paginas=total_paginas)


@app.route('/perfis/novo', methods=['GET', 'POST'])
def perfil_novo():
    nome = ''
    descricao = ''

    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        descricao = request.form.get('descricao', '').strip()

        erros = []

        erro = validar_nome_perfil(nome)
        if erro:
            erros.append(erro)

        erro = validar_descricao_perfil(descricao)
        if erro:
            erros.append(erro)

        if not erros:
            existente = execute_one('SELECT id_perfil FROM perfis WHERE nome = %s', (nome,))
            if existente:
                erros.append('Já existe um perfil com este nome.')

        if erros:
            for mensagem in erros:
                flash(mensagem, 'danger')
        else:
            if descricao == '':
                descricao_gravada = None
            else:
                descricao_gravada = descricao

            try:
                novo_id = execute_insert(
                    'INSERT INTO perfis (nome, descricao) VALUES (%s, %s)',
                    (nome, descricao_gravada),
                )
                flash(f'Perfil "{nome}" cadastrado (código {novo_id}).', 'success')
                return redirect(url_for('lista_perfis'))
            except Error as erro:
                if erro.errno == 1062:
                    flash('Já existe um perfil com este nome.', 'danger')
                else:
                    raise

    return render_template('perfil_form.html', nome=nome, descricao=descricao)


@app.errorhandler(404)
def pagina_nao_encontrada(erro):
    return render_template('404.html'), 404


@app.errorhandler(500)
def erro_no_servidor(erro):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
