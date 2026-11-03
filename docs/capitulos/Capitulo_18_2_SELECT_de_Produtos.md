# Capítulo 18.2 — SELECT de produtos (opcional)

**Disciplina:** Programação para Internet (ILP951)
**Professor:** Ronan Adriel Zenatti · ronan.zenatti@cps.sp.gov.br
**Fatec Jahu — 2º Semestre/2026**

---

## 🎯 Objetivos do Capítulo

Ao final deste capítulo você deverá ser capaz de:

- Ler os produtos do banco com `SELECT` e mostrá-los em uma tabela com `for` e `else`
- Criar um filtro Jinja próprio (`moeda`) que escreve o preço em reais, como `R$ 3.499,90`
- Escolher a cor de um selo do Bootstrap por faixa de estoque, com `if`, `elif` e `else`
- Mostrar a miniatura da foto a partir do caminho gravado no banco, e um quadrado cinza quando não há foto

Este capítulo é **opcional**: o Capítulo 18 constrói o CRUD inteiro de produtos em um só arquivo, e este percorre só a **lista**: o `SELECT`, o filtro `moeda`, os selos de estoque e a miniatura da foto, em um arquivo menor e com o seu próprio zip. O Capítulo 19 parte do zip do Capítulo 18, e não deste. Ao final, a página **Produtos** deixa de ser provisória e mostra o que está no banco.

## 📦 Ponto de partida

Este capítulo continua do **seu** repositório `sistema-gestao`, como ficou no fim do Capítulo 18.1 (ou do Tópico 5 do Capítulo 18): com o cadastro de produto funcionando, a foto gravada em `static/uploads` e a página `/produtos` ainda provisória.

Se o seu projeto não está funcionando, baixe o código de Capítulo 18.1 e descompacte. Depois de descompactar, crie o ambiente virtual e o `.env`, como no [Capítulo 11, Tópico 4](Capitulo_11_Projeto_Novo_e_Banco.md#topico-4-o-arquivo-env), e importe o `banco.sql` no phpMyAdmin:

➡️ [Baixar p2_cap_18_1.zip](../arquivos/p2_cap_18_1.zip)

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

---

## Tópico 1 — A lista de produtos (SELECT)

### Antes de começar

Ligue o **Apache** e o **MySQL** no painel do XAMPP. Abra a pasta `sistema-gestao` no VS Code, o terminal (`Ctrl + '`), ative o ambiente virtual e confira o Git:

```bash
venv\Scripts\activate
git status
```

O `git status` deve dizer `nothing to commit, working tree clean`. Ligue o servidor com `python app.py` e deixe esse terminal rodando durante o capítulo (use um segundo terminal, o ícone **+**, para o Git). Abra **http://127.0.0.1:5000**, entre com a Ana (`ana@exemplo.com`, senha `Senha123`) e abra **Produtos** no menu: a página provisória, com o botão **Novo produto**.

Para a lista ter o que mostrar, cadastre estes quatro produtos pelo formulário **Novo produto** (se você já os cadastrou, pule esta parte), e **um quinto, com foto**: o `Mouse sem fio`, preço `89,90`, estoque `10`, categoria **Periféricos**, com uma imagem `.jpg` ou `.png` qualquer do seu computador. Os valores foram escolhidos para ter um produto com estoque alto, baixo e zerado, um inativo e um sem categoria:

| Nome | Descrição | Preço | Estoque | Categoria | Ativo |
|---|---|---|---|---|---|
| Notebook Gamer | Tela de 15,6 polegadas, 16 GB de memória | `3.499,90` | `12` | Informática | sim |
| Teclado Mecânico | (vazia) | `129,90` | `3` | Periféricos | sim |
| Fone de Ouvido | Sem fio, com cancelamento de ruído | `249` | `40` | Áudio | sim |
| Cabo HDMI 2m | (vazia) | `25,00` | `0` | Sem categoria | **não** (desmarque o interruptor) |

### A consulta

A lista precisa ler as colunas da tabela. Como no recurso `usuarios`, as colunas ficam em uma constante no topo do `app.py`, para que a lista e a edição leiam sempre as mesmas. Acrescente **depois** da constante `SELECT_USUARIO`:

```python
# As colunas que as telas de produto leem
SELECT_PRODUTO = (
    'SELECT id_produto, nome, descricao, categoria, preco, estoque, foto, ativo, '
    'criado_em, atualizado_em '
    'FROM produtos'
)
```

A constante termina no `FROM produtos`, sem `WHERE` nem `ORDER BY`: quem usa a constante completa o comando. Agora troque a rota `lista_produtos` para ler o banco:

```python
@app.route('/produtos')
def lista_produtos():
    if 'id_usuario' not in session:
        flash('Entre para continuar.', 'warning')
        return redirect(url_for('login'))

    produtos = execute_query(SELECT_PRODUTO + ' ORDER BY nome', fetch=True)

    return render_template('produtos.html', titulo='Produtos', produtos=produtos)
```

O `execute_query(..., fetch=True)` devolve uma **lista de dicionários**, um por produto, ordenada por nome. O `fetch=True` é o que diz "quero as linhas de volta" (o `INSERT` e o `UPDATE` não pedem).

### A tabela, uma coluna por vez

Troque o conteúdo do `produtos.html` por uma tabela que começa só com o código e o nome. Mantenha o cabeçalho com o botão **Novo produto**, e troque o aviso provisório por:

```html
  <table class="table table-striped table-hover align-middle">
    <thead class="table-light">
      <tr>
        <th>Código</th>
        <th>Nome</th>
        <th>Preço</th>
      </tr>
    </thead>
    <tbody>
      {% for produto in produtos %}
      <tr>
        <td>{{ produto.id_produto }}</td>
        <td>{{ produto.nome }}</td>
        <td>{{ produto.preco }}</td>
      </tr>
      {% else %}
      <tr>
        <td colspan="3" class="text-center text-body-secondary py-4">Nenhum produto cadastrado ainda.</td>
      </tr>
      {% endfor %}
    </tbody>
  </table>
```

O `for` repete a linha `<tr>` para cada produto. O `{% else %}` do próprio `for` roda quando a lista está vazia, e mostra a mensagem em vez de uma tabela sem linhas. Salve e recarregue **Produtos**: os produtos cadastrados aparecem. Olhe a coluna **Preço**: `3499.90`, `129.90`, `249.00`. É o que o `Decimal` tem de texto, com ponto decimal e sem milhar, e não o jeito brasileiro de ler dinheiro.

### O filtro `moeda`

Poderia ser resolvido em cada tela com `replace`, mas a expressão ficaria repetida, e esse é o problema que os Capítulos 5 e 6 deixaram anotado. O Flask permite criar um **filtro próprio**, uma função que o template chama com o `|`, como o `data_br` e o `cpf_oculto` que você já tem. Acrescente no `app.py`, **depois** do filtro `cpf_oculto`:

```python
def formatar_numero(valor):
    # 1234.5 vira '1.234,50': o Python escreve 1,234.50, e as trocas acertam a pontuação
    texto = f'{valor:,.2f}'
    texto = texto.replace(',', 'X').replace('.', ',').replace('X', '.')

    return texto


@app.template_filter('moeda')
def moeda(valor):
    return 'R$ ' + formatar_numero(valor)
```

!!! note "Python: `f'{valor:,.2f}'`"
    Dentro de uma `f-string`, o que vem depois dos dois-pontos é a formatação: `.2f` pede 2 casas decimais, e a vírgula pede separador de milhar. Só que o Python escreve no padrão americano, `3,499.90`. As trocas acertam: a vírgula vira `X` (um marcador provisório), o ponto vira vírgula, e o `X` vira ponto, dando `3.499,90`. Se trocasse direto uma vírgula por ponto e depois o ponto por vírgula, os dois se atropelariam. O `formatar_numero` não escreve o `R$` de propósito: a edição vai usá-lo no campo de preço, onde o `R$` já está na tela.

O `@app.template_filter('moeda')` registra a função com o nome `moeda`, que é o que se escreve depois do `|` no template. Troque a célula do preço no `produtos.html`:

```html
        <td>{{ produto.preco|moeda }}</td>
```

Salve e recarregue: o notebook aparece como `R$ 3.499,90`, o teclado como `R$ 129,90` e o fone como `R$ 249,00`.

### Mais colunas: categoria, estoque e situação

Acrescente os cabeçalhos **Estoque** e **Situação** depois do **Preço**:

```html
        <th>Estoque</th>
        <th>Situação</th>
```

Um estoque de 3 unidades e um de 300 não deveriam ter a mesma aparência. A célula do estoque usa o `if / elif / else` do Capítulo 5, agora para escolher a **cor** de um selo (*badge*) do Bootstrap. Acrescente depois da célula do preço:

```html
        <td>
          {% if produto.estoque == 0 %}
            <span class="badge text-bg-danger">Sem estoque</span>
          {% elif produto.estoque < 5 %}
            <span class="badge text-bg-warning">Estoque baixo ({{ produto.estoque }})</span>
          {% else %}
            <span class="badge text-bg-success">Em estoque ({{ produto.estoque }})</span>
          {% endif %}
        </td>
```

E a célula da situação. A coluna `ativo` chega como `1` ou `0`, e para o Jinja o `0` é falso:

```html
        <td>
          {% if produto.ativo %}
            <span class="badge text-bg-primary">Ativo</span>
          {% else %}
            <span class="badge text-bg-secondary">Inativo</span>
          {% endif %}
        </td>
```

Por último, a categoria vai embaixo do nome, em letra pequena, como o e-mail na lista de usuários. Troque a célula do nome por:

```html
        <td>
          <span id="nome_produto_{{ produto.id_produto }}">{{ produto.nome }}</span><br>
          <small class="text-body-secondary">{{ produto.categoria|default('Sem categoria', true) }}</small>
        </td>
```

O `<span>` com o `id` terminado no código do produto vai servir à janela de exclusão, mais adiante. E o `default('Sem categoria', true)` escreve esse texto quando a categoria é `NULL`: o segundo argumento, `true`, faz o filtro agir também quando o valor é vazio ou `None` (sem ele, o `default` só age quando a variável não existe, e a tela mostraria a palavra `None`). Acerte o `colspan` da linha da lista vazia para `5`.

Salve e recarregue. O Notebook e o Fone aparecem em verde (**Em estoque**), o Teclado em amarelo (**Estoque baixo (3)**), e o Cabo HDMI em vermelho (**Sem estoque**) e com o selo cinza **Inativo**. A ordem é a alfabética pelo nome.

### A miniatura da foto

Falta a primeira coluna: a foto. Acrescente o cabeçalho **antes** do **Código**:

```html
        <th>Foto</th>
```

E a célula, antes da célula do código:

```html
        <td>
          {% if produto.foto %}
            <img src="{{ url_for('static', filename=produto.foto) }}" alt="Foto de {{ produto.nome }}" class="foto-produto">
          {% else %}
            <span class="foto-produto foto-vazia">sem foto</span>
          {% endif %}
        </td>
```

A coluna `foto` guarda `uploads/ab12cd34.png`, e o `url_for('static', filename=produto.foto)` monta o endereço `/static/uploads/ab12cd34.png`. Quando a coluna é `NULL`, o `if` cai no `else`, que desenha um quadrado cinza com o texto "sem foto". O `alt` descreve a imagem para quem usa leitor de tela. Acerte o `colspan` para `6`.

As duas classes (`foto-produto` e `foto-vazia`) são regras de CSS próprias. Acrescente no **final** do `static/estilo.css`:

```css
/* Foto do produto na lista: quadrado de 56 px, com o recorte centralizado */
.foto-produto {
  width: 56px;
  height: 56px;
  object-fit: cover;
  border-radius: 0.375rem;
}

/* Quadrado cinza para o produto sem foto */
.foto-vazia {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #e9ecef;
  color: #6c757d;
  font-size: 0.7rem;
  text-align: center;
}
```

O `object-fit: cover` recorta a imagem no centro para ela preencher o quadrado, sem esticar. Salve e recarregue (`Ctrl + F5`, para o navegador buscar o CSS novo): o produto que tem foto aparece com a miniatura, e os outros com o quadrado cinza. Se nenhum dos seus produtos tem foto, cadastre um agora com uma imagem `.jpg` ou `.png` do seu computador.

| O que conferir | Onde |
|---|---|
| Preço no formato `R$ 3.499,90` | Coluna **Preço** |
| Três cores de estoque (verde, amarelo, vermelho) | Coluna **Estoque** |
| `Ativo` e `Inativo` | Coluna **Situação** |
| `Sem categoria` no Cabo HDMI | Embaixo do nome |
| Miniatura ou quadrado "sem foto" | Primeira coluna |
| A lista continua ordenada pelo nome | Linhas |

```bash
git add .
git commit -m "Adiciona a lista de produtos com filtro moeda, selos de estoque e miniatura"
git push
```

---

## Os arquivos completos do capítulo

O `app.py`:

```python
import os
import uuid

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash, abort, session
from flask_wtf.csrf import CSRFProtect
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from db import execute_query, execute_one, execute_insert
from validacoes import (
    UFS, CATEGORIAS, validar_nome_perfil, validar_descricao_perfil,
    validar_nome_usuario, validar_email, validar_senha, validar_celular,
    validar_cpf, validar_data_nascimento, validar_cep, validar_estado,
    validar_tamanho, formatar_celular, formatar_cpf, formatar_cep,
    validar_nome_produto, validar_categoria, validar_preco, validar_estoque,
    converter_preco, validar_extensao_foto,
)

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

CSRFProtect(app)

# As fotos dos produtos ficam em static/uploads. O Flask recusa (erro 413) pedidos com mais de 2 MB.
PASTA_UPLOADS = os.path.join(app.root_path, 'static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024

os.makedirs(PASTA_UPLOADS, exist_ok=True)

# As colunas que as telas de usuário leem. A senha fica de fora de propósito: o que não é
# lido do banco não tem como vazar para a página.
SELECT_USUARIO = (
    'SELECT u.id_usuario, u.nome, u.email, u.celular, u.data_nascimento, u.cpf, '
    'u.perfil_id, u.cep, u.endereco, u.numero, u.complemento, u.cidade, u.estado, '
    'u.criado_em, u.atualizado_em, p.nome AS perfil, p.descricao AS perfil_descricao '
    'FROM usuarios u '
    'JOIN perfis p ON p.id_perfil = u.perfil_id'
)

# As colunas que as telas de produto leem
SELECT_PRODUTO = (
    'SELECT id_produto, nome, descricao, categoria, preco, estoque, foto, ativo, '
    'criado_em, atualizado_em '
    'FROM produtos'
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


def formatar_numero(valor):
    # 1234.5 vira '1.234,50': o Python escreve 1,234.50, e as trocas acertam a pontuação
    texto = f'{valor:,.2f}'
    texto = texto.replace(',', 'X').replace('.', ',').replace('X', '.')

    return texto


@app.template_filter('moeda')
def moeda(valor):
    return 'R$ ' + formatar_numero(valor)


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
def index():
    if 'id_usuario' not in session:
        flash('Entre para continuar.', 'warning')
        return redirect(url_for('login'))

    perfis = execute_one('SELECT COUNT(*) AS total FROM perfis')
    usuarios = execute_one('SELECT COUNT(*) AS total FROM usuarios')
    produtos = execute_one('SELECT COUNT(*) AS total FROM produtos')

    return render_template('index.html', titulo='Sistema de Gestão',
                           total_perfis=perfis['total'],
                           total_usuarios=usuarios['total'],
                           total_produtos=produtos['total'])


@app.route('/perfis')
def lista_perfis():
    if 'id_usuario' not in session:
        flash('Entre para continuar.', 'warning')
        return redirect(url_for('login'))

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
def perfil_novo():
    if 'id_usuario' not in session:
        flash('Entre para continuar.', 'warning')
        return redirect(url_for('login'))

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
def perfil_editar(id_perfil):
    if 'id_usuario' not in session:
        flash('Entre para continuar.', 'warning')
        return redirect(url_for('login'))

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
def perfil_excluir(id_perfil):
    if 'id_usuario' not in session:
        flash('Entre para continuar.', 'warning')
        return redirect(url_for('login'))

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
    if 'id_usuario' not in session:
        flash('Entre para continuar.', 'warning')
        return redirect(url_for('login'))

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
def usuario_novo():
    if 'id_usuario' not in session:
        flash('Entre para continuar.', 'warning')
        return redirect(url_for('login'))

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
def usuario_detalhe(id_usuario):
    if 'id_usuario' not in session:
        flash('Entre para continuar.', 'warning')
        return redirect(url_for('login'))

    usuario = execute_one(SELECT_USUARIO + ' WHERE u.id_usuario = %s', (id_usuario,))
    if usuario is None:
        abort(404)

    return render_template('usuario_detalhe.html', usuario=usuario)


@app.route('/usuarios/<int:id_usuario>/editar', methods=['GET', 'POST'])
def usuario_editar(id_usuario):
    if 'id_usuario' not in session:
        flash('Entre para continuar.', 'warning')
        return redirect(url_for('login'))

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
def usuario_excluir(id_usuario):
    if 'id_usuario' not in session:
        flash('Entre para continuar.', 'warning')
        return redirect(url_for('login'))

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


@app.route('/produtos')
def lista_produtos():
    if 'id_usuario' not in session:
        flash('Entre para continuar.', 'warning')
        return redirect(url_for('login'))

    produtos = execute_query(SELECT_PRODUTO + ' ORDER BY nome', fetch=True)

    return render_template('produtos.html', titulo='Produtos', produtos=produtos)


def ler_formulario_produto(form):
    campos = {}
    campos['nome'] = form.get('nome', '').strip()
    campos['descricao'] = form.get('descricao', '').strip()
    campos['preco'] = form.get('preco', '').strip()
    campos['estoque'] = form.get('estoque', '').strip()
    campos['categoria'] = form.get('categoria', '')

    if form.get('ativo') == '1':
        campos['ativo'] = 1
    else:
        campos['ativo'] = 0

    return campos


def ler_foto(arquivos):
    foto = arquivos.get('foto')

    if foto is None or foto.filename == '':
        return None

    return foto


def extensao_da_foto(nome_arquivo):
    nome_seguro = secure_filename(nome_arquivo)

    if '.' not in nome_seguro:
        return ''

    return nome_seguro.rsplit('.', 1)[1].lower()


def salvar_foto(foto):
    nome_arquivo = uuid.uuid4().hex + '.' + extensao_da_foto(foto.filename)
    foto.save(os.path.join(PASTA_UPLOADS, nome_arquivo))

    return 'uploads/' + nome_arquivo


def conferir_produto(campos, foto):
    erros = []

    erro = validar_nome_produto(campos['nome'])
    if erro:
        erros.append(erro)

    erro = validar_tamanho(campos['descricao'], 'descrição', 2000)
    if erro:
        erros.append(erro)

    erro = validar_preco(campos['preco'])
    if erro:
        erros.append(erro)

    erro = validar_estoque(campos['estoque'])
    if erro:
        erros.append(erro)

    erro = validar_categoria(campos['categoria'])
    if erro:
        erros.append(erro)

    if foto is not None:
        erro = validar_extensao_foto(extensao_da_foto(foto.filename))
        if erro:
            erros.append(erro)

    return erros


@app.route('/produtos/novo', methods=['GET', 'POST'])
def produto_novo():
    if 'id_usuario' not in session:
        flash('Entre para continuar.', 'warning')
        return redirect(url_for('login'))

    dados = {'estoque': '0', 'ativo': '1'}

    if request.method == 'POST':
        campos = ler_formulario_produto(request.form)
        foto = ler_foto(request.files)

        erros = conferir_produto(campos, foto)

        if erros:
            for mensagem in erros:
                flash(mensagem, 'danger')
        else:
            caminho_foto = None
            if foto is not None:
                caminho_foto = salvar_foto(foto)

            novo_id = execute_insert(
                'INSERT INTO produtos (nome, descricao, categoria, preco, estoque, foto, ativo) '
                'VALUES (%s, %s, %s, %s, %s, %s, %s)',
                (
                    campos['nome'],
                    vazio_para_none(campos['descricao']),
                    vazio_para_none(campos['categoria']),
                    converter_preco(campos['preco']),
                    int(campos['estoque']),
                    caminho_foto,
                    campos['ativo'],
                ),
            )
            flash(f'Produto "{campos["nome"]}" cadastrado (código {novo_id}).', 'success')
            return redirect(url_for('lista_produtos'))

        dados = request.form

    return render_template('produto_form.html', dados=dados, categorias=CATEGORIAS)


@app.errorhandler(404)
def pagina_nao_encontrada(erro):
    return render_template('404.html'), 404


@app.errorhandler(413)
def arquivo_grande_demais(erro):
    return render_template('413.html'), 413


@app.errorhandler(500)
def erro_no_servidor(erro):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
```

O `templates/produtos.html`:

```html
{% extends 'base.html' %}

{% block titulo_aba %}{{ titulo }} — Sistema de Gestão{% endblock %}

{% block conteudo %}
  <div class="d-flex justify-content-between align-items-center mb-3">
    <h1 class="h2 mb-0">{{ titulo }}</h1>
    <a href="{{ url_for('produto_novo') }}" class="btn btn-primary">Novo produto</a>
  </div>

  <table class="table table-striped table-hover align-middle">
    <thead class="table-light">
      <tr>
        <th>Foto</th>
        <th>Código</th>
        <th>Nome</th>
        <th>Preço</th>
        <th>Estoque</th>
        <th>Situação</th>
      </tr>
    </thead>
    <tbody>
      {% for produto in produtos %}
      <tr>
        <td>
          {% if produto.foto %}
            <img src="{{ url_for('static', filename=produto.foto) }}" alt="Foto de {{ produto.nome }}" class="foto-produto">
          {% else %}
            <span class="foto-produto foto-vazia">sem foto</span>
          {% endif %}
        </td>
        <td>{{ produto.id_produto }}</td>
        <td>
          <span id="nome_produto_{{ produto.id_produto }}">{{ produto.nome }}</span><br>
          <small class="text-body-secondary">{{ produto.categoria|default('Sem categoria', true) }}</small>
        </td>
        <td>{{ produto.preco|moeda }}</td>
        <td>
          {% if produto.estoque == 0 %}
            <span class="badge text-bg-danger">Sem estoque</span>
          {% elif produto.estoque < 5 %}
            <span class="badge text-bg-warning">Estoque baixo ({{ produto.estoque }})</span>
          {% else %}
            <span class="badge text-bg-success">Em estoque ({{ produto.estoque }})</span>
          {% endif %}
        </td>
        <td>
          {% if produto.ativo %}
            <span class="badge text-bg-primary">Ativo</span>
          {% else %}
            <span class="badge text-bg-secondary">Inativo</span>
          {% endif %}
        </td>
      </tr>
      {% else %}
      <tr>
        <td colspan="6" class="text-center text-body-secondary py-4">Nenhum produto cadastrado ainda.</td>
      </tr>
      {% endfor %}
    </tbody>
  </table>
{% endblock %}
```

O `static/estilo.css`:

```css
/* Regras próprias do sistema. O resto do visual vem do Bootstrap. */

body {
  background-color: #f4f6f8;
}

/* Cor da barra de navegação */
.navbar {
  background-color: #1f4e79;
}

/* Foto do produto na lista: quadrado de 56 px, com o recorte centralizado */
.foto-produto {
  width: 56px;
  height: 56px;
  object-fit: cover;
  border-radius: 0.375rem;
}

/* Quadrado cinza para o produto sem foto */
.foto-vazia {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #e9ecef;
  color: #6c757d;
  font-size: 0.7rem;
  text-align: center;
}
```

Os demais arquivos (`validacoes.py`, `db.py`, `produto_form.html`, `base.html`, `413.html` e os outros) são os do Capítulo 18.1.

---

## 📦 Código deste capítulo

Compare com o seu projeto, ou use como ponto de partida do Capítulo 18.3. O zip tem todos os arquivos do projeto, com o `app.py`, o `produtos.html` e o `estilo.css` atualizados, e a pasta `static/uploads` vazia. O ambiente virtual e o `.env` **não** vão no zip: depois de descompactar, crie o ambiente com os comandos acima e rode `copy .env.example .env`, trocando os marcadores `SUA_SENHA_AQUI` e `NOME_BANCO_DADOS` como no [Capítulo 11](Capitulo_11_Projeto_Novo_e_Banco.md#topico-4-o-arquivo-env). O banco também não vai dentro do zip: importe o `banco.sql` no phpMyAdmin e cadastre os três perfis e os três usuários pelo formulário. As fotos enviadas também não: a pasta `static/uploads` vem vazia, só com o `.gitkeep`.

➡️ [Baixar p2_cap_18_2.zip](../arquivos/p2_cap_18_2.zip)

---

## 🃏 Flashcards de Revisão

Tente responder mentalmente antes de abrir.

??? question "Por que o `{% else %}` do `for` é útil na lista de produtos?"
    Porque ele roda quando a lista está vazia, e mostra a mensagem `Nenhum produto cadastrado ainda.` em vez de uma tabela só com o cabeçalho.

??? question "Para que serve o filtro `moeda`, e por que ele foi criado em vez de repetir o `replace` em cada template?"
    O `Decimal` chega ao template como `3499.90`, e no Brasil se escreve `R$ 3.499,90`. O filtro `@app.template_filter('moeda')` faz a conversão em um só lugar, e qualquer template o usa com `|moeda`. Repetir a expressão em cada tela obrigaria a corrigir todas elas a cada mudança.

??? question "Por que o `default('Sem categoria', true)` leva o segundo argumento?"
    Porque, sem o `true`, o filtro `default` só age quando a variável **não existe**. Uma categoria `NULL` chega ao template como `None`, que existe, e a tela mostraria a palavra `None`. O `true` faz o filtro agir também quando o valor é vazio ou `None`.

??? question "Como a miniatura chega à página, se o banco guarda só um texto?"
    A coluna `foto` guarda `uploads/ab12cd34.png`, e o `url_for('static', filename=produto.foto)` monta o endereço `/static/uploads/ab12cd34.png`, que o Flask serve a partir da pasta `static`. Sem foto (`NULL`), o `if` cai no `else`, que desenha um quadrado cinza.

---

## 📝 Resumo

A lista lê as colunas de `produtos` por uma constante (`SELECT_PRODUTO`), e quem a usa completa o comando (aqui, `ORDER BY nome`). A tabela repete uma linha por produto com o `for`, e o `else` do próprio `for` cuida da lista vazia. O preço, um `Decimal`, passa pelo filtro próprio `moeda` e aparece em reais; o estoque ganha um selo vermelho, amarelo ou verde conforme a faixa; a situação, `Ativo` ou `Inativo`; e a primeira coluna mostra a miniatura da foto, ou um quadrado cinza quando a coluna é `NULL`. Os botões **Editar** e **Excluir** chegam nos próximos capítulos.

---

## 🔗 Navegação

⬅️ [Capítulo 18.1 — INSERT de produtos](Capitulo_18_1_INSERT_de_Produtos.md) · ➡️ [Capítulo 18.3 — UPDATE de produtos (opcional)](Capitulo_18_3_UPDATE_de_Produtos.md) · [Capítulo 18 — CRUD de produtos](Capitulo_18_CRUD_de_Produtos.md) · 🔒 Capítulo 19 — em breve.

---

*Fatec Jahu · ILP951 · Prof. Ronan Adriel Zenatti · 2026*
