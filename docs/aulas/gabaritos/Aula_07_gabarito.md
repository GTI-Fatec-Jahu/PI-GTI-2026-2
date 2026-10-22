# Gabarito — Tópico 06 — CRUD: Inserção e Leitura

> Soluções comentadas dos mini-desafios de "🔎 Verifique seu Entendimento" do
> [Tópico 06](../Aula_07_CRUD_Insercao_e_Leitura.md). Tente resolver cada desafio por
> conta própria antes de conferir aqui.

---

## Parte 1 — O mapa de rotas do assistente de estudos com IA

**Desafio proposto:** montar a tabela de rotas do recurso `pergunta` (ver o histórico, salvar uma pergunta, corrigir o título e excluir), indicando a letra do CRUD, o comando SQL, o método HTTP e uma rota Flask para cada necessidade.

**Solução comentada:**

| Necessidade | CRUD | SQL | Método HTTP | Rota sugerida |
|---|---|---|---|---|
| Ver o histórico de perguntas | **R**ead | `SELECT` | `GET` | `/perguntas` (lista) e `/perguntas/<int:pergunta_id>` (detalhe) |
| Salvar uma pergunta nova | **C**reate | `INSERT` | `GET` (mostra o formulário) e `POST` (grava) | `/perguntas/nova` |
| Corrigir o título de uma pergunta | **U**pdate | `UPDATE ... WHERE id` | `GET` (formulário preenchido) e `POST` (grava) | `/perguntas/<int:pergunta_id>/editar` |
| Excluir uma pergunta | **D**elete | `DELETE ... WHERE id` (ou `UPDATE ativa = 0`) | `POST` | `/perguntas/<int:pergunta_id>/excluir` |

O ponto central é a coluna "Método HTTP": só a consulta usa apenas `GET`. As outras três operações têm uma etapa que **altera dados** e, por isso, chegam por `POST`. Criar e atualizar ainda precisam de um `GET` anterior, para exibir o formulário (vazio ou preenchido). O nome das rotas é uma convenção, não uma regra: o que importa é que cada operação tenha uma URL própria e previsível, e que o `id` venha sempre com o conversor `<int:...>`.

---

## Parte 2 — Cadastro de estações de bike-sharing

**Desafio proposto:** escrever a rota `/estacoes/nova` (`GET` e `POST`) que coleta `nome`, `bairro` e `capacidade`, valida e grava com `execute_insert`, redirecionando para `lista_estacoes` com uma flash de sucesso.

**Solução comentada:**

```python
@app.route('/estacoes/nova', methods=['GET', 'POST'])
def estacao_nova():

    if request.method == 'POST':

        # ===== COLETA =====
        nome           = request.form.get('nome', '').strip()
        bairro         = request.form.get('bairro', '').strip()
        capacidade_txt = request.form.get('capacidade', '').strip()

        # ===== VALIDAÇÃO E CONVERSÃO =====
        erros = []

        if not nome:
            erros.append('O nome da estação é obrigatório.')
        if not bairro:
            erros.append('O bairro é obrigatório.')

        capacidade = capacidade_txt   # se a conversão falhar, mantém o texto para repopular
        try:
            valor = int(capacidade_txt)
        except ValueError:
            erros.append('A capacidade deve ser um número inteiro.')
        else:
            if valor < 1:
                erros.append('A capacidade deve ser de pelo menos 1 bicicleta.')
            else:
                capacidade = valor

        estacao = {'nome': nome, 'bairro': bairro, 'capacidade': capacidade}

        if erros:
            for erro in erros:
                flash(erro, 'danger')
            return render_template('estacao_form.html', estacao=estacao)

        # ===== GRAVAÇÃO =====
        novo_id = execute_insert(
            'INSERT INTO estacao (nome, bairro, capacidade) VALUES (%s, %s, %s)',
            (nome, bairro, capacidade)
        )
        flash(f'Estação "{nome}" cadastrada com sucesso (código #{novo_id}).', 'success')
        return redirect(url_for('lista_estacoes'))   # PRG: redirect depois do POST

    # Método GET: formulário vazio
    return render_template('estacao_form.html', estacao={})
```

A estrutura é a mesma da rota de produtos: **coletar → validar e converter → decidir entre mostrar erros ou gravar → redirecionar**. Três decisões importam: a conversão com `int()` dentro de `try/except ValueError` (tudo que vem de `request.form` é texto), a regra `valor < 1` no ramo `else` (que só roda se a conversão deu certo) e os valores sempre em placeholders `%s`, nunca concatenados. Uma variação válida seria envolver o `execute_insert` em `try/except Exception`, como no cadastro de produtos, para mostrar uma mensagem amigável se o banco falhar.

---

## Parte 3 — Badges para os pontos de coleta

**Desafio proposto:** escrever o `<td>` com `if / elif / else` que exibe o badge de cada `ponto`: verde "Meta atingida" (100 kg ou mais), amarelo "Em andamento" (entre 0 e 100 kg) e cinza "Sem coletas" (0 kg).

**Solução comentada:**

```html
<td>
  {% if ponto.quilos_coletados >= 100 %}
    <span class="badge bg-success">Meta atingida</span>
  {% elif ponto.quilos_coletados > 0 %}
    <span class="badge bg-warning text-dark">Em andamento</span>
  {% else %}
    <span class="badge bg-secondary">Sem coletas</span>
  {% endif %}
</td>
```

A **ordem** das condições é o que faz a lógica funcionar: o `if` testa a faixa mais exigente (`>= 100`) primeiro; se ela falha, o `elif` só precisa testar `> 0`, porque quem chegou até ali já tem menos de 100; o `else` fica com o que sobrou, exatamente 0. É o mesmo encadeamento das faixas de classificação do Tópico 04, aplicado a uma cor em vez de a um texto. Um detalhe: `quilos_coletados` vem do MySQL como `Decimal` (a coluna é `DECIMAL(10, 2)`), e comparar um `Decimal` com um inteiro funciona normalmente no Jinja2.

---

## Parte 4 — Filtros dinâmicos de eventos

**Desafio proposto:** escrever a rota `lista_eventos` com três filtros opcionais (`busca`, `cidade`, `disponiveis=1`), consulta montada com `WHERE 1=1` e ordenada por `data_evento`.

**Solução comentada:**

```python
@app.route('/eventos')
def lista_eventos():
    busca          = request.args.get('busca', '').strip()
    cidade         = request.args.get('cidade', '').strip()
    so_disponiveis = request.args.get('disponiveis') == '1'

    # Base da consulta: 1=1 é sempre verdadeiro, então todo filtro entra com AND
    sql = 'SELECT * FROM evento WHERE 1=1'
    params = []

    if busca:
        sql += ' AND nome LIKE %s'
        params.append(f'%{busca}%')      # curingas no VALOR, nunca no texto do SQL

    if cidade:
        sql += ' AND cidade = %s'
        params.append(cidade)

    if so_disponiveis:
        sql += ' AND esgotado = 0'       # constante do nosso código: não precisa de placeholder

    sql += ' ORDER BY data_evento'

    try:
        eventos = execute_query(sql, params, fetch=True)
    except Exception as e:
        flash(f'Erro ao carregar eventos: {e}', 'danger')
        eventos = []

    return render_template('eventos.html', eventos=eventos, total=len(eventos),
                           busca=busca, cidade=cidade, so_disponiveis=so_disponiveis)
```

Os dois filtros que dependem de um texto digitado pelo usuário (`busca` e `cidade`) usam placeholders `%s` e vão para `params`. O filtro `esgotado = 0` **não** usa placeholder porque o usuário não envia um valor: ele só liga ou desliga o filtro, e o texto que entra no SQL é uma constante escrita pelo nosso código. Perceba também que a ordem das chamadas a `params.append` precisa acompanhar a ordem em que os `%s` aparecem em `sql`: o primeiro `%s` recebe o primeiro item da lista, e assim por diante. É o que faz a combinação "nome + cidade" funcionar sem nenhum `if` para decidir se é o primeiro filtro.

---

## Parte 5 — Detalhe de uma conversa com IA

**Desafio proposto:** escrever a rota `conversa_detalhe` (conversor de inteiro, `execute_one` e `abort(404)`) e explicar o que o Flask faz sozinho em `/conversas/abc`.

**Solução comentada:**

```python
@app.route('/conversas/<int:conversa_id>')
def conversa_detalhe(conversa_id):
    conversa = execute_one('SELECT * FROM conversa WHERE id = %s', (conversa_id,))
    if conversa is None:
        abort(404)   # id inexistente: "não encontrado", e não um erro 500
    return render_template('conversa_detalhe.html', conversa=conversa)
```

Quando alguém acessa `/conversas/abc`, o Flask **nem chega a executar a função**: como `abc` não é um inteiro, a URL não casa com o padrão `<int:conversa_id>` e o próprio Flask responde com `404 Not Found`. Isso protege a consulta de lixo na URL antes mesmo de ela existir. Já `abort(404)` cobre o caso complementar: a URL é válida (por exemplo `/conversas/99999`), mas não existe uma conversa com esse `id`. Sem essa checagem, `execute_one` devolveria `None` e o template quebraria com um erro 500, que sinaliza defeito do servidor, e não um pedido por algo que não existe.

---

*Fatec Jahu · ILP951 · Prof. Ronan Adriel Zenatti · 2026*
