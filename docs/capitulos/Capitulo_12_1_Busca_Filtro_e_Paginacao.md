# Capítulo 12.1 — Busca, filtro e paginação (opcional)

**Disciplina:** Programação para Internet (ILP951)
**Professor:** Ronan Adriel Zenatti · ronan.zenatti@cps.sp.gov.br
**Fatec Jahu — 2º Semestre/2026**

---

## 🎯 Objetivos do Capítulo

Ao final deste capítulo você deverá ser capaz de:

- Importar um arquivo `.sql` de dados com `INSERT IGNORE` sem duplicar nem alterar o que já existe
- Buscar em mais de uma coluna com `LIKE`, mantendo o `%` no valor e nunca no texto do SQL
- Montar uma consulta com filtros opcionais usando `WHERE 1=1` e uma lista de valores (`params`)
- Filtrar colunas que aceitam `NULL` com `IS NULL` e `IS NOT NULL`
- Escolher a ordenação por uma lista de valores permitidos, já que o `ORDER BY` não aceita `%s`
- Dividir uma lista em páginas com `LIMIT`, `OFFSET` e `COUNT(*)`
- Montar os botões de página do Bootstrap preservando a busca, o filtro e a ordenação

Este capítulo é **opcional**: o Capítulo 13 continua do código do Capítulo 12, e não deste. O Capítulo 12 deixou uma lista de perfis que funciona bem com três linhas. Num sistema de verdade a lista cresce, e quem administra precisa **achar** um perfil, **separar** os que interessam e **não rolar** uma página de centenas de linhas. Aqui o banco é populado com um arquivo pronto, porque é impossível sentir o problema de uma lista grande com três perfis.

## 📦 Ponto de partida

Este capítulo continua do **seu** repositório `sistema-gestao`, como ficou no fim do Capítulo 12: com o `app.py`, o `db.py`, o `validacoes.py`, a pasta `templates` (`layout/base_menu.html`, `layout/base_limpo.html`, `login.html`, `dashboard.html`, `perfis/perfis_lista.html`, `perfis/perfil_form.html`, `404.html` e `500.html`) e os perfis Administrador, Gerente e Usuário cadastrados.

Se o seu projeto não está funcionando, baixe o código do Capítulo 12 e descompacte. Depois de descompactar, crie o ambiente virtual e o `.env`, como no [Capítulo 11](Capitulo_11_Projeto_Novo_e_Banco.md#topico-4-o-arquivo-env), e importe o `banco.sql` no phpMyAdmin:

➡️ [Baixar p2_cap_12.zip](../arquivos/p2_cap_12.zip)

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

---

## Tópico 1 — Trinta perfis para buscar

### Baixando o arquivo

Ligue o **Apache** e o **MySQL** no XAMPP, ative o ambiente virtual e deixe o servidor rodando (`python app.py`) em um terminal, com o segundo terminal livre para o Git. Baixe o arquivo e salve-o **dentro da pasta `sistema-gestao`**, ao lado do `app.py`:

➡️ [Baixar perfis_30.sql](../arquivos/perfis_30.sql)

Abra o arquivo no VS Code antes de importar. Depois dos comentários do início, o que importa é o comando:

```sql
INSERT IGNORE INTO perfis (nome, descricao, criado_em) VALUES
    ('Administrador',          'Acesso total ao sistema',                          '2026-01-05 09:00:00'),
    ...
    ('Comprador',              NULL,                                               '2026-04-13 13:10:00'),
    ...
```

Três detalhes:

- **`INSERT IGNORE`**: no [Capítulo 12](Capitulo_12_INSERT_e_SELECT_de_Perfis.md#topico-6-nome-repetido-o-erro-1062), cadastrar um nome repetido causava o erro `1062`. Com o `IGNORE`, o MySQL **pula** a linha que causaria esse erro e segue com as outras. Se você já cadastrou `Administrador`, `Gerente` e `Usuário`, o arquivo não os altera nem os duplica, e a descrição que você escolheu continua valendo. Se não cadastrou algum deles, o arquivo o cria. Em qualquer caso, a tabela termina com **30 perfis**.
- **`NULL` em algumas descrições**: alguns perfis ficam sem descrição de propósito, para o filtro "sem descrição" ter o que mostrar.
- **`criado_em` explícito**: as datas estão espalhadas de janeiro a outubro de 2026. Sem isso, os 30 perfis teriam o mesmo instante de criação, e ordenar por "mais recentes" não faria diferença.

### Importando e conferindo

No phpMyAdmin, abra a aba **Importar** (*Import*), escolha o `perfis_30.sql` e clique em **Importar**, como no [Capítulo 10](Capitulo_10_Banco_de_Dados.md#importando). Depois abra a tabela `perfis`: são 30 linhas. Importe o arquivo **uma segunda vez**: nenhum erro e continuam 30 linhas, porque o `IGNORE` pulou tudo.

Abra **http://127.0.0.1:5000/perfis**. A lista funciona, mas já é uma página longa: todos os 30 perfis de uma vez, sem como achar um. Com 3 mil seria pior, e a consulta traria as 3 mil linhas do banco a cada visita à página. O resto do capítulo resolve isso.

```bash
git add .
git commit -m "Adiciona o perfis_30.sql com perfis para busca e paginação"
git push
```

---

## Tópico 2 — Buscar pelo nome ou pela descrição

### O formulário de busca

A busca é uma **leitura**: usa o método **GET**, e o termo vai no endereço (`/perfis?busca=analista`), que pode ser copiado e compartilhado, como no [Capítulo 7](Capitulo_07_Formularios.md#topico-2-formulario-get-buscar-produtos-pelo-nome). No `app.py`, a rota `lista_perfis` passa a ler o `busca` e a devolvê-lo ao template. Troque a rota por esta (o `request` já está importado):

```python
@app.route('/perfis')
def lista_perfis():
    busca = request.args.get('busca', '').strip()

    perfis = execute_query(
        'SELECT id_perfil, nome, descricao, criado_em FROM perfis ORDER BY nome',
        fetch=True,
    )

    return render_template('perfis/perfis_lista.html', titulo='Perfis', perfis=perfis, busca=busca)
```

No `templates/perfis/perfis_lista.html`, entre o cabeçalho (o `<div class="d-flex ...">`) e a `<table>`, acrescente o formulário. Repare que ele **não** tem `csrf_token` nem `method="post"`: um GET não altera nada, então não precisa de proteção CSRF.

```html
  <form action="{{ url_for('lista_perfis') }}" method="get" class="row g-2 mb-3">
    <div class="col-sm-8 col-lg-5">
      <label for="busca" class="visually-hidden">Buscar no nome ou na descrição</label>
      <input type="search" class="form-control" id="busca" name="busca" placeholder="Buscar no nome ou na descrição" value="{{ busca }}">
    </div>
    <div class="col-auto">
      <button type="submit" class="btn btn-primary">Buscar</button>
      <a href="{{ url_for('lista_perfis') }}" class="btn btn-outline-secondary">Limpar</a>
    </div>
  </form>
```

Salve, digite `analista` e clique em **Buscar**. O endereço muda para `/perfis?busca=analista` e o campo continua preenchido, **mas a lista não mudou**: a rota lê a busca e ainda a ignora.

### A consulta com LIKE

O `LIKE` e o `%s` foram explicados no [Capítulo 10](Capitulo_10_Banco_de_Dados.md#a-busca-com-like-e-o-s). Aqui a busca olha **duas** colunas, o nome e a descrição. Troque o `execute_query` da rota por este `if`:

```python
    if busca:
        perfis = execute_query(
            'SELECT id_perfil, nome, descricao, criado_em FROM perfis '
            'WHERE nome LIKE %s OR descricao LIKE %s ORDER BY nome',
            ('%' + busca + '%', '%' + busca + '%'),
            fetch=True,
        )
    else:
        perfis = execute_query(
            'SELECT id_perfil, nome, descricao, criado_em FROM perfis ORDER BY nome',
            fetch=True,
        )
```

São dois `%s`, então a tupla leva o valor **duas vezes**, na mesma ordem. Os `%` do `LIKE` ficam no **valor**, e o texto do SQL só tem o marcador. Salve e teste:

- `analista`: três perfis (Analista de Dados, Analista de Sistemas e Analista Financeiro).
- `ANALISTA`: o mesmo resultado, porque a ordenação `utf8mb4_unicode_ci` ignora maiúsculas e acentos.
- `estoque`: **Almoxarife** e **Contador**. A palavra não está no nome deles, está na **descrição**.
- `' OR '1'='1`: nenhum resultado. O texto vira só um termo a procurar, nunca um pedaço do comando (o *SQL Injection* do Capítulo 10).

Para mostrar quantos perfis a busca encontrou, acrescente no `perfis_lista.html`, entre o formulário e a tabela:

```html
  <p class="text-body-secondary">{{ perfis|length }} perfil(is) encontrado(s).</p>
```

```bash
git add .
git commit -m "Adiciona a busca de perfis por nome e descrição"
git push
```

---

## Tópico 3 — Mais de um filtro: o WHERE 1=1

### A dor: uma consulta para cada combinação

Quem administra também quer separar os perfis **com** descrição dos **sem** descrição. Agora são dois filtros opcionais, e a consulta muda conforme a pessoa preencheu um, o outro, os dois ou nenhum:

| O que foi preenchido | O SQL precisaria ser |
|---|---|
| Nada | `... FROM perfis ORDER BY nome` |
| Só a busca | `... WHERE nome LIKE ... OR descricao LIKE ... ORDER BY nome` |
| Só a descrição | `... WHERE descricao IS NULL ORDER BY nome` |
| Os dois | `... WHERE (nome LIKE ... OR descricao LIKE ...) AND descricao IS NULL ORDER BY nome` |

Quatro `if` para dois filtros, e com três filtros seriam oito. O obstáculo é que o primeiro filtro precisa de `WHERE` e os seguintes de `AND`, e a rota não sabe qual é o primeiro. A saída é começar a consulta com uma condição que **sempre é verdadeira**, o `WHERE 1=1`: ela não filtra nada, e todo filtro preenchido entra depois dela com `AND`, sem exceção.

### O formulário com o segundo filtro

No `perfis_lista.html`, acrescente o `<select>` da descrição ao formulário. Troque o formulário inteiro por este (os campos agora dividem a linha em colunas):

```html
  <form action="{{ url_for('lista_perfis') }}" method="get" class="row g-2 align-items-end mb-3">
    <div class="col-md-6">
      <label for="busca" class="form-label">Buscar no nome ou na descrição</label>
      <input type="search" class="form-control" id="busca" name="busca" placeholder="Ex.: analista" value="{{ busca }}">
    </div>
    <div class="col-md-3">
      <label for="descricao" class="form-label">Descrição</label>
      <select class="form-select" id="descricao" name="descricao">
        <option value="" {% if descricao == '' %}selected{% endif %}>Todos</option>
        <option value="com" {% if descricao == 'com' %}selected{% endif %}>Com descrição</option>
        <option value="sem" {% if descricao == 'sem' %}selected{% endif %}>Sem descrição</option>
      </select>
    </div>
    <div class="col-md-3 d-flex gap-2">
      <button type="submit" class="btn btn-primary">Filtrar</button>
      <a href="{{ url_for('lista_perfis') }}" class="btn btn-outline-secondary">Limpar</a>
    </div>
  </form>
```

O `selected` marca a opção que a pessoa tinha escolhido, como no Capítulo 9. Falta a rota entregar a variável `descricao`. Acrescente a leitura e o `descricao=descricao` no `render_template`, **sem** mudar a consulta ainda:

```python
    busca = request.args.get('busca', '').strip()
    descricao = request.args.get('descricao', '')

    if descricao not in ('com', 'sem'):
        descricao = ''
```

O `if` confere que o valor é uma das duas opções (ou fica vazio): o endereço pode ser digitado à mão, e o servidor não confia no que chega.

### Montando a consulta aos poucos

Agora a rota passa a montar o SQL em duas variáveis: o texto (`condicoes`) e a lista dos valores dos `%s` (`params`). Primeiro só com a busca, **para conferir que nada quebrou**. Troque o `if busca:` e o `else` inteiros por:

```python
    condicoes = ' WHERE 1=1'
    params = []

    if busca:
        condicoes += ' AND (nome LIKE %s OR descricao LIKE %s)'
        params.append('%' + busca + '%')
        params.append('%' + busca + '%')

    sql = 'SELECT id_perfil, nome, descricao, criado_em FROM perfis' + condicoes + ' ORDER BY nome'
    perfis = execute_query(sql, params, fetch=True)
```

!!! note "Python: o `+=` e o `append`"
    O `condicoes += ' AND ...'` **acrescenta** texto ao final do que já havia em `condicoes`, e equivale a `condicoes = condicoes + ' AND ...'`. Já o `params.append(valor)` acrescenta um item ao final da lista. O texto do SQL e a lista dos valores crescem **juntos**, na mesma ordem: cada `%s` colocado em `condicoes` tem o seu valor guardado em `params`.

Salve e repita as buscas `analista` e `estoque`: os resultados são os mesmos do tópico anterior. Os parênteses em volta do `OR` são essenciais: o `AND` é avaliado **antes** do `OR`, e sem eles o `OR` se misturaria com os filtros que vêm depois e o resultado seria outro.

Agora o segundo filtro, **antes** da linha que monta o `sql`:

```python
    if descricao == 'com':
        condicoes += ' AND descricao IS NOT NULL'
    elif descricao == 'sem':
        condicoes += ' AND descricao IS NULL'
```

!!! note "SQL: `IS NULL`, e não `= NULL`"
    No MySQL, `NULL` significa "sem valor", e nada é igual a "sem valor", nem outro `NULL`. Por isso `descricao = NULL` nunca é verdadeiro. Para perguntar se a coluna está vazia, o SQL tem `IS NULL` e `IS NOT NULL`. Funciona porque, desde o Capítulo 12, a descrição vazia é gravada como `NULL`, e não como `''`.

Repare que esses dois filtros **não têm `%s`**: o texto que entra no SQL é uma constante escrita por nós, e o que vem do endereço só decide qual das duas alternativas vale. Salve e teste:

- **Descrição:** `Sem descrição` mostra os perfis sem descrição, entre eles o Gerente (se você o cadastrou sem descrição, como no Capítulo 12, são 7 perfis). `Com descrição` mostra os outros 23.
- **Busca e descrição juntos:** `analista` e `Com descrição`: os três analistas. `analista` e `Sem descrição`: nenhum.

A consulta que o MySQL recebe muda a cada combinação, mas o **seu código não mudou**. É a vantagem do `WHERE 1=1`: cada filtro novo é um `if` novo, e não o dobro de consultas. Veja como o texto e a lista crescem juntos quando você busca `analista` com `Com descrição`:

| Momento | `condicoes` | `params` |
|---|---|---|
| Começo | `' WHERE 1=1'` | `[]` |
| Depois da busca | `... AND (nome LIKE %s OR descricao LIKE %s)` | `['%analista%', '%analista%']` |
| Depois da descrição | `... AND descricao IS NOT NULL` | `['%analista%', '%analista%']` |

!!! danger "Só texto escrito por você entra no SQL"
    Concatenar texto no SQL é seguro aqui por um motivo preciso: tudo o que é somado a `condicoes` é um trecho fixo escrito no código. Os valores digitados vão **sempre** em `params`, para o `%s`. Se alguém somasse o `busca` direto em `condicoes`, estaria de volta o *SQL Injection*.

```bash
git add .
git commit -m "Adiciona o filtro de descrição e monta a consulta com WHERE 1=1"
git push
```

---

## Tópico 4 — Ordenar a lista

### O ORDER BY não aceita %s

Quem administra também quer a ordem: pelo nome, ou os perfis criados mais recentemente primeiro. A tentação é fazer `ORDER BY %s` e passar o que veio do endereço. Não funciona: o `%s` só substitui **valores** (textos e números). O nome de uma coluna e palavras como `DESC` pertencem à **estrutura** do SQL, e o conector colocaria aspas em volta, quebrando a consulta. E concatenar o que o usuário digitou nessa posição reabriria a porta do *SQL Injection*.

A solução é uma **lista de valores permitidos**: um dicionário em que a chave é o que vem do endereço e o valor é o trecho de SQL, escrito por nós. No `app.py`, logo abaixo do `CSRFProtect(app)`:

```python
# Ordenações permitidas: a chave vem do endereço, o valor é o SQL fixo escrito por nós
ORDENACOES = {
    'nome': 'nome ASC',
    'recentes': 'criado_em DESC, id_perfil DESC',
}
```

O `'recentes'` ordena por `criado_em` do mais novo ao mais antigo, e o `id_perfil DESC` **desempata** perfis criados no mesmo instante, como os que você cadastrou à mão.

Na rota, leia a opção, confira que ela existe no dicionário e use o SQL guardado nele. Acrescente a leitura junto das outras duas e a conferência abaixo do `if descricao not in ...`:

```python
    ordem = request.args.get('ordem', 'nome')

    if ordem not in ORDENACOES:
        ordem = 'nome'
```

!!! note "Python: `in` e `[ ]` com dicionário"
    Num dicionário, `ordem in ORDENACOES` pergunta se `ordem` é uma das **chaves**. E `ORDENACOES[ordem]` devolve o **valor** guardado nessa chave. Se alguém digitar uma chave inventada no endereço, o `if` a troca por `'nome'` antes de chegar ao dicionário.

Agora a consulta usa o dicionário. Troque a linha do `sql` por:

```python
    sql = ('SELECT id_perfil, nome, descricao, criado_em FROM perfis' + condicoes
           + ' ORDER BY ' + ORDENACOES[ordem])
```

(Os parênteses permitem quebrar a linha longa em duas.) E devolva a variável ao template, acrescentando `ordem=ordem` no `render_template`. No formulário do `perfis_lista.html`, acrescente o `<select>` da ordem **depois** do da descrição. Para a linha continuar somando 12 colunas do Bootstrap, troque o `col-md-6` do campo de busca por `col-md-5` e o `col-md-3` da `<div>` dos botões por `col-md-2` (o `col-md-3` da descrição não muda):

```html
    <div class="col-md-2">
      <label for="ordem" class="form-label">Ordenar por</label>
      <select class="form-select" id="ordem" name="ordem">
        <option value="nome" {% if ordem == 'nome' %}selected{% endif %}>Nome (A–Z)</option>
        <option value="recentes" {% if ordem == 'recentes' %}selected{% endif %}>Mais recentes</option>
      </select>
    </div>
```

Salve e teste **Mais recentes**: no alto aparecem os três perfis que você cadastrou no Capítulo 12 (criados hoje) e, em seguida, **Gestor de Projetos**, **Vendedor** e **Técnico de Suporte**, do mais novo ao mais antigo do arquivo.

Agora tente quebrar a ordenação, digitando na barra de endereço:

```text
http://127.0.0.1:5000/perfis?ordem=nome;DROP TABLE perfis
```

A lista aparece em ordem alfabética e a tabela segue intacta: a chave inventada caiu no `'nome'`. Mesmo princípio, duas defesas: o `%s` protege os **valores**, e a lista de valores permitidos protege a **estrutura**.

```bash
git add .
git commit -m "Adiciona a ordenação da lista de perfis por lista de valores permitidos"
git push
```

---

## Tópico 5 — Paginação

### LIMIT e OFFSET

Falta dividir a lista em páginas. O SQL tem duas palavras para isso:

- **`LIMIT n`**: devolve no máximo `n` linhas.
- **`OFFSET m`**: **pula** as primeiras `m` linhas antes de começar a devolver.

Com 10 perfis por página, a conta é sempre a mesma:

| Página | `LIMIT` | `OFFSET` | Linhas devolvidas |
|---|---|---|---|
| 1 | 10 | 0 | da 1ª à 10ª |
| 2 | 10 | 10 | da 11ª à 20ª |
| 3 | 10 | 20 | da 21ª à 30ª |

O `OFFSET` é `(página - 1) * 10`. Vamos escrever isso na rota.

### Lendo a página

No `app.py`, acrescente a constante com o tamanho da página, logo acima do `ORDENACOES`:

```python
POR_PAGINA = 10
```

Na rota, leia a página junto das outras:

```python
    pagina = request.args.get('pagina', 1, type=int)
```

!!! note "Flask: `type=int` no `request.args.get`"
    O segundo argumento (`1`) é o valor **padrão**, usado quando o `pagina` não vem no endereço. O `type=int` converte o texto para número inteiro. Se a conversão não for possível (`?pagina=abc`), o Flask não dá erro: devolve o valor padrão.

Troque a montagem do `sql` para incluir o `LIMIT` e o `OFFSET`, que são **valores** e por isso usam `%s`:

```python
    deslocamento = (pagina - 1) * POR_PAGINA

    sql = ('SELECT id_perfil, nome, descricao, criado_em FROM perfis' + condicoes
           + ' ORDER BY ' + ORDENACOES[ordem] + ' LIMIT %s OFFSET %s')
    perfis = execute_query(sql, params + [POR_PAGINA, deslocamento], fetch=True)
```

O `params + [POR_PAGINA, deslocamento]` junta duas listas: os valores dos filtros e, no fim, os dois últimos `%s`, na mesma ordem em que aparecem no SQL. Salve e abra, pela barra de endereço, `/perfis`, `/perfis?pagina=2` e `/perfis?pagina=3`: **10 perfis em cada uma**, sem repetir nenhum. Ainda não há botões, a página é escolhida pelo endereço.

Agora o problema: abra `/perfis?pagina=0`. O deslocamento vira `-10`, e a página de depuração mostra `1064 (42000): You have an error in your SQL syntax ... near '-10'`. O `OFFSET` não aceita número negativo. E o `/perfis?pagina=99` mostra uma tabela vazia, porque não há 99 páginas. A rota precisa saber **quantas páginas existem** e manter a página dentro desse limite.

### Contando as páginas

Para saber quantas páginas existem, é preciso saber quantos perfis **a busca encontrou**. O `COUNT(*)` conta, e ele precisa usar as **mesmas condições** da lista, senão a contagem seria de todos os perfis, e não dos filtrados. Por isso o texto das condições foi guardado numa variável. Acrescente, **antes** do `deslocamento`:

```python
    contagem = execute_one('SELECT COUNT(*) AS total FROM perfis' + condicoes, params)
    total = contagem['total']

    total_paginas = math.ceil(total / POR_PAGINA)
    if total_paginas < 1:
        total_paginas = 1

    if pagina < 1:
        pagina = 1
    if pagina > total_paginas:
        pagina = total_paginas
```

E importe o módulo `math` na **primeira linha** do `app.py`:

```python
import math
import os
```

!!! note "Python: `import math` e `math.ceil`"
    O módulo `math` vem com o Python e traz funções de matemática. O `math.ceil` **arredonda para cima**: `math.ceil(2.1)` é `3`. O `/` do Python sempre devolve um número com vírgula (`25 / 10` é `2.5`), então 25 perfis a 10 por página dão `math.ceil(2.5)`, ou seja, **3 páginas**: duas cheias e uma com 5. Quando o total é `0`, o resultado seria `0` páginas, por isso o `if` o troca por `1`: uma página vazia continua sendo uma página.

As duas últimas conferências mantêm `pagina` entre `1` e `total_paginas`. Com elas, `?pagina=0` e `?pagina=abc` mostram a primeira página, e `?pagina=99` mostra a última. O `render_template` passa a entregar o total e as páginas. Acrescente `total=total`, `pagina=pagina` e `total_paginas=total_paginas` aos argumentos. Para o texto do template, troque a linha da contagem por esta:

```html
  <p class="text-body-secondary">{{ total }} perfil(is) encontrado(s). Página {{ pagina }} de {{ total_paginas }}.</p>
```

Salve e recarregue: `30 perfil(is) encontrado(s). Página 1 de 3.` Teste `?pagina=0`, `?pagina=99` e `?pagina=abc`: nenhum quebra. Teste a busca `analista`: `3 perfil(is) encontrado(s). Página 1 de 1.` O `total` agora vem do `COUNT(*)`, que conta todas as linhas do filtro, e não só as 10 da página.

### Os botões de página

Para navegar sem digitar o endereço, o Bootstrap tem o componente `pagination`. Acrescente no `perfis_lista.html`, **depois** da `</table>`:

```html
  {% if total_paginas > 1 %}
  <nav aria-label="Páginas da lista de perfis">
    <ul class="pagination justify-content-center">
      <li class="page-item {% if pagina == 1 %}disabled{% endif %}">
        <a class="page-link" href="{{ url_for('lista_perfis', busca=busca, descricao=descricao, ordem=ordem, pagina=pagina - 1) }}">Anterior</a>
      </li>
      {% for numero in range(1, total_paginas + 1) %}
      <li class="page-item {% if numero == pagina %}active{% endif %}">
        <a class="page-link" href="{{ url_for('lista_perfis', busca=busca, descricao=descricao, ordem=ordem, pagina=numero) }}">{{ numero }}</a>
      </li>
      {% endfor %}
      <li class="page-item {% if pagina == total_paginas %}disabled{% endif %}">
        <a class="page-link" href="{{ url_for('lista_perfis', busca=busca, descricao=descricao, ordem=ordem, pagina=pagina + 1) }}">Próxima</a>
      </li>
    </ul>
  </nav>
  {% endif %}
```

Os pontos novos:

- **`range(1, total_paginas + 1)`**: no Jinja, gera os números de `1` até `total_paginas` (o último número do `range` não entra, por isso o `+ 1`). O `for` cria um botão para cada um.
- **`active` e `disabled`**: classes do Bootstrap. A página atual fica destacada, e o **Anterior** (na página 1) e o **Próxima** (na última) ficam desabilitados.
- **`url_for` com os filtros**: cada link leva o `busca`, o `descricao` e a `ordem` atuais, além da página. Sem isso, clicar em "2" faria a pessoa **perder a busca**. Os argumentos do `url_for` que não estão no caminho da rota viram parâmetros depois do `?`.
- **`{% if total_paginas > 1 %}`**: com uma página só, os botões não aparecem.

Salve e teste:

1. Sem filtros, clique em **2** e em **Próxima**: a página 3 tem os 10 últimos, e o botão **Próxima** fica cinza.
2. Escolha **Mais recentes**, depois **Com descrição**, depois vá à página 2: a ordenação e o filtro continuam valendo, e o endereço mostra todos eles (`/perfis?busca=&descricao=com&ordem=recentes&pagina=2`).
3. Busque `analista`: uma página só e **nenhum botão**.

Com centenas de páginas, uma fileira de números não caberia na tela, e os sistemas mostram só uma janela em volta da página atual. Para os 30 perfis deste capítulo, a fileira completa é o suficiente.

```bash
git add .
git commit -m "Adiciona a paginação da lista de perfis com LIMIT, OFFSET e COUNT"
git push
```

---

## Os arquivos completos do capítulo

A rota `lista_perfis` e as constantes do `app.py` (o resto do arquivo é o do Capítulo 12, com o `import math` na primeira linha):

```python
POR_PAGINA = 10

# Ordenações permitidas: a chave vem do endereço, o valor é o SQL fixo escrito por nós
ORDENACOES = {
    'nome': 'nome ASC',
    'recentes': 'criado_em DESC, id_perfil DESC',
}
```

```python
@app.route('/perfis')
def lista_perfis():
    busca = request.args.get('busca', '').strip()
    descricao = request.args.get('descricao', '')
    ordem = request.args.get('ordem', 'nome')
    pagina = request.args.get('pagina', 1, type=int)

    if descricao not in ('com', 'sem'):
        descricao = ''

    if ordem not in ORDENACOES:
        ordem = 'nome'

    # WHERE 1=1 é sempre verdadeiro: todo filtro preenchido entra com AND
    condicoes = ' WHERE 1=1'
    params = []

    if busca:
        condicoes += ' AND (nome LIKE %s OR descricao LIKE %s)'
        params.append('%' + busca + '%')
        params.append('%' + busca + '%')

    if descricao == 'com':
        condicoes += ' AND descricao IS NOT NULL'
    elif descricao == 'sem':
        condicoes += ' AND descricao IS NULL'

    contagem = execute_one('SELECT COUNT(*) AS total FROM perfis' + condicoes, params)
    total = contagem['total']

    total_paginas = math.ceil(total / POR_PAGINA)
    if total_paginas < 1:
        total_paginas = 1

    if pagina < 1:
        pagina = 1
    if pagina > total_paginas:
        pagina = total_paginas

    deslocamento = (pagina - 1) * POR_PAGINA

    sql = ('SELECT id_perfil, nome, descricao, criado_em FROM perfis' + condicoes
           + ' ORDER BY ' + ORDENACOES[ordem] + ' LIMIT %s OFFSET %s')
    perfis = execute_query(sql, params + [POR_PAGINA, deslocamento], fetch=True)

    return render_template('perfis/perfis_lista.html', titulo='Perfis', perfis=perfis, total=total,
                           busca=busca, descricao=descricao, ordem=ordem,
                           pagina=pagina, total_paginas=total_paginas)
```

O `templates/perfis/perfis_lista.html`:

```html
{% extends 'layout/base_menu.html' %}

{% block titulo_aba %}{{ titulo }} — Sistema de Gestão{% endblock %}

{% block conteudo %}
  <div class="d-flex justify-content-between align-items-center mb-3">
    <h1 class="h2 mb-0">{{ titulo }}</h1>
    <a href="{{ url_for('perfil_novo') }}" class="btn btn-primary">Novo perfil</a>
  </div>

  <form action="{{ url_for('lista_perfis') }}" method="get" class="row g-2 align-items-end mb-3">
    <div class="col-md-5">
      <label for="busca" class="form-label">Buscar no nome ou na descrição</label>
      <input type="search" class="form-control" id="busca" name="busca" placeholder="Ex.: analista" value="{{ busca }}">
    </div>
    <div class="col-md-3">
      <label for="descricao" class="form-label">Descrição</label>
      <select class="form-select" id="descricao" name="descricao">
        <option value="" {% if descricao == '' %}selected{% endif %}>Todos</option>
        <option value="com" {% if descricao == 'com' %}selected{% endif %}>Com descrição</option>
        <option value="sem" {% if descricao == 'sem' %}selected{% endif %}>Sem descrição</option>
      </select>
    </div>
    <div class="col-md-2">
      <label for="ordem" class="form-label">Ordenar por</label>
      <select class="form-select" id="ordem" name="ordem">
        <option value="nome" {% if ordem == 'nome' %}selected{% endif %}>Nome (A–Z)</option>
        <option value="recentes" {% if ordem == 'recentes' %}selected{% endif %}>Mais recentes</option>
      </select>
    </div>
    <div class="col-md-2 d-flex gap-2">
      <button type="submit" class="btn btn-primary">Filtrar</button>
      <a href="{{ url_for('lista_perfis') }}" class="btn btn-outline-secondary">Limpar</a>
    </div>
  </form>

  <p class="text-body-secondary">{{ total }} perfil(is) encontrado(s). Página {{ pagina }} de {{ total_paginas }}.</p>

  <table class="table table-striped table-hover">
    <thead class="table-light">
      <tr>
        <th>Código</th>
        <th>Nome</th>
        <th>Descrição</th>
        <th>Criado em</th>
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
        <td>{{ perfil.criado_em.strftime('%d/%m/%Y') }}</td>
      </tr>
      {% else %}
      <tr>
        <td colspan="4" class="text-center text-body-secondary py-4">Nenhum perfil encontrado.</td>
      </tr>
      {% endfor %}
    </tbody>
  </table>

  {% if total_paginas > 1 %}
  <nav aria-label="Páginas da lista de perfis">
    <ul class="pagination justify-content-center">
      <li class="page-item {% if pagina == 1 %}disabled{% endif %}">
        <a class="page-link" href="{{ url_for('lista_perfis', busca=busca, descricao=descricao, ordem=ordem, pagina=pagina - 1) }}">Anterior</a>
      </li>
      {% for numero in range(1, total_paginas + 1) %}
      <li class="page-item {% if numero == pagina %}active{% endif %}">
        <a class="page-link" href="{{ url_for('lista_perfis', busca=busca, descricao=descricao, ordem=ordem, pagina=numero) }}">{{ numero }}</a>
      </li>
      {% endfor %}
      <li class="page-item {% if pagina == total_paginas %}disabled{% endif %}">
        <a class="page-link" href="{{ url_for('lista_perfis', busca=busca, descricao=descricao, ordem=ordem, pagina=pagina + 1) }}">Próxima</a>
      </li>
    </ul>
  </nav>
  {% endif %}
{% endblock %}
```

Os demais arquivos (`db.py`, `validacoes.py`, `perfil_form.html`, os layouts e os outros templates) são os do Capítulo 12.

---

## 📦 Código deste capítulo

Compare com o seu projeto. Este capítulo é opcional, então o **Capítulo 13 não parte deste zip**, e sim do zip do Capítulo 12. O zip tem o `app.py`, o `db.py`, o `validacoes.py`, o `testar_conexao.py`, o `banco.sql`, o `perfis_30.sql`, o `.env.example`, o `.gitignore`, o `requirements.txt`, a pasta `templates` e a pasta `static`. O ambiente virtual e o `.env` **não** vão no zip: crie-os como no Capítulo 11. Importe o `banco.sql` e, depois dele, o `perfis_30.sql`.

➡️ [Baixar p2_cap_12_1.zip](../arquivos/p2_cap_12_1.zip)

---

## 🃏 Flashcards de Revisão

Tente responder mentalmente antes de abrir.

??? question "Para que serve o `WHERE 1=1` e por que ele é seguro?"
    A condição `1=1` é sempre verdadeira, então não filtra nada, e todo filtro opcional pode entrar depois dela com `AND`, sem a rota precisar saber qual é o primeiro. É seguro porque o texto somado à consulta é sempre um trecho fixo escrito no código. Os valores digitados vão separados, na lista `params`, para os `%s`.

??? question "Por que a busca tem parênteses em `AND (nome LIKE %s OR descricao LIKE %s)`?"
    Porque o `AND` é avaliado antes do `OR`. Sem os parênteses, o `OR` se misturaria com os filtros seguintes e a consulta devolveria linhas que não deveriam aparecer.

??? question "Por que não dá para usar `ORDER BY %s`, e o que se faz no lugar?"
    O `%s` só substitui valores, e o nome de uma coluna pertence à estrutura do SQL. No lugar, usa-se um dicionário de valores permitidos: a chave vem do endereço e o valor é o trecho de SQL escrito no código. Uma chave inventada cai na ordenação padrão.

??? question "Qual a diferença entre `descricao = NULL` e `descricao IS NULL`?"
    O `= NULL` nunca é verdadeiro, porque nada é igual a "sem valor". Só o `IS NULL` e o `IS NOT NULL` perguntam se a coluna está vazia.

??? question "Como o `LIMIT` e o `OFFSET` formam a página 3, com 10 perfis por página?"
    O `OFFSET` pula `(3 - 1) * 10 = 20` linhas, e o `LIMIT 10` devolve as 10 seguintes: da 21ª à 30ª.

??? question "Por que o `COUNT(*)` usa as mesmas condições da lista?"
    Porque o total de páginas depende de quantos perfis o filtro encontrou, e não de quantos existem na tabela. Contar todos faria a paginação mostrar páginas vazias depois de uma busca.

---

## 📝 Resumo

O `perfis_30.sql` encheu a tabela com `INSERT IGNORE`, que pula os nomes que já existem sem alterar nada. A lista passou a aceitar uma busca com `LIKE` em duas colunas, um filtro de descrição com `IS NULL` e `IS NOT NULL` e uma ordenação escolhida num dicionário de valores permitidos. A consulta é montada aos poucos sobre o `WHERE 1=1`, com o texto em `condicoes` e os valores em `params`, e só texto escrito no código entra no SQL. A paginação usa o `LIMIT` e o `OFFSET` para trazer só 10 perfis, o `COUNT(*)` com as mesmas condições para saber quantas páginas existem e os botões do Bootstrap, cujos links levam a busca, o filtro e a ordenação junto da página. O Capítulo 13 continua do código do Capítulo 12, com a edição e a exclusão de perfis.

---

## 🔗 Navegação

⬅️ [Capítulo 12 — INSERT e SELECT de perfis](Capitulo_12_INSERT_e_SELECT_de_Perfis.md) · ➡️ [Capítulo 13 — UPDATE e DELETE de perfis](Capitulo_13_UPDATE_e_DELETE_de_Perfis.md)

---

*Fatec Jahu · ILP951 · Prof. Ronan Adriel Zenatti · 2026*
