# Apoio aos Tópicos 06 e 07 — O CRUD com a tabela `produto`

**Disciplina:** Programação para Internet (ILP951)
**Professor:** Ronan Adriel Zenatti · ronan.zenatti@cps.sp.gov.br
**Fatec Jahu — 2º Semestre/2026**

> 📎 **Material de apoio.** O CRUD dos Tópicos 06 e 07 foi construído sobre **usuários e perfis**. Algumas técnicas só aparecem quando o registro tem **dinheiro, estoque e uma categoria fixa**, e por isso ficaram fora do texto principal: converter e validar `Decimal` e `int`, formatar moeda com um filtro Jinja2 próprio, colorir badges por faixa de estoque, evoluir a tabela com `ALTER TABLE` para criar uma categoria e validar uma lista fixa de categorias. Esta página reúne todas elas, usando a tabela **`produto`** (veja a criação em [Apoio ao Tópico 05](Aula_05_apoio_produto.md)) como exemplo. Se o domínio do **seu** sistema tem valores monetários, é aqui que você vai buscar o que precisa.
>
> Os trechos supõem que você já fez o CRUD de usuários: a estrutura de rotas, o PRG, o padrão de validação e os filtros com `WHERE 1=1` são os mesmos, só mudam os campos.

---

## 1. Evoluir a tabela: a coluna `categoria` (`ALTER TABLE`)

O nosso formulário vai pedir a **categoria** do produto (para filtrar por ela mais adiante), mas a tabela criada no Tópico 05 não tem essa coluna. Em vez de apagar a tabela e perder os dados, usamos o `ALTER TABLE`, que **altera a estrutura** de uma tabela existente. No Workbench, execute:

```sql
USE projeto_web;

-- Nova coluna: texto curto, obrigatório, com valor padrão para as linhas que já existem
ALTER TABLE produto
    ADD COLUMN categoria VARCHAR(50) NOT NULL DEFAULT 'Outros' AFTER descricao;
-- AFTER descricao: posiciona a coluna logo depois de 'descricao' (só estética)
-- DEFAULT 'Outros': as linhas já cadastradas recebem este valor automaticamente
```

Rode e, em seguida, confira o resultado:

```sql
SELECT id, nome, categoria FROM produto;
```

Todos os produtos aparecem com `Outros`. Vamos categorizá-los. Confira os `id` na grade e ajuste os números abaixo se os seus forem diferentes:

```sql
UPDATE produto SET categoria = 'Computadores' WHERE id = 1;
UPDATE produto SET categoria = 'Periféricos'  WHERE id IN (2, 3, 4);
UPDATE produto SET categoria = 'Áudio'        WHERE id = 5;
```

Rode o `SELECT` de novo e confirme as categorias.

> ⚠️ **O Workbench recusou o `UPDATE` com o erro 1175?** Ele vem com o modo *Safe Updates* ativado, que bloqueia `UPDATE` e `DELETE` cujo `WHERE` não use uma chave (como o `id`). É por isso que usamos `WHERE id ...` e não `WHERE nome LIKE ...`, e é uma proteção bem-vinda, lembra do aviso sobre o `WHERE` no Tópico 05?
>
> Se você recriar o banco do zero pelo `db_setup.py` do Tópico 05, acrescente `categoria VARCHAR(50) NOT NULL DEFAULT 'Outros'` ao `CREATE TABLE` (ou rode o `ALTER TABLE` de novo).

---

## 2. Os campos do formulário de produto

Um produto tem descrição, preço, estoque e categoria. Para a categoria usaremos uma lista única, que servirá ao formulário **e** à validação. No topo do `app.py`, logo depois de `app.secret_key = ...`, defina:

```python
# Categorias aceitas pelo sistema — fonte única para o formulário e para a validação
CATEGORIAS = ['Computadores', 'Periféricos', 'Áudio', 'Acessórios', 'Outros']
```

Na rota, passe a lista ao template (daqui em diante, toda chamada a `render_template('produto_form.html', ...)` deve receber também `categorias=CATEGORIAS`):

```python
    return render_template('produto_form.html', produto={}, categorias=CATEGORIAS)
```

No template, logo **abaixo** do campo Nome e **acima** dos botões, adicione os demais campos, um bloco por vez. Primeiro a descrição (opcional, por isso sem `required`):

```html
          <div class="mb-3">
            <label for="descricao" class="form-label">Descrição</label>
            <textarea class="form-control" id="descricao" name="descricao"
                      rows="3">{{ produto.descricao | default('', true) }}</textarea>
          </div>
```

> 💡 **Por que `default('', true)`?** O filtro `default` normalmente só age quando a variável **não existe**. O segundo argumento `true` faz ele agir também quando o valor é **vazio ou `None`**. Isso importa porque uma descrição `NULL` no banco chega ao Python como `None`, e sem esse argumento o campo exibiria o texto "None". No primeiro acesso, como `produto` é `{}`, a variável não existe, e o filtro devolve `''` de qualquer jeito.

Salve, recarregue e veja o campo de descrição aparecer. Agora, em uma linha com três colunas, o preço (com o prefixo `R$`), o estoque e a categoria:

```html
          <div class="row">
            <div class="col-md-4 mb-3">
              <label for="preco" class="form-label">Preço <span class="text-danger">*</span></label>
              <div class="input-group">
                <span class="input-group-text">R$</span>
                <input type="number" class="form-control" id="preco" name="preco"
                       step="0.01" min="0.01" placeholder="0,00" required
                       value="{{ produto.preco | default('') }}">
              </div>
            </div>
            <div class="col-md-4 mb-3">
              <label for="estoque" class="form-label">Estoque <span class="text-danger">*</span></label>
              <input type="number" class="form-control" id="estoque" name="estoque"
                     min="0" step="1" required
                     value="{{ produto.estoque | default(0) }}">
            </div>
            <div class="col-md-4 mb-3">
              <label for="categoria" class="form-label">Categoria <span class="text-danger">*</span></label>
              <select class="form-select" id="categoria" name="categoria" required>
                <option value="">-- Selecione --</option>
                {% for c in categorias %}
                  <option value="{{ c }}" {% if produto.categoria == c %}selected{% endif %}>{{ c }}</option>
                {% endfor %}
              </select>
            </div>
          </div>
```

Salve e recarregue. Observe: o campo de estoque já vem com `0`, as opções do `<select>` são geradas pelo `for` a partir de `CATEGORIAS` (altere a lista no Python, recarregue, e o formulário muda sozinho), e os campos numéricos recusam letras. Lembre-se, porém, da regra do Tópico 04: o navegador é só a primeira linha de defesa. A validação de verdade acontece no servidor.

---

## 3. Validar e converter o preço (`Decimal`) e o estoque (`int`)

Tudo que vem de `request.form` é texto. Para o dinheiro, o tipo certo é `Decimal`, e não `float`.

### Passo 7 — validar e converter o preço

O preço é o campo mais delicado. Ele precisa virar um número, e não pode ser um `float`: lembra do flashcard do Tópico 05 sobre `DECIMAL`? Números de ponto flutuante binário erram em casas decimais (`0.1 + 0.2` dá `0.30000000000000004`), o que é inaceitável para dinheiro. O Python tem o tipo `Decimal` para isso (já importado no Passo 3). Acrescente, logo depois da validação do nome:

```python
        preco = preco_txt   # se a conversão falhar, mantém o texto digitado para repopular o formulário
        try:
            valor = Decimal(preco_txt.replace(',', '.'))
            # replace: quem digita "449,90" (vírgula brasileira) também é aceito
        except InvalidOperation:
            erros.append('Informe um preço válido, por exemplo 199.90.')
        else:
            # O else do try roda só se a conversão deu certo
            if not valor.is_finite() or valor <= 0:
                # Decimal("NaN") e Decimal("Infinity") também "convertem" sem erro, por isso is_finite()
                erros.append('O preço deve ser um número maior que zero.')
            elif valor > Decimal('99999999.99'):
                erros.append('O preço máximo permitido é 99999999.99.')
                # DECIMAL(10, 2) comporta no máximo 8 dígitos antes da vírgula
            else:
                preco = valor.quantize(Decimal('0.01'))
                # quantize: arredonda para 2 casas decimais, o formato do DECIMAL(10, 2)
```

### Passo 8 — validar e converter o estoque

O estoque segue o mesmo raciocínio, agora com `int`:

```python
        estoque = estoque_txt
        try:
            valor_estoque = int(estoque_txt)
        except ValueError:
            erros.append('O estoque deve ser um número inteiro.')
        else:
            if valor_estoque < 0:
                erros.append('O estoque não pode ser negativo.')
            elif valor_estoque > 1000000:
                erros.append('O estoque máximo permitido é 1.000.000.')
            else:
                estoque = valor_estoque
```

Troque o `print` do Passo 5 por `print(erros, preco, estoque)`, salve e teste: envie o formulário com o estoque `-3` (apague o atributo `min` pelo DevTools para o navegador deixar enviar) e depois com preço `abc` (troque o `type="number"` por `type="text"` no DevTools). Observe no terminal as mensagens acumuladas na lista, e perceba que, nos campos inválidos, `preco` e `estoque` continuam sendo o texto digitado, enquanto nos válidos já viraram `Decimal` e `int`.

---

## 4. Formatar moeda: um filtro Jinja2 próprio

Hoje o preço aparece como `R$ 3499.90`, com ponto decimal e sem separador de milhar. No Brasil, queremos `R$ 3.499,90`. Em vez de repetir uma conversão em cada template, vamos criar um **filtro Jinja2 próprio**: uma função Python registrada com `@app.template_filter`, que o template chama com o mesmo `|` dos filtros que você já conhece (`upper`, `default`...). Acrescente ao `app.py`, depois da lista `CATEGORIAS`:

```python
@app.template_filter('moeda')
def formatar_moeda(valor):
    """Formata um número como moeda brasileira: 4500.5 -> R$ 4.500,50"""
    texto = f'{valor:,.2f}'                                   # 4,500.50 (padrão americano)
    texto = texto.replace(',', 'X').replace('.', ',').replace('X', '.')
    # Troca em três passos, para o ponto e a vírgula não se atropelarem
    return f'R$ {texto}'
```

No `templates/produtos.html`, troque a célula do preço:

```html
          <td>{{ produto.preco | moeda }}</td>
```

Salve e recarregue `http://localhost:5000/produtos`: o notebook agora aparece como `R$ 3.499,90`. O nome do filtro (`'moeda'`) é o que você escreve depois do `|` no template, e o nome da função (`formatar_moeda`) é livre.

### Passo 2 — colunas de identificação e categoria

Em um CRUD, mostrar o `id` e a categoria ajuda a distinguir os registros. No `<thead>`, acrescente os cabeçalhos; no `<tbody>`, as células correspondentes (e troque o `loop.index` pelo `id` real do banco):

```html
          <th>#</th>
          <th>Nome</th>
          <th>Categoria</th>
          <th>Preço</th>
```

```html
          <td>{{ produto.id }}</td>
          <td>{{ produto.nome }}</td>
          <td>{{ produto.categoria }}</td>
          <td>{{ produto.preco | moeda }}</td>
```

Salve, recarregue e confira as colunas. Note a diferença sutil entre `loop.index` (posição na tela, sempre 1, 2, 3...) e `produto.id` (identidade no banco, que não muda quando a ordem muda).

---

## 5. Badges por faixa de estoque

Um estoque de `3` unidades e um de `300` não deveriam ter a mesma aparência. Troque a célula de estoque, que usava `<td class="table-danger">`, por **badges** do Bootstrap coloridos por faixa, e faça o mesmo com o status:

```html
          <td>
            {% if produto.estoque == 0 %}
              <span class="badge bg-danger">Sem estoque</span>
            {% elif produto.estoque < 5 %}
              <span class="badge bg-warning text-dark">Estoque baixo ({{ produto.estoque }})</span>
            {% else %}
              <span class="badge bg-success">Em estoque ({{ produto.estoque }})</span>
            {% endif %}
          </td>
          <td>
            {% if produto.ativo %}
              <span class="badge bg-primary">Ativo</span>
            {% else %}
              <span class="badge bg-secondary">Inativo</span>
            {% endif %}
          </td>
```

Salve e recarregue: o Teclado (estoque 3) aparece em amarelo, e qualquer produto com estoque 0 aparece em vermelho. Altere um estoque no formulário de cadastro, ou direto no Workbench pelo `id`, para ver as três cores. É o mesmo `if / elif / else` das faixas de classificação do Tópico 04, agora decidindo uma cor.

---

## 6. A validação de produto em uma função reutilizável (Tópico 07)

No Tópico 07 a validação do formulário vira uma função usada pelo cadastro e pela edição. Esta é a versão para produtos, com `Decimal` e `int`:

```python
def validar_produto(form):
    """
    Valida e converte os campos do formulário de produto.

    Retorna (dados, erros):
        dados — dict com os valores do formulário; preco vira Decimal e estoque vira int
                quando válidos. Se inválidos, mantém o texto digitado, para repopular o form.
        erros — lista de mensagens de erro (vazia quando tudo está válido).
    """
    nome        = form.get('nome', '').strip()
    descricao   = form.get('descricao', '').strip()
    preco_txt   = form.get('preco', '').strip()
    estoque_txt = form.get('estoque', '').strip()
    categoria   = form.get('categoria', '')

    erros = []

    if not nome:
        erros.append('O nome é obrigatório.')
    elif len(nome) < 3:
        erros.append('O nome deve ter pelo menos 3 caracteres.')
    elif len(nome) > 200:
        erros.append('O nome pode ter no máximo 200 caracteres.')

    preco = preco_txt
    try:
        valor = Decimal(preco_txt.replace(',', '.'))
    except InvalidOperation:
        erros.append('Informe um preço válido, por exemplo 199.90.')
    else:
        if not valor.is_finite() or valor <= 0:
            erros.append('O preço deve ser um número maior que zero.')
        elif valor > Decimal('99999999.99'):
            erros.append('O preço máximo permitido é 99999999.99.')
        else:
            preco = valor.quantize(Decimal('0.01'))

    estoque = estoque_txt
    try:
        valor_estoque = int(estoque_txt)
    except ValueError:
        erros.append('O estoque deve ser um número inteiro.')
    else:
        if valor_estoque < 0:
            erros.append('O estoque não pode ser negativo.')
        elif valor_estoque > 1000000:
            erros.append('O estoque máximo permitido é 1.000.000.')
        else:
            estoque = valor_estoque

    if categoria not in CATEGORIAS:
        erros.append('Selecione uma categoria válida.')

    dados = {'nome': nome, 'descricao': descricao, 'preco': preco,
             'estoque': estoque, 'categoria': categoria}
    return dados, erros
```

Todo o conteúdo é o código que você já escreveu na Parte 2 do tópico anterior, apenas **movido**. A função recebe `request.form` e devolve duas coisas: os `dados` (já convertidos quando válidos) e a lista de `erros`.

---

⬅️ [Voltar ao Tópico 06](../Aula_07_CRUD_Insercao_e_Leitura.md) · [Voltar ao Tópico 07](../Aula_08_CRUD_Edicao_e_Exclusao.md)

*Fatec Jahu · ILP951 · Prof. Ronan Adriel Zenatti · 2026*
