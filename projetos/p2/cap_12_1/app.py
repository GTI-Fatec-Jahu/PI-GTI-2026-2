import math
import os

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_wtf.csrf import CSRFProtect
from mysql.connector import Error

from db import execute_insert, execute_one, execute_query
from validacoes.validacoes_perfil import validar_perfil

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Liga a proteção CSRF: todo formulário POST do sistema vai precisar do token
CSRFProtect(app)

# Quantos perfis aparecem em cada página da lista
POR_PAGINA = 10

# Ordenações permitidas: a chave vem do endereço, o valor é o SQL fixo escrito por nós
ORDENACOES = {
    'nome': 'nome ASC',
    'recentes': 'criado_em DESC, id_perfil DESC',
}


# ==============================================================================
# PÁGINAS PRINCIPAIS
# ==============================================================================

@app.route('/')
def index():
    # A raiz não mostra nada: só leva para a tela de login
    return redirect(url_for('login'))


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    # Conta as linhas de cada tabela para os cartões da Home
    perfis = execute_one('SELECT COUNT(*) AS total FROM perfis')
    usuarios = execute_one('SELECT COUNT(*) AS total FROM usuarios')
    produtos = execute_one('SELECT COUNT(*) AS total FROM produtos')

    return render_template('dashboard.html', titulo='Sistema de Gestão',
                           total_perfis=perfis['total'],
                           total_usuarios=usuarios['total'],
                           total_produtos=produtos['total'])


# ==============================================================================
# PERFIS
# ==============================================================================

@app.route('/perfis')
def listar_perfis():
    # 1. Lê os filtros do endereço (?busca=...&descricao=...&ordem=...&pagina=...)
    busca = request.args.get('busca', '').strip()
    descricao = request.args.get('descricao', '')
    ordem = request.args.get('ordem', 'nome')
    pagina = request.args.get('pagina', 1, type=int)

    # Valores fora da lista permitida voltam ao padrão
    if descricao not in ('com', 'sem'):
        descricao = ''

    if ordem not in ORDENACOES:
        ordem = 'nome'

    # -------------------------------------------------------------------------
    # 2. Monta o WHERE aos poucos
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

    # -------------------------------------------------------------------------
    # 3. Conta quantos perfis passam nos filtros e calcula as páginas
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

    # -------------------------------------------------------------------------
    # 4. Busca só os perfis da página pedida
    sql = ('SELECT id_perfil, nome, descricao, criado_em FROM perfis' + condicoes
           + ' ORDER BY ' + ORDENACOES[ordem] + ' LIMIT %s OFFSET %s')
    perfis = execute_query(sql, params + [POR_PAGINA, deslocamento], fetch=True)

    return render_template('perfis/perfis_lista.html', titulo='Perfis', perfis=perfis, total=total,
                           busca=busca, descricao=descricao, ordem=ordem,
                           pagina=pagina, total_paginas=total_paginas)


@app.route('/perfis/inserir', methods=['GET', 'POST'])
def inserir_perfil():
    # Inicializa variáveis para cada campo do formulário
    nome = ''
    descricao = ''

    # Executado apenas no envio do formulário (POST)
    if request.method == 'POST':
        # 1. Coleta os dados do formulário
        nome = request.form.get('nome', '').strip()

        # 'or None' garante que string vazia vire None (gravado como NULL no MySQL)
        descricao = request.form.get('descricao', '').strip() or None

        # -------------------------------------------------------------------------
        # 2. Validação dos campos
        erros = validar_perfil(nome, descricao)

        # 3. Se houver erros, exibe as mensagens
        if erros:
            for mensagem in erros:
                flash(mensagem, 'danger')

        # -------------------------------------------------------------------------
        # 4. Se não houver erros, tenta salvar no banco
        else:
            try:
                novo_id = execute_insert(
                    'INSERT INTO perfis (nome, descricao) VALUES (%s, %s)',
                    (nome, descricao),
                )

                flash(f'Perfil "{nome}" cadastrado (código {novo_id}).', 'success')
                return redirect(url_for('listar_perfis'))

            # Trata concorrência (duplicidade no momento do insert)
            except Error as erro:
                if erro.errno == 1062:
                    flash('Já existe um perfil com este nome.', 'danger')
                else:
                    # Com o raise: Se o MySQL cair, o cabo de rede desconectar ou houver um erro de
                    # sintaxe no SQL, o Python interrompe a execução imediatamente e mostra o
                    # Traceback com o erro real no console/log.
                    raise

    # Exibe a tela em caso de GET ou se houver erros (de validação ou de nome repetido)
    return render_template('perfis/perfil_form.html', nome=nome, descricao=descricao)


# ==============================================================================
# TELAS DE ERROS
# ==============================================================================

@app.errorhandler(404)
def pagina_nao_encontrada(erro):
    return render_template('404.html'), 404


@app.errorhandler(500)
def erro_no_servidor(erro):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
