# Gabarito — Aula 03 — Templates Jinja2 e Rotas

> Soluções comentadas dos mini-desafios de "🔎 Verifique seu Entendimento" da
> [Aula 03](../Aula_03_Templates_Jinja2_e_Rotas.md). Tente resolver cada desafio por
> conta própria antes de conferir aqui.

---

## Parte 1 — Exibindo os créditos de IA

**Desafio proposto:** exibir a variável `creditos` e escrever um comentário Jinja2
explicando sua origem.

**Solução comentada:**

```html
{# Este valor vem da API de créditos de IA — não editar manualmente #}
<p>Você ainda tem {{ creditos }} créditos hoje.</p>
```

`{{ creditos }}` é a marcação de **expressão**: exibe o valor da variável na página.
`{# ... #}` é a marcação de **comentário**: some completamente do HTML final, então
serve só para deixar um aviso para quem for mexer no template depois — o navegador
nunca chega a vê-lo.

---

## Parte 2 — Dados do app de bike-sharing

**Desafio proposto:** rota que monta um dicionário com estações, bicicletas livres e
tarifa, enviado com `**dados`, e as marcações que exibem cada valor.

**Solução comentada:**

```python
@app.route('/')
def pagina_inicial():
    dados = {
        'estacoes': 34,
        'bicicletas_livres': 128,
        'tarifa_hora': 6.50,
    }
    return render_template('index.html', **dados)
```

```html
<p>Estações disponíveis: {{ estacoes }}</p>
<p>Bicicletas livres agora: {{ bicicletas_livres }}</p>
<p>Tarifa por hora: R$ {{ tarifa_hora }}</p>
```

Cada chave do dicionário `dados` vira uma variável independente no template, graças
ao `**dados` desempacotando o dicionário em argumentos nomeados para
`render_template`.

---

## Parte 3 — Filtros para o evento de sustentabilidade

**Desafio proposto:** exibir `nome_evento` em maiúsculas com valor padrão, e
`pegada_carbono` arredondado para 1 casa decimal.

**Solução comentada:**

```html
<p>{{ nome_evento | default('Evento sem nome') | upper }}</p>
<p>Pegada de carbono: {{ pegada_carbono | round(1) }} toneladas</p>
```

A ordem dos filtros importa: `default` precisa vir **antes** de `upper` para que, se
`nome_evento` não existir, o valor padrão `'Evento sem nome'` seja o que recebe a
transformação para maiúsculas — e não o contrário. `round(1)` arredonda o número para
uma casa decimal (`2.4371` vira `2.4`).

---

## Parte 4 — Ranking de e-sports com medalha

**Desafio proposto:** rota com lista de jogadores e template que numera com
`loop.index` e destaca o primeiro com `loop.first`.

**Solução comentada:**

```python
@app.route('/ranking-esports')
def ranking_esports():
    jogadores = [
        {'nome': 'ProGamerBR', 'pontos': 9800},
        {'nome': 'NightFox', 'pontos': 8700},
        {'nome': 'LunaStrike', 'pontos': 8100},
    ]
    return render_template('ranking.html', jogadores=jogadores)
```

```html
{% for jogador in jogadores %}
  <p>
    {{ loop.index }}º — {{ jogador.nome }} ({{ jogador.pontos }} pts)
    {% if loop.first %}
      🥇
    {% endif %}
  </p>
{% endfor %}
```

`loop.index` numera a partir de 1, e `loop.first` é `True` apenas na primeira volta
do laço — por isso a medalha só aparece ao lado do jogador no topo da lista.

---

## Parte 5 — Página de créditos herdando do base

**Desafio proposto:** `templates/creditos.html` como filha de `base.html`.

**Solução comentada:**

```html
{% extends 'base.html' %}

{% block titulo %}Meus Créditos de IA{% endblock %}

{% block conteudo %}
  <h1>Meus Créditos de IA</h1>
  <p>Você ainda tem {{ creditos }} créditos hoje.</p>
{% endblock %}
```

O `{% extends 'base.html' %}` precisa ser a primeira linha do arquivo. Tudo que a
página realmente precisa declarar são os blocos que ela quer preencher (`titulo` e
`conteudo`) — a navbar, o rodapé e o `<head>` inteiro já vêm do `base.html`.

---

## Parte 6 — Links do app de bike-sharing com url_for

**Desafio proposto:** links de navbar usando `url_for` para as rotas `estacoes` e
`minha_bike`.

**Solução comentada:**

```html
<a class="nav-link" href="{{ url_for('estacoes') }}">Estações</a>
<a class="nav-link" href="{{ url_for('minha_bike') }}">Minha Bike</a>
```

O `url_for` recebe o **nome da função** Python (`estacoes`, `minha_bike`), não a URL
escrita manualmente. Se um dia a rota `/estacoes` virar `/mapa-de-estacoes`, esses
links continuam funcionando sem qualquer alteração no template.

---

## Parte 7 — Rotas da coleta seletiva

**Desafio proposto:** rota `/estacao/<int:id>` e rota `/buscar-pontos` lendo
`material` da query string com valor padrão `'todos'`.

**Solução comentada:**

```python
@app.route('/estacao/<int:id>')
def detalhe_estacao(id):
    return f'Detalhes da estação de reciclagem #{id}'


@app.route('/buscar-pontos')
def buscar_pontos():
    material = request.args.get('material', 'todos')
    return f'Buscando pontos de coleta para: {material}'
```

`<int:id>` garante que `/estacao/abc` já retorna 404 automaticamente, sem precisar de
nenhuma validação manual. Em `/buscar-pontos`, como `material` é opcional,
`request.args.get('material', 'todos')` evita um erro quando ninguém informar esse
parâmetro na URL — acessar só `/buscar-pontos` busca `'todos'` os materiais.

---

## Parte 8 — Confirmando a compra do ingresso

**Desafio proposto:** rota `/comprar-ingresso` com duas flash messages e redirect.

**Solução comentada:**

```python
@app.route('/comprar-ingresso')
def comprar_ingresso():
    flash('Ingresso comprado com sucesso! Confira seu e-mail.', 'success')
    flash('Atenção: o pagamento via cartão internacional cobra uma taxa extra de 3%.', 'warning')
    return redirect(url_for('pagina_inicial'))
```

As duas mensagens ficam guardadas na sessão até a próxima página ser carregada — como
o `redirect` manda o navegador para a página inicial, é lá que os dois alertas
(verde e amarelo) aparecem, um logo abaixo do outro, através do bloco de
`get_flashed_messages()` já existente no `base.html`.

---

*Fatec Jahu · ILP951 · Prof. Ronan Adriel Zenatti · 2026*
