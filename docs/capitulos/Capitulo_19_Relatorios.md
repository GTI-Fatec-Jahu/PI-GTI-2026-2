# Capítulo 19 — Relatórios

**Disciplina:** Programação para Internet (ILP951)
**Professor:** Ronan Adriel Zenatti · ronan.zenatti@cps.sp.gov.br
**Fatec Jahu — 2º Semestre/2026**

---

## 🎯 Objetivos do Capítulo

Ao final deste capítulo você deverá ser capaz de:

- Explicar a diferença entre uma **lista** (mostra as linhas) e um **relatório** (responde quantos, quanto e em média)
- Contar linhas com `COUNT` e separá-las em grupos com `GROUP BY`
- Usar `LEFT JOIN` para mostrar também os perfis que não têm nenhum usuário, e explicar por que o `JOIN` comum os esconde e por que `COUNT(*)` erra nessa consulta
- Agrupar usuários por estado (com o `NULL` virando uma linha própria) e por mês de cadastro, com `DATE_FORMAT`
- Somar e tirar a média com `SUM` e `AVG`, calcular o valor em estoque com `SUM(preco * estoque)` e tratar o `NULL` que essas funções devolvem em uma tabela vazia, com `COALESCE`
- Filtrar com `WHERE` **antes** de agrupar, listar os produtos com estoque baixo e passar o limite para a consulta com `%s`
- Mostrar cada resultado em uma tabela HTML, com a linha de total e o estado vazio

Até o Capítulo 18, cada tela do sistema **lista linhas**: os perfis, os usuários, os produtos. Uma lista responde "quais são?", mas ninguém olha 27 usuários para descobrir quantos são gerentes, nem soma 21 preços de cabeça para saber quanto vale o estoque. Este capítulo acrescenta ao sistema as telas que **resumem**: os relatórios. São só tabelas, e quase tudo acontece no SQL: o `GROUP BY`, as funções `COUNT`, `SUM` e `AVG`, o `LEFT JOIN` e o `DATE_FORMAT`. A rota continua simples (uma consulta, um `render_template`), e cada tópico traz uma pergunta nova para o banco responder.

## 📦 Ponto de partida

Este capítulo continua do **seu** repositório `sistema-gestao`, como ficou no fim do Capítulo 18: com o CRUD de produtos funcionando e o login exigido em todas as rotas. Os Capítulos 18.1 a 18.4 são subcapítulos opcionais que percorrem o mesmo caminho do 18 em arquivos menores: este capítulo parte do código do **18 completo**, e não deles.

Se o seu projeto não está funcionando, baixe o código do Capítulo 18 e descompacte. Depois de descompactar, crie o ambiente virtual e o `.env`, como no [Capítulo 11, Tópico 4](Capitulo_11_Projeto_Novo_e_Banco.md#topico-4-o-arquivo-env), e importe o `banco.sql` no phpMyAdmin:

➡️ [Baixar p2_cap_18.zip](../arquivos/p2_cap_18.zip)

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

!!! note "E se o banco estiver vazio?"
    Este capítulo traz um arquivo com 24 usuários e 21 produtos de exemplo, que o Tópico 1 importa. Se o seu banco não tem a Ana, o Bruno e a Carla, o zip não os traz, mas **o arquivo de exemplo traz usuários com a senha `Senha123`**: depois de importá-lo, entre com `marcos.oliveira@exemplo.com`, que é Administrador. Nesse caso os números do texto serão três a menos nos usuários (24 em vez de 27).

---

## Tópico 1 — Dados para os relatórios

### Antes de começar

Ligue o **Apache** e o **MySQL** no painel do XAMPP. Abra a pasta `sistema-gestao` no VS Code, o terminal (`Ctrl + '`), ative o ambiente virtual e confira o Git:

```bash
venv\Scripts\activate
git status
```

O `git status` deve dizer `nothing to commit, working tree clean`. Ligue o servidor com `python app.py` e deixe esse terminal rodando durante o capítulo (use um segundo terminal, o ícone **+**, para o Git).

### Por que um relatório?

Abra **http://127.0.0.1:5000/usuarios**. A lista tem 3 usuários, e uma pergunta como "quantos gerentes temos?" se responde olhando a coluna **Perfil**. Com 300 usuários, ninguém conta na tela. O banco, por outro lado, conta 300 linhas em um instante, e é para isso que serve um **relatório**: o `SELECT` já devolve a resposta (um número, uma soma, uma média), e a página só a mostra.

| | Lista | Relatório |
|---|---|---|
| Pergunta | Quais são os usuários? | Quantos usuários há por perfil? |
| O `SELECT` devolve | Uma linha por usuário | Uma linha por **grupo** (por perfil, por estado, por mês) |
| Quem faz a conta | Você, olhando a tela | O banco, com `COUNT`, `SUM`, `AVG` |

Para um relatório ter o que contar, o banco precisa de mais dados do que três usuários e nenhum produto. Baixe o arquivo de exemplo e salve-o **dentro da pasta `sistema-gestao`**, ao lado do `app.py`:

➡️ [Baixar relatorios_dados.sql](../arquivos/relatorios_dados.sql)

### O que o arquivo faz

Abra o arquivo no VS Code antes de importar. Os comentários do início explicam o que ele traz; o resto são três blocos:

- **Os três perfis** (`Administrador`, `Gerente` e `Usuário`) com `INSERT IGNORE`. Se você já os cadastrou no [Capítulo 12](Capitulo_12_INSERT_e_SELECT_de_Perfis.md), o `IGNORE` pula a linha e a descrição que você escolheu continua valendo.
- **24 usuários**, também com `INSERT IGNORE`: a coluna `email` é `UNIQUE`, então um e-mail que já existe é pulado. O `perfil_id` de cada um é buscado **pelo nome do perfil** (`SET @id_gerente = (SELECT id_perfil FROM perfis WHERE nome = 'Gerente')`), para funcionar seja qual for o número que o seu banco gerou. A senha de todos é `Senha123`, guardada como **hash** na variável `@senha`, como qualquer usuário criado pelo sistema.
- **21 produtos**, que entram com `INSERT ... SELECT ... WHERE NOT EXISTS`. A tabela `produtos` não tem nenhuma coluna `UNIQUE` além da chave, então o `IGNORE` sozinho duplicaria tudo a cada importação. O `NOT EXISTS` só deixa entrar o produto cujo nome ainda não existe.

Nos usuários e nos produtos, o `criado_em` está escrito de propósito, espalhado de fevereiro a outubro de 2026 (os usuários **sem nenhum cadastro em junho**, e você vai ver por quê no Tópico 3). Sem isso, todas as linhas teriam o mesmo instante, e o relatório por mês teria uma linha só.

### Importando e conferindo

No phpMyAdmin, abra a aba **Importar** (*Import*), escolha o `relatorios_dados.sql` e clique em **Importar**, como no [Capítulo 10](Capitulo_10_Banco_de_Dados.md#importando). Importe o arquivo **uma segunda vez**: nenhum erro, e nada muda, porque o `IGNORE` e o `NOT EXISTS` pularam tudo.

Abra o **Home** pelo menu e olhe os cartões do dashboard: **3** perfis, **27** usuários (os 24 do arquivo mais a Ana, o Bruno e a Carla) e **21** produtos. Se você cadastrou outros usuários ou produtos nos capítulos anteriores, os seus números serão maiores, e as tabelas que aparecem mais adiante vão diferir das do texto. O que importa é entender cada consulta.

### O mapa do recurso

Os relatórios ficam em três telas, uma de entrada e uma para cada assunto:

| Rota | Método | O que faz | Função no `app.py` | Template | Tópico |
|---|---|---|---|---|---|
| `/relatorios` | GET | Entrada, com um cartão por relatório | `relatorios` | `relatorios/relatorios.html` | 1 |
| `/relatorios/usuarios` | GET | Usuários por perfil, por estado e por mês | `relatorio_usuarios` | `relatorios/relatorio_usuarios.html` | 2 e 3 |
| `/relatorios/produtos` | GET | Resumo, por categoria e estoque baixo | `relatorio_produtos` | `relatorios/relatorio_produtos.html` | 4 e 5 |

Nenhuma delas grava nada: relatório só lê, por isso só existe `GET`.

### A entrada e o menu

Comece pela porta de entrada, ainda **provisória**: sem consulta ao banco, como foi a página `/produtos` no Capítulo 18. No `app.py`, acrescente a rota **depois** da `produto_excluir` e **antes** dos `@app.errorhandler`:

```python
@app.route('/relatorios')
def relatorios():
    if 'id_usuario' not in session:
        flash('Entre para continuar.', 'warning')
        return redirect(url_for('login'))

    return render_template('relatorios/relatorios.html', titulo='Relatórios')
```

O `if` do começo é o mesmo das outras rotas desde o [Capítulo 17](Capitulo_17_Login.md): quem não fez login vai para a tela de entrada. Crie a pasta `templates/relatorios` e, dentro dela, o `relatorios.html`:

```html
{% extends 'layout/base_menu.html' %}

{% block titulo_aba %}{{ titulo }} — Sistema de Gestão{% endblock %}

{% block conteudo %}
  <h1 class="h2 mb-3">{{ titulo }}</h1>

  <div class="alert alert-info" role="alert">
    Os relatórios aparecem aqui, um de cada vez, ao longo do capítulo.
  </div>
{% endblock %}
```

Agora o menu. No `templates/layout/base_menu.html`, acrescente o item **Relatórios** **depois** do menu Produtos, ainda no primeiro `<ul class="navbar-nav me-auto">`:

```html
          <li class="nav-item">
            <a class="nav-link {% if request.endpoint in ['relatorios', 'relatorio_usuarios', 'relatorio_produtos'] %}active{% endif %}" href="{{ url_for('relatorios') }}">Relatórios</a>
          </li>
```

Ele é um link simples, e não um menu suspenso como os de Perfis, Usuários e Produtos, porque os relatórios têm uma única porta de entrada, a página que você acabou de criar. A lista de endpoints faz o item ficar destacado em qualquer uma das telas do recurso, inclusive nas que ainda vão ser construídas. Salve, recarregue e clique em **Relatórios**: a página provisória aparece, com o item do menu destacado.

Para registrar este ponto no Git (o `relatorios_dados.sql` entra junto, para o seu repositório guardar de onde vieram os dados de exemplo):

```bash
git add .
git commit -m "Adiciona o relatorios_dados.sql e a página de entrada dos relatórios"
git push
```

---

## Tópico 2 — Usuários por perfil: `COUNT`, `GROUP BY` e `LEFT JOIN`

### Contar tudo, e contar por grupo

Você já escreveu `SELECT COUNT(*) AS total FROM usuarios` no dashboard: o `COUNT(*)` **conta as linhas**. Teste no **phpMyAdmin** (banco `gestao`, aba **SQL**), antes de levar a consulta para o Python:

```sql
SELECT COUNT(*) AS total FROM usuarios;
```

O resultado é uma linha, com o número `27`. Para saber quantos usuários há **em cada perfil**, falta dizer ao banco como separar as linhas em grupos. É o `GROUP BY`: o banco junta as linhas que têm o mesmo valor na coluna indicada (como separar cartas em pilhas, uma por naipe) e aplica o `COUNT(*)` **a cada pilha**:

```sql
SELECT perfil_id, COUNT(*) AS total
FROM usuarios
GROUP BY perfil_id;
```

| `perfil_id` | `total` |
|---|---|
| 1 | 3 |
| 2 | 6 |
| 3 | 18 |

Em vez de 27 linhas, o resultado tem **uma por perfil**. Mas o relatório mostra o número do perfil, e ninguém lê "perfil 3 tem 18 usuários". O nome está na tabela `perfis`, e para buscá-lo você já conhece o `JOIN` (veja o [Capítulo 15, Tópico 2](Capitulo_15_SELECT_Relacional_de_Usuario.md#topico-2-o-nome-do-perfil-com-join)):

```sql
SELECT p.nome AS perfil, COUNT(*) AS total
FROM usuarios u
JOIN perfis p ON p.id_perfil = u.perfil_id
GROUP BY p.id_perfil, p.nome
ORDER BY total DESC, p.nome;
```

| `perfil` | `total` |
|---|---|
| Usuário | 18 |
| Gerente | 6 |
| Administrador | 3 |

Dois detalhes. O `ORDER BY total DESC` ordena pelo apelido `total` (o `DESC` põe o maior primeiro), e o `p.nome` desempata. E o `GROUP BY` leva `p.id_perfil, p.nome`: a regra é que **toda coluna do `SELECT` que não está dentro de uma função como o `COUNT` precisa aparecer no `GROUP BY`**. Alguns servidores recusam a consulta quando falta uma, e o MariaDB do XAMPP aceita e escolhe um valor qualquer do grupo, o que esconde o erro. Escreva sempre completo.

### Levar a consulta para a rota

Acrescente a rota **depois** da `relatorios` e **antes** dos `@app.errorhandler`:

```python
@app.route('/relatorios/usuarios')
def relatorio_usuarios():
    if 'id_usuario' not in session:
        flash('Entre para continuar.', 'warning')
        return redirect(url_for('login'))

    por_perfil = execute_query(
        'SELECT p.nome AS perfil, COUNT(*) AS total '
        'FROM usuarios u '
        'JOIN perfis p ON p.id_perfil = u.perfil_id '
        'GROUP BY p.id_perfil, p.nome '
        'ORDER BY total DESC, p.nome',
        fetch=True,
    )

    return render_template('relatorios/relatorio_usuarios.html', titulo='Relatório de usuários',
                           por_perfil=por_perfil)
```

Cada linha chega ao template como um dicionário, com as chaves `perfil` e `total`: são os apelidos (`AS`) que dão nome às chaves, como no [Capítulo 15](Capitulo_15_SELECT_Relacional_de_Usuario.md). Crie o `templates/relatorios/relatorio_usuarios.html`:

```html
{% extends 'layout/base_menu.html' %}

{% block titulo_aba %}{{ titulo }} — Sistema de Gestão{% endblock %}

{% block conteudo %}
  <div class="d-flex justify-content-between align-items-center mb-3">
    <h1 class="h2 mb-0">{{ titulo }}</h1>
    <a href="{{ url_for('relatorios') }}" class="btn btn-outline-secondary">Voltar</a>
  </div>

  <section class="mb-5">
    <h2 class="h4">Usuários por perfil</h2>

    <table class="table table-striped table-hover">
      <thead class="table-light">
        <tr>
          <th>Perfil</th>
          <th class="text-end">Usuários</th>
        </tr>
      </thead>
      <tbody>
        {% for linha in por_perfil %}
        <tr>
          <td>{{ linha.perfil }}</td>
          <td class="text-end">{{ linha.total }}</td>
        </tr>
        {% else %}
        <tr>
          <td colspan="2" class="text-center text-body-secondary py-4">Nenhum perfil cadastrado ainda.</td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </section>
{% endblock %}
```

É o molde das outras tabelas: um `{% for %}` com o `{% else %}` para o estado vazio. A coluna de números vai alinhada à direita (`text-end`), como se faz em qualquer relatório. Falta o link na entrada. No `relatorios.html`, **apague o aviso azul** (o `<div class="alert alert-info">` inteiro) e coloque no lugar o primeiro cartão:

```html
  <div class="row g-3">
    <div class="col-md-6">
      <div class="card h-100">
        <div class="card-body">
          <h2 class="h5 card-title">Usuários</h2>
          <p class="card-text">Quantos usuários há por perfil, por estado e por mês de cadastro.</p>
          <a href="{{ url_for('relatorio_usuarios') }}" class="btn btn-primary">Abrir relatório</a>
        </div>
      </div>
    </div>
  </div>
```

Salve, abra **http://127.0.0.1:5000/relatorios** e clique em **Abrir relatório**. A tabela mostra **Usuário 18**, **Gerente 6** e **Administrador 3**.

### A linha que some

Uma linha de total ajuda a conferir o relatório: a soma dos grupos tem de dar o número de usuários. No `relatorio_usuarios.html`, **depois** do `</tbody>` e antes do `</table>`, acrescente:

```html
      <tfoot>
        <tr class="fw-bold">
          <td>Total</td>
          <td class="text-end">{{ por_perfil|sum(attribute='total') }}</td>
        </tr>
      </tfoot>
```

!!! note "Jinja: `sum(attribute='total')`"
    O filtro `sum` soma os números de uma lista. Quando a lista é de dicionários, o `attribute='total'` diz **qual chave** somar: `por_perfil|sum(attribute='total')` soma o `total` de cada linha. O `<tfoot>` é o rodapé da tabela, onde ficam os totais.

Salve e recarregue: o total é **27**, igual ao cartão do dashboard. Agora um teste. Cadastre um perfil novo pelo sistema, em **Perfis > Cadastrar Perfil** (como no [Capítulo 12](Capitulo_12_INSERT_e_SELECT_de_Perfis.md)): nome `Visitante`, descrição `Só consulta`. Confira que ele aparece na lista de `/perfis`, e volte ao relatório.

**O `Visitante` não está lá.** O perfil existe, mas nenhum usuário aponta para ele, e o `JOIN` comum (o `INNER JOIN`) só devolve as linhas que têm **par** nas duas tabelas: sem usuário, sem linha. Para um relatório isso é um defeito, porque "nenhum usuário com este perfil" também é uma informação, e quem lê o relatório quer ver o `0`. A solução é o `LEFT JOIN`, que traz **todas as linhas da tabela da esquerda**, tenham par ou não. Quando não há par, as colunas da outra tabela vêm como `NULL`. A tabela que precisa aparecer sempre é `perfis`, então ela passa a ser a primeira (a da esquerda). Teste no phpMyAdmin:

```sql
SELECT p.nome AS perfil, COUNT(*) AS total
FROM perfis p
LEFT JOIN usuarios u ON u.perfil_id = p.id_perfil
GROUP BY p.id_perfil, p.nome
ORDER BY total DESC, p.nome;
```

| `perfil` | `total` |
|---|---|
| Usuário | 18 |
| Gerente | 6 |
| Administrador | 3 |
| Visitante | **1** |

O `Visitante` apareceu, mas com **1** usuário, e ele não tem nenhum. O erro está no `COUNT(*)`: ele conta **linhas**, e o `LEFT JOIN` devolveu uma linha para o `Visitante` (com todas as colunas de `usuarios` em `NULL`). A saída é contar uma coluna da tabela da direita: o `COUNT(coluna)` **ignora os `NULL`**. Troque `COUNT(*)` por `COUNT(u.id_usuario)`:

```sql
SELECT p.nome AS perfil, COUNT(u.id_usuario) AS total
FROM perfis p
LEFT JOIN usuarios u ON u.perfil_id = p.id_perfil
GROUP BY p.id_perfil, p.nome
ORDER BY total DESC, p.nome;
```

Agora o `Visitante` mostra **0**. Leve a versão certa para a rota: na `relatorio_usuarios`, troque a consulta de `por_perfil` por esta:

```python
    por_perfil = execute_query(
        'SELECT p.nome AS perfil, COUNT(u.id_usuario) AS total '
        'FROM perfis p '
        'LEFT JOIN usuarios u ON u.perfil_id = p.id_perfil '
        'GROUP BY p.id_perfil, p.nome '
        'ORDER BY total DESC, p.nome',
        fetch=True,
    )
```

Salve e recarregue o relatório: **Visitante 0** aparece na última linha, e o total continua **27**. Acrescente uma frase de ajuda abaixo do `<h2>`, para quem lê o relatório entender:

```html
    <p class="text-body-secondary">Todos os perfis aparecem, inclusive os que ainda não têm nenhum usuário.</p>
```

!!! note "`COUNT(*)` ou `COUNT(coluna)`?"
    `COUNT(*)` conta as **linhas** do grupo. `COUNT(coluna)` conta só as linhas em que a coluna **não é `NULL`**. Em uma consulta sem `LEFT JOIN` dão o mesmo número, porque nenhuma linha é vazia. Depois de um `LEFT JOIN`, a linha "sem par" existe e conta para o `COUNT(*)`, mas é `NULL` na coluna da outra tabela, e o `COUNT(coluna)` a ignora.

```bash
git add .
git commit -m "Adiciona o relatório de usuários por perfil com LEFT JOIN"
git push
```

---

## Tópico 3 — Usuários por estado e por mês

### Por estado: o `NULL` também é um grupo

O mesmo molde responde outra pergunta: quantos usuários há em cada estado. A tabela `usuarios` já guarda o estado, então não precisa de `JOIN`. Teste no phpMyAdmin:

```sql
SELECT estado, COUNT(*) AS total
FROM usuarios
GROUP BY estado
ORDER BY total DESC, estado;
```

| `estado` | `total` |
|---|---|
| SP | 13 |
| `NULL` | 6 |
| MG | 3 |
| PR | 2 |
| RJ | 2 |
| RS | 1 |

O estado é um campo **opcional** do cadastro, e quem não o informou tem `NULL`. O `GROUP BY` trata todos os `NULL` como **um grupo só**: há uma linha para eles, com o total de quem não informou. Na rota, acrescente a consulta depois da de `por_perfil` e passe o resultado ao template:

```python
    por_estado = execute_query(
        'SELECT estado, COUNT(*) AS total '
        'FROM usuarios '
        'GROUP BY estado '
        'ORDER BY total DESC, estado',
        fetch=True,
    )

    return render_template('relatorios/relatorio_usuarios.html', titulo='Relatório de usuários',
                           por_perfil=por_perfil, por_estado=por_estado)
```

E, no `relatorio_usuarios.html`, depois do `</section>` do primeiro relatório e antes do `{% endblock %}`, a segunda seção:

```html
  <section class="mb-5">
    <h2 class="h4">Usuários por estado</h2>
    <p class="text-body-secondary">O estado é opcional no cadastro, então quem não o informou aparece em uma linha própria.</p>

    <table class="table table-striped table-hover">
      <thead class="table-light">
        <tr>
          <th>Estado</th>
          <th class="text-end">Usuários</th>
        </tr>
      </thead>
      <tbody>
        {% for linha in por_estado %}
        <tr>
          <td>{{ linha.estado }}</td>
          <td class="text-end">{{ linha.total }}</td>
        </tr>
        {% else %}
        <tr>
          <td colspan="2" class="text-center text-body-secondary py-4">Nenhum usuário cadastrado ainda.</td>
        </tr>
        {% endfor %}
      </tbody>
      <tfoot>
        <tr class="fw-bold">
          <td>Total</td>
          <td class="text-end">{{ por_estado|sum(attribute='total') }}</td>
        </tr>
      </tfoot>
    </table>
  </section>
```

Salve e recarregue. A linha dos 6 usuários sem estado mostra a palavra **None**, o incômodo que o [Capítulo 15](Capitulo_15_SELECT_Relacional_de_Usuario.md#topico-3-filtros-proprios-campos-vazios-datas-e-cpf) já resolveu com o filtro `default` e o segundo argumento `true`. Troque a célula do estado por:

```html
          <td>{{ linha.estado|default('Não informado', true) }}</td>
```

Salve e recarregue: a linha agora diz **Não informado**, e o total continua **27**.

### Por mês: `DATE_FORMAT`

Agora, quantos usuários se cadastraram em cada mês. Não existe uma coluna "mês": existe `criado_em`, uma data com hora. É preciso **cortar** a data até sobrar o ano e o mês, e agrupar por esse pedaço. A função `DATE_FORMAT` escreve uma data no formato pedido, e cada letra do formato é uma peça:

| Letra | O que escreve | Exemplo para `2026-03-12 16:20:00` |
|---|---|---|
| `%Y` | Ano com 4 dígitos | `2026` |
| `%m` | Mês com 2 dígitos | `03` |
| `%d` | Dia com 2 dígitos | `12` |
| `%H` | Hora de 00 a 23 | `16` |

Teste no phpMyAdmin:

```sql
SELECT criado_em, DATE_FORMAT(criado_em, '%Y-%m') AS mes
FROM usuarios
ORDER BY criado_em
LIMIT 3;
```

Cada data virou um texto como `2026-02`. Agora é só agrupar por ele:

```sql
SELECT DATE_FORMAT(criado_em, '%Y-%m') AS mes, COUNT(*) AS total
FROM usuarios
GROUP BY mes
ORDER BY mes;
```

| `mes` | `total` |
|---|---|
| 2026-02 | 2 |
| 2026-03 | 3 |
| 2026-04 | 4 |
| 2026-05 | 3 |
| 2026-07 | 4 |
| 2026-08 | 3 |
| 2026-09 | 3 |
| 2026-10 | 2 |
| 2026-11 | 3 |

Três coisas para reparar. **Primeira:** o formato é `%Y-%m`, ano **antes** do mês, de propósito. Como o resultado é um texto, ordenar por ele coloca `2026-02` antes de `2026-10`, que é a ordem do calendário. Com `%m/%Y` (`02/2026`, `10/2026`) o ano 2027 viria no meio do 2026. **Segunda:** o `GROUP BY` e o `ORDER BY` usam o apelido `mes`. **Terceira:** não há linha para **junho**. O `GROUP BY` só cria grupos para o que existe: um mês em que ninguém se cadastrou não vira "0", **simplesmente não aparece**. É o que o arquivo de exemplo mostra de propósito, e quem lê o relatório precisa saber disso (o texto de ajuda da tabela diz). A última linha também depende de você: é o mês em que você cadastrou a Ana, o Bruno e a Carla, e nos exemplos do texto é novembro de 2026.

Leve para a rota. Acrescente a consulta depois da de `por_estado` e passe o resultado ao template:

```python
    por_mes = execute_query(
        "SELECT DATE_FORMAT(criado_em, '%Y-%m') AS mes, COUNT(*) AS total "
        'FROM usuarios '
        'GROUP BY mes '
        'ORDER BY mes',
        fetch=True,
    )

    return render_template('relatorios/relatorio_usuarios.html', titulo='Relatório de usuários',
                           por_perfil=por_perfil, por_estado=por_estado, por_mes=por_mes)
```

Repare que a primeira linha do SQL usa **aspas duplas** por fora: dentro dela há aspas simples (`'%Y-%m'`), e as duas se misturariam se o texto também começasse com aspas simples.

O banco entrega `2026-03`, e no Brasil se escreve `03/2026`. Reescrever o mês é função de um filtro próprio, como o `data_br` do Capítulo 15. No `app.py`, **depois** do filtro `moeda`, escreva:

```python
@app.template_filter('mes_br')
def mes_br(valor):
    # '2026-03' vira '03/2026'
    partes = valor.split('-')

    return partes[1] + '/' + partes[0]
```

!!! note "Python: `split` e o índice de uma lista"
    O método `split('-')` **corta** um texto em cada `-` e devolve uma **lista** com os pedaços: `'2026-03'.split('-')` vira `['2026', '03']`. Em uma lista, os itens são numerados a partir do **zero**: `partes[0]` é o `'2026'` e `partes[1]` é o `'03'`. O `+` entre textos os cola, e a função devolve `'03/2026'` (a revisão de listas está no [Capítulo 2.1](Capitulo_02_1_Python_Essencial.md)).

E a terceira seção, no `relatorio_usuarios.html`, depois da seção do estado:

```html
  <section class="mb-5">
    <h2 class="h4">Cadastros por mês</h2>
    <p class="text-body-secondary">Um mês em que ninguém se cadastrou não tem linha.</p>

    <table class="table table-striped table-hover">
      <thead class="table-light">
        <tr>
          <th>Mês</th>
          <th class="text-end">Cadastros</th>
        </tr>
      </thead>
      <tbody>
        {% for linha in por_mes %}
        <tr>
          <td>{{ linha.mes|mes_br }}</td>
          <td class="text-end">{{ linha.total }}</td>
        </tr>
        {% else %}
        <tr>
          <td colspan="2" class="text-center text-body-secondary py-4">Nenhum usuário cadastrado ainda.</td>
        </tr>
        {% endfor %}
      </tbody>
      <tfoot>
        <tr class="fw-bold">
          <td>Total</td>
          <td class="text-end">{{ por_mes|sum(attribute='total') }}</td>
        </tr>
      </tfoot>
    </table>
  </section>
```

Salve e recarregue. A terceira tabela mostra `02/2026`, `03/2026`, e assim por diante, sem o `06/2026`, e o total é **27** nas três tabelas. Os três totais iguais são a conferência: se um deles diferisse, a consulta estaria perdendo ou repetindo usuários.

```bash
git add .
git commit -m "Adiciona os relatórios de usuários por estado e por mês"
git push
```

---

## Tópico 4 — Produtos: totais, `SUM` e `AVG`

### Contar, somar e tirar a média

Até aqui o relatório **contou**. Os produtos pedem outras contas: quantas unidades há no estoque, quanto vale esse estoque e qual é o preço médio. Cada uma é uma função de agregação (como o `COUNT`), que resume **todas as linhas** em um valor:

| Função | O que devolve |
|---|---|
| `COUNT(*)` | Quantas linhas |
| `SUM(coluna)` | A soma da coluna |
| `AVG(coluna)` | A média da coluna |

Teste no phpMyAdmin. Primeiro, quantos produtos há e quantos estão ativos. A coluna `ativo` guarda `1` (ativo) ou `0` (inativo), então **somar** a coluna conta os ativos:

```sql
SELECT COUNT(*) AS total, SUM(ativo) AS ativos
FROM produtos;
```

| `total` | `ativos` |
|---|---|
| 21 | 19 |

Os inativos são `total - ativos`: **2**. Agora as contas de estoque, **só dos produtos ativos** (um produto inativo não está à venda, e contar o estoque dele inflaria os números). O `WHERE` vem antes de tudo e escolhe as linhas que entram na conta:

```sql
SELECT SUM(estoque) AS unidades,
       SUM(preco * estoque) AS valor,
       AVG(preco) AS preco_medio
FROM produtos
WHERE ativo = 1;
```

| `unidades` | `valor` | `preco_medio` |
|---|---|---|
| 393 | 95224.30 | 747.536842 |

O `SUM(preco * estoque)` multiplica o preço pelo estoque **linha a linha** e soma o resultado: é o valor do estoque. A conta é feita em `DECIMAL`, exata ao centavo (lembre-se do aviso do [Capítulo 18](Capitulo_18_CRUD_de_Produtos.md) sobre o `float` e o dinheiro). Já o `AVG` devolveu **seis casas decimais** que ninguém lê. A função `ROUND(valor, 2)` arredonda para duas:

```sql
SELECT ROUND(AVG(preco), 2) AS preco_medio
FROM produtos
WHERE ativo = 1;
```

O resultado é `747.54`.

### O relatório de produtos, em duas consultas

Leve a primeira pergunta para uma rota nova. No `app.py`, acrescente **depois** da `relatorio_usuarios` e antes dos `@app.errorhandler`:

```python
@app.route('/relatorios/produtos')
def relatorio_produtos():
    if 'id_usuario' not in session:
        flash('Entre para continuar.', 'warning')
        return redirect(url_for('login'))

    contagem = execute_one(
        'SELECT COUNT(*) AS total, SUM(ativo) AS ativos '
        'FROM produtos'
    )

    return render_template('relatorios/relatorio_produtos.html', titulo='Relatório de produtos',
                           contagem=contagem)
```

A rota usa o `execute_one` (do [Capítulo 11](Capitulo_11_Projeto_Novo_e_Banco.md)), que devolve **uma** linha, e não uma lista: a consulta sem `GROUP BY` sempre devolve exatamente uma. Em vez de percorrer com `for`, o template lê direto `contagem.total` e `contagem.ativos`. Crie o `templates/relatorios/relatorio_produtos.html`, com o cabeçalho e a primeira tabela:

```html
{% extends 'layout/base_menu.html' %}

{% block titulo_aba %}{{ titulo }} — Sistema de Gestão{% endblock %}

{% block conteudo %}
  <div class="d-flex justify-content-between align-items-center mb-3">
    <h1 class="h2 mb-0">{{ titulo }}</h1>
    <a href="{{ url_for('relatorios') }}" class="btn btn-outline-secondary">Voltar</a>
  </div>

  <section class="mb-5">
    <h2 class="h4">Resumo do catálogo</h2>

    <table class="table table-striped">
      <tbody>
        <tr>
          <th scope="row">Produtos cadastrados</th>
          <td class="text-end">{{ contagem.total }}</td>
        </tr>
        <tr>
          <th scope="row">Ativos</th>
          <td class="text-end">{{ contagem.ativos }}</td>
        </tr>
        <tr>
          <th scope="row">Inativos</th>
          <td class="text-end">{{ contagem.total - contagem.ativos }}</td>
        </tr>
      </tbody>
    </table>
  </section>
{% endblock %}
```

Esta tabela é diferente das anteriores: não tem cabeçalho de colunas nem `for`, porque não lista linhas, e sim **indicadores**, um por linha. O `<th scope="row">` marca o rótulo de cada linha, e o Jinja faz a conta `contagem.total - contagem.ativos` na hora de escrever a página. Falta o cartão na entrada. No `relatorios.html`, dentro da `<div class="row g-3">`, **depois** do cartão de Usuários:

```html
    <div class="col-md-6">
      <div class="card h-100">
        <div class="card-body">
          <h2 class="h5 card-title">Produtos</h2>
          <p class="card-text">Estoque, valor em estoque, preço médio e produtos com estoque baixo.</p>
          <a href="{{ url_for('relatorio_produtos') }}" class="btn btn-primary">Abrir relatório</a>
        </div>
      </div>
    </div>
```

Salve, abra **http://127.0.0.1:5000/relatorios**, clique em **Abrir relatório** no cartão de Produtos e confira: **21** cadastrados, **19** ativos e **2** inativos. Agora a segunda consulta. Na rota, depois da `contagem`, acrescente o `resumo` e passe-o ao template:

```python
    resumo = execute_one(
        'SELECT SUM(estoque) AS unidades, '
        'SUM(preco * estoque) AS valor, '
        'AVG(preco) AS preco_medio '
        'FROM produtos '
        'WHERE ativo = 1'
    )

    return render_template('relatorios/relatorio_produtos.html', titulo='Relatório de produtos',
                           contagem=contagem, resumo=resumo)
```

E, no template, acrescente estas três linhas **depois** da linha dos **Inativos** e antes do `</tbody>`:

```html
        <tr>
          <th scope="row">Unidades em estoque</th>
          <td class="text-end">{{ resumo.unidades }}</td>
        </tr>
        <tr>
          <th scope="row">Valor em estoque</th>
          <td class="text-end">{{ resumo.valor|moeda }}</td>
        </tr>
        <tr>
          <th scope="row">Preço médio</th>
          <td class="text-end">{{ resumo.preco_medio|moeda }}</td>
        </tr>
```

O `moeda` é o filtro do [Capítulo 18](Capitulo_18_CRUD_de_Produtos.md), que escreve `R$ 95.224,30`. Salve e recarregue: **393** unidades, **R$ 95.224,30** de valor em estoque e **R$ 747,54** de preço médio (o filtro já arredondou as seis casas para duas na hora de escrever).

### Quando não há nenhuma linha

A página funciona, mas há um defeito escondido, e ele aparece com uma tabela vazia (ou sem nenhum produto ativo). Teste no phpMyAdmin, com um `WHERE` que **nenhuma linha** satisfaz (`1 = 0` é sempre falso):

```sql
SELECT SUM(estoque) AS unidades, AVG(preco) AS preco_medio
FROM produtos
WHERE 1 = 0;
```

| `unidades` | `preco_medio` |
|---|---|
| `NULL` | `NULL` |

Somar zero linhas **não dá 0, dá `NULL`**: o banco entende "não há o que somar" como "sem resposta". Na página, o `resumo.valor` chegaria ao filtro `moeda` como `None`, e o Python pararia com o erro:

```text
TypeError: unsupported format string passed to NoneType.__format__
```

É o erro que o seu relatório mostraria no primeiro dia de uma loja nova, antes do primeiro cadastro. A função `COALESCE(a, b)` resolve: ela devolve **o primeiro valor que não é `NULL`**. `COALESCE(SUM(estoque), 0)` é a soma, ou `0` se a soma for `NULL`:

```sql
SELECT COALESCE(SUM(estoque), 0) AS unidades,
       COALESCE(SUM(preco * estoque), 0) AS valor,
       COALESCE(ROUND(AVG(preco), 2), 0) AS preco_medio
FROM produtos
WHERE 1 = 0;
```

| `unidades` | `valor` | `preco_medio` |
|---|---|---|
| 0 | 0 | 0 |

Aproveite para trocar o `AVG(preco)` por `ROUND(AVG(preco), 2)`, como no teste de antes: o banco entrega o número já como será lido. Na rota, troque a consulta do `resumo` por esta (e a da `contagem` ganha o `COALESCE` também, porque o `SUM(ativo)` tem o mesmo problema):

```python
    contagem = execute_one(
        'SELECT COUNT(*) AS total, COALESCE(SUM(ativo), 0) AS ativos '
        'FROM produtos'
    )

    resumo = execute_one(
        'SELECT COALESCE(SUM(estoque), 0) AS unidades, '
        'COALESCE(SUM(preco * estoque), 0) AS valor, '
        'COALESCE(ROUND(AVG(preco), 2), 0) AS preco_medio '
        'FROM produtos '
        'WHERE ativo = 1'
    )
```

Salve e recarregue: os números são os mesmos de antes, porque a tabela tem produtos. A diferença é que, **vazia**, a página mostraria `0` e `R$ 0,00` em vez do erro. Acrescente a frase de ajuda abaixo do `<h2>` do resumo:

```html
    <p class="text-body-secondary">As unidades, o valor e o preço médio consideram só os produtos ativos.</p>
```

!!! note "`COUNT` não tem esse problema"
    O `COUNT(*)` de zero linhas devolve `0`, não `NULL`. Só `SUM`, `AVG`, `MIN` e `MAX` devolvem `NULL` quando não há linha nenhuma. E `AVG` e `SUM` **ignoram** as linhas em que a coluna é `NULL`: a média de `preco` não conta produto sem preço (aqui o preço é `NOT NULL`, então nenhuma é ignorada).

```bash
git add .
git commit -m "Adiciona o resumo do catálogo com SUM, AVG e COALESCE"
git push
```

---

## Tópico 5 — Produtos por categoria e estoque baixo

### Por categoria: o `GROUP BY` de novo

O resumo diz que o preço médio do catálogo é R$ 747,54, mas um notebook e um cabo HDMI não têm nada a ver um com o outro. Agrupar por categoria separa o que é comparável, e junta tudo o que você aprendeu: `GROUP BY`, `COUNT`, `SUM`, `AVG`, `ROUND` e `WHERE`. Teste no phpMyAdmin:

```sql
SELECT categoria,
       COUNT(*) AS produtos,
       SUM(estoque) AS unidades,
       SUM(preco * estoque) AS valor,
       ROUND(AVG(preco), 2) AS preco_medio
FROM produtos
WHERE ativo = 1
GROUP BY categoria
ORDER BY valor DESC;
```

| `categoria` | `produtos` | `unidades` | `valor` | `preco_medio` |
|---|---|---|---|---|
| Informática | 5 | 47 | 68183.80 | 2207.64 |
| Periféricos | 5 | 74 | 14735.40 | 303.54 |
| Áudio | 3 | 51 | 4834.00 | 176.27 |
| Acessórios | 3 | 90 | 3391.00 | 49.90 |
| Outros | 2 | 11 | 2292.10 | 476.95 |
| `NULL` | 1 | 120 | 1788.00 | 14.90 |

Uma única consulta calculou cinco números para cada categoria. O `WHERE ativo = 1` **vem antes do `GROUP BY`**: ele escolhe quais linhas entram nos grupos, e só então o banco agrupa e calcula. A categoria também é opcional, então o `NULL` forma o seu grupo, como o estado fez no Tópico 3.

!!! note "`WHERE` filtra linhas, `HAVING` filtra grupos"
    O `WHERE` age **antes** de agrupar e decide quais linhas participam. Para filtrar pelo **resultado** de um grupo (por exemplo, só as categorias com mais de 3 produtos), existe o `HAVING`, escrito depois do `GROUP BY`: `HAVING COUNT(*) > 3`. Este capítulo não precisa dele, mas é o que você procuraria ao pensar em "mostrar só os grupos que...".

Na rota, acrescente a consulta depois do `resumo` e passe o resultado ao template:

```python
    por_categoria = execute_query(
        'SELECT categoria, COUNT(*) AS produtos, SUM(estoque) AS unidades, '
        'SUM(preco * estoque) AS valor, ROUND(AVG(preco), 2) AS preco_medio '
        'FROM produtos '
        'WHERE ativo = 1 '
        'GROUP BY categoria '
        'ORDER BY valor DESC',
        fetch=True,
    )

    return render_template('relatorios/relatorio_produtos.html', titulo='Relatório de produtos',
                           contagem=contagem, resumo=resumo, por_categoria=por_categoria)
```

E, no `relatorio_produtos.html`, depois do `</section>` do resumo e antes do `{% endblock %}`:

```html
  <section class="mb-5">
    <h2 class="h4">Produtos ativos por categoria</h2>
    <p class="text-body-secondary">Ordenado pelo valor em estoque, do maior para o menor.</p>

    <table class="table table-striped table-hover">
      <thead class="table-light">
        <tr>
          <th>Categoria</th>
          <th class="text-end">Produtos</th>
          <th class="text-end">Unidades</th>
          <th class="text-end">Valor em estoque</th>
          <th class="text-end">Preço médio</th>
        </tr>
      </thead>
      <tbody>
        {% for linha in por_categoria %}
        <tr>
          <td>{{ linha.categoria|default('Sem categoria', true) }}</td>
          <td class="text-end">{{ linha.produtos }}</td>
          <td class="text-end">{{ linha.unidades }}</td>
          <td class="text-end">{{ linha.valor|moeda }}</td>
          <td class="text-end">{{ linha.preco_medio|moeda }}</td>
        </tr>
        {% else %}
        <tr>
          <td colspan="5" class="text-center text-body-secondary py-4">Nenhum produto ativo cadastrado ainda.</td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </section>
```

Salve e recarregue. Para conferir, some de cabeça (ou na calculadora) a coluna **Valor em estoque**: `68.183,80 + 14.735,40 + 4.834,00 + 3.391,00 + 2.292,10 + 1.788,00` dá **R$ 95.224,30**, o mesmo valor do resumo lá de cima. A tabela por categoria e o resumo olham para os mesmos dados de dois jeitos, e os números têm de bater.

### Estoque baixo: um limite que vai para a consulta

O último relatório é o mais útil no dia a dia: quais produtos estão acabando. O sistema já tem uma regra para isso: na lista de produtos, o selo amarelo aparece quando o estoque é **menor que 5**. O relatório usa o mesmo limite, e para não escrever o número `5` dentro do SQL (e de novo no texto da página), ele vira uma **constante**. No `app.py`, logo depois da constante `SELECT_PRODUTO`, acrescente:

```python
# Abaixo desta quantidade, o produto entra no relatório de estoque baixo (o mesmo limite do selo amarelo da lista)
LIMITE_ESTOQUE_BAIXO = 5
```

A consulta, no phpMyAdmin, com o número direto:

```sql
SELECT id_produto, nome, categoria, estoque
FROM produtos
WHERE ativo = 1 AND estoque < 5
ORDER BY estoque, nome;
```

| `id_produto` | `nome` | `categoria` | `estoque` |
|---|---|---|---|
| 5 | SSD 480 GB | Informática | 0 |
| 14 | Microfone de Mesa USB | Áudio | 1 |
| 20 | Cadeira de Escritório | Outros | 2 |
| 9 | Webcam HD 1080p | Periféricos | 2 |
| 2 | Notebook Zenith Pro | Informática | 3 |
| 8 | Mouse Gamer 7200 DPI | Periféricos | 4 |

O `ORDER BY estoque, nome` põe os mais urgentes primeiro, e o nome desempata. Repare no que **não** está na lista, e confira na tabela `produtos`: o **Hub USB 4 Portas** tem estoque 5, e `estoque < 5` não inclui o 5 (com `<=` ele entraria); o **Suporte para Notebook** tem estoque 3, mas está **inativo**, e a **Caixa de Som Bluetooth** tem estoque 0 e também está inativa. O `ativo = 1` os deixa de fora, porque produto que não está à venda não precisa de reposição.

Na rota, o limite vai por `%s`, como qualquer valor, e **não** colado no texto do SQL (a regra do projeto: o SQL é sempre parametrizado, mesmo quando o valor vem de uma constante nossa e não de um formulário). Acrescente a consulta depois da `por_categoria` e passe o resultado e o limite ao template:

```python
    estoque_baixo = execute_query(
        'SELECT id_produto, nome, categoria, estoque '
        'FROM produtos '
        'WHERE ativo = 1 AND estoque < %s '
        'ORDER BY estoque, nome',
        (LIMITE_ESTOQUE_BAIXO,),
        fetch=True,
    )

    return render_template('relatorios/relatorio_produtos.html', titulo='Relatório de produtos',
                           contagem=contagem, resumo=resumo, por_categoria=por_categoria,
                           estoque_baixo=estoque_baixo, limite=LIMITE_ESTOQUE_BAIXO)
```

Os valores de um `%s` vão em uma **tupla**, e com um valor só ela leva a vírgula no fim: `(LIMITE_ESTOQUE_BAIXO,)`. Sem a vírgula, os parênteses não formam uma tupla. Agora a seção, no `relatorio_produtos.html`, depois da seção por categoria:

```html
  <section class="mb-5">
    <h2 class="h4">Estoque baixo</h2>
    <p class="text-body-secondary">Produtos ativos com menos de {{ limite }} unidades.</p>

    <table class="table table-striped table-hover">
      <thead class="table-light">
        <tr>
          <th>Código</th>
          <th>Produto</th>
          <th>Categoria</th>
          <th>Estoque</th>
        </tr>
      </thead>
      <tbody>
        {% for produto in estoque_baixo %}
        <tr>
          <td>{{ produto.id_produto }}</td>
          <td>{{ produto.nome }}</td>
          <td>{{ produto.categoria|default('Sem categoria', true) }}</td>
          <td>
            {% if produto.estoque == 0 %}
              <span class="badge text-bg-danger">Sem estoque</span>
            {% else %}
              <span class="badge text-bg-warning">{{ produto.estoque }}</span>
            {% endif %}
          </td>
        </tr>
        {% else %}
        <tr>
          <td colspan="4" class="text-center text-body-secondary py-4">Nenhum produto com estoque baixo.</td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </section>
```

Salve e recarregue. A tabela mostra os seis produtos acima, com **Sem estoque** em vermelho para o SSD e o número do estoque em amarelo para os outros.

### O relatório acompanha o banco

Um relatório não guarda nada: a cada visita, a consulta roda de novo. Para ver isso, abra **Produtos > Novo produto** e cadastre um produto com nome `Teclado Compacto`, preço `129,90`, estoque `2` e o campo **Ativo** marcado. Volte ao relatório de produtos e recarregue:

- o resumo mostra **22** cadastrados e **20** ativos;
- o valor em estoque subiu em R$ 259,80 (`129,90 × 2`);
- o `Teclado Compacto` apareceu na tabela de estoque baixo.

Agora abra a edição desse produto e **desmarque** o campo Ativo. Recarregue o relatório: os ativos voltam a **19**, o valor em estoque volta a **R$ 95.224,30** e o produto sai do estoque baixo, enquanto os cadastrados seguem **22**. É o `WHERE ativo = 1` trabalhando.

```bash
git add .
git commit -m "Adiciona os relatórios por categoria e de estoque baixo"
git push
```

---

## 📦 Código deste capítulo

Compare com o seu projeto. O zip tem o sistema completo, com os relatórios: o `app.py`, o `db.py`, o `validacoes.py`, o `testar_conexao.py`, o `banco.sql`, o `relatorios_dados.sql`, o `.env.example`, o `.gitignore`, o `requirements.txt`, a pasta `templates` (com a subpasta `relatorios`) e a pasta `static` (com `static/uploads` vazia, só com o `.gitkeep`). O ambiente virtual e o `.env` **não** vão no zip: depois de descompactar, crie o ambiente com os comandos do início, rode `copy .env.example .env` e troque os marcadores `SUA_SENHA_AQUI` e `NOME_BANCO_DADOS` como no [Capítulo 11](Capitulo_11_Projeto_Novo_e_Banco.md#topico-4-o-arquivo-env). O banco também não vai dentro do zip: importe o `banco.sql` e, depois dele, o `relatorios_dados.sql` no phpMyAdmin.

➡️ [Baixar p2_cap_19.zip](../arquivos/p2_cap_19.zip)

---

## 🃏 Flashcards de Revisão

Tente responder mentalmente antes de abrir.

??? question "Qual é a diferença entre uma lista e um relatório?"
    A lista mostra **uma linha por registro** (quais são os usuários?). O relatório mostra **uma linha por grupo ou por resumo** (quantos usuários há por perfil?), e quem faz a conta é o banco, com `COUNT`, `SUM`, `AVG` e `GROUP BY`.

??? question "O que o `GROUP BY` faz, e o que vai no `SELECT` de uma consulta com ele?"
    Ele junta as linhas que têm o mesmo valor na coluna indicada e aplica a função (como o `COUNT`) a cada grupo. No `SELECT` só entram as colunas do `GROUP BY` e as funções de agregação.

??? question "Por que o `JOIN` comum esconde um perfil sem usuários, e como o `LEFT JOIN` resolve?"
    O `JOIN` comum só devolve as linhas que têm par nas duas tabelas. O `LEFT JOIN` devolve **todas** as linhas da tabela da esquerda (`perfis`), e as colunas da outra tabela vêm como `NULL` quando não há par.

??? question "Por que `COUNT(*)` dá 1 para um perfil sem usuários depois de um `LEFT JOIN`?"
    Porque o `COUNT(*)` conta **linhas**, e o `LEFT JOIN` devolveu uma linha para o perfil, com as colunas do usuário em `NULL`. O `COUNT(u.id_usuario)` conta só onde a coluna não é `NULL` e dá 0.

??? question "Por que usar `COALESCE` com `SUM` e `AVG`?"
    Porque, sem nenhuma linha para somar ou tirar a média, essas funções devolvem `NULL` (e não 0), e o `NULL` quebraria o filtro `moeda` com um `TypeError`. O `COALESCE(valor, 0)` devolve o primeiro valor que não é `NULL`.

??? question "Por que o formato do mês é `%Y-%m` e não `%m/%Y`?"
    Porque o resultado é um texto, e a ordem alfabética de `2026-02`, `2026-10` é a ordem do calendário. Com o mês na frente, os anos se misturariam. O filtro `mes_br` só inverte a escrita na hora de mostrar.

---

## ✅ Quiz de Fixação

<quiz>
Existe o perfil `Visitante`, sem nenhum usuário. Qual consulta o mostra no relatório, com o total 0?
- [ ] `SELECT p.nome, COUNT(*) AS total FROM usuarios u JOIN perfis p ON p.id_perfil = u.perfil_id GROUP BY p.nome`
> Não. O `JOIN` comum só devolve perfis que têm usuário, então o `Visitante` nem aparece.
- [ ] `SELECT p.nome, COUNT(*) AS total FROM perfis p LEFT JOIN usuarios u ON u.perfil_id = p.id_perfil GROUP BY p.nome`
> Não. O `Visitante` aparece, mas com total 1: o `COUNT(*)` conta a linha que o `LEFT JOIN` criou, mesmo vazia.
- [x] `SELECT p.nome, COUNT(u.id_usuario) AS total FROM perfis p LEFT JOIN usuarios u ON u.perfil_id = p.id_perfil GROUP BY p.nome`
> Correto. O `LEFT JOIN` mantém o perfil, e o `COUNT(u.id_usuario)` ignora o `NULL` da linha vazia, dando 0.
- [ ] `SELECT p.nome, COUNT(u.id_usuario) AS total FROM usuarios u LEFT JOIN perfis p ON p.id_perfil = u.perfil_id GROUP BY p.nome`
> Não. Com `usuarios` à esquerda, o `LEFT JOIN` mantém todos os usuários, e o perfil sem usuário continua de fora.
</quiz>

<quiz>
Quais afirmações sobre `SUM`, `AVG` e `COUNT` estão corretas? (selecione todas que se aplicam)
- [x] `SUM` de uma consulta que não encontra nenhuma linha devolve `NULL`
> Correto. Por isso o relatório usa `COALESCE(SUM(...), 0)`.
- [x] `COUNT(*)` de uma consulta que não encontra nenhuma linha devolve `0`
> Correto. O `COUNT` é a função que não tem o problema do `NULL`.
- [ ] `AVG(preco)` devolve sempre um número inteiro
> Não. O `AVG` devolve um decimal, em geral com várias casas, e por isso o relatório usa `ROUND(AVG(preco), 2)`.
- [x] `SUM(preco * estoque)` multiplica o preço pelo estoque de cada linha e soma os resultados
> Correto. É assim que se calcula o valor total do estoque.
</quiz>

<quiz>
Por que a consulta de cadastros por mês usa `DATE_FORMAT(criado_em, '%Y-%m')`?
- [ ] Porque o `%m/%Y` não existe no MySQL
> Não. Existe, e funciona. A questão é a ordenação.
- [x] Porque o ano antes do mês faz a ordem alfabética do texto coincidir com a ordem do calendário
> Correto. `2026-02` vem antes de `2026-10`, e um ano novo nunca se mistura com o anterior.
- [ ] Porque o `GROUP BY` só aceita datas nesse formato
> Não. O `GROUP BY` agrupa por qualquer valor. O formato foi escolhido para o `ORDER BY` e para cortar a data até o mês.
- [ ] Porque o Jinja só consegue mostrar datas em `%Y-%m`
> Não. O Jinja mostra o texto que receber, e o filtro `mes_br` o reescreve como `03/2026`.
</quiz>

<quiz>
O relatório de estoque baixo usa `WHERE ativo = 1 AND estoque < %s`. O que acontece com um produto **inativo** com estoque 3 e com um produto ativo com estoque 5 (o limite é 5)?
- [ ] Os dois aparecem
> Não. O inativo é excluído por `ativo = 1`, e o de estoque 5 é excluído por `estoque < 5`.
- [ ] Só o inativo aparece
> Não. O `ativo = 1` o deixa de fora.
- [x] Nenhum dos dois aparece
> Correto. O inativo não passa em `ativo = 1`, e o estoque 5 não é **menor** que 5.
- [ ] Só o de estoque 5 aparece
> Não. O `<` não inclui o próprio 5 (com `<=` ele entraria).
</quiz>

---

## 📝 Resumo

Um relatório é um `SELECT` que **resume** em vez de listar, e a conta fica com o banco. O `GROUP BY` forma os grupos, e o `COUNT`, o `SUM` e o `AVG` calculam o que cada grupo diz. O `JOIN` comum esconde o perfil sem usuários, o `LEFT JOIN` o devolve, e só o `COUNT(coluna)` (e não o `COUNT(*)`) conta o zero corretamente. O `NULL` aparece como grupo próprio (o usuário sem estado, o produto sem categoria), o `DATE_FORMAT` corta a data até o mês, e o `SUM` e o `AVG` de zero linhas devolvem `NULL`, que o `COALESCE` troca por 0 antes de chegar ao filtro `moeda`. O `WHERE` escolhe as linhas **antes** de agrupar, e o limite de estoque baixo vai por `%s`, como qualquer valor. As rotas continuam simples (uma consulta, um `render_template`), e a conferência mais barata de um relatório é somar os grupos e comparar com um total conhecido.

---

## 🔗 Navegação

⬅️ [Capítulo 18 — CRUD de produtos](Capitulo_18_CRUD_de_Produtos.md) · 🔒 Capítulo 20 — em breve.

---

*Fatec Jahu · ILP951 · Prof. Ronan Adriel Zenatti · 2026*
