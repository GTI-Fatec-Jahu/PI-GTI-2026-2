# Capítulo 04 — Bootstrap com Flask

**Disciplina:** Programação para Internet (ILP951)
**Professor:** Ronan Adriel Zenatti · ronan.zenatti@cps.sp.gov.br
**Fatec Jahu — 2º Semestre/2026**

---

## 🎯 Objetivos do Capítulo

Ao final deste capítulo você deverá ser capaz de:

- Explicar o que é o Bootstrap, incluí-lo na página por CDN e entender por que a ordem dos arquivos de estilo importa
- Trocar o CSS escrito à mão por classes do Bootstrap, deixando no `estilo.css` só as regras próprias do projeto
- Montar uma barra de navegação (`navbar`) responsiva, que vira um menu "hambúrguer" em telas pequenas
- Organizar o conteúdo com `container`, classes de espaçamento e o grid de 12 colunas
- Estilizar uma tabela, cards e um formulário com classes do Bootstrap
- Usar `url_for` para gerar os endereços das rotas, dos arquivos da pasta `static` e das rotas com variável
- Reconhecer o incômodo de copiar o mesmo menu em cada página

Até o Capítulo 3, todo o visual do catálogo vinha de mais de cem linhas de CSS escritas por você, e ainda assim a página não se ajustava ao celular. Neste capítulo o **Bootstrap** entra para cuidar do visual, e o **`url_for`** entra para cuidar dos endereços. Os dois deixam o projeto mais curto e mais fácil de mudar.

## 📦 Ponto de partida

Este capítulo parte do **seu** repositório `catalogo-produtos`, como ele ficou no fim do Capítulo 3: com `app.py`, as pastas `templates` (`index.html`, `cadastro.html` e `produto.html`) e `static` (`estilo.css` e `produto.js`), o `requirements.txt`, o `.gitignore` e a pasta `treino`.

Se o seu projeto não está funcionando, baixe o código do Capítulo 3 e descompacte na Área de Trabalho. Depois de descompactar, crie o ambiente virtual:

➡️ [Baixar p1_cap_03.zip](../arquivos/p1_cap_03.zip)

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## Tópico 1 — Bootstrap: estilo pronto, sem escrever CSS

### O problema: CSS escrito à mão é demorado

O `estilo.css` do catálogo tem mais de cem linhas, e elas cuidam só de cores, tabela, formulário e botões de três páginas. Cada página nova pede mais regras. E nada disso se adapta sozinho a uma tela de celular.

O **Bootstrap** é uma biblioteca de CSS (com um pouco de JavaScript) que já traz centenas de estilos prontos: botões, tabelas, menus, formulários, cartões. Você não escreve as regras, só **escolhe as classes** no HTML. Compare:

```html
<!-- sem Bootstrap: o botão fica com a aparência padrão do navegador -->
<a href="/cadastro">Cadastrar</a>

<!-- com Bootstrap: duas classes e o link vira um botão azul -->
<a href="/cadastro" class="btn btn-primary">Cadastrar</a>
```

### Como o Bootstrap chega à página: CDN

O Bootstrap é um arquivo CSS e um arquivo JavaScript. Em vez de baixá-los, vamos usar uma **CDN** (*Content Delivery Network*): uma rede de servidores que hospeda bibliotecas populares e as entrega a quem pedir. Basta apontar o `<link>` e o `<script>` para o endereço dela.

!!! note "A CDN precisa de internet"
    Com a CDN, o navegador baixa o Bootstrap da internet a cada visita. Se o computador estiver sem conexão, a página aparece sem o Bootstrap. O número da versão (`5.3.8`) fica **dentro do endereço**: assim o site não muda de aparência se o Bootstrap lançar uma versão nova.

### Antes de começar

Abra a pasta `catalogo-produtos` no VS Code e abra o terminal com `Ctrl + '`. Rode:

```bash
git pull
git status
```

O `git status` deve dizer `nothing to commit, working tree clean`. Se algo estiver pendente, faça o ciclo do Capítulo 1 (`git add .`, `git commit -m "..."`, `git push`) antes de seguir.

Ative o ambiente virtual (`venv\Scripts\activate`) e ligue o servidor:

```bash
python app.py
```

Deixe esse terminal rodando durante o capítulo: o modo de desenvolvimento reinicia o servidor sozinho quando você salva. Quando precisar do Git, abra um segundo terminal (o ícone **+** do painel). Abra **http://127.0.0.1:5000** e deixe a página à vista: ela é o ponto de comparação.

### Ligando o Bootstrap ao `index.html`

No `templates/index.html`, acrescente o `<link>` do Bootstrap dentro do `<head>`, **antes** do link do `estilo.css`:

```html
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="/static/estilo.css">
```

Salve e recarregue a página. Alguma coisa mudou: os títulos ficaram com outro tamanho e outra espessura. Mas o cabeçalho azul, a tabela e o menu continuam como estavam. Agora a página tem **duas fontes de estilo**, o Bootstrap e o seu `estilo.css`, e as duas mexem nos mesmos elementos.

!!! note "Quem vence quando duas regras disputam o mesmo elemento?"
    Em CSS, se duas regras têm a mesma força, **vale a que vem por último**. Por isso o `estilo.css` vem **depois** do Bootstrap: o que você escrever ajusta o que o Bootstrap fez, e não o contrário.

### Deixando o Bootstrap cuidar do visual

Manter as duas fontes brigando não faz sentido: as regras de `header`, `nav a`, `table`, `form`, `input` e `button` que você escreveu nos Capítulos 1 e 2 são justamente o que o Bootstrap faz melhor. A decisão é: **o Bootstrap cuida do visual, e o `estilo.css` guarda só o que é próprio do catálogo**.

Substitua **todo o conteúdo** do `static/estilo.css` por:

```css
/* Regras próprias do catálogo. O resto do visual vem do Bootstrap. */

body {
  background-color: #f4f6f8;
}

/* Cor da barra de navegação (o azul do cabeçalho do Capítulo 1) */
.navbar {
  background-color: #1f4e79;
}

/* Borda vermelha em campo inválido (Capítulo 2) */
.form-control:user-invalid,
.form-select:user-invalid {
  border-color: #c0392b;
}
```

Restaram três regras: o fundo cinza da página, a cor da futura barra de navegação e a borda vermelha dos campos inválidos (a mesma ideia do Capítulo 2, agora para os campos do Bootstrap). O CSS antigo continua guardado no histórico do Git, caso você queira ver o que havia ali.

Salve e recarregue. A página perdeu as cores: o cabeçalho virou texto simples, o menu virou links azuis e a tabela ficou sem linhas. É assim que uma página fica só com o Bootstrap **sem classes**: ele normaliza a aparência, e o visual aparece quando você pede cada componente com uma classe. É o que os próximos tópicos fazem.

### O JavaScript do Bootstrap

Alguns componentes, como o menu que abre e fecha no celular, precisam de JavaScript. Acrescente a linha do `<script>` no fim do `<body>` do `index.html`, antes de `</body>`:

```html
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js"></script>
```

Você não vai escrever JavaScript: o Bootstrap lê atributos do HTML e faz o resto.

### As outras duas páginas

Cada página é um arquivo HTML independente, então cada uma precisa dos mesmos dois links. Abra `templates/cadastro.html` e `templates/produto.html` e faça o mesmo nas duas.

No `<head>`, o link do Bootstrap vai **antes** do `estilo.css`:

```html
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="/static/estilo.css">
```

No fim do `<body>`, o script do Bootstrap vai **antes** dos scripts próprios. No `produto.html`, ele é o único script. No `cadastro.html`, ele fica acima do `produto.js`:

```html
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js"></script>
  <script src="/static/produto.js"></script>
```

Salve e navegue pelas três páginas. Todas estão "cruas", mas já carregam o Bootstrap. Registre este ponto no Git (em um segundo terminal):

```bash
git add .
git commit -m "Adiciona o Bootstrap e enxuga o estilo.css"
git push
```

---

## Tópico 2 — A barra de navegação

### Trocando o cabeçalho pela `navbar`

A **navbar** é a barra de navegação do topo. Ela substitui o `<header>` com os três links que você escreveu no Capítulo 1. Vamos montá-la aos poucos, para enxergar o que cada pedaço faz.

**Primeira etapa: a barra e a marca.** No `templates/index.html`, **apague** o `<header>` inteiro (do `<header>` ao `</header>`) e coloque no lugar, logo depois de `<body>`:

```html
  <nav class="navbar navbar-expand-lg" data-bs-theme="dark">
    <div class="container">
      <a class="navbar-brand" href="/">Catálogo de Produtos</a>
    </div>
  </nav>
```

O título e a frase que ficavam no cabeçalho vão para dentro do `<main>`, no começo, antes de `<section id="produtos">`:

```html
  <main>
    <h1>Catálogo de Produtos</h1>
    <p class="lead">Papelaria, informática, casa e acessórios para o dia a dia.</p>

    <section id="produtos">
```

Salve e recarregue. Surge uma faixa azul no topo, com o nome do catálogo em branco, à esquerda. A cor azul vem da regra `.navbar` do seu `estilo.css`. O `data-bs-theme="dark"` avisa ao Bootstrap que o fundo é escuro, então ele usa texto claro. (A classe `lead` deixa a frase um pouco maior, como um texto de abertura.)

**Segunda etapa: o botão "hambúrguer" e o primeiro link.** Dentro do `<div class="container">`, logo depois do `navbar-brand`, acrescente o botão que só aparece em telas pequenas e a área que se recolhe, com um link:

```html
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse"
              data-bs-target="#menu" aria-controls="menu" aria-expanded="false"
              aria-label="Abrir o menu">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="menu">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <a class="nav-link active" href="/#produtos">Produtos</a>
          </li>
        </ul>
      </div>
```

Salve e recarregue: o link **Produtos** aparece à direita. Agora **estreite a janela do navegador** até ela ficar com menos de uns mil pixels de largura. O link some e surge o ícone de três tracinhos. Clique nele: o menu abre e fecha. Esse comportamento é do Bootstrap, e você não escreveu JavaScript nenhum.

**Terceira etapa: os outros links.** Dentro do mesmo `<ul>`, depois do item **Produtos**, acrescente mais dois:

```html
          <li class="nav-item">
            <a class="nav-link" href="/#categorias">Categorias</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="/cadastro">Cadastrar</a>
          </li>
```

Salve, recarregue e confira os três links, e o menu recolhido na janela estreita.

### O que cada classe faz

| Classe ou atributo | Para que serve |
|---|---|
| `navbar` | Declara que o bloco é uma barra de navegação |
| `navbar-expand-lg` | Em telas grandes (a partir de 992 px) o menu fica aberto; em telas menores, ele se recolhe |
| `container` | Centraliza o conteúdo e limita a largura (detalhado no Tópico 3) |
| `navbar-brand` | O nome do site, à esquerda |
| `navbar-toggler` | O botão "hambúrguer" |
| `collapse navbar-collapse` | A área dos links que se recolhe nas telas pequenas |
| `navbar-nav` | A lista de links do menu |
| `ms-auto` | Empurra a lista para a direita (*margin start: auto*) |
| `nav-item` e `nav-link` | Cada item do menu e o seu link |
| `active` | Destaca o link da página atual |

Os atributos `data-bs-toggle="collapse"` e `data-bs-target="#menu"` são o que liga o botão à área recolhível: o `#menu` aponta para o elemento com `id="menu"`, e **os dois precisam bater**. É o `bootstrap.bundle.min.js` que lê esses atributos. Os `aria-...` servem aos leitores de tela, que anunciam o botão para quem não enxerga.

### O mesmo menu nas outras páginas

O `cadastro.html` e o `produto.html` também precisam do menu. Em cada um, **apague o `<header>`** e cole a mesma `navbar`, completa, logo depois de `<body>`:

```html
  <nav class="navbar navbar-expand-lg" data-bs-theme="dark">
    <div class="container">
      <a class="navbar-brand" href="/">Catálogo de Produtos</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse"
              data-bs-target="#menu" aria-controls="menu" aria-expanded="false"
              aria-label="Abrir o menu">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="menu">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <a class="nav-link active" href="/#produtos">Produtos</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="/#categorias">Categorias</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="/cadastro">Cadastrar</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
```

Só uma coisa muda entre as cópias: a classe `active`, que marca a página atual. No `cadastro.html`, tire o `active` de **Produtos** e coloque em **Cadastrar**. No `produto.html`, deixe em **Produtos**. Salve e navegue entre as três páginas.

!!! warning "Um incômodo que fica de propósito"
    O mesmo bloco de mais de vinte linhas agora existe em **três arquivos**. Para incluir um quarto link no menu, é preciso editar os três, e é fácil esquecer um. O Capítulo 6 resolve isso com herança de templates.

Registre no Git:

```bash
git add .
git commit -m "Adiciona a navbar do Bootstrap às três páginas"
git push
```

---

## Tópico 3 — Container, espaçamento e tabela

### O `container` e o espaçamento

Olhe o catálogo em uma janela larga: o conteúdo gruda na borda esquerda e se estica até a direita. No `templates/index.html`, troque a tag `<main>` por:

```html
  <main class="container my-4">
```

Salve e recarregue. O conteúdo agora fica **centralizado**, com largura limitada e uma folga nas laterais, e ganhou espaço acima e abaixo. O `container` faz o centro e o limite de largura. O `my-4` cuida do espaço vertical.

Os nomes de espaçamento do Bootstrap seguem um padrão: **propriedade + lado + tamanho**.

| Pedaço | Valores | Significado |
|---|---|---|
| propriedade | `m` (*margin*, margem de fora) · `p` (*padding*, espaço de dentro) | de qual espaço se fala |
| lado | `t` topo · `b` base · `s` início · `e` fim · `x` horizontal · `y` vertical | onde aplicar. Sem letra, vale para os quatro lados |
| tamanho | `0` a `5`, do menor ao maior (`1` = 0,25 rem · `3` = 1 rem · `5` = 3 rem) | quanto |

Então `my-4` é "margem vertical, tamanho 4", `mb-5` é "margem na base, tamanho 5" e `py-3` é "espaço de dentro vertical, tamanho 3". Use `mb-5` na seção de produtos, para afastá-la das categorias:

```html
    <section id="produtos" class="mb-5">
```

### A tabela

A tabela voltou a ser o HTML simples, sem linhas. Para estilizá-la, o Bootstrap pede classes na própria tag. Troque a abertura da tabela e a do `<thead>`:

```html
      <table class="table table-striped table-hover">
        <thead class="table-light">
```

Salve e recarregue. A tabela ganha linhas separadoras, as linhas se alternam em duas cores (`table-striped`), a linha sob o mouse fica destacada (`table-hover`) e o cabeçalho fica em cinza claro (`table-light`).

Falta o preço. A coluna usava a classe `preco` (do `estilo.css` antigo) para alinhar à direita, e o Bootstrap tem uma classe pronta para isso: `text-end` (texto alinhado ao fim). Troque `class="preco"` por `class="text-end"` nas **sete** ocorrências (uma no `<th>` e uma em cada `<td>` de preço). No VS Code, use `Ctrl + H`: em *localizar*, `class="preco"`; em *substituir*, `class="text-end"`; clique em **Substituir tudo**. As linhas ficam assim:

```html
            <th class="text-end">Preço</th>
```

```html
            <td class="text-end">R$ 2,50</td>
```

Salve e confira: os preços alinham pela direita.

### O rodapé

O rodapé ainda é o HTML simples. Troque a abertura do `<footer>` e a do `<p>` dentro dele:

```html
  <footer class="text-center text-body-secondary py-3">
    <p class="mb-0">Catálogo de Produtos · Fatec Jahu · ILP951 · 2026</p>
```

O `text-center` centraliza, o `text-body-secondary` deixa o texto em cinza, o `py-3` dá folga em cima e embaixo e o `mb-0` tira a margem do parágrafo (zero, na base). Salve e recarregue.

Registre no Git:

```bash
git add .
git commit -m "Aplica container, espaçamentos e classes de tabela no catálogo"
git push
```

---

## Tópico 4 — Grid e cards

### O grid de 12 colunas

Quando o conteúdo fica lado a lado e precisa se reorganizar em telas pequenas, o Bootstrap oferece o **grid**: cada linha (`row`) é dividida em **12 colunas**, e cada elemento diz quantas ocupa. Quatro elementos de 3 colunas somam 12 e ocupam a linha inteira, lado a lado. Cinco elementos de 3 colunas não cabem, e o quinto desce para a linha de baixo.

As categorias são uma lista simples. Vamos transformá-las em cartões (**cards**) dispostos no grid. No `templates/index.html`, **apague** o `<ul>` da seção de categorias (do `<ul>` ao `</ul>`) e coloque no lugar:

```html
      <div class="row">
        <div class="col-md-3">
          <div class="card">
            <div class="card-body">Papelaria</div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card">
            <div class="card-body">Informática</div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card">
            <div class="card-body">Casa</div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card">
            <div class="card-body">Acessórios</div>
          </div>
        </div>
      </div>
```

Salve e recarregue com a janela larga: as quatro categorias aparecem lado a lado, cada uma em um cartão. Agora estreite a janela abaixo de uns 768 px: os cartões passam a ocupar a linha toda, um embaixo do outro, mas **colados**, sem espaço entre eles.

O `col-md-3` quer dizer: "a partir da tela média (`md`), ocupe 3 das 12 colunas". Abaixo disso, o padrão é ocupar a linha inteira. Os pontos em que o layout muda se chamam **breakpoints**:

| Prefixo | Largura mínima da tela | Tela típica |
|---|---|---|
| (nenhum) | 0 px | celular |
| `sm` | 576 px | celular grande |
| `md` | 768 px | tablet |
| `lg` | 992 px | notebook |
| `xl` | 1200 px | monitor grande |

Para corrigir o espaço, acrescente `g-3` (*gutter*, o espaço entre as colunas) na `row`. E para que o layout tenha três situações em vez de duas, combine **dois** prefixos em cada coluna: `col-sm-6 col-lg-3`.

```html
      <div class="row g-3">
        <div class="col-sm-6 col-lg-3">
```

Troque o `col-md-3` das quatro colunas por `col-sm-6 col-lg-3`, salve e redimensione a janela devagar:

| Largura da janela | Colunas de cada card | Cards por linha |
|---|---|---|
| menos de 576 px | 12 (padrão) | 1 |
| de 576 px a 991 px | 6 | 2 |
| 992 px ou mais | 3 | 4 |

O mesmo HTML se reorganiza conforme a tela, sem uma linha de CSS escrita por você.

### A página de detalhe em um card

Abra o `templates/produto.html`. Troque a tag `<main>` e **substitua a seção inteira** `<section id="detalhe">...</section>` por um card:

```html
  <main class="container my-4">
    <section id="detalhe" class="card">
      <div class="card-body">
        <h1 class="card-title h2">{{ produto.nome }}</h1>
        <p class="card-text"><strong>Código:</strong> {{ produto.id }}</p>
        <p class="card-text"><strong>Categoria:</strong> {{ produto.categoria }}</p>
        <p class="card-text"><strong>Preço:</strong> R$ {{ produto.preco }}</p>
        <a href="/" class="btn btn-primary">Voltar para o catálogo</a>
      </div>
    </section>
  </main>
```

Aplique também a mesma mudança do rodapé que você fez no `index.html` (`class="text-center text-body-secondary py-3"` no `<footer>` e `class="mb-0"` no `<p>`). Salve e abra `/produto/3`.

Três coisas novas aqui:

- o `card` é o cartão, o `card-body` é a área interna com espaço de sobra, e o `card-title` e o `card-text` formatam o título e os parágrafos;
- o link "Voltar" virou um **botão**: `btn` é a base de todo botão e `btn-primary` é a cor azul. Há `btn-secondary`, `btn-success`, `btn-danger`, e a versão só com borda, como `btn-outline-secondary`;
- o título deixou de ser `<h2>` e virou `<h1>`: o cabeçalho que tinha o `<h1>` desapareceu, e cada página deve ter **um** título principal.

!!! note "Significado no HTML, aparência na classe"
    O `<h1>` é o título mais importante da página, e o Bootstrap o desenha grande. Para uma página de detalhe, grande demais. A classe `h2` dá ao `<h1>` o **tamanho** de um `<h2>`, sem mudar o **significado**. É uma regra que vale para todo o Bootstrap: o elemento diz o que o conteúdo é, e a classe diz como ele aparece.

Registre no Git:

```bash
git add .
git commit -m "Mostra as categorias em cards no grid e o produto em um card"
git push
```

---

## Tópico 5 — O formulário de cadastro

### Arrumando a página

O `cadastro.html` voltou ao HTML simples. Comece pelo que você já conhece. Troque a tag `<main>` e o título, e aplique o rodapé do Tópico 3:

```html
  <main class="container my-4">
    <h1 class="h2 mb-4">Cadastrar produto</h1>
```

```html
  <footer class="text-center text-body-secondary py-3">
    <p class="mb-0">Catálogo de Produtos · Fatec Jahu · ILP951 · 2026</p>
  </footer>
```

Salve e recarregue **http://127.0.0.1:5000/cadastro**. O formulário aparece com a aparência padrão do navegador, esticado pela página toda.

### O formulário dentro de um card

Para o formulário não se esticar, use o grid: uma `row` com uma coluna que ocupa metade da largura em telas grandes (`col-lg-6`) e, dentro dela, um card. Embrulhe o `<form>` assim (o `...` é o formulário, que não muda):

```html
    <div class="row">
      <div class="col-lg-6">
        <div class="card">
          <div class="card-body">

            <form action="#" onsubmit="cadastrarProduto(event)">
              ...
            </form>

          </div>
        </div>
      </div>
    </div>
```

Salve e recarregue: o formulário ocupa metade da largura, dentro de um cartão.

### Os campos

No Bootstrap, cada campo fica em uma `<div class="mb-3">` (espaço embaixo), o `<label>` ganha `form-label` e o `<input>` ganha `form-control`. Comece só pelo campo do nome:

```html
              <div class="mb-3">
                <label for="nome" class="form-label">Nome do produto</label>
                <input type="text" class="form-control" id="nome" name="nome" placeholder="Ex.: Caneta esferográfica azul" required minlength="3">
              </div>
```

(Troque a `<div class="campo">` do nome por esta; o `<label>` e o `<input>` mudam só pelas classes novas.) Salve e recarregue: o campo ocupa a largura do cartão, com borda arredondada e destaque azul quando você clica nele. Agora os outros dois. O `<select>` usa `form-select`, e o `<input>` do preço usa `form-control`:

```html
              <div class="mb-3">
                <label for="categoria" class="form-label">Categoria</label>
                <select class="form-select" id="categoria" name="categoria" required>
                  <option value="">Selecione...</option>
                  <option value="Papelaria">Papelaria</option>
                  <option value="Informática">Informática</option>
                  <option value="Casa">Casa</option>
                  <option value="Acessórios">Acessórios</option>
                </select>
              </div>

              <div class="mb-3">
                <label for="preco" class="form-label">Preço (R$)</label>
                <input type="number" class="form-control" id="preco" name="preco" placeholder="0,00" min="0.01" step="0.01" required>
              </div>
```

Salve e recarregue. Os três campos têm o mesmo visual. Digite `ab` no nome e saia do campo: a borda fica vermelha, que é a regra `:user-invalid` do seu `estilo.css`.

### Os botões

Os três botões também ganham classes. Coloque-os dentro de uma `<div class="d-flex gap-2">`, que os alinha lado a lado com espaço entre eles (`d-flex` põe os filhos em linha e `gap-2` define a distância):

```html
              <div class="d-flex gap-2">
                <button type="submit" class="btn btn-primary">Cadastrar produto</button>
                <button type="reset" class="btn btn-outline-secondary">Limpar</button>
                <button type="button" class="btn btn-outline-secondary" onclick="mostrarProduto()">Ver no console</button>
              </div>
```

Salve e recarregue. Para ver que o JavaScript do Capítulo 2 continua funcionando, abra o console (`F12`), preencha o formulário e clique em **Cadastrar produto**: as três linhas aparecem. Os `id` dos campos não mudaram, e é por eles que o `produto.js` encontra os valores. O Bootstrap mudou só a aparência.

Registre no Git:

```bash
git add .
git commit -m "Estiliza o formulário de cadastro com Bootstrap"
git push
```

---

## Tópico 6 — `url_for`: deixe o Flask montar os endereços

### O problema: o endereço escrito à mão em vários lugares

O endereço `/cadastro` está escrito em **três arquivos** (o menu de cada página). Veja o que acontece se você resolver mudar o endereço da página de cadastro. No `app.py`, troque **só o texto da rota**:

```python
@app.route('/novo-produto')
def cadastro():
    return render_template('cadastro.html')
```

Salve e clique em **Cadastrar** no menu de qualquer página: **Not Found**. O Flask passou a responder em `/novo-produto`, mas os três menus continuam apontando para `/cadastro`. Seria preciso editar três arquivos, um por um, e esquecer um deixa um link quebrado.

### A solução: `url_for`

O `url_for` recebe o **nome da função** da rota e devolve o endereço dela. Se o endereço mudar, o template continua certo, porque quem informa o endereço é o Flask. Nos três arquivos (`index.html`, `cadastro.html` e `produto.html`), troque o link **Cadastrar** do menu:

```html
            <a class="nav-link" href="{{ url_for('cadastro') }}">Cadastrar</a>
```

(No `cadastro.html`, esse link é o que tem a classe `active`.) Salve e clique em **Cadastrar**: a página abre, agora em `/novo-produto`. O `{{ }}` é o mesmo do Capítulo 3: o que está dentro é calculado e o resultado entra no HTML. Olhe o código-fonte da página (`Ctrl + U`): o link é `href="/novo-produto"`, o endereço que o Flask escolheu.

!!! note "Python: argumento nomeado e o nome da função"
    O `url_for` recebe o **nome da função** como texto (`'cadastro'`), e não o endereço (`'/cadastro'`). É um erro comum escrever o endereço. Quando a rota tem variável, o valor vai com o nome dela, no formato `nome=valor`: `url_for('produto', produto_id=3)`. Isso se chama **argumento nomeado**, e você já usou o formato em `render_template('produto.html', produto=produto_encontrado)` e em `app.run(debug=True)`.

Faça o mesmo com os outros links do menu e com o nome do catálogo, nos três arquivos. A função da página inicial se chama `index`:

```html
      <a class="navbar-brand" href="{{ url_for('index') }}">Catálogo de Produtos</a>
```

```html
            <a class="nav-link active" href="{{ url_for('index') }}#produtos">Produtos</a>
```

```html
            <a class="nav-link" href="{{ url_for('index') }}#categorias">Categorias</a>
```

O `#produtos` e o `#categorias` continuam escritos à mão, **depois** do `url_for`: o `url_for` devolve `/`, e o navegador acrescenta a âncora. No `produto.html`, troque também o botão **Voltar**:

```html
        <a href="{{ url_for('index') }}" class="btn btn-primary">Voltar para o catálogo</a>
```

Para ver o alívio, volte o endereço no `app.py` para o original:

```python
@app.route('/cadastro')
```

Salve e navegue: os três menus continuam funcionando, e **nenhum template foi editado**. Você mudou o endereço duas vezes e só mexeu no `app.py`.

### O `url_for` para a pasta `static`

Os arquivos `estilo.css` e `produto.js` também estão com o caminho escrito à mão (`/static/...`). O Flask cria sozinho uma rota chamada `static` para a pasta `static`, e o `url_for` a usa com o argumento `filename`, que é o nome do arquivo **dentro** da pasta. Nos três arquivos, troque o link do CSS:

```html
  <link rel="stylesheet" href="{{ url_for('static', filename='estilo.css') }}">
```

E, no `cadastro.html`, o script no fim do `<body>`:

```html
  <script src="{{ url_for('static', filename='produto.js') }}"></script>
```

Salve e recarregue as páginas: nada muda na tela, e é esse o objetivo. O resultado é o mesmo `/static/estilo.css` de antes, mas agora quem o monta é o Flask. O link do Bootstrap **não** muda: ele vem da internet, e não da pasta `static`.

### O `url_for` para a rota com variável

A tabela do `index.html` ainda tem os seis links `/produto/1` a `/produto/6` escritos à mão. A rota `produto` espera o número com o nome `produto_id`, e o `url_for` o recebe como argumento nomeado. Troque o link de cada produto, mudando só o número:

```html
            <td><a href="{{ url_for('produto', produto_id=1) }}">Caneta esferográfica azul</a></td>
            <td><a href="{{ url_for('produto', produto_id=2) }}">Caderno universitário 96 folhas</a></td>
            <td><a href="{{ url_for('produto', produto_id=3) }}">Mouse sem fio</a></td>
            <td><a href="{{ url_for('produto', produto_id=4) }}">Teclado USB</a></td>
            <td><a href="{{ url_for('produto', produto_id=5) }}">Garrafa térmica 500 ml</a></td>
            <td><a href="{{ url_for('produto', produto_id=6) }}">Mochila escolar</a></td>
```

Salve, clique em cada produto e confira. O resumo do que o `url_for` substituiu:

| Antes (endereço à mão) | Agora (`url_for`) |
|---|---|
| `href="/"` | `href="{{ url_for('index') }}"` |
| `href="/cadastro"` | `href="{{ url_for('cadastro') }}"` |
| `href="/produto/3"` | `href="{{ url_for('produto', produto_id=3) }}"` |
| `href="/static/estilo.css"` | `href="{{ url_for('static', filename='estilo.css') }}"` |
| `src="/static/produto.js"` | `src="{{ url_for('static', filename='produto.js') }}"` |

O `templates/index.html` completo ao final do capítulo:

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Catálogo de Produtos</title>
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
    <h1>Catálogo de Produtos</h1>
    <p class="lead">Papelaria, informática, casa e acessórios para o dia a dia.</p>

    <section id="produtos" class="mb-5">
      <h2>Produtos</h2>
      <table class="table table-striped table-hover">
        <thead class="table-light">
          <tr>
            <th>Nome</th>
            <th>Categoria</th>
            <th class="text-end">Preço</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><a href="{{ url_for('produto', produto_id=1) }}">Caneta esferográfica azul</a></td>
            <td>Papelaria</td>
            <td class="text-end">R$ 2,50</td>
          </tr>
          <tr>
            <td><a href="{{ url_for('produto', produto_id=2) }}">Caderno universitário 96 folhas</a></td>
            <td>Papelaria</td>
            <td class="text-end">R$ 18,90</td>
          </tr>
          <tr>
            <td><a href="{{ url_for('produto', produto_id=3) }}">Mouse sem fio</a></td>
            <td>Informática</td>
            <td class="text-end">R$ 59,90</td>
          </tr>
          <tr>
            <td><a href="{{ url_for('produto', produto_id=4) }}">Teclado USB</a></td>
            <td>Informática</td>
            <td class="text-end">R$ 89,90</td>
          </tr>
          <tr>
            <td><a href="{{ url_for('produto', produto_id=5) }}">Garrafa térmica 500 ml</a></td>
            <td>Casa</td>
            <td class="text-end">R$ 49,90</td>
          </tr>
          <tr>
            <td><a href="{{ url_for('produto', produto_id=6) }}">Mochila escolar</a></td>
            <td>Acessórios</td>
            <td class="text-end">R$ 129,00</td>
          </tr>
        </tbody>
      </table>
    </section>

    <section id="categorias">
      <h2>Categorias</h2>
      <div class="row g-3">
        <div class="col-sm-6 col-lg-3">
          <div class="card">
            <div class="card-body">Papelaria</div>
          </div>
        </div>
        <div class="col-sm-6 col-lg-3">
          <div class="card">
            <div class="card-body">Informática</div>
          </div>
        </div>
        <div class="col-sm-6 col-lg-3">
          <div class="card">
            <div class="card-body">Casa</div>
          </div>
        </div>
        <div class="col-sm-6 col-lg-3">
          <div class="card">
            <div class="card-body">Acessórios</div>
          </div>
        </div>
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

O `app.py` volta a ser o do fim do Capítulo 3, sem nenhuma mudança: o Bootstrap e o `url_for` mexeram só nos templates e no CSS.

!!! warning "Dois incômodos que continuam de propósito"
    1. **O menu está copiado em três arquivos.** O Capítulo 6 resolve isso com um template-base.
    2. **Os produtos ainda estão escritos duas vezes**: na lista do `app.py` e na tabela do `index.html`. O Capítulo 5 faz o template percorrer a lista do Python e montar a tabela sozinho.

Registre no Git:

```bash
git add .
git commit -m "Troca os endereços escritos à mão por url_for"
git push
```

---

## 📦 Código deste capítulo

Compare com o seu projeto, ou use como ponto de partida do próximo capítulo. O zip tem o `app.py`, a pasta `templates` (`index.html`, `cadastro.html` e `produto.html`), a pasta `static` (`estilo.css` e `produto.js`), o `requirements.txt`, o `.gitignore` e a pasta `treino`. O ambiente virtual **não** vai no zip: depois de descompactar, crie-o com os três comandos do Capítulo 3 (`python -m venv venv`, `venv\Scripts\activate` e `pip install -r requirements.txt`).

➡️ [Baixar p1_cap_04.zip](../arquivos/p1_cap_04.zip)

---

## 🃏 Flashcards de Revisão

Tente responder mentalmente antes de abrir.

??? question "O que é o Bootstrap e como ele chega à página neste projeto?"
    É uma biblioteca de CSS (e um pouco de JavaScript) com estilos e componentes prontos, que se ativam por classes no HTML. Neste projeto ele vem de uma CDN: um `<link>` no `<head>` para o CSS e um `<script>` no fim do `<body>` para o JavaScript. Por isso o navegador precisa de internet.

??? question "Por que o link do `estilo.css` vem depois do link do Bootstrap?"
    Quando duas regras de mesma força disputam o mesmo elemento, vale a que vem por último. Com o `estilo.css` depois, as suas regras ajustam o que o Bootstrap fez.

??? question "Para que serve o `data-bs-target="#menu"` do botão da navbar?"
    Liga o botão "hambúrguer" à área que ele abre e fecha: o `#menu` aponta para o elemento com `id="menu"`, e os dois precisam bater. Quem lê esses atributos é o `bootstrap.bundle.min.js`.

??? question "Como funciona o grid do Bootstrap, e o que quer dizer `col-sm-6 col-lg-3`?"
    Cada `row` tem 12 colunas. A classe diz quantas o elemento ocupa a partir de cada largura de tela: `col-sm-6` ocupa 6 (metade) a partir de 576 px, e `col-lg-3` ocupa 3 (um quarto) a partir de 992 px. Abaixo de `sm`, o elemento ocupa a linha inteira.

??? question "Por que o título da página de detalhe é `<h1 class="card-title h2">`?"
    O elemento (`<h1>`) diz o que o conteúdo é: o título principal da página. A classe `h2` só muda a aparência, dando a ele o tamanho de um `<h2>`. O HTML guarda o significado, e a classe cuida do visual.

??? question "O que o `url_for('produto', produto_id=3)` devolve, e qual a vantagem sobre escrever `/produto/3`?"
    Devolve o endereço da rota da função `produto` com o número 3, ou seja, `/produto/3`. Se o endereço da rota mudar no `app.py`, os templates continuam certos, porque o endereço é montado pelo Flask em vez de escrito à mão em cada link.

---

## ✅ Quiz de Fixação

<quiz>
No `<head>` há dois links de estilo: o do Bootstrap e o do `estilo.css`. Por que o do `estilo.css` fica **depois**?
- [ ] Para a página carregar mais rápido
> Não. A ordem dos links não muda a velocidade em que a página carrega.
- [ ] Porque o Flask só encontra o `estilo.css` se ele vier em segundo lugar
> Não. O Flask entrega o arquivo da pasta `static` em qualquer posição: a ordem só importa para o navegador.
- [x] Porque, quando duas regras disputam o mesmo elemento, vale a que vem por último, e assim as suas regras ajustam as do Bootstrap
> Correto. Se o `estilo.css` viesse antes, o Bootstrap sobrescreveria as suas regras.
- [ ] Porque o Bootstrap não funciona se vier antes de outro arquivo
> Não. O Bootstrap funciona em qualquer posição: o que muda é qual regra vence em um conflito.
</quiz>

<quiz>
Quais afirmações sobre a `navbar` do catálogo estão corretas? (selecione todas que se aplicam)
- [x] A classe `navbar-expand-lg` deixa o menu aberto em telas grandes e o recolhe em telas menores
> Correto. A partir de 992 px o menu aparece aberto; abaixo disso, ele vira o botão "hambúrguer".
- [x] O valor de `data-bs-target` (`#menu`) precisa bater com o `id` da área que se recolhe
> Correto. É assim que o botão sabe qual elemento abrir e fechar.
- [x] O botão "hambúrguer" depende do `bootstrap.bundle.min.js` carregado na página
> Correto. É o JavaScript do Bootstrap que lê os atributos `data-bs-...`. Sem ele, o botão aparece, mas não abre o menu.
- [ ] Para o menu abrir e fechar, é preciso escrever uma função em JavaScript
> Não. O comportamento vem do Bootstrap, ativado só pelos atributos do HTML.
</quiz>

<quiz>
Cada card de categoria tem `class="col-sm-6 col-lg-3"`. Em uma janela de 700 px de largura, quantos cards aparecem por linha?
- [ ] 1
> Não. A janela passou dos 576 px, então a regra `col-sm-6` já vale. Uma única coluna por linha só acontece abaixo de 576 px.
- [x] 2
> Correto. Com 700 px, vale o `col-sm-6` (6 de 12 colunas, metade da linha), e o `col-lg-3` ainda não, porque ele só vale a partir de 992 px.
- [ ] 3
> Não. Nenhuma das classes ocupa 4 colunas, e é isso que daria 3 por linha.
- [ ] 4
> Não. Quatro por linha exige `col-lg-3` valendo, o que só acontece a partir de 992 px.
</quiz>

<quiz>
A rota é `@app.route('/cadastro')` sobre a função `def cadastro():`. Você muda o texto da rota para `/novo-produto`. Qual link do menu continua funcionando **sem nenhuma edição** no template?
- [ ] `<a href="/cadastro">`
> Não. O endereço escrito à mão ficou desatualizado, e o Flask responde 404.
- [x] `<a href="{{ url_for('cadastro') }}">`
> Correto. O `url_for` recebe o nome da função e devolve o endereço atual da rota, que agora é `/novo-produto`.
- [ ] `<a href="{{ url_for('/cadastro') }}">`
> Não. O `url_for` recebe o **nome da função**, e não o endereço. Com `'/cadastro'`, o Flask acusa erro, porque nenhuma função tem esse nome.
- [ ] `<a href="{{ url_for('novo-produto') }}">`
> Não. `novo-produto` é o endereço novo, e não o nome da função. O `url_for` procura uma função com esse nome e não encontra.
</quiz>

<quiz>
No `index.html`, o link do CSS é `<link rel="stylesheet" href="{{ url_for('static', filename='estilo.css') }}">`. O que o navegador recebe nesse `href`?
- [ ] O conteúdo do arquivo `estilo.css`
> Não. O `href` recebe só o endereço do arquivo. O navegador faz um segundo pedido a esse endereço para baixar o CSS.
- [ ] Apenas `estilo.css`
> Não. O `url_for` devolve o endereço completo da rota `static`, começando pela pasta.
- [x] O endereço `/static/estilo.css`
> Correto. O `static` é a rota que o Flask cria para a pasta `static`, e o `filename` é o nome do arquivo dentro dela.
- [ ] O endereço `/templates/estilo.css`
> Não. O CSS fica na pasta `static`, e a pasta `templates` guarda só as páginas HTML.
</quiz>

---

## 📝 Resumo

Você ligou o Bootstrap ao catálogo por CDN, deixou nele o visual da página e reduziu o `estilo.css` a três regras próprias. Montou uma navbar responsiva, organizou o conteúdo com `container`, espaçamentos e o grid de 12 colunas, e estilizou a tabela, os cards e o formulário só com classes. Depois trocou os endereços escritos à mão por `url_for`, que monta o endereço de uma rota, de um arquivo da pasta `static` e de uma rota com variável a partir do nome da função. Ficaram dois incômodos de propósito: a navbar copiada em três arquivos e os produtos escritos duas vezes. O Capítulo 5 resolve o segundo, com os recursos do Jinja2, e o Capítulo 6 resolve o primeiro, com herança de templates.

---

## 🔗 Navegação

⬅️ [Capítulo 3 — Flask](Capitulo_03_Flask.md) · ➡️ [Capítulo 5 — Variáveis, filtros, `if` e `for`](Capitulo_05_Variaveis_Filtros_If_e_For.md)

---

*Fatec Jahu · ILP951 · Prof. Ronan Adriel Zenatti · 2026*
