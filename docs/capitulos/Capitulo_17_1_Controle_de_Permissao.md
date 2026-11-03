# Capítulo 17.1 — Controle de permissão (opcional)

**Disciplina:** Programação para Internet (ILP951)
**Professor:** Ronan Adriel Zenatti · ronan.zenatti@cps.sp.gov.br
**Fatec Jahu — 2º Semestre/2026**

---

## 🎯 Objetivos do Capítulo

Ao final deste capítulo você deverá ser capaz de:

- Explicar o que é um decorador: uma função que recebe uma função e devolve uma função nova
- Trocar as dez cópias do `if 'id_usuario' not in session` por um decorador, o `@login_required`
- Explicar por que o decorador precisa do `@wraps`, e por que o `@app.route` vai sempre por cima
- Escrever o `@perfil_required`, um decorador que recebe argumentos, para liberar uma rota só a certos perfis
- Responder com a página 403 quando o perfil não tem permissão
- Fazer o menu e os botões da lista seguirem o perfil de quem está logado, sabendo que isso é cortesia e não proteção

Este capítulo é **opcional**: o Capítulo 18 continua do código do Capítulo 17, e não deste. O Capítulo 17 deixou o sistema seguro contra quem não fez login, mas com dois incômodos: o mesmo `if` repetido em dez rotas e, principalmente, o fato de **qualquer** pessoa logada poder tudo. A Carla, que é do perfil **Usuário**, consegue abrir a edição de perfis e excluir usuários. Aqui cada perfil passa a abrir só o que lhe cabe.

## 📦 Ponto de partida

Este capítulo continua do **seu** repositório `sistema-gestao`, como ficou no fim do Capítulo 17: com o login funcionando, as dez rotas protegidas pelo `if` e a Ana, o Bruno e a Carla cadastrados com a senha `Senha123`.

Se o seu projeto não está funcionando, baixe o código do Capítulo 17 e descompacte. Depois de descompactar, crie o ambiente virtual e o `.env`, como no [Capítulo 11, Tópico 4](Capitulo_11_Projeto_Novo_e_Banco.md#topico-4-o-arquivo-env), importe o `banco.sql` no phpMyAdmin e cadastre os três perfis (**Administrador**, **Gerente** e **Usuário**) e os três usuários. O zip já traz as rotas protegidas, então o cadastro precisa ser feito antes, no zip do [Capítulo 16](Capitulo_16_UPDATE_e_DELETE_de_Usuario.md), que ainda não tem login:

➡️ [Baixar p2_cap_17.zip](../arquivos/p2_cap_17.zip)

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

---

## Tópico 1 — O decorador `@login_required`

### Antes de começar

Ligue o **Apache** e o **MySQL** no painel do XAMPP, abra a pasta `sistema-gestao` no VS Code, ative o ambiente virtual (`venv\Scripts\activate`) e confira o `git status`: deve dizer `nothing to commit, working tree clean`. Ligue o servidor com `python app.py` e deixe esse terminal rodando durante o capítulo.

### O que é um decorador

Você usa um decorador desde o [Capítulo 3](Capitulo_03_Flask.md): o `@app.route('/')` que fica em cima de cada função. Um **decorador** é uma função que recebe outra função e devolve uma função **nova**, que faz algo antes ou depois da original. A ideia deste tópico é escrever um decorador que faz, antes de qualquer rota, a conferência do login. Cada rota passa a ter uma linha, `@login_required`, no lugar das três do Capítulo 17.

No `app.py`, escreva a função **acima** da rota `login`:

```python
def login_required(funcao):
    def envolvida(*args, **kwargs):
        if 'id_usuario' not in session:
            flash('Entre para continuar.', 'warning')
            return redirect(url_for('login'))

        return funcao(*args, **kwargs)

    return envolvida
```

Leia de dentro para fora. A função `envolvida` é a rota "embrulhada": ela faz a conferência do login (as mesmas linhas do Capítulo 17) e, se a pessoa estiver logada, chama a função original (`funcao`) e devolve a resposta dela. A `login_required` recebe a rota, devolve a `envolvida`, e é a `envolvida` que passa a atender o endereço.

!!! note "Python: funções dentro de funções, `*args` e `**kwargs`"
    Uma função pode ser escrita dentro de outra, e pode ser devolvida com `return` **sem os parênteses** (`return envolvida` entrega a função, e `return envolvida()` a executaria). O `*args, **kwargs` é a forma de dizer "receba o que vier e repasse tudo": a rota `usuario_editar`, por exemplo, recebe o `id_usuario`, e a `envolvida` precisa entregá-lo à função original sem saber de antemão quantos argumentos existem.

### Usar em uma rota

Em `lista_usuarios`, **apague** as três linhas do `if` e coloque o decorador **abaixo** do `@app.route`:

```python
@app.route('/usuarios')
@login_required
def lista_usuarios():
    usuarios = execute_query(SELECT_USUARIO + ' ORDER BY u.nome', fetch=True)

    return render_template('usuarios.html', titulo='Usuários', usuarios=usuarios)
```

Salve e teste, como no Capítulo 17: logado, `/usuarios` abre; depois de **Sair**, `/usuarios` leva ao login, com a faixa amarela. Uma linha faz o que faziam as três.

### O erro que aparece na segunda rota

Faça o mesmo na `lista_perfis`: apague o `if` e coloque `@login_required` embaixo do `@app.route`. Salve. O servidor **não sobe**, e o terminal mostra:

```
AssertionError: View function mapping is overwriting an existing endpoint function: envolvida
```

O Flask identifica cada rota pelo **nome da função** (é o nome que o `url_for` usa). Depois do decorador, as duas funções, `lista_usuarios` e `lista_perfis`, passaram a se chamar `envolvida`, e o Flask recusa duas rotas com o mesmo nome. O conserto é o decorador `@wraps`, que copia o nome (e a documentação) da função original para a nova. Ele fica na biblioteca padrão do Python. No começo do `app.py`, acrescente a importação:

```python
from functools import wraps
```

E, na `login_required`, coloque o `@wraps(funcao)` em cima da `envolvida`:

```python
def login_required(funcao):
    @wraps(funcao)
    def envolvida(*args, **kwargs):
        if 'id_usuario' not in session:
            flash('Entre para continuar.', 'warning')
            return redirect(url_for('login'))

        return funcao(*args, **kwargs)

    return envolvida
```

Salve: o servidor sobe de novo, e as duas listas continuam protegidas.

### As outras oito rotas

Agora o ganho. Em cada uma destas oito funções, **apague** as três linhas do `if 'id_usuario' not in session` e acrescente `@login_required` embaixo do `@app.route`: `index`, `perfil_novo`, `perfil_editar`, `perfil_excluir`, `usuario_novo`, `usuario_detalhe`, `usuario_editar` e `usuario_excluir`. No `usuario_excluir`, o bloco que impede a exclusão do próprio usuário **continua**: ele é outra regra, e não faz parte do login. Por exemplo:

```python
@app.route('/usuarios/<int:id_usuario>/excluir', methods=['POST'])
@login_required
def usuario_excluir(id_usuario):
    if id_usuario == session['id_usuario']:
        flash('Você não pode excluir o seu próprio usuário.', 'danger')
        return redirect(url_for('lista_usuarios'))

    usuario = execute_one(
```

!!! danger "O `@app.route` sempre fica por cima"
    A ordem dos decoradores importa. O que está **mais perto da função** é aplicado primeiro, e o `@app.route` precisa receber a função **já embrulhada**. Faça o teste com a rota `index`: troque a ordem, deixando o `@login_required` **acima** do `@app.route('/')`. Salve, saia do sistema e abra `/`: a página inicial **abre** para qualquer pessoa. O `@app.route` registrou a função original, sem o embrulho, e o `@login_required` embrulhou uma função que o Flask não usa. Não dá erro nenhum, a rota só fica aberta. **Desfaça a troca** e deixe o `@app.route` em cima.

Salve e confira, sem estar logado, as rotas `/`, `/perfis`, `/perfis/novo`, `/usuarios`, `/usuarios/novo`, `/usuarios/1` e `/usuarios/1/editar`: todas levam a `/login`. Logado como Ana, tudo funciona como no Capítulo 17. O comportamento é o mesmo, mas a conferência agora vive em **um** lugar: se a mensagem mudar, muda uma vez.

```bash
git add .
git commit -m "Troca o if do login por um decorador @login_required"
git push
```

---

## Tópico 2 — O decorador `@perfil_required`

### A dor: todo mundo que entra pode tudo

Entre como a **Carla** (`carla@exemplo.com`, perfil **Usuário**). No menu aparecem **Perfis** e **Usuários**, e ambos abrem. Digite `/perfis/novo` e crie um perfil. Abra a edição de qualquer usuário. O sistema sabe quem a Carla é, mas ainda não sabe **o que ela pode fazer**. O `perfil` que o login gravou na `session` (Capítulo 17) é exatamente a informação que falta.

### A tabela de permissões

Antes de programar, uma decisão de projeto. A tabela diz quem pode abrir o quê:

| Área | Administrador | Gerente | Usuário |
|---|---|---|---|
| Início | ✔ | ✔ | ✔ |
| Usuários: lista e detalhe | ✔ | ✔ | 403 |
| Usuários: novo, editar e excluir | ✔ | 403 | 403 |
| Perfis: as quatro rotas | ✔ | 403 | 403 |

O **403** é o código HTTP de "você está identificado, mas não tem permissão". Ele é diferente do que o login resolve: quem **não entrou** é mandado a `/login`, e quem **entrou sem permissão** recebe o 403.

### Um decorador com o perfil fixo

Escreva, no `app.py`, **logo abaixo** da `login_required`, um decorador que só deixa passar o **Administrador**. Ele é parecido com o anterior:

```python
def apenas_administrador(funcao):
    @wraps(funcao)
    def envolvida(*args, **kwargs):
        if session.get('perfil') != 'Administrador':
            abort(403)

        return funcao(*args, **kwargs)

    return envolvida
```

O `session.get('perfil')` devolve `None` quando a chave não existe, em vez de dar erro (como o `.get` do `request.form`). Use-o na `perfil_novo`, **embaixo** do `@login_required`:

```python
@app.route('/perfis/novo', methods=['GET', 'POST'])
@login_required
@apenas_administrador
def perfil_novo():
```

Salve e teste: como **Ana**, `/perfis/novo` abre. Como **Carla** (saia e entre de novo, porque a `session` guarda o perfil do login), a página mostra um **Forbidden** simples, em inglês, que é a página padrão do Flask para o 403.

### A página 403

Troque a página padrão por uma do sistema, como as de 404 e 500 (Capítulo 6). Crie o `templates/403.html`:

```html
{% extends 'base.html' %}

{% block titulo_aba %}Acesso negado — Sistema de Gestão{% endblock %}

{% block conteudo %}
  <div class="text-center py-5">
    <h1 class="display-1">403</h1>
    <p class="lead">O seu perfil não tem permissão para abrir esta página.</p>
    <a href="{{ url_for('index') }}" class="btn btn-primary">Voltar para o início</a>
  </div>
{% endblock %}
```

E, no `app.py`, acrescente o tratador **acima** do `@app.errorhandler(404)`:

```python
@app.errorhandler(403)
def acesso_negado(erro):
    return render_template('403.html'), 403
```

Salve e repita o teste com a Carla em `/perfis/novo`: agora a página 403 do sistema, com o menu e o botão **Voltar para o início**.

### Tornar o decorador reutilizável

Falta o Gerente: ele abre a **lista** de usuários, mas não o `/perfis`. O `apenas_administrador` serve a um perfil só. A saída é um decorador que **recebe o nome dos perfis permitidos**, usado assim: `@perfil_required('Administrador', 'Gerente')`. Ele é um decorador com argumentos, e isso exige uma camada a mais. **Apague** o `apenas_administrador` e escreva no lugar:

```python
def perfil_required(*permitidos):
    def decorador(funcao):
        @wraps(funcao)
        def envolvida(*args, **kwargs):
            if session.get('perfil') not in permitidos:
                abort(403)

            return funcao(*args, **kwargs)

        return envolvida

    return decorador
```

São três funções, cada uma com um papel e uma hora em que é chamada:

| Função | Quem a chama | Quando |
|---|---|---|
| `perfil_required('Administrador')` | O Python, ao ler o `@perfil_required(...)` | Uma vez, quando o servidor carrega o `app.py`. Devolve o `decorador` |
| `decorador(funcao)` | O Python, logo em seguida | Uma vez, com a rota. Devolve a `envolvida` |
| `envolvida(...)` | O Flask | **A cada pedido** à rota. É ela que confere o perfil |

O `*permitidos` recebe os nomes que foram escritos entre parênteses e os junta numa lista (`('Administrador', 'Gerente')`), e o `not in` pergunta se o perfil de quem está logado **não** está entre eles. Na `perfil_novo`, troque o decorador antigo pelo novo, sem mudar o resultado:

```python
@app.route('/perfis/novo', methods=['GET', 'POST'])
@login_required
@perfil_required('Administrador')
def perfil_novo():
```

Salve e repita: a Ana abre, a Carla recebe o 403. A ordem dos dois decoradores **também importa**: o `@login_required` vem primeiro, para a pessoa sem login ir ao `/login`. Se o `@perfil_required` viesse sozinho, quem não entrou receberia o 403, e não o convite para entrar.

### Aplicar a tabela

Acrescente o `@perfil_required` às outras rotas, **embaixo** do `@login_required`, conforme a tabela:

| Função | Decoradores abaixo do `@app.route` |
|---|---|
| `index` | `@login_required` (já tem) |
| `lista_perfis`, `perfil_editar`, `perfil_excluir` | `@login_required` e `@perfil_required('Administrador')` |
| `lista_usuarios`, `usuario_detalhe` | `@login_required` e `@perfil_required('Administrador', 'Gerente')` |
| `usuario_novo`, `usuario_editar`, `usuario_excluir` | `@login_required` e `@perfil_required('Administrador')` |

Por exemplo, a lista de usuários fica:

```python
@app.route('/usuarios')
@login_required
@perfil_required('Administrador', 'Gerente')
def lista_usuarios():
```

Salve e confira, entrando como cada usuário e digitando os endereços:

| Endereço | Ana (Administrador) | Bruno (Gerente) | Carla (Usuário) |
|---|---|---|---|
| `/` | abre | abre | abre |
| `/perfis`, `/perfis/novo`, `/perfis/1/editar` | abre | 403 | 403 |
| `/usuarios`, `/usuarios/1` | abre | abre | 403 |
| `/usuarios/novo`, `/usuarios/1/editar` | abre | 403 | 403 |

Um endereço que não existe continua dando 404 (`/usuarios/99999` para a Ana e o Bruno), e os `POST` de exclusão seguem a mesma tabela: um Gerente que enviasse um `POST` para `/usuarios/3/excluir` receberia o 403 antes de qualquer consulta.

```bash
git add .
git commit -m "Adiciona o decorador @perfil_required e a página 403"
git push
```

---

## Tópico 3 — O menu e os botões seguem o perfil

### A dor: um link que leva ao 403

Entre como o **Bruno** (Gerente). O menu mostra **Perfis**, e o clique leva ao 403. Abra **Usuários**: a lista mostra **Novo usuário**, **Editar** e **Excluir**, e todos levam ao 403. O sistema nega o acesso, mas oferece o botão. Menu e botões devem mostrar só o que a pessoa pode usar.

No `templates/base.html`, envolva os itens **Perfis** e **Usuários** em um `if` cada um. Os outros itens do menu (**Início**, o nome e o **Sair**) continuam como estão:

```html
          {% if session['perfil'] == 'Administrador' %}
          <li class="nav-item">
            <a class="nav-link {% if request.endpoint in ['lista_perfis', 'perfil_novo', 'perfil_editar'] %}active{% endif %}" href="{{ url_for('lista_perfis') }}">Perfis</a>
          </li>
          {% endif %}
          {% if session['perfil'] in ['Administrador', 'Gerente'] %}
          <li class="nav-item">
            <a class="nav-link {% if request.endpoint in ['lista_usuarios', 'usuario_novo', 'usuario_detalhe', 'usuario_editar'] %}active{% endif %}" href="{{ url_for('lista_usuarios') }}">Usuários</a>
          </li>
          {% endif %}
```

Os testes do Jinja repetem a tabela de permissões: **Perfis** só para o Administrador, **Usuários** para o Administrador e o Gerente. Salve e entre como cada usuário: a Ana vê os dois itens, o Bruno só **Usuários**, e a Carla nenhum dos dois (só **Início**).

Falta a lista de usuários. No `templates/usuarios.html`, envolva o botão **Novo usuário** e os botões **Editar** e **Excluir**, que só o Administrador usa:

```html
    {% if session['perfil'] == 'Administrador' %}
    <a href="{{ url_for('usuario_novo') }}" class="btn btn-primary">Novo usuário</a>
    {% endif %}
```

```html
          {% if session['perfil'] == 'Administrador' %}
          <a href="{{ url_for('usuario_editar', id_usuario=usuario.id_usuario) }}" class="btn btn-sm btn-outline-primary">Editar</a>
          <button type="button" class="btn btn-sm btn-outline-danger" data-bs-toggle="modal" data-bs-target="#modalExcluir" onclick="prepararExclusao({{ usuario.id_usuario }})">Excluir</button>
          {% endif %}
```

O **Ver** fica de fora do `if`, porque o Gerente também pode abrir o detalhe. Salve e entre como o Bruno: a lista mostra só o botão **Ver**, e como a Ana ela continua completa.

!!! warning "Esconder é cortesia, proteger é a rota"
    Entre como o Bruno e digite `/usuarios/novo` na barra de endereço: o 403 aparece, mesmo sem nenhum botão que leve até lá. Os `if` do menu e dos botões servem para a pessoa não ver o que não pode usar, e **não impedem nada**. Quem impede são os decoradores das rotas, do Tópico 2. Se um dia um `if` de template for esquecido, o sistema continua seguro; se um decorador for esquecido, a rota fica aberta.

!!! note "Os limites deste controle"
    O `@perfil_required` compara o **nome** do perfil gravado na `session` no momento do login. Duas consequências:

    - Se a Ana mudar o perfil do Bruno de **Gerente** para **Usuário**, a mudança só vale no **próximo login** dele: a `session` dele ainda diz Gerente.
    - Se alguém renomear o perfil **Administrador** (Capítulo 13), nenhum administrador passa mais nos decoradores, porque o nome `'Administrador'` está escrito no código. O sistema não impede essa troca, então ela exige cuidado.

```bash
git add .
git commit -m "Faz o menu e os botões seguirem o perfil de quem está logado"
git push
```

---

## Os arquivos completos do capítulo

O `app.py`:

```python
import os
from functools import wraps

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash, abort, session
from flask_wtf.csrf import CSRFProtect
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash

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


def login_required(funcao):
    @wraps(funcao)
    def envolvida(*args, **kwargs):
        if 'id_usuario' not in session:
            flash('Entre para continuar.', 'warning')
            return redirect(url_for('login'))

        return funcao(*args, **kwargs)

    return envolvida


def perfil_required(*permitidos):
    def decorador(funcao):
        @wraps(funcao)
        def envolvida(*args, **kwargs):
            if session.get('perfil') not in permitidos:
                abort(403)

            return funcao(*args, **kwargs)

        return envolvida

    return decorador


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'id_usuario' in session:
        return redirect(url_for('index'))

    email = ''

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        senha = request.form.get('senha', '')

        usuario = execute_one(
            'SELECT u.id_usuario, u.nome, u.senha, p.nome AS perfil '
            'FROM usuarios u '
            'JOIN perfis p ON p.id_perfil = u.perfil_id '
            'WHERE u.email = %s',
            (email,),
        )

        if usuario is not None and check_password_hash(usuario['senha'], senha):
            session.clear()
            session['id_usuario'] = usuario['id_usuario']
            session['nome'] = usuario['nome']
            session['perfil'] = usuario['perfil']
            flash(f'Você entrou como {usuario["nome"]}.', 'success')
            return redirect(url_for('index'))

        flash('E-mail ou senha incorretos.', 'danger')

    return render_template('login.html', email=email)


@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    flash('Você saiu do sistema.', 'success')

    return redirect(url_for('login'))


@app.route('/')
@login_required
def index():
    perfis = execute_one('SELECT COUNT(*) AS total FROM perfis')
    usuarios = execute_one('SELECT COUNT(*) AS total FROM usuarios')
    produtos = execute_one('SELECT COUNT(*) AS total FROM produtos')

    return render_template('index.html', titulo='Sistema de Gestão',
                           total_perfis=perfis['total'],
                           total_usuarios=usuarios['total'],
                           total_produtos=produtos['total'])


@app.route('/perfis')
@login_required
@perfil_required('Administrador')
def lista_perfis():
    perfis = execute_query(
        'SELECT id_perfil, nome, descricao, criado_em FROM perfis ORDER BY nome',
        fetch=True,
    )

    return render_template('perfis.html', titulo='Perfis', perfis=perfis)


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
@login_required
@perfil_required('Administrador')
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

    return render_template('perfil_form.html', acao='criar', id_perfil=None,
                           nome=nome, descricao=descricao)


@app.route('/perfis/<int:id_perfil>/editar', methods=['GET', 'POST'])
@login_required
@perfil_required('Administrador')
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

    return render_template('perfil_form.html', acao='editar', id_perfil=id_perfil,
                           nome=nome, descricao=descricao)


@app.route('/perfis/<int:id_perfil>/excluir', methods=['POST'])
@login_required
@perfil_required('Administrador')
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
@login_required
@perfil_required('Administrador', 'Gerente')
def lista_usuarios():
    usuarios = execute_query(SELECT_USUARIO + ' ORDER BY u.nome', fetch=True)

    return render_template('usuarios.html', titulo='Usuários', usuarios=usuarios)


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
@login_required
@perfil_required('Administrador')
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

    return render_template('usuario_form.html', acao='criar', id_usuario=None,
                           dados=request.form, perfis=perfis, ufs=UFS)


@app.route('/usuarios/<int:id_usuario>')
@login_required
@perfil_required('Administrador', 'Gerente')
def usuario_detalhe(id_usuario):
    usuario = execute_one(SELECT_USUARIO + ' WHERE u.id_usuario = %s', (id_usuario,))
    if usuario is None:
        abort(404)

    return render_template('usuario_detalhe.html', usuario=usuario)


@app.route('/usuarios/<int:id_usuario>/editar', methods=['GET', 'POST'])
@login_required
@perfil_required('Administrador')
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

    return render_template('usuario_form.html', acao='editar', id_usuario=id_usuario,
                           dados=dados, perfis=perfis, ufs=UFS)


@app.route('/usuarios/<int:id_usuario>/excluir', methods=['POST'])
@login_required
@perfil_required('Administrador')
def usuario_excluir(id_usuario):
    if id_usuario == session['id_usuario']:
        flash('Você não pode excluir o seu próprio usuário.', 'danger')
        return redirect(url_for('lista_usuarios'))

    usuario = execute_one(
        'SELECT id_usuario, nome FROM usuarios WHERE id_usuario = %s',
        (id_usuario,),
    )
    if usuario is None:
        abort(404)

    execute_query('DELETE FROM usuarios WHERE id_usuario = %s', (id_usuario,))
    flash(f'Usuário "{usuario["nome"]}" excluído.', 'success')

    return redirect(url_for('lista_usuarios'))


@app.errorhandler(403)
def acesso_negado(erro):
    return render_template('403.html'), 403


@app.errorhandler(404)
def pagina_nao_encontrada(erro):
    return render_template('404.html'), 404


@app.errorhandler(500)
def erro_no_servidor(erro):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
```

O `templates/403.html` é o do Tópico 2. O `templates/base.html`:

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{% block titulo_aba %}Sistema de Gestão{% endblock %}</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="{{ url_for('static', filename='estilo.css') }}">
</head>
<body>

  <nav class="navbar navbar-expand-lg" data-bs-theme="dark">
    <div class="container">
      <a class="navbar-brand" href="{{ url_for('index') }}">Sistema de Gestão</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse"
              data-bs-target="#menu" aria-controls="menu" aria-expanded="false"
              aria-label="Abrir o menu">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="menu">
        <ul class="navbar-nav ms-auto align-items-lg-center">
          {% if 'id_usuario' in session %}
          <li class="nav-item">
            <a class="nav-link {% if request.endpoint == 'index' %}active{% endif %}" href="{{ url_for('index') }}">Início</a>
          </li>
          {% if session['perfil'] == 'Administrador' %}
          <li class="nav-item">
            <a class="nav-link {% if request.endpoint in ['lista_perfis', 'perfil_novo', 'perfil_editar'] %}active{% endif %}" href="{{ url_for('lista_perfis') }}">Perfis</a>
          </li>
          {% endif %}
          {% if session['perfil'] in ['Administrador', 'Gerente'] %}
          <li class="nav-item">
            <a class="nav-link {% if request.endpoint in ['lista_usuarios', 'usuario_novo', 'usuario_detalhe', 'usuario_editar'] %}active{% endif %}" href="{{ url_for('lista_usuarios') }}">Usuários</a>
          </li>
          {% endif %}
          <li class="nav-item">
            <span class="navbar-text ms-lg-3 me-lg-3">{{ session['nome'] }} · {{ session['perfil'] }}</span>
          </li>
          <li class="nav-item">
            <form action="{{ url_for('logout') }}" method="post">
              <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
              <button type="submit" class="btn btn-sm btn-outline-light">Sair</button>
            </form>
          </li>
          {% else %}
          <li class="nav-item">
            <a class="nav-link {% if request.endpoint == 'login' %}active{% endif %}" href="{{ url_for('login') }}">Entrar</a>
          </li>
          {% endif %}
        </ul>
      </div>
    </div>
  </nav>

  <main class="container my-4">
    {% for tipo, mensagem in get_flashed_messages(with_categories=true) %}
    <div class="alert alert-{{ tipo }} alert-dismissible fade show" role="alert">
      {{ mensagem }}
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Fechar"></button>
    </div>
    {% endfor %}

    {% block conteudo %}{% endblock %}
  </main>

  <footer class="text-center text-body-secondary py-3">
    <p class="mb-0">Sistema de Gestão · Fatec Jahu · ILP951 · 2026</p>
  </footer>

  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js"></script>
  {% block scripts %}{% endblock %}

</body>
</html>
```

O `templates/usuarios.html`:

```html
{% extends 'base.html' %}

{% block titulo_aba %}{{ titulo }} — Sistema de Gestão{% endblock %}

{% block conteudo %}
  <div class="d-flex justify-content-between align-items-center mb-3">
    <h1 class="h2 mb-0">{{ titulo }}</h1>
    {% if session['perfil'] == 'Administrador' %}
    <a href="{{ url_for('usuario_novo') }}" class="btn btn-primary">Novo usuário</a>
    {% endif %}
  </div>

  <table class="table table-striped table-hover">
    <thead class="table-light">
      <tr>
        <th>Código</th>
        <th>Nome</th>
        <th>CPF</th>
        <th>Cidade</th>
        <th>Nascimento</th>
        <th>Perfil</th>
        <th class="text-end">Ações</th>
      </tr>
    </thead>
    <tbody>
      {% for usuario in usuarios %}
      <tr>
        <td>{{ usuario.id_usuario }}</td>
        <td>
          <span id="nome_usuario_{{ usuario.id_usuario }}">{{ usuario.nome }}</span><br>
          <small class="text-body-secondary">{{ usuario.email }}</small>
        </td>
        <td>{{ usuario.cpf|cpf_oculto }}</td>
        <td>{{ usuario.cidade|default('—', true) }}{% if usuario.estado %}/{{ usuario.estado }}{% endif %}</td>
        <td>{{ usuario.data_nascimento|data_br }}</td>
        <td>{% include '_badge_perfil.html' %}</td>
        <td class="text-end">
          <a href="{{ url_for('usuario_detalhe', id_usuario=usuario.id_usuario) }}" class="btn btn-sm btn-outline-primary">Ver</a>
          {% if session['perfil'] == 'Administrador' %}
          <a href="{{ url_for('usuario_editar', id_usuario=usuario.id_usuario) }}" class="btn btn-sm btn-outline-primary">Editar</a>
          <button type="button" class="btn btn-sm btn-outline-danger" data-bs-toggle="modal" data-bs-target="#modalExcluir" onclick="prepararExclusao({{ usuario.id_usuario }})">Excluir</button>
          {% endif %}
        </td>
      </tr>
      {% else %}
      <tr>
        <td colspan="7" class="text-center text-body-secondary py-4">Nenhum usuário cadastrado ainda.</td>
      </tr>
      {% endfor %}
    </tbody>
  </table>

  <div class="modal fade" id="modalExcluir" tabindex="-1" aria-labelledby="tituloModalExcluir" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h2 class="modal-title h5" id="tituloModalExcluir">Excluir usuário</h2>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Fechar"></button>
        </div>
        <form id="formExcluir" action="" method="post">
          <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
          <div class="modal-body">
            <p class="mb-0">Excluir o usuário <strong id="nomeExcluir"></strong>? Esta ação não pode ser desfeita.</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">Cancelar</button>
            <button type="submit" class="btn btn-danger">Excluir</button>
          </div>
        </form>
      </div>
    </div>
  </div>
{% endblock %}

{% block scripts %}
<script>
  function prepararExclusao(id) {
    const nome = document.getElementById('nome_usuario_' + id).textContent;
    document.getElementById('nomeExcluir').textContent = nome;
    document.getElementById('formExcluir').action = '/usuarios/' + id + '/excluir';
  }
</script>
{% endblock %}
```

Os demais arquivos (`db.py`, `validacoes.py`, `login.html`, `index.html`, `perfis.html`, `perfil_form.html`, `usuario_form.html`, `usuario_detalhe.html`, `_badge_perfil.html`, `404.html`, `500.html`, `estilo.css`, `testar_conexao.py`) são os do Capítulo 17.

---

## 📦 Código deste capítulo

Compare com o seu projeto. Este capítulo é opcional, então o **Capítulo 18 não parte deste zip**, e sim do zip do Capítulo 17. O zip tem o `app.py`, o `db.py`, o `validacoes.py`, o `testar_conexao.py`, o `banco.sql`, o `.env.example`, o `.gitignore`, o `requirements.txt`, a pasta `templates` (com o novo `403.html`) e a pasta `static`. O ambiente virtual e o `.env` **não** vão no zip: crie-os como no Capítulo 11.

➡️ [Baixar p2_cap_17_1.zip](../arquivos/p2_cap_17_1.zip)

---

## 🃏 Flashcards de Revisão

Tente responder mentalmente antes de abrir.

??? question "O que é um decorador?"
    É uma função que recebe outra função e devolve uma função nova, que faz algo antes ou depois da original. O `@app.route` é um decorador, e o `@login_required` é outro: ele embrulha a rota com a conferência do login.

??? question "Por que o `@login_required` precisa do `@wraps(funcao)`?"
    Porque o Flask identifica cada rota pelo nome da função. Sem o `@wraps`, todas as rotas embrulhadas passam a se chamar `envolvida`, e o Flask recusa a segunda com o erro `View function mapping is overwriting an existing endpoint function`. O `@wraps` copia o nome da função original para a nova.

??? question "Por que o `@app.route` fica sempre por cima dos outros decoradores?"
    Porque o decorador mais próximo da função é aplicado primeiro, e o `@app.route` precisa registrar a função **já embrulhada**. Se o `@login_required` ficar acima, o Flask registra a função original, sem a conferência, e a rota abre para todo mundo, sem nenhum erro avisando.

??? question "Por que o `@perfil_required` tem três funções, uma dentro da outra?"
    Porque ele recebe argumentos (`@perfil_required('Administrador')`). A primeira função recebe os nomes e devolve o decorador, o decorador recebe a rota e devolve a função embrulhada, e esta é a que confere o perfil a cada pedido.

??? question "Qual a diferença entre o redirect para o login e a página 403?"
    O redirect é para quem **não entrou**: o sistema não sabe quem é, e pede o login. O 403 é para quem **entrou, mas o perfil não tem permissão**: o sistema sabe quem é, e nega. Por isso o `@login_required` vem antes do `@perfil_required`.

??? question "Se o menu já esconde o item, por que a rota ainda precisa do `@perfil_required`?"
    Porque esconder um link não impede ninguém de digitar o endereço. O menu é só cortesia, para a pessoa não ver o que não pode usar. A proteção de verdade está nos decoradores das rotas, que valem mesmo para quem digita o endereço ou envia um `POST` direto.

---

## 📝 Resumo

O `@login_required` troca as dez cópias do `if` por uma linha por rota: é uma função que recebe a rota e devolve uma versão embrulhada com a conferência do login, e o `@wraps` mantém o nome da rota para o Flask não confundir as funções. O `@perfil_required('Administrador', 'Gerente')` é um decorador com argumentos, em três camadas, que compara o perfil guardado na `session` com os nomes permitidos e responde com a página 403 quando o perfil não está entre eles. A ordem importa: o `@app.route` por cima, depois o `@login_required`, depois o `@perfil_required`. O menu e os botões da lista seguem o perfil, mas isso só poupa a pessoa de ver o que não pode usar: a proteção está nas rotas. Como o perfil é lido da `session`, uma mudança de perfil só vale no próximo login. O Capítulo 18 continua do código do Capítulo 17, com o cadastro de produtos.

---

## 🔗 Navegação

⬅️ [Capítulo 17 — Login](Capitulo_17_Login.md) · 🔒 Capítulo 18 — em breve.

---

*Fatec Jahu · ILP951 · Prof. Ronan Adriel Zenatti · 2026*
