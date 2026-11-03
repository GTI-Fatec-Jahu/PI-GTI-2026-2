# Capítulo 05 — Variáveis, filtros, `if` e `for`

**Disciplina:** Programação para Internet (ILP951)
**Professor:** Ronan Adriel Zenatti · ronan.zenatti@cps.sp.gov.br
**Fatec Jahu — 2º Semestre/2026**

---

## 🎯 Objetivos do Capítulo

Ao final deste capítulo você deverá ser capaz de:

- Enviar dados do Python para o template com `render_template` e exibi-los com `{{ }}`
- Distinguir as três marcações do Jinja2: `{{ }}` (mostra um valor), `{% %}` (controla o HTML) e `{# #}` (comentário)
- Percorrer uma lista com `{% for %}` para montar a tabela de produtos, os cards de categorias e as opções de um `<select>`
- Numerar as linhas com `loop.index` e tratar a lista vazia com o `{% else %}` do `for`
- Formatar o que aparece na tela com **filtros** (`length`, `default`, `upper`, `format` e `replace`) e encadear dois filtros
- Decidir o que aparece na página com `{% if %}`, `{% elif %}` e `{% else %}`, mostrando uma faixa de preço
- Reconhecer que o menu continua copiado em cada página

Até o Capítulo 4, os seis produtos do catálogo existiam **duas vezes**: na lista do `app.py` e escritos à mão na tabela do `index.html`. Para incluir um sétimo produto era preciso editar os dois lugares. Neste capítulo o template aprende a **ler os dados que o Python entrega**: a tabela, as categorias e até as opções do formulário passam a ser montadas a partir da lista, e o HTML deixa de repetir o que o Python já sabe.

## 📦 Ponto de partida

Este capítulo parte do **seu** repositório `catalogo-produtos`, como ele ficou no fim do Capítulo 4: com o `app.py`, as pastas `templates` (`index.html`, `cadastro.html` e `produto.html`) e `static` (`estilo.css` e `produto.js`), o `requirements.txt`, o `.gitignore` e a pasta `treino`.

Se o seu projeto não está funcionando, baixe o código do Capítulo 4 e descompacte na Área de Trabalho. Depois de descompactar, crie o ambiente virtual:

➡️ [Baixar p1_cap_04.zip](../arquivos/p1_cap_04.zip)

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

---

## Tópico 1 — Do Python para o template

### Antes de começar

Abra a pasta `catalogo-produtos` no VS Code e o terminal com `Ctrl + '`. Rode:

```bash
git pull
git status
```

O `git status` deve dizer `nothing to commit, working tree clean`. Se algo estiver pendente, faça o ciclo do Capítulo 1 (`git add .`, `git commit -m "..."`, `git push`) antes de seguir.

Ative o ambiente virtual (`.venv\Scripts\activate`) e ligue o servidor:

```bash
python app.py
```

Deixe esse terminal rodando durante o capítulo e use um segundo terminal (o ícone **+** do painel) para o Git. Abra **http://127.0.0.1:5000** e deixe a página à vista.

### Uma variável do Python no template

O `index.html` tem o título "Catálogo de Produtos" escrito em dois lugares: dentro do `<title>` (o texto da aba do navegador) e no `<h1>`. Vamos fazer o Python entregar esse texto. No `app.py`, troque a rota `index`:

```python
@app.route('/')
def index():
    return render_template('index.html', titulo='Catálogo de Produtos')
```

No `templates/index.html`, troque o texto do `<title>` e o do `<h1>` por `{{ titulo }}`:

```html
  <title>{{ titulo }}</title>
```

```html
    <h1>{{ titulo }}</h1>
```

Salve os dois arquivos e recarregue a página: nada mudou na tela, e é esse o objetivo. Agora volte ao `app.py`, troque o texto `'Catálogo de Produtos'` por `'Meu Catálogo'`, salve e recarregue: a aba e o título da página acompanham, sem você tocar no HTML. Desfaça a troca antes de seguir.

!!! note "O nome à esquerda é o que o template enxerga"
    Em `titulo='Catálogo de Produtos'`, o nome à esquerda (`titulo`) é a **variável** que o template recebe, e o valor à direita é o que ela guarda. O que está entre `{{ }}` no HTML é trocado pelo valor da variável **antes** de a página ir para o navegador. O navegador nunca vê o `{{ }}`: só vê o texto final.

### As três marcações do Jinja2

O Jinja2, o motor de templates do Flask, entende três marcações. Você já usou a primeira. As outras duas aparecem ao longo do capítulo:

| Marcação | Nome | O que faz | Aparece no HTML final? |
|---|---|---|---|
| `{{ ... }}` | expressão | calcula e **mostra** um valor | sim, o valor |
| `{% ... %}` | instrução | **controla** o HTML (repetir, decidir) | não, só o que ela gera |
| `{# ... #}` | comentário | anotação para quem lê o template | não |

Experimente o comentário. No `index.html`, logo acima do `<h1>`, acrescente:

```html
    {# O título vem da rota index(), no app.py #}
    <h1>{{ titulo }}</h1>
```

Salve, recarregue e abra o código-fonte da página (`Ctrl + U`). Procure o comentário: ele **não está lá**. Um comentário do HTML (`<!-- ... -->`) seria enviado ao navegador e qualquer pessoa o veria no código-fonte. O `{# #}` é descartado pelo Flask antes do envio.

### A lista de produtos chega ao template

Para a tabela deixar de ser escrita à mão, o template precisa receber a lista `produtos`. No `app.py`, acrescente o segundo dado à rota `index`. Como a linha ficou comprida, quebre-a depois da vírgula:

```python
@app.route('/')
def index():
    return render_template('index.html', titulo='Catálogo de Produtos',
                           produtos=produtos)
```

!!! note "Python: quebra de linha dentro dos parênteses"
    Dentro de parênteses, o Python permite continuar a instrução na linha de baixo. A segunda linha só precisa estar **alinhada** com o que vem depois do parêntese, para ficar fácil de ler. O `produtos=produtos` segue a mesma ideia do `titulo`: a variável do template (esquerda) recebe a lista do Python (direita).

Para ver o que chegou, coloque uma linha provisória no `index.html`, logo abaixo de `<h2>Produtos</h2>`:

```html
      <p>{{ produtos }}</p>
```

Salve e recarregue: a lista inteira aparece impressa, com colchetes, chaves e aspas, exatamente como o Python a escreve. Ela chegou, e os dicionários estão lá dentro. **Apague** a linha provisória.

Registre este ponto no Git (em um segundo terminal):

```bash
git add .
git commit -m "Envia o título e a lista de produtos da rota para o template"
git push
```

---

## Tópico 2 — `for`: a tabela se monta sozinha

### Repetir uma linha para cada produto

O `{% for %}` do Jinja2 repete um pedaço do HTML **uma vez para cada item** de uma lista. Comece pelo mais simples: só os nomes. Logo abaixo de `<h2>Produtos</h2>` do `index.html`, escreva uma lista provisória:

```html
      <ul>
        {% for produto in produtos %}
        <li>{{ produto.nome }}</li>
        {% endfor %}
      </ul>
```

Salve e recarregue. Acima da tabela aparece uma lista com os seis nomes. O `<li>` foi escrito **uma vez**, e o Jinja2 o repetiu seis vezes.

!!! note "`{% for %}` é o `for` do Python, dentro do HTML"
    Lê-se como no Python: "para cada `produto` em `produtos`". A cada volta, a variável `produto` guarda um dos dicionários da lista, e `{{ produto.nome }}` mostra o nome dele. Uma diferença: no template o bloco não termina pela indentação, e sim por uma marca de fechamento, o `{% endfor %}`. Se você esquecer o `{% endfor %}`, o Flask mostra um erro `TemplateSyntaxError`, e o texto do erro diz qual marca está faltando.

### A tabela inteira

Agora o que vale: trocar as seis linhas escritas à mão por uma só. **Apague** a `<ul>` provisória e, dentro do `<tbody>`, **apague as seis `<tr>`**. No lugar delas, escreva:

```html
        <tbody>
          {% for produto in produtos %}
          <tr>
            <td><a href="{{ url_for('produto', produto_id=produto.id) }}">{{ produto.nome }}</a></td>
            <td>{{ produto.categoria }}</td>
            <td class="text-end">R$ {{ produto.preco }}</td>
          </tr>
          {% endfor %}
        </tbody>
```

Salve e recarregue. A tabela voltou, com os seis produtos e os links de cada um. Repare em dois detalhes:

- O link usa `produto_id=produto.id`. No Capítulo 4 você escreveu o número à mão (`produto_id=1`, `produto_id=2`...). Agora o `id` vem do próprio produto. O `'produto'` **entre aspas** é o nome da função da rota. O `produto` **sem aspas** é a variável do `for`. São coisas diferentes que, por acaso, têm o mesmo nome.
- Os preços aparecem como `R$ 2.5`, `R$ 18.9` e `R$ 129.0`: com ponto, e sem o zero final. Antes, escritos à mão, eram `R$ 2,50`. O Tópico 4 arruma isso.

### O alívio: um produto novo sem mexer no HTML

Abra o `app.py` e acrescente um sétimo produto **no fim da lista**, antes do `]`:

```python
    {'id': 7, 'nome': 'Fone de ouvido', 'categoria': 'Informática', 'preco': 79.90},
```

Salve e recarregue a página. O **Fone de ouvido** aparece na tabela, e o link dele (`/produto/7`) funciona. Você editou **um** arquivo, uma linha, e o `index.html` não foi tocado. É o fim do primeiro incômodo do Capítulo 4: os dados estão em um lugar só.

Registre no Git:

```bash
git add .
git commit -m "Monta a tabela de produtos com for"
git push
```

---

## Tópico 3 — Mais usos do `for`

### As categorias também viram dados

As quatro categorias estão escritas à mão em **dois** lugares: nos cards do `index.html` e nas opções do `<select>` do `cadastro.html`. É o mesmo problema da tabela. No `app.py`, logo abaixo de `app = Flask(__name__)`, crie a lista:

```python
categorias = ['Papelaria', 'Informática', 'Casa', 'Acessórios']
```

!!! note "Python: lista de textos"
    Até agora, as listas do projeto guardavam dicionários. Uma lista também pode guardar valores simples, como textos: cada item entre aspas, separados por vírgula. Aqui, cada categoria é só um nome, então um texto basta.

Envie a lista ao template, junto com os outros dois dados:

```python
@app.route('/')
def index():
    return render_template('index.html', titulo='Catálogo de Produtos',
                           produtos=produtos, categorias=categorias)
```

No `index.html`, na seção de categorias, **apague os quatro blocos** `<div class="col-sm-6 col-lg-3">...</div>` e escreva um só, dentro de um `for`:

```html
      <div class="row g-3">
        {% for categoria in categorias %}
        <div class="col-sm-6 col-lg-3">
          <div class="card">
            <div class="card-body">{{ categoria }}</div>
          </div>
        </div>
        {% endfor %}
      </div>
```

Salve e recarregue: os quatro cards continuam ali, agora montados pelo template. Veja a vantagem: no `app.py`, acrescente `'Esportes'` ao fim da lista de categorias, salve e recarregue. Surge um **quinto card**, que o grid coloca em uma nova linha. Deixe o `'Esportes'` por enquanto.

### As opções do `<select>`

Falta o formulário. A rota `cadastro` também precisa enviar a lista:

```python
@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html', categorias=categorias)
```

No `templates/cadastro.html`, **apague as quatro** `<option>` de categorias (a `<option value="">Selecione...</option>` fica) e escreva:

```html
                <select class="form-select" id="categoria" name="categoria" required>
                  <option value="">Selecione...</option>
                  {% for categoria in categorias %}
                  <option value="{{ categoria }}">{{ categoria }}</option>
                  {% endfor %}
                </select>
```

Salve e abra **http://127.0.0.1:5000/cadastro**. O `<select>` lista as quatro categorias **e também o Esportes**. Uma única lista no `app.py` alimenta os cards e o formulário. Agora **apague** o `'Esportes'` da lista, para o catálogo voltar às quatro categorias.

### Numerando as linhas: `loop.index`

Dentro de um `for`, o Jinja2 oferece a variável `loop`, com informações sobre a volta atual. A mais usada é `loop.index`, o número da volta, **começando em 1**. Acrescente uma coluna de número à tabela do `index.html`. No cabeçalho, antes de `Nome`:

```html
            <th>Nº</th>
```

E, na linha repetida, antes do `<td>` do nome:

```html
            <td>{{ loop.index }}</td>
```

Salve e recarregue: os produtos aparecem numerados de 1 a 7. Repare que esse número é a posição na tabela, e não o `id` do produto.

### Quando a lista está vazia: o `{% else %}` do `for`

O que aparece se não houver nenhum produto? Para testar, no `app.py`, logo **depois** do `]` que fecha a lista de produtos, acrescente uma linha provisória:

```python
produtos = []
```

Como essa linha vem depois, ela substitui a lista por uma lista vazia. Salve e recarregue: a tabela aparece só com o cabeçalho, sem nenhuma explicação. O `for` aceita um `{% else %}`, que só é usado quando **não há nenhum item**. Acrescente-o antes do `{% endfor %}`:

```html
          {% else %}
          <tr>
            <td colspan="4" class="text-center text-body-secondary">Nenhum produto cadastrado.</td>
          </tr>
          {% endfor %}
```

O `colspan="4"` faz a célula ocupar as quatro colunas da tabela. Salve e recarregue: a mensagem aparece. **Apague** a linha provisória `produtos = []` e confira que os sete produtos voltaram. O `{% else %}` fica no template, pronto para quando a lista esvaziar.

Registre no Git:

```bash
git add .
git commit -m "Usa for nas categorias, no select e na numeração da tabela"
git push
```

---

## Tópico 4 — Filtros: formatando o que aparece

Um **filtro** transforma um valor **na hora de exibi-lo**. Escreve-se depois de uma barra vertical `|` (o *pipe*, que no teclado ABNT é a tecla `\` com o `Shift` apertado). O dado original, no Python, não muda: só a exibição.

### Contar com `length`

Quantos produtos o catálogo tem? Em vez de contar à mão, o filtro `length` conta os itens de uma lista. No `index.html`, logo abaixo de `<h2>Produtos</h2>`:

```html
      <p class="text-body-secondary">{{ produtos|length }} produtos no catálogo.</p>
```

Salve e recarregue: "7 produtos no catálogo." Se acrescentar ou apagar um produto no `app.py`, o número acompanha.

### Mudar o texto com `upper`

Experimente outro filtro, só para ver. No `<h1>`, troque `{{ titulo }}` por `{{ titulo|upper }}`. Salve e recarregue: o título aparece todo em maiúsculas, mas a aba do navegador, que continua com `{{ titulo }}`, não mudou. O filtro mexeu apenas onde foi escrito. Volte o `<h1>` para `{{ titulo }}`.

### Um valor que falta: `default`

E se um produto vier sem categoria? No `app.py`, **apague** de um produto o trecho `'categoria': 'Papelaria', `, deixando o produto 1 assim:

```python
    {'id': 1, 'nome': 'Caneta esferográfica azul', 'preco': 2.50},
```

Salve e recarregue: a célula da categoria da caneta ficou **vazia**, e a tabela parece quebrada. O filtro `default` diz o que mostrar quando o valor não existe. Na tabela do `index.html`:

```html
            <td>{{ produto.categoria|default('Sem categoria') }}</td>
```

Salve e recarregue: aparece **Sem categoria**. Agora devolva a categoria ao produto 1:

```python
    {'id': 1, 'nome': 'Caneta esferográfica azul', 'categoria': 'Papelaria', 'preco': 2.50},
```

!!! note "O `default` age quando o valor não existe"
    Ele cobre o caso de a chave estar ausente, como acabamos de provocar. Um valor presente e vazio (`''`) o `default` não substitui. A validação dos dados que chegam por formulário é assunto do Capítulo 9.

### O preço: dois filtros encadeados

Falta o problema dos preços: `R$ 2.5` e `R$ 129.0`. Um número com duas casas decimais se pede com o filtro `format`, que recebe um **modelo** de formatação:

```html
            <td class="text-end">R$ {{ '%.2f'|format(produto.preco) }}</td>
```

Salve e recarregue: os preços agora aparecem como `R$ 2.50` e `R$ 129.00`, sempre com duas casas.

!!! note "Python: o modelo `'%.2f'`"
    Lê-se assim: `%` começa o modelo, `.2` pede duas casas depois do ponto decimal e `f` diz que o valor é um número com casas decimais. O `format` pega o valor entre parênteses e o encaixa nesse modelo, devolvendo um **texto**: `2.5` vira `'2.50'`.

O ponto continua no lugar da vírgula. Para trocá-lo, use o filtro `replace`, que troca um pedaço do texto por outro. Como os filtros se aplicam **da esquerda para a direita**, é possível **encadeá-los**: o resultado do primeiro entra no segundo.

```html
            <td class="text-end">R$ {{ '%.2f'|format(produto.preco)|replace('.', ',') }}</td>
```

Leia na ordem: pegue o preço, formate com duas casas (`'2.50'`) e troque o ponto por vírgula (`'2,50'`). Salve e recarregue: `R$ 2,50`, `R$ 18,90`, `R$ 129,00`, como no Capítulo 4, mas agora vindo do dado.

A página de detalhe tem o mesmo problema. No `produto.html`, troque a linha do preço:

```html
        <p class="card-text"><strong>Preço:</strong> R$ {{ '%.2f'|format(produto.preco)|replace('.', ',') }}</p>
```

Salve e abra `/produto/1` e `/produto/6` para conferir.

!!! warning "Uma repetição que fica"
    A mesma expressão comprida está escrita em dois arquivos. Para formatar preços sempre do mesmo jeito, o Flask permite criar um filtro próprio. Você faz isso no Capítulo 18.

Registre no Git:

```bash
git add .
git commit -m "Formata o total, a categoria e o preço com filtros"
git push
```

---

## Tópico 5 — `if`: decidir o que aparece

### Uma faixa de preço

Um `{% if %}` mostra um pedaço do HTML **só quando uma condição é verdadeira**, como o `if` do Python. Vamos classificar cada produto em uma faixa de preço e mostrar uma etiqueta colorida (um **badge** do Bootstrap). Na tabela do `index.html`, acrescente a coluna `Faixa` no cabeçalho, **antes** do `Preço`:

```html
            <th>Faixa</th>
```

E, na linha repetida, um `<td>` novo **antes** da célula do preço. Comece pelo `if` mais simples, com só duas saídas:

```html
            <td>
              {% if produto.preco > 100 %}
              <span class="badge bg-warning text-dark">Premium</span>
              {% else %}
              <span class="badge bg-primary">Comum</span>
              {% endif %}
            </td>
```

A tabela agora tem uma coluna a mais: troque também o `colspan="4"` da mensagem de lista vazia por `colspan="5"`. Salve e recarregue: só a **Mochila escolar** (R$ 129,00) é Premium, e os outros seis são Comum.

### Mais de duas saídas: `elif`

Duas faixas são pouco. O `{% elif %}` ("senão, se") acrescenta saídas intermediárias. Troque o `if` por três faixas: até R$ 20, de R$ 20 a R$ 100, e acima de R$ 100:

```html
            <td>
              {% if produto.preco <= 20 %}
              <span class="badge bg-success">Econômico</span>
              {% elif produto.preco <= 100 %}
              <span class="badge bg-primary">Intermediário</span>
              {% else %}
              <span class="badge bg-warning text-dark">Premium</span>
              {% endif %}
            </td>
```

Salve e recarregue: a caneta e o caderno aparecem como **Econômico**, o mouse, o teclado, a garrafa e o fone como **Intermediário**, e a mochila como **Premium**.

O Jinja2 testa as condições **em ordem** e para na primeira verdadeira. O caderno custa 18,90: ele satisfaz `<= 20` e também `<= 100`, mas fica com a primeira. Por isso o segundo teste nem precisa dizer "maior que 20".

Os operadores de comparação são os mesmos do Python:

| Operador | Significa |
|---|---|
| `==` e `!=` | igual e diferente |
| `<` e `<=` | menor e menor ou igual |
| `>` e `>=` | maior e maior ou igual |

Também valem `and`, `or` e `not`, como no Python.

Para ver o `if` obedecendo ao dado, troque no `app.py` o preço do mouse de `59.90` para `15.00`, salve e recarregue: o mouse vira **Econômico**. Devolva o `59.90`.

### A mesma faixa na página de detalhe

Abra o `templates/produto.html` e, logo **abaixo** da linha do preço, acrescente a faixa dentro do card:

```html
        <p class="card-text">
          <strong>Faixa:</strong>
          {% if produto.preco <= 20 %}
          <span class="badge bg-success">Econômico</span>
          {% elif produto.preco <= 100 %}
          <span class="badge bg-primary">Intermediário</span>
          {% else %}
          <span class="badge bg-warning text-dark">Premium</span>
          {% endif %}
        </p>
```

Salve e abra `/produto/1` (Econômico) e `/produto/6` (Premium).

### Os arquivos completos do capítulo

O `app.py`:

```python
from flask import Flask, render_template, abort

app = Flask(__name__)

categorias = ['Papelaria', 'Informática', 'Casa', 'Acessórios']

produtos = [
    {'id': 1, 'nome': 'Caneta esferográfica azul', 'categoria': 'Papelaria', 'preco': 2.50},
    {'id': 2, 'nome': 'Caderno universitário 96 folhas', 'categoria': 'Papelaria', 'preco': 18.90},
    {'id': 3, 'nome': 'Mouse sem fio', 'categoria': 'Informática', 'preco': 59.90},
    {'id': 4, 'nome': 'Teclado USB', 'categoria': 'Informática', 'preco': 89.90},
    {'id': 5, 'nome': 'Garrafa térmica 500 ml', 'categoria': 'Casa', 'preco': 49.90},
    {'id': 6, 'nome': 'Mochila escolar', 'categoria': 'Acessórios', 'preco': 129.00},
    {'id': 7, 'nome': 'Fone de ouvido', 'categoria': 'Informática', 'preco': 79.90},
]


@app.route('/')
def index():
    return render_template('index.html', titulo='Catálogo de Produtos',
                           produtos=produtos, categorias=categorias)


@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html', categorias=categorias)


@app.route('/produto/<int:produto_id>')
def produto(produto_id):
    produto_encontrado = None
    for item in produtos:
        if item['id'] == produto_id:
            produto_encontrado = item

    if produto_encontrado is None:
        abort(404)

    return render_template('produto.html', produto=produto_encontrado)


if __name__ == '__main__':
    app.run(debug=True)
```

O `templates/index.html`:

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{ titulo }}</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="{{ url_for('static', filename='estilo.css') }}">
</head>
<body>

  <nav class="navbar navbar-expand-lg" data-bs-theme="dark">
    <div class="container">
      <a class="navbar-brand" href="{{ url_for('index') }}">Catálogo de Produtos</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse"
              data-bs-target="#menu" aria-controls="menu" aria-expanded="false"
              aria-label="Abrir o menu">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="menu">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <a class="nav-link active" href="{{ url_for('index') }}#produtos">Produtos</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="{{ url_for('index') }}#categorias">Categorias</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="{{ url_for('cadastro') }}">Cadastrar</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>

  <main class="container my-4">
    {# O título vem da rota index(), no app.py #}
    <h1>{{ titulo }}</h1>
    <p class="lead">Papelaria, informática, casa e acessórios para o dia a dia.</p>

    <section id="produtos" class="mb-5">
      <h2>Produtos</h2>
      <p class="text-body-secondary">{{ produtos|length }} produtos no catálogo.</p>
      <table class="table table-striped table-hover">
        <thead class="table-light">
          <tr>
            <th>Nº</th>
            <th>Nome</th>
            <th>Categoria</th>
            <th>Faixa</th>
            <th class="text-end">Preço</th>
          </tr>
        </thead>
        <tbody>
          {% for produto in produtos %}
          <tr>
            <td>{{ loop.index }}</td>
            <td><a href="{{ url_for('produto', produto_id=produto.id) }}">{{ produto.nome }}</a></td>
            <td>{{ produto.categoria|default('Sem categoria') }}</td>
            <td>
              {% if produto.preco <= 20 %}
              <span class="badge bg-success">Econômico</span>
              {% elif produto.preco <= 100 %}
              <span class="badge bg-primary">Intermediário</span>
              {% else %}
              <span class="badge bg-warning text-dark">Premium</span>
              {% endif %}
            </td>
            <td class="text-end">R$ {{ '%.2f'|format(produto.preco)|replace('.', ',') }}</td>
          </tr>
          {% else %}
          <tr>
            <td colspan="5" class="text-center text-body-secondary">Nenhum produto cadastrado.</td>
          </tr>
          {% endfor %}
        </tbody>
      </table>
    </section>

    <section id="categorias">
      <h2>Categorias</h2>
      <div class="row g-3">
        {% for categoria in categorias %}
        <div class="col-sm-6 col-lg-3">
          <div class="card">
            <div class="card-body">{{ categoria }}</div>
          </div>
        </div>
        {% endfor %}
      </div>
    </section>
  </main>

  <footer class="text-center text-body-secondary py-3">
    <p class="mb-0">Catálogo de Produtos · Fatec Jahu · ILP951 · 2026</p>
  </footer>

  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js"></script>

</body>
</html>
```

O `<main>` do `templates/produto.html`:

```html
  <main class="container my-4">
    <section id="detalhe" class="card">
      <div class="card-body">
        <h1 class="card-title h2">{{ produto.nome }}</h1>
        <p class="card-text"><strong>Código:</strong> {{ produto.id }}</p>
        <p class="card-text"><strong>Categoria:</strong> {{ produto.categoria }}</p>
        <p class="card-text"><strong>Preço:</strong> R$ {{ '%.2f'|format(produto.preco)|replace('.', ',') }}</p>
        <p class="card-text">
          <strong>Faixa:</strong>
          {% if produto.preco <= 20 %}
          <span class="badge bg-success">Econômico</span>
          {% elif produto.preco <= 100 %}
          <span class="badge bg-primary">Intermediário</span>
          {% else %}
          <span class="badge bg-warning text-dark">Premium</span>
          {% endif %}
        </p>
        <a href="{{ url_for('index') }}" class="btn btn-primary">Voltar para o catálogo</a>
      </div>
    </section>
  </main>
```

E o `<select>` do `templates/cadastro.html`, que é o único trecho do arquivo que mudou:

```html
                <select class="form-select" id="categoria" name="categoria" required>
                  <option value="">Selecione...</option>
                  {% for categoria in categorias %}
                  <option value="{{ categoria }}">{{ categoria }}</option>
                  {% endfor %}
                </select>
```

!!! warning "Dois incômodos que continuam de propósito"
    1. **O menu está copiado em três arquivos.** Os dados já têm um lugar só, mas a `navbar` ainda se repete em cada página. O Capítulo 6 resolve isso com um template-base.
    2. **O mesmo `if` das faixas de preço está em dois arquivos** (`index.html` e `produto.html`). O Capítulo 6 também mostra como guardar um pedaço de HTML em um arquivo e usá-lo nos dois.

Registre no Git:

```bash
git add .
git commit -m "Mostra a faixa de preço com if, elif e else"
git push
```

---

## 📦 Código deste capítulo

Compare com o seu projeto, ou use como ponto de partida do próximo capítulo. O zip tem o `app.py`, a pasta `templates` (`index.html`, `cadastro.html` e `produto.html`), a pasta `static` (`estilo.css` e `produto.js`), o `requirements.txt`, o `.gitignore` e a pasta `treino`. O ambiente virtual **não** vai no zip: depois de descompactar, crie-o com os três comandos do Capítulo 3 (`python -m venv .venv`, `.venv\Scripts\activate` e `pip install -r requirements.txt`).

➡️ [Baixar p1_cap_05.zip](../arquivos/p1_cap_05.zip)

---

## 🃏 Flashcards de Revisão

Tente responder mentalmente antes de abrir.

??? question "Qual a diferença entre `{{ }}`, `{% %}` e `{# #}` no Jinja2?"
    `{{ }}` calcula e **mostra** um valor. `{% %}` **controla** o HTML, como o `for` e o `if`, e não mostra nada por si só. `{# #}` é um **comentário**: o Flask o descarta e ele não vai para o navegador, nem para o código-fonte da página.

??? question "Como o template recebe a lista `produtos` do Python?"
    Pela rota, com `render_template('index.html', produtos=produtos)`. O nome à esquerda do `=` é a variável que o template enxerga, e o valor à direita é a lista do Python. Se a rota não enviar o dado, o template não tem como usá-lo.

??? question "Em `url_for('produto', produto_id=produto.id)`, por que aparece `produto` duas vezes?"
    O primeiro, **entre aspas**, é o nome da função da rota. O segundo, **sem aspas**, é a variável do `for`, o produto da volta atual. São duas coisas diferentes que têm o mesmo nome.

??? question "Para que serve o `{% else %}` dentro de um `{% for %}`?"
    Ele só é usado quando a lista **não tem nenhum item**. No catálogo, mostra a mensagem "Nenhum produto cadastrado." em vez de deixar a tabela vazia, sem explicação.

??? question "O que é um filtro, e o `{{ titulo|upper }}` muda a variável `titulo`?"
    Um filtro transforma um valor na hora de exibi-lo, e se escreve depois de `|`. Não muda a variável: o `titulo` continua com o mesmo valor no Python, e só o lugar onde o filtro foi escrito mostra o texto em maiúsculas.

??? question "O Flask mostra um erro `TemplateSyntaxError` depois que você escreve um `{% for %}` ou `{% if %}`. Qual a causa mais provável?"
    Faltou a marca de fechamento: `{% endfor %}` para o `for` e `{% endif %}` para o `if`. O texto do erro informa qual marca o Jinja2 esperava.

---

## ✅ Quiz de Fixação

<quiz>
Qual marcação do Jinja2 **mostra o valor** de uma variável na página?
- [ ] `{# titulo #}`
> Não. O `{# #}` é um comentário: o Flask o descarta e nada aparece na página.
- [ ] `{% titulo %}`
> Não. O `{% %}` serve para instruções de controle, como `for` e `if`, e `titulo` não é uma instrução.
- [x] `{{ titulo }}`
> Correto. As chaves duplas calculam o que está dentro e colocam o resultado no HTML.
- [ ] `<!-- titulo -->`
> Não. Isso é um comentário do HTML, não do Jinja2, e é enviado ao navegador sem trocar nada.
</quiz>

<quiz>
Quais afirmações sobre o `{% for produto in produtos %}` do catálogo estão corretas? (selecione todas que se aplicam)
- [x] O bloco termina com `{% endfor %}`
> Correto. No template, a marca de fechamento é obrigatória, ao contrário do Python, que usa a indentação.
- [x] A cada volta, `produto` guarda um dos dicionários da lista
> Correto. É por isso que `{{ produto.nome }}` mostra o nome do produto da volta atual.
- [x] Acrescentar um produto à lista do `app.py` faz a linha dele aparecer na tabela, sem editar o `index.html`
> Correto. O `for` repete a linha para cada item da lista, então a lista passa a ser a única fonte dos dados.
- [ ] O `for` apaga da lista do `app.py` cada produto que já foi mostrado
> Não. O template só lê os dados. A lista do Python continua intacta.
</quiz>

<quiz>
O preço de um produto é `2.5`. O que o template mostra com `{{ '%.2f'|format(preco)|replace('.', ',') }}`?
- [ ] `2.5`
> Não. O `format` com `'%.2f'` sempre dá duas casas decimais, então o resultado não fica só `2.5`.
- [ ] `2.50`
> Não. O `format` realmente produz `'2.50'`, mas em seguida o `replace` troca o ponto por vírgula.
- [x] `2,50`
> Correto. Os filtros se aplicam da esquerda para a direita: primeiro o `format` gera `'2.50'`, depois o `replace` troca o ponto por vírgula.
- [ ] `2,5`
> Não. A vírgula vem do `replace`, mas as duas casas decimais já foram fixadas antes pelo `format`.
</quiz>

<quiz>
O template tem `{% if produto.preco <= 20 %}` Econômico, `{% elif produto.preco <= 100 %}` Intermediário e `{% else %}` Premium. Que etiqueta aparece para um produto de R$ 18,90?
- [x] Econômico
> Correto. O Jinja2 testa as condições em ordem e para na primeira verdadeira: 18,90 já satisfaz `<= 20`.
- [ ] Intermediário
> Não. Também é verdade que 18,90 é menor ou igual a 100, mas o `elif` só é testado se o `if` anterior for falso, e ele foi verdadeiro.
- [ ] Premium
> Não. O `else` só vale quando nenhum teste anterior foi verdadeiro, e aqui o primeiro já foi.
- [ ] Nenhuma, porque duas condições são verdadeiras
> Não. Duas condições verdadeiras não são problema: o Jinja2 executa o primeiro bloco cuja condição é verdadeira e ignora o resto.
</quiz>

<quiz>
Na tabela, o `{% for %}` tem um `{% else %}` com a mensagem "Nenhum produto cadastrado.". Quando essa mensagem aparece?
- [ ] Sempre, depois da última linha de produto
> Não. O `{% else %}` do `for` não é um "depois de tudo": ele só é usado quando o `for` não tem nenhum item.
- [ ] Quando um produto tem o preço igual a zero
> Não. O `else` do `for` não olha o conteúdo dos itens, só se existem itens.
- [x] Quando a lista `produtos` está vazia
> Correto. Sem nenhum item para percorrer, o Jinja2 não repete o bloco do `for` e usa o `{% else %}`.
- [ ] Quando o `{% endfor %}` está faltando
> Não. Sem o `{% endfor %}` o Flask mostra um `TemplateSyntaxError`, e a página não é montada.
</quiz>

---

## 📝 Resumo

Você fez o template ler os dados do Python: o `render_template` envia variáveis, o `{{ }}` as mostra e o `{# #}` guarda anotações que não saem para o navegador. Com o `{% for %}`, a tabela de produtos, os cards de categorias e as opções do formulário passaram a ser montados a partir de listas do `app.py`, e um produto novo aparece sem editar o HTML. Os filtros (`length`, `default`, `upper`, `format` e `replace`) formatam o que é exibido sem alterar o dado, e podem ser encadeados. O `{% if %}` com `{% elif %}` e `{% else %}` decide qual faixa de preço mostrar. O primeiro incômodo do Capítulo 4 acabou, e o segundo ficou: o menu ainda está copiado em três arquivos, e o Capítulo 6 o resolve.

---

## 🔗 Navegação

⬅️ [Capítulo 4 — Bootstrap com Flask](Capitulo_04_Bootstrap_com_Flask.md) · 🔒 Capítulo 6 — em breve.

---

*Fatec Jahu · ILP951 · Prof. Ronan Adriel Zenatti · 2026*
