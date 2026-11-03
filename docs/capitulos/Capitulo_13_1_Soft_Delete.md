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

Ligue o servidor (`python app.py`), com o XAMPP ligado, e abra o `app.py`. Na rota `perfil_excluir`, a exclusão vira a marcação. A contagem de usuários e o `try/except` do erro `1451` saem: um `UPDATE` não infringe a chave estrangeira (a linha do perfil continua existindo), e o banco nunca recusa. Substitua a rota inteira por esta:

```python
@app.route('/perfis/<int:perfil_id>/excluir', methods=['POST'])
def perfil_excluir(perfil_id):
    perfil = execute_one(
        'SELECT id_perfil, nome FROM perfis WHERE id_perfil = %s',
        (perfil_id,),
    )
    if perfil is None:
        abort(404)

    execute_query('UPDATE perfis SET deletado_em = NOW() WHERE id_perfil = %s', (perfil_id,))
    flash(f'Perfil "{perfil["nome"]}" enviado para a lixeira.', 'success')

    return redirect(url_for('lista_perfis'))
```

Salve, abra a lista e exclua o `Teste` pelo modal. A faixa verde diz `Perfil "Teste" enviado para a lixeira.`, mas o perfil **continua na lista**, porque a lista ainda não filtra. No phpMyAdmin, o `deletado_em` do `Teste` está preenchido. É a dor da exclusão lógica: **toda consulta** passa a precisar do filtro.

### Filtrando a lista

Na rota `lista_perfis`, acrescente o filtro ao `SELECT`:

```python
    perfis = execute_query(
        'SELECT id_perfil, nome, descricao, criado_em FROM perfis '
        'WHERE deletado_em IS NULL ORDER BY nome',
        fetch=True,
    )
```

!!! note "SQL: `IS NULL`"
    No MySQL, nada é igual a `NULL`, nem outro `NULL`, por isso a pergunta é feita com `IS NULL` (e `IS NOT NULL` para o contrário), como no [Capítulo 12.1](Capitulo_12_1_Busca_Filtro_e_Paginacao.md#topico-3-mais-de-um-filtro-o-where-11). Aqui, `deletado_em IS NULL` significa "perfis que **não** foram excluídos".

Salve e recarregue: o `Teste` sumiu da lista. Nem toda tela olha para essa lista, e o filtro precisa estar em **todo lugar** que lê perfis. Três lugares do `app.py` ainda não sabem da lixeira:

1. **O cartão do Início**, que conta os perfis. Na rota `index`, troque a contagem por:

    ```python
        perfis = execute_one('SELECT COUNT(*) AS total FROM perfis WHERE deletado_em IS NULL')
    ```

2. **A edição**: um perfil na lixeira não deve abrir para edição. No `SELECT` da rota `perfil_editar`:

    ```python
        perfil = execute_one(
            'SELECT id_perfil, nome, descricao FROM perfis '
            'WHERE id_perfil = %s AND deletado_em IS NULL',
            (perfil_id,),
        )
    ```

3. **A exclusão**: um perfil que já está na lixeira não deve ser excluído de novo. No `SELECT` da rota `perfil_excluir`:

    ```python
        perfil = execute_one(
            'SELECT id_perfil, nome FROM perfis WHERE id_perfil = %s AND deletado_em IS NULL',
            (perfil_id,),
        )
    ```

Salve e confira: o cartão **perfis** do Início não conta o `Teste`, e `/perfis/` + o código do `Teste` + `/editar` mostra a página 404, como se o perfil não existisse para o sistema. Para o banco ele continua existindo, e é isso que permite restaurá-lo.

```bash
git add .
git commit -m "Troca o DELETE de perfil por UPDATE em deletado_em e filtra os excluídos"
git push
```

---

## Tópico 2 — A lixeira e a restauração

### A lista dos excluídos

O perfil excluído sumiu de todas as telas, e ninguém consegue trazê-lo de volta. A lixeira resolve isso. No `app.py`, **depois** da `lista_perfis`, acrescente a rota. A consulta é o inverso da lista: `IS NOT NULL`, com os excluídos mais recentemente no alto:

```python
@app.route('/perfis/lixeira')
def lixeira_perfis():
    perfis = execute_query(
        'SELECT id_perfil, nome, descricao, deletado_em FROM perfis '
        'WHERE deletado_em IS NOT NULL ORDER BY deletado_em DESC',
        fetch=True,
    )

    return render_template('perfis_lixeira.html', titulo='Lixeira de perfis', perfis=perfis)
```

Crie o `templates/perfis_lixeira.html`, parecido com o da lista, com a coluna **Excluído em** no lugar de **Criado em** (o `%H:%M` do `strftime` acrescenta a hora, como no [Capítulo 12](Capitulo_12_INSERT_e_SELECT_de_Perfis.md#a-coluna-criado-em)):

```html
{% extends 'base.html' %}

{% block titulo_aba %}{{ titulo }} — Sistema de Gestão{% endblock %}

{% block conteudo %}
  <div class="d-flex justify-content-between align-items-center mb-3">
    <h1 class="h2 mb-0">{{ titulo }}</h1>
    <a href="{{ url_for('lista_perfis') }}" class="btn btn-outline-secondary">Voltar para os perfis</a>
  </div>

  <table class="table table-striped table-hover">
    <thead class="table-light">
      <tr>
        <th>Código</th>
        <th>Nome</th>
        <th>Descrição</th>
        <th>Excluído em</th>
      </tr>
    </thead>
    <tbody>
      {% for perfil in perfis %}
      <tr>
        <td>{{ perfil.id_perfil }}</td>
        <td>{{ perfil.nome }}</td>
        <td>
          {% if perfil.descricao %}
            {{ perfil.descricao }}
          {% else %}
            <span class="text-body-secondary">—</span>
          {% endif %}
        </td>
        <td>{{ perfil.deletado_em.strftime('%d/%m/%Y %H:%M') }}</td>
      </tr>
      {% else %}
      <tr>
        <td colspan="4" class="text-center text-body-secondary py-4">A lixeira está vazia.</td>
      </tr>
      {% endfor %}
    </tbody>
  </table>
{% endblock %}
```

Salve e abra **http://127.0.0.1:5000/perfis/lixeira**: o `Teste` aparece, com a data e a hora em que foi excluído. Para chegar à lixeira sem digitar o endereço, acrescente um botão no cabeçalho do `perfis.html`. Troque o botão **Novo perfil** do cabeçalho por este grupo:

```html
    <div class="d-flex gap-2">
      <a href="{{ url_for('lixeira_perfis') }}" class="btn btn-outline-secondary">Lixeira</a>
      <a href="{{ url_for('perfil_novo') }}" class="btn btn-primary">Novo perfil</a>
    </div>
```

E, no `base.html`, o item **Perfis** do menu continua destacado na lixeira, acrescentando `'lixeira_perfis'` à lista do `request.endpoint`:

```html
            <a class="nav-link {% if request.endpoint in ['lista_perfis', 'perfil_novo', 'perfil_editar', 'lixeira_perfis'] %}active{% endif %}" href="{{ url_for('lista_perfis') }}">Perfis</a>
```

Salve e navegue: **Perfis**, **Lixeira**, **Voltar para os perfis**.

### Restaurar

Restaurar é desfazer a exclusão: `deletado_em` volta a ser `NULL`. É uma ação que **altera** dados, então, como a exclusão, é um `POST` com `csrf_token` (não precisa de modal: restaurar não perde nada). No `perfis_lixeira.html`, acrescente o cabeçalho depois de `Excluído em`:

```html
        <th class="text-end">Ações</th>
```

E, na linha do `for`, depois da célula do `deletado_em`:

```html
        <td class="text-end">
          <form action="{{ url_for('perfil_restaurar', perfil_id=perfil.id_perfil) }}" method="post" class="d-inline">
            <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
            <button type="submit" class="btn btn-sm btn-outline-success">Restaurar</button>
          </form>
        </td>
```

O `colspan` do `{% else %}` passa de `4` para `5`. Falta a rota. No `app.py`, depois da `perfil_excluir`:

```python
@app.route('/perfis/<int:perfil_id>/restaurar', methods=['POST'])
def perfil_restaurar(perfil_id):
    perfil = execute_one(
        'SELECT id_perfil, nome FROM perfis WHERE id_perfil = %s AND deletado_em IS NOT NULL',
        (perfil_id,),
    )
    if perfil is None:
        abort(404)

    execute_query('UPDATE perfis SET deletado_em = NULL WHERE id_perfil = %s', (perfil_id,))
    flash(f'Perfil "{perfil["nome"]}" restaurado.', 'success')

    return redirect(url_for('lista_perfis'))
```

O `SELECT` procura só entre os que **estão** na lixeira (`IS NOT NULL`): restaurar um perfil que não foi excluído, ou que não existe, responde 404. Salve, abra a lixeira e clique em **Restaurar** no `Teste`: você volta para a lista, com a faixa verde `Perfil "Teste" restaurado.` e o perfil no lugar. A lixeira mostra `A lixeira está vazia.`

Para o texto do modal deixar de prometer uma exclusão sem volta, troque, no `perfis.html`, a frase da janela de confirmação:

```html
            <p class="mb-0">Excluir o perfil <strong id="nomeExcluir"></strong>? Ele vai para a lixeira e pode ser restaurado depois.</p>
```

```bash
git add .
git commit -m "Adiciona a lixeira de perfis e a restauração"
git push
```

---

## Tópico 3 — O nome na lixeira e o perfil em uso

### O nome que ninguém vê

Há um detalhe: a coluna `nome` é `UNIQUE`, e o banco **não** sabe de `deletado_em`. Um perfil na lixeira continua ocupando o nome dele. Veja o efeito: exclua o `Teste` pelo modal e tente cadastrar de novo um perfil chamado `Teste`. A faixa vermelha diz `Já existe um perfil com este nome.`, mas a lista **não mostra** nenhum `Teste`. Para quem usa o sistema, a mensagem parece um erro. A mensagem precisa dizer que o nome está na lixeira.

A `conferir_perfil` busca o perfil com aquele nome e precisa saber **se ele foi excluído**. No `app.py`, troque o `SELECT` e o `if existente` da função por:

```python
        existente = execute_one(
            'SELECT id_perfil, deletado_em FROM perfis WHERE nome = %s AND id_perfil <> %s',
            (nome, id_atual),
        )
        if existente:
            if existente['deletado_em'] is None:
                erros.append('Já existe um perfil com este nome.')
            else:
                erros.append('Já existe um perfil excluído com este nome. Restaure-o na lixeira.')
```

Salve e tente cadastrar `Teste` de novo: a faixa vermelha agora diz `Já existe um perfil excluído com este nome. Restaure-o na lixeira.` A mesma conferência vale na edição (renomear o `Gerente` para `Teste` dá o mesmo aviso), porque as duas rotas usam a função. O erro `1062` das rotas de cadastro e de edição continua valendo como barreira final, com a mensagem de sempre.

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

## As mudanças completas do capítulo

As rotas alteradas ou novas do `app.py` (o resto do arquivo é o do Capítulo 13, sem a contagem de usuários e sem o `1451` na exclusão):

```python
@app.route('/')
def index():
    perfis = execute_one('SELECT COUNT(*) AS total FROM perfis WHERE deletado_em IS NULL')
    usuarios = execute_one('SELECT COUNT(*) AS total FROM usuarios')
    produtos = execute_one('SELECT COUNT(*) AS total FROM produtos')

    return render_template('index.html', titulo='Sistema de Gestão',
                           total_perfis=perfis['total'],
                           total_usuarios=usuarios['total'],
                           total_produtos=produtos['total'])


@app.route('/perfis')
def lista_perfis():
    perfis = execute_query(
        'SELECT id_perfil, nome, descricao, criado_em FROM perfis '
        'WHERE deletado_em IS NULL ORDER BY nome',
        fetch=True,
    )

    return render_template('perfis.html', titulo='Perfis', perfis=perfis)


@app.route('/perfis/lixeira')
def lixeira_perfis():
    perfis = execute_query(
        'SELECT id_perfil, nome, descricao, deletado_em FROM perfis '
        'WHERE deletado_em IS NOT NULL ORDER BY deletado_em DESC',
        fetch=True,
    )

    return render_template('perfis_lixeira.html', titulo='Lixeira de perfis', perfis=perfis)


def conferir_perfil(nome, descricao, id_atual):
    erros = []

    erro = validar_nome_perfil(nome)
    if erro:
        erros.append(erro)

    erro = validar_descricao_perfil(descricao)
    if erro:
        erros.append(erro)

    if not erros:
        existente = execute_one(
            'SELECT id_perfil, deletado_em FROM perfis WHERE nome = %s AND id_perfil <> %s',
            (nome, id_atual),
        )
        if existente:
            if existente['deletado_em'] is None:
                erros.append('Já existe um perfil com este nome.')
            else:
                erros.append('Já existe um perfil excluído com este nome. Restaure-o na lixeira.')

    return erros


@app.route('/perfis/<int:perfil_id>/excluir', methods=['POST'])
def perfil_excluir(perfil_id):
    perfil = execute_one(
        'SELECT id_perfil, nome FROM perfis WHERE id_perfil = %s AND deletado_em IS NULL',
        (perfil_id,),
    )
    if perfil is None:
        abort(404)

    execute_query('UPDATE perfis SET deletado_em = NOW() WHERE id_perfil = %s', (perfil_id,))
    flash(f'Perfil "{perfil["nome"]}" enviado para a lixeira.', 'success')

    return redirect(url_for('lista_perfis'))


@app.route('/perfis/<int:perfil_id>/restaurar', methods=['POST'])
def perfil_restaurar(perfil_id):
    perfil = execute_one(
        'SELECT id_perfil, nome FROM perfis WHERE id_perfil = %s AND deletado_em IS NOT NULL',
        (perfil_id,),
    )
    if perfil is None:
        abort(404)

    execute_query('UPDATE perfis SET deletado_em = NULL WHERE id_perfil = %s', (perfil_id,))
    flash(f'Perfil "{perfil["nome"]}" restaurado.', 'success')

    return redirect(url_for('lista_perfis'))
```

Na rota `perfil_editar`, o único acréscimo é o `AND deletado_em IS NULL` no `SELECT` do começo (Tópico 1). O `templates/perfis_lixeira.html`, com a coluna de ações:

```html
{% extends 'base.html' %}

{% block titulo_aba %}{{ titulo }} — Sistema de Gestão{% endblock %}

{% block conteudo %}
  <div class="d-flex justify-content-between align-items-center mb-3">
    <h1 class="h2 mb-0">{{ titulo }}</h1>
    <a href="{{ url_for('lista_perfis') }}" class="btn btn-outline-secondary">Voltar para os perfis</a>
  </div>

  <table class="table table-striped table-hover">
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
        <td>
          {% if perfil.descricao %}
            {{ perfil.descricao }}
          {% else %}
            <span class="text-body-secondary">—</span>
          {% endif %}
        </td>
        <td>{{ perfil.deletado_em.strftime('%d/%m/%Y %H:%M') }}</td>
        <td class="text-end">
          <form action="{{ url_for('perfil_restaurar', perfil_id=perfil.id_perfil) }}" method="post" class="d-inline">
            <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
            <button type="submit" class="btn btn-sm btn-outline-success">Restaurar</button>
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

No `perfis.html`, as mudanças são o grupo de botões do cabeçalho e a frase do modal (Tópico 2). No `base.html`, o `'lixeira_perfis'` na lista do menu. Os demais arquivos são os do Capítulo 13.

---

## 📦 Código deste capítulo

Compare com o seu projeto. Este capítulo é opcional, então o **Capítulo 14 não parte deste zip**, e sim do zip do Capítulo 13. O zip tem o `app.py`, o `db.py`, o `validacoes.py`, o `testar_conexao.py`, o `banco.sql`, o `.env.example`, o `.gitignore`, o `requirements.txt`, a pasta `templates` (com o novo `perfis_lixeira.html`) e a pasta `static`. O ambiente virtual e o `.env` **não** vão no zip: crie-os como no Capítulo 11.

➡️ [Baixar p2_cap_13_1.zip](../arquivos/p2_cap_13_1.zip)

---

## 🃏 Flashcards de Revisão

Tente responder mentalmente antes de abrir.

??? question "Qual a diferença entre a exclusão física e a exclusão lógica?"
    A física usa `DELETE` e remove a linha, sem volta. A lógica usa `UPDATE ... SET deletado_em = NOW()`: a linha continua no banco, marcada com a data da exclusão, e pode ser restaurada. Em troca, toda consulta precisa filtrar os excluídos.

??? question "Por que a lista de perfis precisa de `WHERE deletado_em IS NULL`?"
    Porque o registro excluído logicamente continua na tabela. Sem o filtro, ele apareceria nas listas e nas contagens como se nada tivesse acontecido. O filtro precisa estar em **todo** lugar que lê perfis: a lista, o cartão do Início, a edição e a exclusão.

??? question "Por que se escreve `IS NULL`, e não `= NULL`?"
    Porque, no MySQL, nada é igual a `NULL`, nem outro `NULL`: `deletado_em = NULL` nunca é verdadeiro. Só `IS NULL` e `IS NOT NULL` perguntam se a coluna está vazia.

??? question "O que a lixeira faz quando a pessoa clica em Restaurar?"
    Envia um `POST` para `/perfis/<id>/restaurar`, e a rota executa `UPDATE perfis SET deletado_em = NULL WHERE id_perfil = %s`. O perfil volta a ser encontrado por todos os filtros `IS NULL`. A rota só procura entre os que estão na lixeira, e responde 404 para os outros.

??? question "Por que o nome de um perfil excluído ainda barra um cadastro?"
    Porque o `UNIQUE` do banco não conhece o `deletado_em`: a linha continua na tabela, ocupando o nome. A função `conferir_perfil` lê o `deletado_em` do perfil encontrado e avisa que o nome está na lixeira, para a pessoa saber que precisa restaurá-lo.

??? question "Por que excluir um perfil com usuários não dá o erro `1451` neste capítulo?"
    Porque o erro vem de um `DELETE`, que removeria a linha da qual os usuários dependem. A exclusão lógica é só um `UPDATE`: a linha do perfil continua existindo, e a chave estrangeira não é infringida. Impedir ou aceitar isso passa a ser uma decisão da rota, e não do banco.

---

## 📝 Resumo

A exclusão lógica guarda o registro e marca a data da exclusão em `deletado_em`, coluna que já existia desde o `banco.sql` do Capítulo 11. O `DELETE` da rota virou um `UPDATE ... SET deletado_em = NOW()`, e todo `SELECT` que lê perfis ganhou o filtro `IS NULL`, na lista, no cartão do Início, na edição e na exclusão. A lixeira lista o que foi excluído (`IS NOT NULL`) e restaura com outro `UPDATE`, que devolve o `NULL`. O nome de um perfil excluído continua ocupado, e a conferência avisa isso em vez de uma mensagem que parece errada. Como o `UPDATE` não infringe a chave estrangeira, o banco deixa de recusar a exclusão de um perfil com usuários, e essa decisão passa a ser da rota. O Capítulo 14 continua do código do Capítulo 13, com o cadastro de usuários.

---

## 🔗 Navegação

⬅️ [Capítulo 13 — UPDATE e DELETE de perfis](Capitulo_13_UPDATE_e_DELETE_de_Perfis.md) · 🔒 Capítulo 14 — em breve.

---

*Fatec Jahu · ILP951 · Prof. Ronan Adriel Zenatti · 2026*
