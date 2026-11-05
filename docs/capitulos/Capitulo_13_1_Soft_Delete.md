# Capítulo 13.1 — Soft-delete (opcional)

**Disciplina:** Programação para Internet (ILP951)
**Professor:** Ronan Adriel Zenatti · ronan.zenatti@cps.sp.gov.br
**Fatec Jahu — 2º Semestre/2026**

---

## 🎯 Objetivos do Capítulo

Ao final deste capítulo você deverá ser capaz de:

- Diferenciar a exclusão **física** (`DELETE`) da exclusão **lógica** (marcar o registro com a data da exclusão) e escolher a adequada para cada situação
- Trocar o `DELETE` por um `UPDATE` que preenche a coluna `deletado_em`
- Filtrar os registros excluídos das listas, das contagens e das rotas com `IS NULL`
- Criar uma lixeira que lista os perfis excluídos e **restaura** os que a pessoa quiser de volta
- Avisar, no cadastro e na edição, quando o nome repetido pertence a um perfil da lixeira
- Explicar por que um perfil na lixeira não dispara o erro `1451`, e o que isso exige de quem usa o sistema

Este capítulo é **opcional**: o Capítulo 14 continua do código do Capítulo 13, que exclui de verdade, e não deste. No Capítulo 13, excluir um perfil o apagava do banco, sem volta. Muitos sistemas preferem **guardar** o registro e só marcá-lo como excluído, para poder desfazer um clique errado e manter o histórico. É o *soft-delete*, a "exclusão suave". Aqui os perfis ganham uma lixeira.

## 📦 Ponto de partida

Este capítulo continua do **seu** repositório `sistema-gestao`, como ficou no fim do Capítulo 13: com a edição e a exclusão de perfis funcionando, o modal de confirmação e o perfil `Teste` para os experimentos.

Se o seu projeto não está funcionando, baixe o código do Capítulo 13 e descompacte. Depois de descompactar, crie o ambiente virtual e o `.env`, como no [Capítulo 11](Capitulo_11_Projeto_Novo_e_Banco.md#topico-4-o-arquivo-env), e importe o `banco.sql` no phpMyAdmin:

➡️ [Baixar p2_cap_13.zip](../arquivos/p2_cap_13.zip)

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

---

## Tópico 1 — Excluir sem apagar

### Duas formas de tirar um registro

Antes de escrever código, há uma decisão de projeto: **o registro precisa mesmo deixar de existir?** Existem duas respostas, cada uma com o seu comando SQL:

| | Exclusão **física** | Exclusão **lógica** (soft-delete) |
|---|---|---|
| **O que faz** | Remove a linha da tabela | Preenche `deletado_em` com a data e a hora; a linha continua no banco |
| **Comando SQL** | `DELETE FROM perfis WHERE id_perfil = %s` | `UPDATE perfis SET deletado_em = NOW() WHERE id_perfil = %s` |
| **Dá para desfazer?** | Não | Sim: `UPDATE perfis SET deletado_em = NULL WHERE ...` |
| **Preserva o histórico?** | Não | Sim: o que apontava para o registro continua apontando |
| **As listas precisam filtrar?** | Não | Sim: `WHERE deletado_em IS NULL` |
| **Bom para** | Lixo: cadastros de teste, duplicados, criados por engano | Dados com histórico, que alguém pode querer de volta |

A coluna `deletado_em` já existe nas tabelas `perfis` e `usuarios` desde o `banco.sql` do Capítulo 11: não é preciso alterar a estrutura de nenhuma tabela. Confira no phpMyAdmin, na estrutura da tabela `perfis`: `deletado_em`, do tipo `DATETIME`, aceitando `NULL`. O raciocínio é: `NULL` significa "não foi excluído", e uma data significa "foi excluído neste momento".

!!! note "Exclusão lógica e dados pessoais"
    Perfis não guardam dados de pessoas, e por isso a lixeira não traz risco algum. Quando o registro **é** uma pessoa (nome, CPF, endereço), a lei de proteção de dados garante ao titular o direito de pedir a eliminação do que o sistema sabe sobre ele, e marcar como excluído pode não bastar. Escolher entre a exclusão lógica e a física é uma decisão de negócio, e às vezes jurídica, e não só técnica.

### Ensaiando no phpMyAdmin

Antes de mudar o código, veja o que a exclusão lógica faz com a tabela. Confirme que existe o perfil `Teste` na lista (cadastre-o, se não existir). No phpMyAdmin, banco `gestao`, aba **SQL**:

```sql
UPDATE perfis SET deletado_em = NOW() WHERE nome = 'Teste';
SELECT id_perfil, nome, deletado_em FROM perfis WHERE nome = 'Teste';
```

O `NOW()` é uma função do MySQL que devolve a data e a hora de agora. O `SELECT` mostra o perfil com a data preenchida: **a linha continua lá**. Agora recarregue **http://127.0.0.1:5000/perfis** no navegador: o `Teste` **continua na lista**, porque a consulta do sistema não sabe da coluna `deletado_em`. Desfaça o ensaio:

```sql
UPDATE perfis SET deletado_em = NULL WHERE nome = 'Teste';
```

### O UPDATE no lugar do DELETE

Ligue o servidor (`python app.py`), com o XAMPP ligado, e abra o `app.py`. Na rota `perfil_excluir`, a exclusão vira a marcação. A contagem de usuários e o `try/except` do erro `1451` saem: um `UPDATE` não infringe a chave estrangeira (a linha do perfil continua existindo), e o banco nunca recusa. Substitua a rota `perfil_excluir` inteira por esta:

```python
@app.route('/perfis/<int:id_perfil>/excluir', methods=['POST'])
def perfil_excluir(id_perfil):
    # Busca o perfil, só entre os que não estão na lixeira
    perfil = execute_one(
        'SELECT id_perfil, nome FROM perfis WHERE id_perfil = %s AND deletado_em IS NULL',
        (id_perfil,),
    )

    # Código que não existe (ou já está na lixeira): mostra a página 404
    if perfil is None:
        abort(404)

    # Exclusão lógica: marca a data da exclusão em vez de apagar a linha
    execute_query('UPDATE perfis SET deletado_em = NOW() WHERE id_perfil = %s', (id_perfil,))
    flash(f'Perfil "{perfil["nome"]}" enviado para a lixeira.', 'success')

    return redirect(url_for('listar_perfis'))
```

Duas diferenças em relação ao Capítulo 13. O `SELECT` do começo ganhou o `AND deletado_em IS NULL`: um perfil que já está na lixeira não deve ser excluído de novo, e para a rota ele "não existe" (404). E o `DELETE` virou o `UPDATE ... SET deletado_em = NOW()`.

!!! note "SQL: `IS NULL`"
    No MySQL, nada é igual a `NULL`, nem outro `NULL`, por isso a pergunta é feita com `IS NULL` (e `IS NOT NULL` para o contrário), como no [Capítulo 12.1](Capitulo_12_1_Busca_Filtro_e_Paginacao.md#topico-2-buscar-e-filtrar-o-where-11). Aqui, `deletado_em IS NULL` significa "perfis que **não** foram excluídos".

Salve, abra a lista e exclua o `Teste` pelo modal. A faixa verde diz `Perfil "Teste" enviado para a lixeira.`, mas o perfil **continua na lista**, porque a lista ainda não filtra. No phpMyAdmin, o `deletado_em` do `Teste` está preenchido. É a dor da exclusão lógica: **toda consulta** que lê perfis passa a precisar do filtro.

### Filtrando todas as consultas

Três lugares do `app.py` ainda não sabem da lixeira. Em cada um, a mudança é acrescentar o filtro `deletado_em IS NULL`.

**1. A lista.** Na rota `listar_perfis`, troque o `SELECT`:

```python
    # Busca a lista de perfis na tabela do banco
    perfis = execute_query(
        'SELECT id_perfil, nome, descricao, criado_em FROM perfis ORDER BY nome',
        fetch=True,
    )
```

por:

```python
    # Busca a lista de perfis na tabela do banco, sem os que estão na lixeira
    perfis = execute_query(
        'SELECT id_perfil, nome, descricao, criado_em FROM perfis '
        'WHERE deletado_em IS NULL ORDER BY nome',
        fetch=True,
    )
```

**2. O cartão do dashboard**, que conta os perfis. Na rota `dashboard`, troque a primeira contagem:

```python
    perfis = execute_one('SELECT COUNT(*) AS total FROM perfis')
```

por:

```python
    perfis = execute_one('SELECT COUNT(*) AS total FROM perfis WHERE deletado_em IS NULL')
```

**3. A edição**: um perfil na lixeira não deve abrir para edição. No começo da rota `perfil_editar`, troque:

```python
    # Busca o perfil pelo código que veio no endereço
    perfil = execute_one(
        'SELECT id_perfil, nome, descricao FROM perfis WHERE id_perfil = %s',
        (id_perfil,),
    )

    # Código que não existe: mostra a página 404
```

por:

```python
    # Busca o perfil pelo código que veio no endereço, só entre os que não estão na lixeira
    perfil = execute_one(
        'SELECT id_perfil, nome, descricao FROM perfis '
        'WHERE id_perfil = %s AND deletado_em IS NULL',
        (id_perfil,),
    )

    # Código que não existe (ou está na lixeira): mostra a página 404
```

Salve e confira: o `Teste` sumiu da lista, o cartão **perfis** do dashboard não o conta, e `/perfis/` + o código do `Teste` + `/editar` mostra a página 404, como se o perfil não existisse para o sistema. Para o banco ele continua existindo, e é isso que permite restaurá-lo.

```bash
git add .
git commit -m "Troca o DELETE de perfil por UPDATE em deletado_em e filtra os excluídos"
git push
```

---

## Tópico 2 — A lixeira e a restauração

### As duas rotas

O perfil excluído sumiu de todas as telas, e ninguém consegue trazê-lo de volta. A lixeira resolve isso com duas rotas: uma que **lista** os excluídos e outra que **restaura** um deles. No `app.py`, acrescente a rota da lixeira **depois** da `listar_perfis`. A consulta é o inverso da lista: `IS NOT NULL`, com os excluídos mais recentemente no alto:

```python
@app.route('/perfis/lixeira')
def lixeira_perfis():
    # Só os perfis excluídos, os mais recentes primeiro
    perfis = execute_query(
        'SELECT id_perfil, nome, descricao, deletado_em FROM perfis '
        'WHERE deletado_em IS NOT NULL ORDER BY deletado_em DESC',
        fetch=True,
    )

    return render_template('perfis/perfis_lixeira.html', titulo='Lixeira de perfis', perfis=perfis)
```

Restaurar é desfazer a exclusão: `deletado_em` volta a ser `NULL`. É uma ação que **altera** dados, então, como a exclusão, é um `POST` com `csrf_token`. Acrescente a rota **depois** da `perfil_excluir`:

```python
@app.route('/perfis/<int:id_perfil>/restaurar', methods=['POST'])
def perfil_restaurar(id_perfil):
    # Busca o perfil, só entre os que estão na lixeira
    perfil = execute_one(
        'SELECT id_perfil, nome FROM perfis WHERE id_perfil = %s AND deletado_em IS NOT NULL',
        (id_perfil,),
    )

    if perfil is None:
        abort(404)

    # Restaurar é desfazer a marcação: deletado_em volta a ser NULL
    execute_query('UPDATE perfis SET deletado_em = NULL WHERE id_perfil = %s', (id_perfil,))
    flash(f'Perfil "{perfil["nome"]}" restaurado.', 'success')

    return redirect(url_for('listar_perfis'))
```

O `SELECT` procura só entre os que **estão** na lixeira (`IS NOT NULL`): restaurar um perfil que não foi excluído, ou que não existe, responde 404.

### A página da lixeira

Crie o `templates/perfis/perfis_lixeira.html`. Ele é parecido com o da lista, com a coluna **Excluído em** no lugar de **Criado em** (com a data e a hora, pelo mesmo `strftime` do [Capítulo 12](Capitulo_12_INSERT_e_SELECT_de_Perfis.md#a-tabela-com-todas-as-colunas)) e, na coluna de ações, um botão verde **Restaurar**:

```html
{% extends 'layout/base_menu.html' %}

{% block titulo_aba %}{{ titulo }} — Sistema de Gestão{% endblock %}

{% block conteudo %}
  <div class="d-flex justify-content-between align-items-center mb-3">
    <h1 class="h2 mb-0">{{ titulo }}</h1>
    <a href="{{ url_for('listar_perfis') }}" class="btn btn-outline-secondary">Voltar para os perfis</a>
  </div>

  <table class="table table-striped table-hover align-middle">
    <thead class="table-light">
      <tr>
        <th>Código</th>
        <th>Nome</th>
        <th>Descrição</th>
        <th>Excluído em</th>
        <th class="text-end">Ações</th>
      </tr>
    </thead>
    <tbody>
      {% for perfil in perfis %}
      <tr>
        <td>{{ perfil.id_perfil }}</td>
        <td>{{ perfil.nome }}</td>
        <td>{{ perfil.descricao if perfil.descricao else '—' }}</td>
        <td>{{ perfil.deletado_em.strftime('%d/%m/%Y %H:%M') }}</td>
        <td class="text-end text-nowrap">
          <form action="{{ url_for('perfil_restaurar', id_perfil=perfil.id_perfil) }}" method="post" class="d-inline">
            <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
            <button type="submit" class="btn btn-sm btn-success" title="Restaurar"><i class="bi bi-arrow-counterclockwise"></i> Restaurar</button>
          </form>
        </td>
      </tr>
      {% else %}
      <tr>
        <td colspan="5" class="text-center text-body-secondary py-4">A lixeira está vazia.</td>
      </tr>
      {% endfor %}
    </tbody>
  </table>
{% endblock %}
```

O botão **Restaurar** fica dentro de um formulário `POST`, com o `csrf_token`, e envia direto, sem modal: restaurar não perde nada. O `class="d-inline"` mantém o formulário na linha da tabela.

### Os caminhos até a lixeira

**Na lista.** No cabeçalho do `perfis_lista.html`, o botão **Novo perfil** passa a dividir o espaço com o botão **Lixeira**. Troque a linha:

```html
<a href="{{ url_for('inserir_perfil') }}" class="btn btn-primary">Novo perfil</a>
```

por este grupo:

```html
<div class="d-flex gap-2">
  <a href="{{ url_for('lixeira_perfis') }}" class="btn btn-outline-secondary"><i class="bi bi-trash"></i> Lixeira</a>
  <a href="{{ url_for('inserir_perfil') }}" class="btn btn-primary">Novo perfil</a>
</div>
```

**No modal.** O texto da janela de confirmação não promete mais uma exclusão sem volta. No mesmo arquivo, troque a frase:

```html
<p class="mb-0">Excluir o perfil <strong id="nomeExcluir"></strong>? Esta ação não pode ser desfeita.</p>
```

por:

```html
<p class="mb-0">Excluir o perfil <strong id="nomeExcluir"></strong>? Ele vai para a lixeira e pode ser restaurado depois.</p>
```

**No menu.** O menu **Perfis** continua destacado na lixeira. No `base_menu.html`, no botão do menu suspenso **Perfis**, troque o trecho do `{% if %}`:

```html
{% if request.endpoint in ['listar_perfis', 'inserir_perfil', 'perfil_editar'] %}active{% endif %}
```

por:

```html
{% if request.endpoint in ['listar_perfis', 'inserir_perfil', 'perfil_editar', 'lixeira_perfis'] %}active{% endif %}
```

Salve e navegue: **Perfis > Listar Perfis**, **Lixeira** (o `Teste` aparece, com a data e a hora em que foi excluído), **Restaurar**. Você volta para a lista, com a faixa verde `Perfil "Teste" restaurado.` e o perfil no lugar. Abra a lixeira de novo: `A lixeira está vazia.`

```bash
git add .
git commit -m "Adiciona a lixeira de perfis e a restauração"
git push
```

---

## Tópico 3 — O nome na lixeira e o perfil em uso

### O nome que ninguém vê

Há um detalhe: a coluna `nome` é `UNIQUE`, e o banco **não** sabe de `deletado_em`. Um perfil na lixeira continua ocupando o nome dele. Veja o efeito: exclua o `Teste` pelo modal e tente cadastrar de novo um perfil chamado `Teste`. A faixa vermelha diz `Já existe um perfil com este nome.`, mas a lista **não mostra** nenhum `Teste`. Para quem usa o sistema, a mensagem parece um erro. A mensagem precisa dizer que o nome está na lixeira.

A `validar_perfil` busca o perfil com aquele nome e precisa saber **se ele foi excluído**. Abra o `validacoes/validacoes_perfil.py` e, na seção do nome repetido, troque:

```python
    if not erros:
        existente = execute_one(
            'SELECT id_perfil FROM perfis WHERE nome = %s AND id_perfil <> %s',
            (nome, id_perfil),
        )

        if existente:
            erros.append('Já existe um perfil com este nome.')
```

por:

```python
    if not erros:
        existente = execute_one(
            'SELECT id_perfil, deletado_em FROM perfis WHERE nome = %s AND id_perfil <> %s',
            (nome, id_perfil),
        )

        # O nome pode pertencer a um perfil da lixeira, que não aparece na lista
        if existente:
            if existente['deletado_em'] is None:
                erros.append('Já existe um perfil com este nome.')
            else:
                erros.append('Já existe um perfil excluído com este nome. Restaure-o na lixeira.')
```

O `SELECT` passou a trazer também o `deletado_em`, e o `if` escolhe a mensagem. Salve e tente cadastrar `Teste` de novo: a faixa vermelha agora diz `Já existe um perfil excluído com este nome. Restaure-o na lixeira.` A mesma conferência vale na edição (renomear o `Gerente` para `Teste` dá o mesmo aviso), porque as duas rotas usam a mesma função. O erro `1062` das rotas de cadastro e de edição continua valendo como barreira final, com a mensagem de sempre.

Restaure o `Teste` pela lixeira para os próximos experimentos.

### O perfil que tem usuários

No Capítulo 13, excluir um perfil com usuários era **impedido**: o banco recusava com o erro `1451`. Agora a exclusão é só um `UPDATE`, e a linha do perfil continua existindo: o banco não tem nada a recusar. Veja pelo phpMyAdmin. Cadastre pelo sistema um perfil `Visitante`, e na aba **SQL** crie o usuário de teste (a senha é só um texto qualquer, o hash de verdade chega no Capítulo 14):

```sql
INSERT INTO usuarios (nome, email, senha, perfil_id)
VALUES ('Usuário de Teste', 'teste@exemplo.com', 'hash-de-teste',
        (SELECT id_perfil FROM perfis WHERE nome = 'Visitante'));
```

Exclua o `Visitante` pelo sistema: ele vai para a lixeira, **sem erro**, e o usuário de teste continua apontando para ele. Isso é uma consequência da escolha, e não um defeito: a exclusão lógica troca a recusa do banco por uma **decisão de quem projeta o sistema**. Há dois caminhos: bloquear a exclusão de um perfil com usuários (como no Capítulo 13, com a contagem de usuários antes do `UPDATE`) ou aceitar que o perfil na lixeira continue sendo o perfil de quem já o tinha. Neste capítulo, a escolha é aceitar: o perfil vai para a lixeira, o usuário mantém o perfil dele e quem administra pode restaurá-lo quando quiser.

Limpe o experimento. No phpMyAdmin, aba **SQL**:

```sql
DELETE FROM usuarios WHERE email = 'teste@exemplo.com';
```

```bash
git add .
git commit -m "Avisa quando o nome de perfil pertence a um perfil da lixeira"
git push
```

---

## Os arquivos completos do capítulo

O `app.py`:

```python
import os

from dotenv import load_dotenv
from flask import Flask, abort, flash, redirect, render_template, request, url_for
from flask_wtf.csrf import CSRFProtect
from mysql.connector import Error

from db import execute_insert, execute_one, execute_query
from validacoes.validacoes_perfil import validar_perfil

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Liga a proteção CSRF: todo formulário POST do sistema vai precisar do token
CSRFProtect(app)


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
    perfis = execute_one('SELECT COUNT(*) AS total FROM perfis WHERE deletado_em IS NULL')
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
    # Busca a lista de perfis na tabela do banco, sem os que estão na lixeira
    perfis = execute_query(
        'SELECT id_perfil, nome, descricao, criado_em FROM perfis '
        'WHERE deletado_em IS NULL ORDER BY nome',
        fetch=True,
    )

    return render_template('perfis/perfis_lista.html', titulo='Perfis', perfis=perfis)


@app.route('/perfis/lixeira')
def lixeira_perfis():
    # Só os perfis excluídos, os mais recentes primeiro
    perfis = execute_query(
        'SELECT id_perfil, nome, descricao, deletado_em FROM perfis '
        'WHERE deletado_em IS NOT NULL ORDER BY deletado_em DESC',
        fetch=True,
    )

    return render_template('perfis/perfis_lixeira.html', titulo='Lixeira de perfis', perfis=perfis)


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
    return render_template('perfis/perfil_form.html', acao='criar', id_perfil=None,
                           nome=nome, descricao=descricao)


@app.route('/perfis/<int:id_perfil>/editar', methods=['GET', 'POST'])
def perfil_editar(id_perfil):
    # Busca o perfil pelo código que veio no endereço, só entre os que não estão na lixeira
    perfil = execute_one(
        'SELECT id_perfil, nome, descricao FROM perfis '
        'WHERE id_perfil = %s AND deletado_em IS NULL',
        (id_perfil,),
    )

    # Código que não existe (ou está na lixeira): mostra a página 404
    if perfil is None:
        abort(404)

    # O formulário começa com os valores que estão no banco
    nome = perfil['nome']
    descricao = perfil['descricao']

    # Executado apenas no envio do formulário (POST)
    if request.method == 'POST':
        # 1. Coleta os dados do formulário
        nome = request.form.get('nome', '').strip()

        # 'or None' garante que string vazia vire None (gravado como NULL no MySQL)
        descricao = request.form.get('descricao', '').strip() or None

        # -------------------------------------------------------------------------
        # 2. Validação dos campos (o id_perfil faz o próprio perfil não contar como repetido)
        erros = validar_perfil(nome, descricao, id_perfil)

        # 3. Se houver erros, exibe as mensagens
        if erros:
            for mensagem in erros:
                flash(mensagem, 'danger')

        # -------------------------------------------------------------------------
        # 4. Se não houver erros, tenta salvar no banco
        else:
            try:
                # O WHERE garante que só este perfil seja alterado
                execute_query(
                    'UPDATE perfis SET nome = %s, descricao = %s WHERE id_perfil = %s',
                    (nome, descricao, id_perfil),
                )

                flash(f'Perfil "{nome}" atualizado.', 'success')
                return redirect(url_for('listar_perfis'))

            # Trata concorrência (duplicidade no momento do update)
            except Error as erro:
                if erro.errno == 1062:
                    flash('Já existe um perfil com este nome.', 'danger')
                else:
                    raise

    # Exibe a tela em caso de GET ou se houver erros (de validação ou de nome repetido)
    return render_template('perfis/perfil_form.html', acao='editar', id_perfil=id_perfil,
                           nome=nome, descricao=descricao)


@app.route('/perfis/<int:id_perfil>/excluir', methods=['POST'])
def perfil_excluir(id_perfil):
    # Busca o perfil, só entre os que não estão na lixeira
    perfil = execute_one(
        'SELECT id_perfil, nome FROM perfis WHERE id_perfil = %s AND deletado_em IS NULL',
        (id_perfil,),
    )

    # Código que não existe (ou já está na lixeira): mostra a página 404
    if perfil is None:
        abort(404)

    # Exclusão lógica: marca a data da exclusão em vez de apagar a linha
    execute_query('UPDATE perfis SET deletado_em = NOW() WHERE id_perfil = %s', (id_perfil,))
    flash(f'Perfil "{perfil["nome"]}" enviado para a lixeira.', 'success')

    return redirect(url_for('listar_perfis'))


@app.route('/perfis/<int:id_perfil>/restaurar', methods=['POST'])
def perfil_restaurar(id_perfil):
    # Busca o perfil, só entre os que estão na lixeira
    perfil = execute_one(
        'SELECT id_perfil, nome FROM perfis WHERE id_perfil = %s AND deletado_em IS NOT NULL',
        (id_perfil,),
    )

    if perfil is None:
        abort(404)

    # Restaurar é desfazer a marcação: deletado_em volta a ser NULL
    execute_query('UPDATE perfis SET deletado_em = NULL WHERE id_perfil = %s', (id_perfil,))
    flash(f'Perfil "{perfil["nome"]}" restaurado.', 'success')

    return redirect(url_for('listar_perfis'))


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
```

O `validacoes/validacoes_perfil.py`:

```python
from db import execute_one


def validar_perfil(nome, descricao, id_perfil=0):
    erros = []

    # ================ VALIDAÇÕES PARA O CAMPO nome =====================
    if not nome:
        erros.append('Informe o nome do perfil.')
    elif len(nome) < 3:
        erros.append('O nome deve ter pelo menos 3 caracteres.')
    elif len(nome) > 100:
        erros.append('O nome deve ter no máximo 100 caracteres.')

    # ================ VALIDAÇÕES PARA O CAMPO descricao =====================
    # Como descricao pode ser None, checamos antes de usar len()
    if descricao and len(descricao) > 255:
        erros.append('A descrição deve ter no máximo 255 caracteres.')

    # ================ NOME REPETIDO (CONSULTA AO BANCO) =====================
    # Se as regras básicas passaram, checa unicidade no banco de dados
    # O id_perfil <> %s ignora o próprio perfil na edição (no cadastro, o id_perfil vale 0)
    if not erros:
        existente = execute_one(
            'SELECT id_perfil, deletado_em FROM perfis WHERE nome = %s AND id_perfil <> %s',
            (nome, id_perfil),
        )

        # O nome pode pertencer a um perfil da lixeira, que não aparece na lista
        if existente:
            if existente['deletado_em'] is None:
                erros.append('Já existe um perfil com este nome.')
            else:
                erros.append('Já existe um perfil excluído com este nome. Restaure-o na lixeira.')

    return erros
```

O `templates/perfis/perfis_lista.html`:

```html
{% extends 'layout/base_menu.html' %}

{% block titulo_aba %}{{ titulo }} — Sistema de Gestão{% endblock %}

{% block conteudo %}
  <div class="d-flex justify-content-between align-items-center mb-3">
    <h1 class="h2 mb-0">{{ titulo }}</h1>
    <div class="d-flex gap-2">
      <a href="{{ url_for('lixeira_perfis') }}" class="btn btn-outline-secondary"><i class="bi bi-trash"></i> Lixeira</a>
      <a href="{{ url_for('inserir_perfil') }}" class="btn btn-primary">Novo perfil</a>
    </div>
  </div>

  <table class="table table-striped table-hover align-middle">
    <thead class="table-light">
      <tr>
        <th>Código</th>
        <th>Nome</th>
        <th>Descrição</th>
        <th>Criado em</th>
        <th class="text-end">Ações</th>
      </tr>
    </thead>
    <tbody>
      {% for perfil in perfis %}
      <tr>
        <td>{{ perfil.id_perfil }}</td>
        <td id="nome_perfil_{{ perfil.id_perfil }}">{{ perfil.nome }}</td>
        <td>{{ perfil.descricao if perfil.descricao else '—' }}</td>
        <td>{{ perfil.criado_em.strftime('%d/%m/%Y %H:%M') }}</td>
        <td class="text-end text-nowrap">
          <a href="{{ url_for('perfil_editar', id_perfil=perfil.id_perfil) }}" class="btn btn-sm btn-warning" title="Editar"><i class="bi bi-pencil-square"></i></a>
          <button type="button" class="btn btn-sm btn-danger" title="Excluir" data-bs-toggle="modal" data-bs-target="#modalExcluir" onclick="prepararExclusao({{ perfil.id_perfil }})"><i class="bi bi-trash"></i></button>
        </td>
      </tr>
      {% else %}
      <tr>
        <td colspan="5" class="text-center text-body-secondary py-4">Nenhum perfil cadastrado ainda.</td>
      </tr>
      {% endfor %}
    </tbody>
  </table>

  <div class="modal fade" id="modalExcluir" tabindex="-1" aria-labelledby="tituloModalExcluir" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h2 class="modal-title h5" id="tituloModalExcluir">Excluir perfil</h2>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Fechar"></button>
        </div>
        <form id="formExcluir" action="" method="post">
          <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
          <div class="modal-body">
            <p class="mb-0">Excluir o perfil <strong id="nomeExcluir"></strong>? Ele vai para a lixeira e pode ser restaurado depois.</p>
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
    const nome = document.getElementById('nome_perfil_' + id).textContent;
    document.getElementById('nomeExcluir').textContent = nome;
    document.getElementById('formExcluir').action = '/perfis/' + id + '/excluir';
  }
</script>
{% endblock %}
```

O `templates/perfis/perfis_lixeira.html`:

```html
{% extends 'layout/base_menu.html' %}

{% block titulo_aba %}{{ titulo }} — Sistema de Gestão{% endblock %}

{% block conteudo %}
  <div class="d-flex justify-content-between align-items-center mb-3">
    <h1 class="h2 mb-0">{{ titulo }}</h1>
    <a href="{{ url_for('listar_perfis') }}" class="btn btn-outline-secondary">Voltar para os perfis</a>
  </div>

  <table class="table table-striped table-hover align-middle">
    <thead class="table-light">
      <tr>
        <th>Código</th>
        <th>Nome</th>
        <th>Descrição</th>
        <th>Excluído em</th>
        <th class="text-end">Ações</th>
      </tr>
    </thead>
    <tbody>
      {% for perfil in perfis %}
      <tr>
        <td>{{ perfil.id_perfil }}</td>
        <td>{{ perfil.nome }}</td>
        <td>{{ perfil.descricao if perfil.descricao else '—' }}</td>
        <td>{{ perfil.deletado_em.strftime('%d/%m/%Y %H:%M') }}</td>
        <td class="text-end text-nowrap">
          <form action="{{ url_for('perfil_restaurar', id_perfil=perfil.id_perfil) }}" method="post" class="d-inline">
            <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
            <button type="submit" class="btn btn-sm btn-success" title="Restaurar"><i class="bi bi-arrow-counterclockwise"></i> Restaurar</button>
          </form>
        </td>
      </tr>
      {% else %}
      <tr>
        <td colspan="5" class="text-center text-body-secondary py-4">A lixeira está vazia.</td>
      </tr>
      {% endfor %}
    </tbody>
  </table>
{% endblock %}
```

No `base_menu.html`, a única mudança é o `'lixeira_perfis'` na lista do menu **Perfis** (Tópico 2). Os demais arquivos são os do Capítulo 13.

---

## 📦 Código deste capítulo

Compare com o seu projeto. Este capítulo é opcional, então o **Capítulo 14 não parte deste zip**, e sim do zip do Capítulo 13. O zip tem o `app.py`, o `db.py`, a pasta `validacoes`, o `testar_conexao.py`, o `banco.sql`, o `.env.example`, o `.gitignore`, o `requirements.txt`, a pasta `templates` (com o novo `perfis/perfis_lixeira.html`) e a pasta `static`. O ambiente virtual e o `.env` **não** vão no zip: crie-os como no Capítulo 11.

➡️ [Baixar p2_cap_13_1.zip](../arquivos/p2_cap_13_1.zip)

---

## 🃏 Flashcards de Revisão

Tente responder mentalmente antes de abrir.

??? question "Qual a diferença entre a exclusão física e a exclusão lógica?"
    A física usa `DELETE` e remove a linha, sem volta. A lógica usa `UPDATE ... SET deletado_em = NOW()`: a linha continua no banco, marcada com a data da exclusão, e pode ser restaurada. Em troca, toda consulta precisa filtrar os excluídos.

??? question "Por que a lista de perfis precisa de `WHERE deletado_em IS NULL`?"
    Porque o registro excluído logicamente continua na tabela. Sem o filtro, ele apareceria nas listas e nas contagens como se nada tivesse acontecido. O filtro precisa estar em **todo** lugar que lê perfis: a lista, o cartão do dashboard, a edição e a exclusão.

??? question "Por que se escreve `IS NULL`, e não `= NULL`?"
    Porque, no MySQL, nada é igual a `NULL`, nem outro `NULL`: `deletado_em = NULL` nunca é verdadeiro. Só `IS NULL` e `IS NOT NULL` perguntam se a coluna está vazia.

??? question "O que a lixeira faz quando a pessoa clica em Restaurar?"
    Envia um `POST` para `/perfis/<id>/restaurar`, e a rota executa `UPDATE perfis SET deletado_em = NULL WHERE id_perfil = %s`. O perfil volta a ser encontrado por todos os filtros `IS NULL`. A rota só procura entre os que estão na lixeira, e responde 404 para os outros.

??? question "Por que o nome de um perfil excluído ainda barra um cadastro?"
    Porque o `UNIQUE` do banco não conhece o `deletado_em`: a linha continua na tabela, ocupando o nome. A função `validar_perfil` lê o `deletado_em` do perfil encontrado e avisa que o nome está na lixeira, para a pessoa saber que precisa restaurá-lo.

??? question "Por que excluir um perfil com usuários não dá o erro `1451` neste capítulo?"
    Porque o erro vem de um `DELETE`, que removeria a linha da qual os usuários dependem. A exclusão lógica é só um `UPDATE`: a linha do perfil continua existindo, e a chave estrangeira não é infringida. Impedir ou aceitar isso passa a ser uma decisão da rota, e não do banco.

---

## 📝 Resumo

A exclusão lógica guarda o registro e marca a data da exclusão em `deletado_em`, coluna que já existia desde o `banco.sql` do Capítulo 11. O `DELETE` da rota virou um `UPDATE ... SET deletado_em = NOW()`, e todo `SELECT` que lê perfis ganhou o filtro `IS NULL`, na lista, no cartão do dashboard, na edição e na exclusão. A lixeira lista o que foi excluído (`IS NOT NULL`) e restaura com outro `UPDATE`, que devolve o `NULL`. O nome de um perfil excluído continua ocupado, e a conferência avisa isso em vez de uma mensagem que parece errada. Como o `UPDATE` não infringe a chave estrangeira, o banco deixa de recusar a exclusão de um perfil com usuários, e essa decisão passa a ser da rota. O Capítulo 14 continua do código do Capítulo 13, com o cadastro de usuários.

---

## 🔗 Navegação

⬅️ [Capítulo 13 — UPDATE e DELETE de perfis](Capitulo_13_UPDATE_e_DELETE_de_Perfis.md) · ➡️ [Capítulo 14 — INSERT relacional de usuário](Capitulo_14_INSERT_Relacional_de_Usuario.md)

---

*Fatec Jahu · ILP951 · Prof. Ronan Adriel Zenatti · 2026*
