import os

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_wtf.csrf import CSRFProtect
from mysql.connector import Error
from werkzeug.security import generate_password_hash

from db import execute_query, execute_one, execute_insert
from validacoes import (
    UFS, validar_nome_perfil, validar_descricao_perfil,
    validar_nome_usuario, validar_email, validar_senha, validar_celular,
    validar_cpf, validar_data_nascimento, validar_cep, validar_estado,
    validar_tamanho, formatar_celular, formatar_cpf, formatar_cep,
)

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

CSRFProtect(app)

# As colunas que as telas de usuário leem. A senha fica de fora de propósito: o que não é
# lido do banco não tem como vazar para a página.
SELECT_USUARIO = (
    'SELECT u.id_usuario, u.nome, u.email, u.celular, u.data_nascimento, u.cpf, '
    'u.perfil_id, u.cep, u.endereco, u.numero, u.complemento, u.cidade, u.estado, '
    'u.criado_em, u.atualizado_em, p.nome AS perfil, p.descricao AS perfil_descricao '
    'FROM usuarios u '
    'JOIN perfis p ON p.id_perfil = u.perfil_id'
)


@app.template_filter('data_br')
def data_br(valor):
    if valor is None:
        return '—'

    return valor.strftime('%d/%m/%Y')


@app.template_filter('data_hora_br')
def data_hora_br(valor):
    if valor is None:
        return '—'

    return valor.strftime('%d/%m/%Y às %H:%M')


@app.template_filter('cpf_oculto')
def cpf_oculto(cpf):
    if cpf is None:
        return '—'

    return '***.' + cpf[4:11] + '-**'


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    perfis = execute_one('SELECT COUNT(*) AS total FROM perfis')
    usuarios = execute_one('SELECT COUNT(*) AS total FROM usuarios')
    produtos = execute_one('SELECT COUNT(*) AS total FROM produtos')

    return render_template('dashboard.html', titulo='Sistema de Gestão',
                           total_perfis=perfis['total'],
                           total_usuarios=usuarios['total'],
                           total_produtos=produtos['total'])


@app.route('/perfis')
def lista_perfis():
    perfis = execute_query(
        'SELECT id_perfil, nome, descricao, criado_em FROM perfis ORDER BY nome',
        fetch=True,
    )

    return render_template('perfis/perfis_lista.html', titulo='Perfis', perfis=perfis)


def conferir_perfil(nome, descricao, id_perfil):
    erros = []

    erro = validar_nome_perfil(nome)
    if erro:
        erros.append(erro)

    erro = validar_descricao_perfil(descricao)
    if erro:
        erros.append(erro)

    if not erros:
        existente = execute_one(
            'SELECT id_perfil FROM perfis WHERE nome = %s AND id_perfil <> %s',
            (nome, id_perfil),
        )
        if existente:
            erros.append('Já existe um perfil com este nome.')

    return erros


@app.route('/perfis/novo', methods=['GET', 'POST'])
def perfil_novo():
    nome = ''
    descricao = ''

    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        descricao = request.form.get('descricao', '').strip()

        erros = conferir_perfil(nome, descricao, 0)

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

    return render_template('perfis/perfil_form.html', acao='criar', id_perfil=None,
                           nome=nome, descricao=descricao)


@app.route('/perfis/<int:id_perfil>/editar', methods=['GET', 'POST'])
def perfil_editar(id_perfil):
    perfil = execute_one(
        'SELECT id_perfil, nome, descricao FROM perfis WHERE id_perfil = %s',
        (id_perfil,),
    )
    if perfil is None:
        abort(404)

    nome = perfil['nome']
    descricao = perfil['descricao']
    if descricao is None:
        descricao = ''

    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        descricao = request.form.get('descricao', '').strip()

        erros = conferir_perfil(nome, descricao, id_perfil)

        if erros:
            for mensagem in erros:
                flash(mensagem, 'danger')
        else:
            if descricao == '':
                descricao_gravada = None
            else:
                descricao_gravada = descricao

            try:
                execute_query(
                    'UPDATE perfis SET nome = %s, descricao = %s WHERE id_perfil = %s',
                    (nome, descricao_gravada, id_perfil),
                )
                flash(f'Perfil "{nome}" atualizado.', 'success')
                return redirect(url_for('lista_perfis'))
            except Error as erro:
                if erro.errno == 1062:
                    flash('Já existe um perfil com este nome.', 'danger')
                else:
                    raise

    return render_template('perfis/perfil_form.html', acao='editar', id_perfil=id_perfil,
                           nome=nome, descricao=descricao)


@app.route('/perfis/<int:id_perfil>/excluir', methods=['POST'])
def perfil_excluir(id_perfil):
    perfil = execute_one(
        'SELECT id_perfil, nome FROM perfis WHERE id_perfil = %s',
        (id_perfil,),
    )
    if perfil is None:
        abort(404)

    usuarios = execute_one(
        'SELECT COUNT(*) AS total FROM usuarios WHERE perfil_id = %s',
        (id_perfil,),
    )
    if usuarios['total'] > 0:
        flash(f'O perfil "{perfil["nome"]}" tem {usuarios["total"]} usuário(s) e não pode ser excluído.', 'danger')
        return redirect(url_for('lista_perfis'))

    try:
        execute_query('DELETE FROM perfis WHERE id_perfil = %s', (id_perfil,))
        flash(f'Perfil "{perfil["nome"]}" excluído.', 'success')
    except Error as erro:
        if erro.errno == 1451:
            flash(f'O perfil "{perfil["nome"]}" está em uso e não pode ser excluído.', 'danger')
        else:
            raise

    return redirect(url_for('lista_perfis'))


@app.route('/usuarios')
def lista_usuarios():
    usuarios = execute_query(SELECT_USUARIO + ' ORDER BY u.nome', fetch=True)

    return render_template('usuarios/usuarios_lista.html', titulo='Usuários', usuarios=usuarios)


def vazio_para_none(valor):
    if valor == '':
        return None

    return valor


def texto_ou_vazio(valor):
    if valor is None:
        return ''

    return str(valor)


def conferir_perfil_do_usuario(perfil_txt):
    try:
        id_perfil = int(perfil_txt)
    except ValueError:
        return 'Selecione um perfil.'

    perfil = execute_one(
        'SELECT id_perfil FROM perfis WHERE id_perfil = %s',
        (id_perfil,),
    )
    if perfil is None:
        return 'Selecione um perfil válido.'

    return None


def ler_formulario(form):
    campos = {}
    campos['nome'] = form.get('nome', '').strip()
    campos['email'] = form.get('email', '').strip().lower()
    campos['senha'] = form.get('senha', '')
    campos['confirmacao'] = form.get('confirmacao', '')
    campos['celular'] = form.get('celular', '').strip()
    campos['data_nascimento'] = form.get('data_nascimento', '').strip()
    campos['cpf'] = form.get('cpf', '').strip()
    campos['perfil_id'] = form.get('perfil_id', '')
    campos['cep'] = form.get('cep', '').strip()
    campos['endereco'] = form.get('endereco', '').strip()
    campos['numero'] = form.get('numero', '').strip()
    campos['complemento'] = form.get('complemento', '').strip()
    campos['cidade'] = form.get('cidade', '').strip()
    campos['estado'] = form.get('estado', '')

    return campos


def conferir_usuario(campos, id_usuario):
    erros = []

    erro = validar_nome_usuario(campos['nome'])
    if erro:
        erros.append(erro)

    erro = validar_email(campos['email'])
    if erro:
        erros.append(erro)
    else:
        existente = execute_one(
            'SELECT id_usuario FROM usuarios WHERE email = %s AND id_usuario <> %s',
            (campos['email'], id_usuario),
        )
        if existente:
            erros.append('Já existe um usuário com este e-mail.')

    if id_usuario == 0 or campos['senha'] != '' or campos['confirmacao'] != '':
        erro = validar_senha(campos['senha'], campos['confirmacao'])
        if erro:
            erros.append(erro)

    erro = conferir_perfil_do_usuario(campos['perfil_id'])
    if erro:
        erros.append(erro)

    erro = validar_celular(campos['celular'])
    if erro:
        erros.append(erro)

    erro = validar_cpf(campos['cpf'])
    if erro:
        erros.append(erro)
    else:
        cpf_formatado = formatar_cpf(campos['cpf'])
        if cpf_formatado != '':
            existente = execute_one(
                'SELECT id_usuario FROM usuarios WHERE cpf = %s AND id_usuario <> %s',
                (cpf_formatado, id_usuario),
            )
            if existente:
                erros.append('Já existe um usuário com este CPF.')

    erro = validar_data_nascimento(campos['data_nascimento'])
    if erro:
        erros.append(erro)

    erro = validar_cep(campos['cep'])
    if erro:
        erros.append(erro)

    erro = validar_tamanho(campos['endereco'], 'endereço', 255)
    if erro:
        erros.append(erro)

    erro = validar_tamanho(campos['numero'], 'número', 20)
    if erro:
        erros.append(erro)

    erro = validar_tamanho(campos['complemento'], 'complemento', 100)
    if erro:
        erros.append(erro)

    erro = validar_tamanho(campos['cidade'], 'cidade', 100)
    if erro:
        erros.append(erro)

    erro = validar_estado(campos['estado'])
    if erro:
        erros.append(erro)

    return erros


@app.route('/usuarios/novo', methods=['GET', 'POST'])
def usuario_novo():
    if request.method == 'POST':
        campos = ler_formulario(request.form)

        erros = conferir_usuario(campos, 0)

        if erros:
            for mensagem in erros:
                flash(mensagem, 'danger')
        else:
            try:
                novo_id = execute_insert(
                    'INSERT INTO usuarios (nome, email, senha, celular, data_nascimento, cpf, '
                    'perfil_id, cep, endereco, numero, complemento, cidade, estado) '
                    'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    (
                        campos['nome'],
                        campos['email'],
                        generate_password_hash(campos['senha']),
                        vazio_para_none(formatar_celular(campos['celular'])),
                        vazio_para_none(campos['data_nascimento']),
                        vazio_para_none(formatar_cpf(campos['cpf'])),
                        int(campos['perfil_id']),
                        vazio_para_none(formatar_cep(campos['cep'])),
                        vazio_para_none(campos['endereco']),
                        vazio_para_none(campos['numero']),
                        vazio_para_none(campos['complemento']),
                        vazio_para_none(campos['cidade']),
                        vazio_para_none(campos['estado']),
                    ),
                )
                flash(f'Usuário "{campos["nome"]}" cadastrado (código {novo_id}).', 'success')
                return redirect(url_for('lista_usuarios'))
            except Error as erro:
                if erro.errno == 1062:
                    flash('Já existe um usuário com este e-mail ou este CPF.', 'danger')
                else:
                    raise

    perfis = execute_query('SELECT id_perfil, nome FROM perfis ORDER BY nome', fetch=True)

    return render_template('usuarios/usuario_form.html', acao='criar', id_usuario=None,
                           dados=request.form, perfis=perfis, ufs=UFS)


@app.route('/usuarios/<int:id_usuario>')
def usuario_detalhe(id_usuario):
    usuario = execute_one(SELECT_USUARIO + ' WHERE u.id_usuario = %s', (id_usuario,))
    if usuario is None:
        abort(404)

    return render_template('usuarios/usuario_detalhe.html', usuario=usuario)


@app.route('/usuarios/<int:id_usuario>/editar', methods=['GET', 'POST'])
def usuario_editar(id_usuario):
    usuario = execute_one(SELECT_USUARIO + ' WHERE u.id_usuario = %s', (id_usuario,))
    if usuario is None:
        abort(404)

    dados = {}
    for chave in usuario:
        dados[chave] = texto_ou_vazio(usuario[chave])

    if request.method == 'POST':
        campos = ler_formulario(request.form)

        erros = conferir_usuario(campos, id_usuario)

        if erros:
            for mensagem in erros:
                flash(mensagem, 'danger')
        else:
            sql = (
                'UPDATE usuarios SET nome = %s, email = %s, celular = %s, '
                'data_nascimento = %s, cpf = %s, perfil_id = %s, cep = %s, '
                'endereco = %s, numero = %s, complemento = %s, cidade = %s, estado = %s'
            )
            params = [
                campos['nome'],
                campos['email'],
                vazio_para_none(formatar_celular(campos['celular'])),
                vazio_para_none(campos['data_nascimento']),
                vazio_para_none(formatar_cpf(campos['cpf'])),
                int(campos['perfil_id']),
                vazio_para_none(formatar_cep(campos['cep'])),
                vazio_para_none(campos['endereco']),
                vazio_para_none(campos['numero']),
                vazio_para_none(campos['complemento']),
                vazio_para_none(campos['cidade']),
                vazio_para_none(campos['estado']),
            ]

            if campos['senha'] != '':
                sql += ', senha = %s'
                params.append(generate_password_hash(campos['senha']))

            sql += ' WHERE id_usuario = %s'
            params.append(id_usuario)

            try:
                execute_query(sql, params)
                flash(f'Usuário "{campos["nome"]}" atualizado.', 'success')
                return redirect(url_for('lista_usuarios'))
            except Error as erro:
                if erro.errno == 1062:
                    flash('Já existe um usuário com este e-mail ou este CPF.', 'danger')
                else:
                    raise

        dados = request.form

    perfis = execute_query('SELECT id_perfil, nome FROM perfis ORDER BY nome', fetch=True)

    return render_template('usuarios/usuario_form.html', acao='editar', id_usuario=id_usuario,
                           dados=dados, perfis=perfis, ufs=UFS)


@app.route('/usuarios/<int:id_usuario>/excluir', methods=['POST'])
def usuario_excluir(id_usuario):
    usuario = execute_one(
        'SELECT id_usuario, nome FROM usuarios WHERE id_usuario = %s',
        (id_usuario,),
    )
    if usuario is None:
        abort(404)

    execute_query('DELETE FROM usuarios WHERE id_usuario = %s', (id_usuario,))
    flash(f'Usuário "{usuario["nome"]}" excluído.', 'success')

    return redirect(url_for('lista_usuarios'))


@app.errorhandler(404)
def pagina_nao_encontrada(erro):
    return render_template('404.html'), 404


@app.errorhandler(500)
def erro_no_servidor(erro):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
