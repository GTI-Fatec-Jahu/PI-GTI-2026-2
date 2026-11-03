# Capítulo 15 — SELECT relacional de usuário

**Disciplina:** Programação para Internet (ILP951)
**Professor:** Ronan Adriel Zenatti · ronan.zenatti@cps.sp.gov.br
**Fatec Jahu — 2º Semestre/2026**

---

## 🎯 Objetivos do Capítulo

Ao final deste capítulo você deverá ser capaz de:

- Listar os usuários em uma tabela HTML, lendo-os do banco com `SELECT`
- Trazer o nome do perfil com um `JOIN`, em vez de mostrar o número guardado em `perfil_id`
- Dar um apelido (`AS`) a uma coluna, para que duas colunas com o mesmo nome não se sobrescrevam no dicionário que o Python recebe
- Guardar a consulta em uma constante, `SELECT_USUARIO`, que **deixa a senha de fora**, e reaproveitá-la na lista e no detalhe
- Criar filtros Jinja próprios (`data_br`, `data_hora_br` e `cpf_oculto`) com `@app.template_filter`
- Mostrar um campo `NULL` como um traço, e explicar por que o filtro `default` precisa do segundo argumento `true`
- Mostrar o perfil em um **badge** colorido e reaproveitar o mesmo trecho de HTML com `{% include %}`
- Criar a página de detalhe `/usuarios/<int:id_usuario>` e responder 404 quando o código não existe

O Capítulo 14 terminou com a página `/usuarios` **provisória**: um aviso azul e nenhuma consulta ao banco. Quem cadastrava um usuário só conferia o resultado no phpMyAdmin. Este capítulo troca o aviso pela lista de verdade e acrescenta a página de detalhe. É também a primeira consulta do projeto que **junta duas tabelas**: o usuário guarda só o número do perfil, e o nome do perfil mora em outra tabela. A edição e a exclusão de usuários ficam para o Capítulo 16.

## 📦 Ponto de partida

Este capítulo continua do **seu** repositório `sistema-gestao`, como ficou no fim do Capítulo 14: com o formulário de novo usuário funcionando e a página provisória em `/usuarios`. Os Capítulos 12.1, 13.1 e 14.1 são opcionais: este capítulo parte do código do 14, e não deles.

Se o seu projeto não está funcionando, baixe o código do Capítulo 14 e descompacte. Depois de descompactar, crie o ambiente virtual e o `.env`, como no [Capítulo 11, Tópico 4](Capitulo_11_Projeto_Novo_e_Banco.md#topico-4-o-arquivo-env), importe o `banco.sql` no phpMyAdmin e cadastre os três perfis pelo formulário:

➡️ [Baixar p2_cap_14.zip](../arquivos/p2_cap_14.zip)

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

---

## Tópico 1 — A lista de usuários

### Antes de começar

Ligue o **Apache** e o **MySQL** no painel do XAMPP. Abra a pasta `sistema-gestao` no VS Code, o terminal (`Ctrl + '`), ative o ambiente virtual e confira o Git:

```bash
venv\Scripts\activate
git status
```

O `git status` deve dizer `nothing to commit, working tree clean`. Ligue o servidor com `python app.py` e deixe esse terminal rodando durante o capítulo (use um segundo terminal, o ícone **+**, para o Git).

Uma lista precisa de usuários para mostrar. Este capítulo usa os três a seguir, todos com a senha `Senha123`. Se o seu banco ainda não os tem, cadastre-os pelo formulário **Novo usuário** (ou use os seus, e o que aparece na tela será diferente do que o texto descreve):

| Nome | E-mail | Perfil | O que preencher |
|---|---|---|---|
| Ana Beatriz Lima | `ana@exemplo.com` | Administrador | só os campos obrigatórios |
| Bruno Souza | `bruno@exemplo.com` | Gerente | todos: celular `14998112030`, nascimento `14/03/1988`, CPF `52998224725`, CEP `17201000`, endereço `Rua das Flores`, número `10`, cidade `Jaú`, estado `SP` |
| Carla Dias | `carla@exemplo.com` | Usuário | só os campos obrigatórios |

O Bruno é o usuário **completo**, e a Ana e a Carla têm os campos opcionais em `NULL`. A diferença entre eles vai aparecer logo.

### O mapa do recurso

O molde de nomes do Capítulo 12 vale para `usuarios`. Este capítulo constrói a lista e o detalhe:

| Rota | Métodos | O que faz | Função no `app.py` | Template | Capítulo |
|---|---|---|---|---|---|
| `/usuarios` | GET | Lista os usuários | `lista_usuarios` | `usuarios.html` | **15** |
| `/usuarios/novo` | GET e POST | GET mostra o formulário, POST confere e grava | `usuario_novo` | `usuario_form.html` | 14 |
| `/usuarios/<int:id_usuario>` | GET | Detalhe de um usuário | `usuario_detalhe` | `usuario_detalhe.html` | **15** |
| `/usuarios/<int:id_usuario>/editar` | GET e POST | Edita o usuário | `usuario_editar` | `usuario_form.html` | 16 |
| `/usuarios/<int:id_usuario>/excluir` | só POST | Exclui o usuário | `usuario_excluir` | (nenhum) | 16 |

### A consulta mais simples

A rota `lista_usuarios` hoje só mostra o aviso. Troque-a por uma consulta ao banco, no mesmo desenho da `lista_perfis` do Capítulo 12. Por enquanto, a consulta pede as colunas **da própria tabela** `usuarios`:

```python
@app.route('/usuarios')
def lista_usuarios():
    usuarios = execute_query(
        'SELECT id_usuario, nome, email, cpf, data_nascimento, cidade, estado, perfil_id '
        'FROM usuarios ORDER BY nome',
        fetch=True,
    )

    return render_template('usuarios.html', titulo='Usuários', usuarios=usuarios)
```

Cada linha do resultado chega ao template como um **dicionário** (o `dictionary=True` do `db.py`, do Capítulo 11), e `usuarios` é a lista desses dicionários. Agora o `templates/usuarios.html`: **apague o aviso azul** (o `<div class="alert alert-info">` inteiro) e coloque no lugar a tabela, só com duas colunas:

```html
  <table class="table table-striped table-hover">
    <thead class="table-light">
      <tr>
        <th>Código</th>
        <th>Nome</th>
      </tr>
    </thead>
    <tbody>
      {% for usuario in usuarios %}
      <tr>
        <td>{{ usuario.id_usuario }}</td>
        <td>
          {{ usuario.nome }}<br>
          <small class="text-body-secondary">{{ usuario.email }}</small>
        </td>
      </tr>
      {% else %}
      <tr>
        <td colspan="2" class="text-center text-body-secondary py-4">Nenhum usuário cadastrado ainda.</td>
      </tr>
      {% endfor %}
    </tbody>
  </table>
```

É o molde da `perfis.html`: um `{% for %}` com o `{% else %}` para a lista vazia (Capítulo 5). Salve e abra **http://127.0.0.1:5000/usuarios**. A tabela mostra o código, o nome e, em letra pequena embaixo, o e-mail de cada usuário.

### Mais colunas, uma por vez

Acrescente o **CPF**. No `<thead>`, depois de `<th>Nome</th>`:

```html
        <th>CPF</th>
```

E no `<tbody>`, depois do `<td>` do nome:

```html
        <td>{{ usuario.cpf }}</td>
```

Salve e recarregue. O Bruno mostra `529.982.247-25`, e a Ana e a Carla mostram a palavra **None**. Guarde esse incômodo, ele vai ser resolvido no Tópico 3. Agora a **cidade**, com o estado ao lado (`<th>Cidade</th>` no `<thead>`, e a célula depois do CPF):

```html
        <td>{{ usuario.cidade }}/{{ usuario.estado }}</td>
```

Salve e recarregue: `Jaú/SP` para o Bruno e `None/None` para os outros dois. Depois a **data de nascimento** (`<th>Nascimento</th>` e a célula):

```html
        <td>{{ usuario.data_nascimento }}</td>
```

Salve e recarregue: o Bruno mostra `1988-03-14`, ano, mês e dia, que é como o banco e o Python escrevem a data, e não como se escreve no Brasil. E, por último, o **perfil** (`<th>Perfil</th>` e a célula):

```html
        <td>{{ usuario.perfil_id }}</td>
```

Salve e recarregue. A coluna **Perfil** mostra `1`, `2` e `3`, e não **Administrador**, **Gerente** e **Usuário**. Ninguém lê uma lista de usuários querendo saber que a Ana é o perfil número 1. Por fim, ajuste o `colspan` do estado vazio para `6`, o número de colunas da tabela.

A lista funciona e mostra os dados, mas tem quatro defeitos, e cada um tem uma solução nos próximos tópicos:

| O que se vê na tela | Por quê | Resolvido no |
|---|---|---|
| O **número** do perfil, em vez do nome | A tabela `usuarios` só guarda `perfil_id`. O nome está em `perfis` | Tópico 2 |
| A palavra `None` nos campos vazios | O `NULL` do banco chega ao Python como `None` | Tópico 3 |
| A data como `1988-03-14` | O banco entrega um objeto de data, e o Jinja o escreve no formato do banco | Tópico 3 |
| O CPF inteiro, para qualquer pessoa que abrir a lista | Nada o esconde | Tópico 3 |

```bash
git add .
git commit -m "Lista os usuários em uma tabela"
git push
```

---

## Tópico 2 — O nome do perfil com JOIN

### Dois lugares, uma informação

Cada usuário aponta para o seu perfil pelo número, a chave estrangeira `perfil_id`. O que o número significa está na tabela `perfis`:

| `usuarios.id_usuario` | `usuarios.nome` | `usuarios.perfil_id` |
|---|---|---|
| 1 | Ana Beatriz Lima | 1 |
| 2 | Bruno Souza | 2 |
| 3 | Carla Dias | 3 |

| `perfis.id_perfil` | `perfis.nome` |
|---|---|
| 1 | Administrador |
| 2 | Gerente |
| 3 | Usuário |

O `JOIN` **junta as linhas das duas tabelas** que têm o mesmo valor na chave: a linha do usuário cujo `perfil_id` vale 2 é emparelhada com a linha do perfil cujo `id_perfil` vale 2. Teste no **phpMyAdmin** (banco `gestao`, aba **SQL**) antes de levar a consulta para o Python:

```sql
SELECT u.id_usuario, u.nome, u.perfil_id, p.nome AS perfil
FROM usuarios u
JOIN perfis p ON p.id_perfil = u.perfil_id
ORDER BY u.nome;
```

O resultado traz uma linha por usuário, já com o nome do perfil ao lado do número:

| `id_usuario` | `nome` | `perfil_id` | `perfil` |
|---|---|---|---|
| 1 | Ana Beatriz Lima | 1 | Administrador |
| 2 | Bruno Souza | 2 | Gerente |
| 3 | Carla Dias | 3 | Usuário |

Três detalhes da consulta, que você já viu no curso de banco de dados. O `u` e o `p` depois dos nomes das tabelas são **apelidos**, para escrever `u.nome` em vez de `usuarios.nome`. O `ON` diz **quais colunas** devem ser iguais. E o `JOIN` sozinho é o `INNER JOIN`: só entram usuários que têm um perfil, e todos têm, porque `perfil_id` é `NOT NULL` e a chave estrangeira não deixa gravar um perfil que não existe.

### Levar o JOIN para a rota

Troque a consulta da `lista_usuarios` por esta. Ela ainda **não** tem o `AS perfil`, de propósito:

```python
    usuarios = execute_query(
        'SELECT u.id_usuario, u.nome, u.email, u.cpf, u.data_nascimento, u.cidade, u.estado, '
        'p.nome '
        'FROM usuarios u '
        'JOIN perfis p ON p.id_perfil = u.perfil_id '
        'ORDER BY u.nome',
        fetch=True,
    )
```

Salve e recarregue a lista. A coluna **Nome** passou a mostrar `Administrador`, `Gerente` e `Usuário`, e os nomes das pessoas **sumiram**. A coluna **Perfil** ficou vazia.

O que aconteceu: o resultado tem **duas colunas chamadas `nome`**, a do usuário e a do perfil. Cada linha vira um dicionário do Python, e um dicionário **não aceita a mesma chave duas vezes**: a segunda `nome` (a do perfil) sobrescreve a primeira. A saída é dar um **apelido à coluna** com `AS`. Troque `'p.nome '` por:

```python
        'p.nome AS perfil '
```

E, no `usuarios.html`, troque `{{ usuario.perfil_id }}` por:

```html
        <td>{{ usuario.perfil }}</td>
```

Salve e recarregue. Os nomes das pessoas voltaram, e a coluna **Perfil** mostra **Administrador**, **Gerente** e **Usuário**. O `AS perfil` é o que dá nome à chave do dicionário: `usuario.perfil`.

### Uma constante para a consulta

A página de detalhe do Tópico 5, e a edição do Capítulo 16, precisam **das mesmas colunas**, com o mesmo `JOIN`. Escrever essa consulta comprida de novo em cada rota é pedir para uma delas ficar diferente das outras. A solução é escrevê-la **uma vez só**, em uma constante no topo do `app.py`. Coloque-a logo depois da linha `CSRFProtect(app)`:

```python
# As colunas que as telas de usuário leem. A senha fica de fora de propósito: o que não é
# lido do banco não tem como vazar para a página.
SELECT_USUARIO = (
    'SELECT u.id_usuario, u.nome, u.email, u.celular, u.data_nascimento, u.cpf, '
    'u.perfil_id, u.cep, u.endereco, u.numero, u.complemento, u.cidade, u.estado, '
    'u.criado_em, u.atualizado_em, p.nome AS perfil, p.descricao AS perfil_descricao '
    'FROM usuarios u '
    'JOIN perfis p ON p.id_perfil = u.perfil_id'
)
```

!!! note "Python: uma constante, e o `+` entre textos"
    Por convenção, uma variável que **não muda** é escrita em MAIÚSCULAS: `SELECT_USUARIO` é um texto que o programa só lê. Os parênteses permitem quebrar o texto em várias linhas, e os pedaços colados, um embaixo do outro, viram **um único texto** (o mesmo recurso do `INSERT` do Capítulo 14). Para acrescentar uma cláusula à consulta, o `+` junta dois textos: `SELECT_USUARIO + ' ORDER BY u.nome'`. Juntar **textos fixos** é seguro. O que nunca se faz é juntar ao SQL o que a pessoa digitou: para isso existem os `%s`, como no resto do projeto.

Agora a rota usa a constante, e a consulta que estava dentro dela sai:

```python
@app.route('/usuarios')
def lista_usuarios():
    usuarios = execute_query(SELECT_USUARIO + ' ORDER BY u.nome', fetch=True)

    return render_template('usuarios.html', titulo='Usuários', usuarios=usuarios)
```

Salve e recarregue: a lista está **igual** à anterior. A mudança foi só de organização, e a lista agora pede mais colunas do que mostra (celular, CEP, endereço e outras), que o detalhe vai usar.

!!! note "A senha não está na lista, e é de propósito"
    Repare no que **falta** no `SELECT_USUARIO`: a coluna `senha`. Nenhuma tela do sistema precisa do hash, e o que não é lido do banco não tem como vazar para a página, nem por um descuido em um template. É por isso que o `SELECT *` não é usado nas telas de usuário: ele traria a senha junto. Só o login, no Capítulo 17, vai ler o hash, em uma consulta própria.

```bash
git add .
git commit -m "Traz o nome do perfil com JOIN e cria o SELECT_USUARIO"
git push
```

---

## Tópico 3 — Filtros próprios: campos vazios, datas e CPF

### O `None` e o `default`

O Capítulo 5 ensinou o filtro `default`, que mostra um texto quando o valor falta. Experimente-o na cidade. No `usuarios.html`, troque a célula da cidade por:

```html
        <td>{{ usuario.cidade|default('—') }}/{{ usuario.estado }}</td>
```

Salve e recarregue. **Nada mudou**: a Ana e a Carla continuam com `None/None`. O motivo está no aviso que o Capítulo 5 deixou: o `default` age quando o valor **não existe**, e o `None` do banco **existe** (é um valor, o "sem valor"). Para o `default` tratar também o que é vazio (`None`, `''`), acrescente um segundo argumento, `true`. E o estado só deve aparecer, com a barra, quando existir:

```html
        <td>{{ usuario.cidade|default('—', true) }}{% if usuario.estado %}/{{ usuario.estado }}{% endif %}</td>
```

!!! note "Jinja: `default('—', true)`"
    O segundo argumento `true` manda o `default` trocar **qualquer valor vazio**, e não só o que não existe: `None` (o `NULL` do banco) e o texto vazio. O `{% if usuario.estado %}` usa a mesma ideia: o `None` conta como falso, então a barra e a sigla só saem quando há um estado.

Salve e recarregue. A Ana e a Carla mostram `—` na coluna da cidade, e o Bruno continua com `Jaú/SP`.

### A data: um filtro só nosso

A data de nascimento aparece como `1988-03-14`, e o Brasil escreve `14/03/1988`. O Capítulo 12 já formatou o `criado_em` direto no template, com o `strftime` (veja [a coluna Criado em](Capitulo_12_INSERT_e_SELECT_de_Perfis.md#a-coluna-criado-em)). Faça o mesmo com o nascimento, **só para ver** o que acontece. Troque a célula por:

```html
        <td>{{ usuario.data_nascimento.strftime('%d/%m/%Y') }}</td>
```

Salve e recarregue. A página quebra na **Ana**, que não tem data de nascimento, com algo assim:

```text
jinja2.exceptions.UndefinedError: 'None' has no attribute 'strftime'
```

A data de nascimento é um campo opcional, e o `None` não tem o método `strftime`. Seria preciso um `{% if %}` em volta de **cada** data de **cada** tela. O Flask oferece um jeito melhor: um **filtro próprio**, uma função Python que o template chama com o mesmo `|` dos filtros que você já conhece. Volte a célula para `{{ usuario.data_nascimento }}` e, no `app.py`, **depois** da constante `SELECT_USUARIO`, escreva:

```python
@app.template_filter('data_br')
def data_br(valor):
    if valor is None:
        return '—'

    return valor.strftime('%d/%m/%Y')
```

!!! note "Flask: `@app.template_filter`"
    É um decorador, como o `@app.route` ([Capítulo 3](Capitulo_03_Flask.md)) e o `@app.errorhandler` ([Capítulo 6](Capitulo_06_Heranca_Include_e_Paginas_de_Erro.md)). O `@app.route` liga uma função a um **endereço**. O `@app.template_filter('data_br')` liga uma função a um **nome de filtro**: a partir daí, o template pode escrever `{{ algo|data_br }}`, e o Jinja chama a função, entregando `algo` no parâmetro `valor` e escrevendo o que ela devolve com `return`. O dado original **não muda**, só a exibição. O nome entre aspas é o que se escreve depois do `|`; o nome da função é livre (aqui são iguais, para não confundir).

A função trata o `None` **uma vez**, e todas as telas se beneficiam. Use o filtro na célula do nascimento:

```html
        <td>{{ usuario.data_nascimento|data_br }}</td>
```

Salve e recarregue. O Bruno mostra `14/03/1988`, e a Ana e a Carla mostram `—`, **sem erro**.

### O filtro vale para o projeto todo

A lista de **perfis**, do Capítulo 12, escreve o `strftime` direto no template. Agora que existe o filtro, a repetição pode sair. No `perfis.html`, troque a célula do **Criado em**:

```html
        <td>{{ perfil.criado_em|data_br }}</td>
```

Salve e abra **http://127.0.0.1:5000/perfis**: a coluna **Criado em** continua com `03/11/2026` (ou a data de hoje), só que escrita agora por uma função que fica em **um** lugar. O filtro funciona com `date` (a data de nascimento) e com `datetime` (o `criado_em`), porque os dois têm o `strftime`.

### O CPF: mostrar o mínimo

Até aqui, o CPF aparece inteiro na lista, para qualquer pessoa que abra a página. O CPF é um **dado pessoal**, protegido pela LGPD (a lei de proteção de dados), e uma tela que o mostra para todo mundo expõe mais do que precisa: para escolher em quem clicar, ninguém precisa do número completo. A solução é a mesma, um filtro próprio, que esconde as pontas do CPF. Acrescente ao `app.py`, depois do `data_br`:

```python
@app.template_filter('cpf_oculto')
def cpf_oculto(cpf):
    if cpf is None:
        return '—'

    return '***.' + cpf[4:11] + '-**'
```

O CPF é gravado como `000.000.000-00` (Capítulo 14), e é isso que a função recebe. Conte as posições, a partir do zero, como no [Capítulo 14](Capitulo_14_INSERT_Relacional_de_Usuario.md): em `529.982.247-25`, o trecho `982.247`, o do meio, ocupa as posições de **4 até antes da 11**, e a fatia `cpf[4:11]` o devolve. O `+` junta os três pedaços. Use o filtro na célula do CPF:

```html
        <td>{{ usuario.cpf|cpf_oculto }}</td>
```

Salve e recarregue. O Bruno mostra `***.982.247-**`, e a Ana e a Carla mostram `—`. A lista mostra o mínimo. O CPF **inteiro** aparece só na página de detalhe, que se abre por escolha de quem a procura (Tópico 5).

Confira a lista inteira: nenhum `None`, nenhuma data no formato do banco, nenhum CPF exposto. O `colspan` já está certo, porque o número de colunas não mudou.

```bash
git add .
git commit -m "Cria os filtros data_br e cpf_oculto e trata os campos vazios"
git push
```

---

## Tópico 4 — O perfil em um badge

### Uma cor para cada perfil

Um **badge** é a etiqueta colorida do Bootstrap (`<span class="badge ...">`). Com ele, o perfil se reconhece de relance, sem ler. Quem decide a cor é um `if/elif/else`, o mesmo do Capítulo 5, que decidia a faixa de preço de um produto. No `usuarios.html`, troque a célula do perfil por:

```html
        <td>
          {% if usuario.perfil == 'Administrador' %}
            <span class="badge text-bg-danger">Administrador</span>
          {% elif usuario.perfil == 'Gerente' %}
            <span class="badge text-bg-warning">Gerente</span>
          {% else %}
            <span class="badge text-bg-secondary">{{ usuario.perfil }}</span>
          {% endif %}
        </td>
```

Salve e recarregue. A Ana aparece com um badge **vermelho**, o Bruno com um **amarelo**, e a Carla com um **cinza**. O `text-bg-danger`, o `text-bg-warning` e o `text-bg-secondary` são classes do Bootstrap que escolhem a cor do fundo **e** uma cor de letra que combina com ela.

!!! note "O `else` cobre os perfis que você ainda não conhece"
    O `if` compara o **nome** do perfil, escrito exatamente como foi cadastrado. Um perfil novo (digamos, **Financeiro**) não cai em nenhum `if` nem `elif`, e o `else` o mostra com o badge cinza e o próprio nome, sem quebrar nada. O mesmo acontece se o perfil do administrador tiver sido cadastrado com outra grafia, como `Admin`: ele aparece em cinza, e não em vermelho.

```bash
git add .
git commit -m "Mostra o perfil do usuário em um badge colorido"
git push
```

---

## Tópico 5 — A página de detalhe

### Uma página para cada usuário

A lista mostra o essencial de todos. O **detalhe** mostra tudo sobre **um** usuário, em um endereço próprio (`/usuarios/2`), que dá para guardar e compartilhar. Os ingredientes você já tem: a variável de rota `<int:id_usuario>` e o `abort(404)` do [Capítulo 13](Capitulo_13_UPDATE_e_DELETE_de_Perfis.md), e o `execute_one`, que o `db.py` trouxe no Capítulo 11. No `app.py`, acrescente a rota **depois** da `usuario_novo` e antes dos `@app.errorhandler`:

```python
@app.route('/usuarios/<int:id_usuario>')
def usuario_detalhe(id_usuario):
    usuario = execute_one(SELECT_USUARIO + ' WHERE u.id_usuario = %s', (id_usuario,))

    return render_template('usuario_detalhe.html', usuario=usuario)
```

A rota **reaproveita** o `SELECT_USUARIO`: o mesmo `JOIN`, as mesmas colunas e, de novo, nenhuma senha. O `WHERE` leva um `%s`, e o código vem na tupla `(id_usuario,)`, com a vírgula do Capítulo 13. O parâmetro leva o nome da chave primária, `id_usuario`, como manda o molde do projeto.

Crie o `templates/usuario_detalhe.html`, por enquanto só com o nome e o botão de voltar:

```html
{% extends 'base.html' %}

{% block titulo_aba %}{{ usuario.nome }} — Sistema de Gestão{% endblock %}

{% block conteudo %}
  <div class="d-flex justify-content-between align-items-center mb-3">
    <h1 class="h2 mb-0">{{ usuario.nome }}</h1>
    <a href="{{ url_for('lista_usuarios') }}" class="btn btn-outline-secondary">Voltar à lista</a>
  </div>
{% endblock %}
```

Salve e abra **http://127.0.0.1:5000/usuarios/2**: o título é **Bruno Souza**, e o botão volta para a lista. Falta o caminho de clique. No `usuarios.html`, acrescente a coluna **Ações**: no `<thead>`, depois de `<th>Perfil</th>`:

```html
        <th class="text-end">Ações</th>
```

E, no `<tbody>`, depois da célula do perfil:

```html
        <td class="text-end">
          <a href="{{ url_for('usuario_detalhe', id_usuario=usuario.id_usuario) }}" class="btn btn-sm btn-outline-primary">Ver</a>
        </td>
```

Troque o `colspan` do estado vazio para `7`. O `url_for` recebe o nome da **função** da rota e o argumento que preenche o `<int:id_usuario>`: gera `/usuarios/1`, `/usuarios/2` e assim por diante, sem escrever endereço nenhum à mão. Salve, recarregue a lista e clique em **Ver**.

### Os dados do usuário

O restante da página é um **cartão** com quatro blocos. Cada dado fica em uma linha de uma **lista de descrição** (`<dl>`), em que o `<dt>` é o rótulo e o `<dd>` é o valor. O `row` e o `col-sm-4`/`col-sm-8` do Bootstrap alinham os dois lado a lado. Acrescente, **dentro** do bloco `conteudo`, abaixo do `<div class="d-flex ...">` do título, o cartão com o primeiro bloco:

```html
  <div class="row">
    <div class="col-lg-8">
      <div class="card">
        <div class="card-body">

          <h2 class="h5 mb-3">Dados principais</h2>
          <dl class="row">
            <dt class="col-sm-4">E-mail</dt>
            <dd class="col-sm-8">{{ usuario.email }}</dd>

            <dt class="col-sm-4">Perfil</dt>
            <dd class="col-sm-8">
              {% if usuario.perfil == 'Administrador' %}
                <span class="badge text-bg-danger">Administrador</span>
              {% elif usuario.perfil == 'Gerente' %}
                <span class="badge text-bg-warning">Gerente</span>
              {% else %}
                <span class="badge text-bg-secondary">{{ usuario.perfil }}</span>
              {% endif %}
              <span class="text-body-secondary">{{ usuario.perfil_descricao|default('', true) }}</span>
            </dd>

            <dt class="col-sm-4">Celular</dt>
            <dd class="col-sm-8">{{ usuario.celular|default('—', true) }}</dd>
          </dl>

        </div>
      </div>
    </div>
  </div>
```

O perfil mostra o badge **e a descrição do perfil**, que veio do `JOIN` (`p.descricao AS perfil_descricao`). O campo celular é opcional, e o `default('—', true)` do Tópico 3 cuida do `NULL`. Salve e recarregue o detalhe do Bruno e o da Ana: o celular dele aparece formatado, e o dela mostra `—`.

Agora os **dados pessoais**. Acrescente, dentro do `<div class="card-body">`, depois do `</dl>` do bloco anterior:

```html
          <h2 class="h5 mb-3">Dados pessoais</h2>
          <dl class="row">
            <dt class="col-sm-4">Data de nascimento</dt>
            <dd class="col-sm-8">{{ usuario.data_nascimento|data_br }}</dd>

            <dt class="col-sm-4">CPF</dt>
            <dd class="col-sm-8">{{ usuario.cpf|default('—', true) }}</dd>
          </dl>
```

Salve e recarregue o detalhe do Bruno: o nascimento usa o filtro `data_br`, e o CPF aparece **inteiro**, `529.982.247-25`, porque aqui ele é só `default`, sem o `cpf_oculto`. Quem chegou ao detalhe escolheu ver aquele usuário. Depois, o **endereço**:

```html
          <h2 class="h5 mb-3">Endereço</h2>
          <dl class="row">
            <dt class="col-sm-4">CEP</dt>
            <dd class="col-sm-8">{{ usuario.cep|default('—', true) }}</dd>

            <dt class="col-sm-4">Endereço</dt>
            <dd class="col-sm-8">{{ usuario.endereco|default('—', true) }}</dd>

            <dt class="col-sm-4">Número</dt>
            <dd class="col-sm-8">{{ usuario.numero|default('—', true) }}</dd>

            <dt class="col-sm-4">Complemento</dt>
            <dd class="col-sm-8">{{ usuario.complemento|default('—', true) }}</dd>

            <dt class="col-sm-4">Cidade</dt>
            <dd class="col-sm-8">{{ usuario.cidade|default('—', true) }}</dd>

            <dt class="col-sm-4">Estado</dt>
            <dd class="col-sm-8">{{ usuario.estado|default('—', true) }}</dd>
          </dl>
```

Salve e recarregue: o Bruno mostra o endereço completo (o complemento, que ele não preencheu, aparece como `—`), e a Ana, seis traços.

### Data e hora: outro filtro

O último bloco mostra **quando** o usuário foi cadastrado e alterado. Essas colunas (`criado_em` e `atualizado_em`) são `TIMESTAMP`, e o interessante é mostrar também a **hora**. O `data_br` só escreve o dia. Em vez de mudar o `data_br`, que a lista continua usando, acrescente um segundo filtro ao `app.py`, depois do `data_br`:

```python
@app.template_filter('data_hora_br')
def data_hora_br(valor):
    if valor is None:
        return '—'

    return valor.strftime('%d/%m/%Y às %H:%M')
```

O `%H:%M` é a hora e os minutos (o [Capítulo 12](Capitulo_12_INSERT_e_SELECT_de_Perfis.md#a-coluna-criado-em) apresentou esses modelos). A hora que aparece é a de Brasília: o `time_zone` do `db.py` (Capítulo 10) faz o banco e o Python concordarem, em qualquer computador. Acrescente o bloco, depois do `</dl>` do endereço:

```html
          <h2 class="h5 mb-3">Registro</h2>
          <dl class="row mb-0">
            <dt class="col-sm-4">Cadastrado em</dt>
            <dd class="col-sm-8">{{ usuario.criado_em|data_hora_br }}</dd>

            <dt class="col-sm-4">Última alteração</dt>
            <dd class="col-sm-8">{{ usuario.atualizado_em|data_hora_br }}</dd>
          </dl>
```

Salve e recarregue: algo como `03/11/2026 às 10:15`. Confira o detalhe dos três usuários. Em nenhum deles aparece a senha: ela nem foi lida do banco.

### O código que não existe

Com a página completa, tente um endereço de um usuário que **não existe**: **http://127.0.0.1:5000/usuarios/99999**. A página de depuração do Flask aparece, com algo assim:

```text
jinja2.exceptions.UndefinedError: 'None' has no attribute 'data_nascimento'
```

O `execute_one` devolveu `None` (nenhuma linha tem esse código), e o template tentou ler a data de nascimento de um usuário que não existe. Quem usa o sistema veria a página 500, mas o defeito **não é do servidor**: é um pedido por algo que não está lá, e o certo é responder **404**. Na rota, entre o `execute_one` e o `render_template`, acrescente a conferência (a mesma da `perfil_editar`, do Capítulo 13):

```python
    if usuario is None:
        abort(404)
```

Salve e abra de novo `/usuarios/99999`: a página 404 do projeto, a do Capítulo 11. O endereço `/usuarios/abc` também responde 404, sem chegar à função: o `<int:id_usuario>` só aceita número.

### O mesmo `if` em dois arquivos

Há uma repetição que fica: o `if/elif/else` do badge está escrito no `usuarios.html` **e** no `usuario_detalhe.html`. Se uma cor mudar, ou um perfil novo ganhar a sua, será preciso lembrar dos dois. É o mesmo problema que o Capítulo 6 resolveu para a faixa de preço, e a ferramenta é a mesma, o `{% include %}`: um pedaço de HTML guardado em um arquivo próprio. Crie o `templates/_badge_perfil.html`:

```html
{% if usuario.perfil == 'Administrador' %}
  <span class="badge text-bg-danger">Administrador</span>
{% elif usuario.perfil == 'Gerente' %}
  <span class="badge text-bg-warning">Gerente</span>
{% else %}
  <span class="badge text-bg-secondary">{{ usuario.perfil }}</span>
{% endif %}
```

No `usuarios.html`, troque o `<td>` do perfil inteiro por:

```html
        <td>{% include '_badge_perfil.html' %}</td>
```

E, no `usuario_detalhe.html`, troque o `if` do perfil (as sete linhas, **sem** a linha da descrição) por:

```html
              {% include '_badge_perfil.html' %}
```

O arquivo incluído enxerga a variável `usuario` do lugar onde foi escrito: na lista, é o `usuario` de cada volta do `for`, e, no detalhe, é o `usuario` que a rota entregou. Por isso as **duas** páginas precisam chamar a variável de `usuario`. Salve e confira: as cores continuam as mesmas, e agora há um só lugar para mudá-las.

### O menu continua aceso

Falta um detalhe do menu. Abra o detalhe de um usuário: o item **Usuários** está **apagado**, porque o `base.html` só o acende nas páginas `lista_usuarios` e `usuario_novo`. No `base.html`, acrescente a nova página à lista do item Usuários:

```html
            <a class="nav-link {% if request.endpoint in ['lista_usuarios', 'usuario_novo', 'usuario_detalhe'] %}active{% endif %}" href="{{ url_for('lista_usuarios') }}">Usuários</a>
```

Salve e recarregue o detalhe: o menu **Usuários** está aceso. Faça agora o caminho completo: **Novo usuário**, cadastre um (o redirect já cai na lista de verdade, com a faixa verde), clique em **Ver** e volte pelo botão. Este capítulo termina sem botões de editar e excluir: eles chegam à lista no Capítulo 16.

| Situação | Quem trata | O que a pessoa vê |
|---|---|---|
| Usuário sem CPF, sem nascimento ou sem cidade | Filtros `cpf_oculto` e `data_br` e `default('—', true)` | Um traço (`—`) |
| Perfil que não é Administrador nem Gerente | O `else` do `_badge_perfil.html` | Badge cinza com o nome do perfil |
| Código de usuário que não existe | `SELECT` + `abort(404)` | A página 404 |
| Endereço com letras (`/usuarios/abc`) | O `<int:id_usuario>` | A página 404 |

```bash
git add .
git commit -m "Adiciona a página de detalhe do usuário, com 404 e o include do badge"
git push
```

---

## Os arquivos completos do capítulo

O `app.py`:

```python
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
    perfis = execute_one('SELECT COUNT(*) AS total FROM perfis')
    usuarios = execute_one('SELECT COUNT(*) AS total FROM usuarios')
    produtos = execute_one('SELECT COUNT(*) AS total FROM produtos')

    return render_template('index.html', titulo='Sistema de Gestão',
                           total_perfis=perfis['total'],
                           total_usuarios=usuarios['total'],
                           total_produtos=produtos['total'])


@app.route('/perfis')
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

    return render_template('usuarios.html', titulo='Usuários', usuarios=usuarios)


def vazio_para_none(valor):
    if valor == '':
        return None

    return valor


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


@app.route('/usuarios/novo', methods=['GET', 'POST'])
def usuario_novo():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip().lower()
        senha = request.form.get('senha', '')
        confirmacao = request.form.get('confirmacao', '')
        celular = request.form.get('celular', '').strip()
        data_nascimento = request.form.get('data_nascimento', '').strip()
        cpf = request.form.get('cpf', '').strip()
        perfil_txt = request.form.get('perfil_id', '')
        cep = request.form.get('cep', '').strip()
        endereco = request.form.get('endereco', '').strip()
        numero = request.form.get('numero', '').strip()
        complemento = request.form.get('complemento', '').strip()
        cidade = request.form.get('cidade', '').strip()
        estado = request.form.get('estado', '')

        erros = []

        erro = validar_nome_usuario(nome)
        if erro:
            erros.append(erro)

        erro = validar_email(email)
        if erro:
            erros.append(erro)
        else:
            existente = execute_one(
                'SELECT id_usuario FROM usuarios WHERE email = %s',
                (email,),
            )
            if existente:
                erros.append('Já existe um usuário com este e-mail.')

        erro = validar_senha(senha, confirmacao)
        if erro:
            erros.append(erro)

        erro = conferir_perfil_do_usuario(perfil_txt)
        if erro:
            erros.append(erro)

        erro = validar_celular(celular)
        if erro:
            erros.append(erro)

        erro = validar_cpf(cpf)
        if erro:
            erros.append(erro)
        else:
            cpf_formatado = formatar_cpf(cpf)
            if cpf_formatado != '':
                existente = execute_one(
                    'SELECT id_usuario FROM usuarios WHERE cpf = %s',
                    (cpf_formatado,),
                )
                if existente:
                    erros.append('Já existe um usuário com este CPF.')

        erro = validar_data_nascimento(data_nascimento)
        if erro:
            erros.append(erro)

        erro = validar_cep(cep)
        if erro:
            erros.append(erro)

        erro = validar_tamanho(endereco, 'endereço', 255)
        if erro:
            erros.append(erro)

        erro = validar_tamanho(numero, 'número', 20)
        if erro:
            erros.append(erro)

        erro = validar_tamanho(complemento, 'complemento', 100)
        if erro:
            erros.append(erro)

        erro = validar_tamanho(cidade, 'cidade', 100)
        if erro:
            erros.append(erro)

        erro = validar_estado(estado)
        if erro:
            erros.append(erro)

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
                        nome,
                        email,
                        generate_password_hash(senha),
                        vazio_para_none(formatar_celular(celular)),
                        vazio_para_none(data_nascimento),
                        vazio_para_none(formatar_cpf(cpf)),
                        int(perfil_txt),
                        vazio_para_none(formatar_cep(cep)),
                        vazio_para_none(endereco),
                        vazio_para_none(numero),
                        vazio_para_none(complemento),
                        vazio_para_none(cidade),
                        vazio_para_none(estado),
                    ),
                )
                flash(f'Usuário "{nome}" cadastrado (código {novo_id}).', 'success')
                return redirect(url_for('lista_usuarios'))
            except Error as erro:
                if erro.errno == 1062:
                    flash('Já existe um usuário com este e-mail ou este CPF.', 'danger')
                else:
                    raise

    perfis = execute_query('SELECT id_perfil, nome FROM perfis ORDER BY nome', fetch=True)

    return render_template('usuario_form.html', dados=request.form, perfis=perfis, ufs=UFS)


@app.route('/usuarios/<int:id_usuario>')
def usuario_detalhe(id_usuario):
    usuario = execute_one(SELECT_USUARIO + ' WHERE u.id_usuario = %s', (id_usuario,))
    if usuario is None:
        abort(404)

    return render_template('usuario_detalhe.html', usuario=usuario)


@app.errorhandler(404)
def pagina_nao_encontrada(erro):
    return render_template('404.html'), 404


@app.errorhandler(500)
def erro_no_servidor(erro):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
```

O `templates/usuarios.html`:

```html
{% extends 'base.html' %}

{% block titulo_aba %}{{ titulo }} — Sistema de Gestão{% endblock %}

{% block conteudo %}
  <div class="d-flex justify-content-between align-items-center mb-3">
    <h1 class="h2 mb-0">{{ titulo }}</h1>
    <a href="{{ url_for('usuario_novo') }}" class="btn btn-primary">Novo usuário</a>
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
          {{ usuario.nome }}<br>
          <small class="text-body-secondary">{{ usuario.email }}</small>
        </td>
        <td>{{ usuario.cpf|cpf_oculto }}</td>
        <td>{{ usuario.cidade|default('—', true) }}{% if usuario.estado %}/{{ usuario.estado }}{% endif %}</td>
        <td>{{ usuario.data_nascimento|data_br }}</td>
        <td>{% include '_badge_perfil.html' %}</td>
        <td class="text-end">
          <a href="{{ url_for('usuario_detalhe', id_usuario=usuario.id_usuario) }}" class="btn btn-sm btn-outline-primary">Ver</a>
        </td>
      </tr>
      {% else %}
      <tr>
        <td colspan="7" class="text-center text-body-secondary py-4">Nenhum usuário cadastrado ainda.</td>
      </tr>
      {% endfor %}
    </tbody>
  </table>
{% endblock %}
```

O `templates/usuario_detalhe.html`:

```html
{% extends 'base.html' %}

{% block titulo_aba %}{{ usuario.nome }} — Sistema de Gestão{% endblock %}

{% block conteudo %}
  <div class="d-flex justify-content-between align-items-center mb-3">
    <h1 class="h2 mb-0">{{ usuario.nome }}</h1>
    <a href="{{ url_for('lista_usuarios') }}" class="btn btn-outline-secondary">Voltar à lista</a>
  </div>

  <div class="row">
    <div class="col-lg-8">
      <div class="card">
        <div class="card-body">

          <h2 class="h5 mb-3">Dados principais</h2>
          <dl class="row">
            <dt class="col-sm-4">E-mail</dt>
            <dd class="col-sm-8">{{ usuario.email }}</dd>

            <dt class="col-sm-4">Perfil</dt>
            <dd class="col-sm-8">
              {% include '_badge_perfil.html' %}
              <span class="text-body-secondary">{{ usuario.perfil_descricao|default('', true) }}</span>
            </dd>

            <dt class="col-sm-4">Celular</dt>
            <dd class="col-sm-8">{{ usuario.celular|default('—', true) }}</dd>
          </dl>

          <h2 class="h5 mb-3">Dados pessoais</h2>
          <dl class="row">
            <dt class="col-sm-4">Data de nascimento</dt>
            <dd class="col-sm-8">{{ usuario.data_nascimento|data_br }}</dd>

            <dt class="col-sm-4">CPF</dt>
            <dd class="col-sm-8">{{ usuario.cpf|default('—', true) }}</dd>
          </dl>

          <h2 class="h5 mb-3">Endereço</h2>
          <dl class="row">
            <dt class="col-sm-4">CEP</dt>
            <dd class="col-sm-8">{{ usuario.cep|default('—', true) }}</dd>

            <dt class="col-sm-4">Endereço</dt>
            <dd class="col-sm-8">{{ usuario.endereco|default('—', true) }}</dd>

            <dt class="col-sm-4">Número</dt>
            <dd class="col-sm-8">{{ usuario.numero|default('—', true) }}</dd>

            <dt class="col-sm-4">Complemento</dt>
            <dd class="col-sm-8">{{ usuario.complemento|default('—', true) }}</dd>

            <dt class="col-sm-4">Cidade</dt>
            <dd class="col-sm-8">{{ usuario.cidade|default('—', true) }}</dd>

            <dt class="col-sm-4">Estado</dt>
            <dd class="col-sm-8">{{ usuario.estado|default('—', true) }}</dd>
          </dl>

          <h2 class="h5 mb-3">Registro</h2>
          <dl class="row mb-0">
            <dt class="col-sm-4">Cadastrado em</dt>
            <dd class="col-sm-8">{{ usuario.criado_em|data_hora_br }}</dd>

            <dt class="col-sm-4">Última alteração</dt>
            <dd class="col-sm-8">{{ usuario.atualizado_em|data_hora_br }}</dd>
          </dl>

        </div>
      </div>
    </div>
  </div>
{% endblock %}
```

O `templates/_badge_perfil.html`:

```html
{% if usuario.perfil == 'Administrador' %}
  <span class="badge text-bg-danger">Administrador</span>
{% elif usuario.perfil == 'Gerente' %}
  <span class="badge text-bg-warning">Gerente</span>
{% else %}
  <span class="badge text-bg-secondary">{{ usuario.perfil }}</span>
{% endif %}
```

As mudanças nos outros arquivos são duas linhas: no `perfis.html`, a célula do **Criado em** (`{{ perfil.criado_em|data_br }}`), e, no `base.html`, o item **Usuários** do menu, com o `usuario_detalhe` na lista. Os demais arquivos (`db.py`, `validacoes.py`, `index.html`, `perfil_form.html`, `usuario_form.html`, `404.html`, `500.html`, `estilo.css`, `testar_conexao.py`) são os do Capítulo 14.

---

## 📦 Código deste capítulo

Compare com o seu projeto, ou use como ponto de partida do próximo capítulo. O zip tem o `app.py`, o `db.py`, o `validacoes.py`, o `testar_conexao.py`, o `banco.sql`, o `.env.example`, o `.gitignore`, o `requirements.txt`, a pasta `templates` (`base.html`, `index.html`, `perfis.html`, `perfil_form.html`, `usuarios.html`, `usuario_form.html`, `usuario_detalhe.html`, `_badge_perfil.html`, `404.html` e `500.html`) e a pasta `static` (`estilo.css`). O ambiente virtual e o `.env` **não** vão no zip: depois de descompactar, crie o ambiente com os três comandos do Capítulo 3 e rode `copy .env.example .env`, trocando os marcadores `SUA_SENHA_AQUI` e `NOME_BANCO_DADOS` como no Capítulo 11. O banco também não vai dentro do zip: importe o `banco.sql`, cadastre os três perfis e alguns usuários pelo formulário.

➡️ [Baixar p2_cap_15.zip](../arquivos/p2_cap_15.zip)

---

## 🃏 Flashcards de Revisão

Tente responder mentalmente antes de abrir.

??? question "Por que a lista de usuários precisa de um `JOIN`?"
    Porque a tabela `usuarios` guarda só o número do perfil (`perfil_id`, a chave estrangeira), e o nome do perfil está na tabela `perfis`. O `JOIN` emparelha cada usuário com a linha do perfil que tem o mesmo valor na chave (`ON p.id_perfil = u.perfil_id`) e devolve os dois juntos, para a lista mostrar **Administrador**, e não `1`.

??? question "Por que a consulta com `JOIN` precisa de `p.nome AS perfil`?"
    Porque o resultado teria duas colunas chamadas `nome`, e cada linha vira um **dicionário** do Python, que não aceita a mesma chave duas vezes: a do perfil sobrescreveria a do usuário, e os nomes das pessoas sumiriam da lista. O `AS perfil` dá a segunda coluna um nome próprio.

??? question "Por que o `SELECT_USUARIO` não tem a coluna `senha`?"
    Porque nenhuma tela precisa do hash, e o que não é lido do banco não tem como vazar para a página, nem por um descuido em um template. É por isso que as telas de usuário não usam `SELECT *`. Só o login lê a senha, em uma consulta própria.

??? question "O que faz o decorador `@app.template_filter('data_br')`?"
    Registra a função logo abaixo como um **filtro** do Jinja, com o nome `data_br`. Depois disso, qualquer template pode escrever `{{ valor|data_br }}`: o Jinja chama a função com o valor e escreve o que ela devolve. A função trata o `None` uma vez, e o dado original não muda, só a exibição.

??? question "Por que `default('—')` não trocou o `None` e `default('—', true)` trocou?"
    O `default` sozinho só age quando o valor **não existe**, e o `NULL` do banco chega ao Python como `None`, que é um valor. O segundo argumento `true` manda o `default` trocar qualquer valor vazio: `None` e o texto vazio.

??? question "Por que o CPF aparece mascarado na lista e inteiro no detalhe?"
    Porque o CPF é um dado pessoal (LGPD), e a lista é vista por quem só quer escolher um usuário: para isso o número completo não faz falta. O detalhe é aberto por quem escolheu ver aquele usuário, e mostra o CPF inteiro. O filtro `cpf_oculto` esconde as pontas, com `'***.' + cpf[4:11] + '-**'`.

---

## ✅ Quiz de Fixação

<quiz>
A lista de usuários mostrava `1`, `2` e `3` na coluna do perfil. O que resolveu o problema?
- [ ] Trocar o `{{ usuario.perfil_id }}` por `{{ usuario.perfil_id|string }}` no template
> Não. O filtro `string` só converte o número em texto, e o texto continuaria sendo `1`.
- [x] Um `JOIN` com a tabela `perfis`, que traz o nome do perfil junto com cada usuário
> Correto. A tabela `usuarios` só tem o número (a chave estrangeira), e o nome mora em `perfis`. O `JOIN` emparelha as duas linhas.
- [ ] Um `SELECT *`, que traz todas as colunas
> Não. O `SELECT *` de `usuarios` traria também a senha, e ainda assim só teria o `perfil_id`, não o nome do perfil.
- [ ] Um `if` no template que troca `1` por `Administrador`
> Não. Isso funcionaria até alguém cadastrar um perfil novo ou mudar o número, e o banco já guarda a resposta certa.
</quiz>

<quiz>
No `JOIN` sem o `AS perfil`, os nomes das pessoas sumiram e a coluna **Nome** passou a mostrar `Administrador`, `Gerente` e `Usuário`. Por quê?
- [ ] O `JOIN` apagou os nomes das pessoas do banco
> Não. O `JOIN` só lê. Os dados continuam intactos no banco.
- [ ] O Jinja escolhe a última coluna com o mesmo nome por conta própria
> Não. Quem sobrescreve é o **dicionário** que o Python monta com cada linha, antes de o Jinja entrar em cena.
- [x] O resultado tinha duas colunas `nome`, e o dicionário de cada linha só guarda uma chave `nome`: a do perfil substituiu a do usuário
> Correto. Um dicionário não aceita a mesma chave duas vezes. O `AS perfil` dá à segunda coluna uma chave própria.
- [ ] A ordenação `ORDER BY u.nome` trocou as colunas de lugar
> Não. O `ORDER BY` só decide a ordem das linhas. Não muda quais colunas existem.
</quiz>

<quiz>
Quais afirmações sobre os filtros próprios (`data_br`, `data_hora_br` e `cpf_oculto`) estão corretas? (selecione todas que se aplicam)
- [x] São funções Python registradas com `@app.template_filter` e chamadas no template com o `|`
> Correto. O nome entre aspas no decorador é o que se escreve depois do `|`.
- [x] Tratam o `None` uma vez, e todas as telas que os usam se beneficiam
> Correto. É a vantagem sobre um `{% if %}` copiado em cada data de cada tela.
- [x] Mudam só o que aparece na página: o valor guardado no banco continua o mesmo
> Correto. O filtro formata na hora de exibir, e a coluna do banco não é tocada.
- [ ] Alteram a coluna do banco, gravando a data como `14/03/1988`
> Não. O banco continua guardando a data como `1988-03-14`. O filtro só escreve a data de outro jeito na tela.
</quiz>

<quiz>
A célula da cidade tinha `{{ usuario.cidade|default('—') }}`, e a Ana continuou com `None`. O que falta?
- [ ] Trocar o `default` por `upper`
> Não. O `upper` põe o texto em maiúsculas e não trata valor vazio.
- [x] O segundo argumento `true`: `default('—', true)`
> Correto. Sem ele, o `default` só age quando o valor não existe, e o `None` do `NULL` existe. Com o `true`, ele troca também o `None` e o texto vazio.
- [ ] Gravar a cidade como texto vazio (`''`), e não como `NULL`
> Não. A regra do projeto é gravar `NULL`, e o texto vazio também não seria trocado pelo `default` sem o `true`.
- [ ] Nada: o navegador mostra o `None` e não tem como mudar
> Não. O texto vem do servidor, e o filtro `default` está no template justamente para trocá-lo.
</quiz>

<quiz>
Alguém abre `/usuarios/99999`, um código que não existe, em uma rota **sem** o `abort(404)`. O que acontece?
- [ ] O Flask responde 404 sozinho
> Não. O 404 automático só acontece para endereços que nenhuma rota reconhece, como `/usuarios/abc`. O `99999` é um número, e a rota o aceita.
- [x] O `execute_one` devolve `None`, o template tenta ler os campos de um usuário que não existe, e a página quebra com erro 500
> Correto. O pedido por algo que não está lá merece 404, e o `if usuario is None: abort(404)` entrega esse código.
- [ ] O banco cria um usuário vazio com esse código
> Não. Um `SELECT` só lê, nunca grava.
- [ ] A rota mostra a lista de usuários no lugar
> Não. Nada na rota decide mostrar a lista. Sem o `abort`, o `usuario` é `None`, e o template quebra.
</quiz>

---

## 📝 Resumo

A lista de usuários nasceu com um `SELECT` simples e quatro defeitos visíveis, e cada um virou uma ferramenta: o `JOIN` traz o nome do perfil, e o `AS` evita que duas colunas `nome` se sobrescrevam no dicionário. Os filtros `data_br`, `data_hora_br` e `cpf_oculto`, registrados com `@app.template_filter`, escrevem as datas à brasileira, mostram o mínimo do CPF na lista e tratam o `NULL` em um lugar só. A constante `SELECT_USUARIO` guarda a consulta para a lista e o detalhe, e deixa a senha de fora de propósito. O `include` do badge acaba com o `if` repetido, e o `abort(404)` responde corretamente a um código que não existe. O Capítulo 16 acrescenta a edição e a exclusão de usuários, os botões que faltam nesta lista.

---

## 🔗 Navegação

⬅️ [Capítulo 14 — INSERT relacional de usuário](Capitulo_14_INSERT_Relacional_de_Usuario.md) · ➡️ [Capítulo 16 — UPDATE e DELETE de usuário](Capitulo_16_UPDATE_e_DELETE_de_Usuario.md)

---

*Fatec Jahu · ILP951 · Prof. Ronan Adriel Zenatti · 2026*
