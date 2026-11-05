# Capítulo 15 — SELECT relacional de usuário

**Disciplina:** Programação para Internet (ILP951)
**Professor:** Ronan Adriel Zenatti · ronan.zenatti@cps.sp.gov.br
**Fatec Jahu — 2º Semestre/2026**

---

## 🎯 Objetivos do Capítulo

Ao final deste capítulo você deverá ser capaz de:

- Trazer o nome do perfil com um `JOIN`, em vez de mostrar o número guardado em `perfil_id`
- Dar um apelido (`AS`) a uma coluna, para que duas colunas com o mesmo nome não se sobrescrevam no dicionário que o Python recebe
- Guardar a consulta em uma constante, `SELECT_USUARIO`, que **deixa a senha de fora**, e reaproveitá-la na lista e no detalhe
- Criar filtros Jinja próprios (`data_br`, `data_hora_br` e `cpf_oculto`) com `@app.template_filter`
- Listar os usuários em uma tabela completa, com o perfil em um **badge** colorido reaproveitado com `{% include %}` e a coluna de ações
- Criar a página de detalhe `/usuarios/<int:id_usuario>` e responder 404 quando o código não existe

O Capítulo 14 terminou com a página `/usuarios` **provisória**: um aviso azul e nenhuma consulta ao banco. Quem cadastrava um usuário só conferia o resultado no phpMyAdmin. Este capítulo troca o aviso pela lista de verdade e acrescenta a página de detalhe. É também a primeira consulta do projeto que **junta duas tabelas**: o usuário guarda só o número do perfil, e o nome do perfil mora em outra tabela. A ordem é: primeiro a consulta e as ferramentas de exibição (os filtros), depois as telas, cada uma escrita de uma vez. A edição e a exclusão de usuários ficam para o Capítulo 16.

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

## Tópico 1 — A consulta com JOIN

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

O Bruno é o usuário **completo**, e a Ana e a Carla têm os campos opcionais em `NULL`. A diferença entre eles vai aparecer nas telas.

### O mapa do recurso

O molde de nomes do Capítulo 12 vale para `usuarios`. Este capítulo constrói a lista e o detalhe:

| Rota | Métodos | O que faz | Função no `app.py` | Template | Capítulo |
|---|---|---|---|---|---|
| `/usuarios` | GET | Lista os usuários | `listar_usuarios` | `usuarios/usuarios_lista.html` | **15** |
| `/usuarios/inserir` | GET e POST | GET mostra o formulário, POST confere e grava | `inserir_usuario` | `usuarios/usuario_form.html` | 14 |
| `/usuarios/<int:id_usuario>` | GET | Detalhe de um usuário | `usuario_detalhe` | `usuarios/usuario_detalhe.html` | **15** |
| `/usuarios/<int:id_usuario>/editar` | GET e POST | Edita o usuário | `usuario_editar` | `usuarios/usuario_form.html` | 16 |
| `/usuarios/<int:id_usuario>/excluir` | só POST | Exclui o usuário | `usuario_excluir` | (nenhum) | 16 |

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

Uma lista que mostrasse só a tabela `usuarios` teria, na coluna do perfil, `1`, `2` e `3`, e ninguém lê uma lista de usuários querendo saber que a Ana é o perfil número 1. O `JOIN` **junta as linhas das duas tabelas** que têm o mesmo valor na chave: a linha do usuário cujo `perfil_id` vale 2 é emparelhada com a linha do perfil cujo `id_perfil` vale 2. Teste no **phpMyAdmin** (banco `gestao`, aba **SQL**) antes de levar a consulta para o Python:

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

Quatro detalhes da consulta, os três primeiros você já viu no curso de banco de dados:

- O `u` e o `p` depois dos nomes das tabelas são **apelidos**, para escrever `u.nome` em vez de `usuarios.nome`.
- O `ON` diz **quais colunas** devem ser iguais.
- O `JOIN` sozinho é o `INNER JOIN`: só entram usuários que têm um perfil, e todos têm, porque `perfil_id` é `NOT NULL` e a chave estrangeira não deixa gravar um perfil que não existe.
- **O `AS perfil` é obrigatório no Python.** As duas tabelas têm uma coluna `nome`. No phpMyAdmin isso não atrapalha, mas no Python cada linha do resultado vira um **dicionário**, e um dicionário **não aceita a mesma chave duas vezes**: sem o apelido, a segunda `nome` (a do perfil) sobrescreveria a primeira, e os nomes das pessoas sumiriam da lista, trocados por `Administrador`, `Gerente` e `Usuário`. O `AS perfil` dá à coluna do perfil uma chave própria: `usuario.perfil`.

### Uma constante para a consulta

A lista e a página de detalhe deste capítulo, e a edição do Capítulo 16, precisam **das mesmas colunas**, com o mesmo `JOIN`. Escrever essa consulta comprida em cada rota é pedir para uma delas ficar diferente das outras. Por isso ela é escrita **uma vez só**, em uma constante no topo do `app.py`. Coloque-a logo depois da linha `CSRFProtect(app)`:

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

A consulta traz todas as colunas de que as telas vão precisar, as do usuário e duas do perfil: o nome (`AS perfil`) e a descrição (`AS perfil_descricao`, também com apelido, pelo mesmo motivo). Ela não tem `WHERE` nem `ORDER BY`: cada rota acrescenta o que precisa.

!!! note "Python: uma constante, e o `+` entre textos"
    Por convenção, uma variável que **não muda** é escrita em MAIÚSCULAS: `SELECT_USUARIO` é um texto que o programa só lê, como a lista `UFS` do Capítulo 14. Os parênteses permitem quebrar o texto em várias linhas, e os pedaços colados, um embaixo do outro, viram **um único texto** (o mesmo recurso do `INSERT` do Capítulo 14). Para acrescentar uma cláusula à consulta, o `+` junta dois textos: `SELECT_USUARIO + ' ORDER BY u.nome'`. Juntar **textos fixos** é seguro. O que nunca se faz é juntar ao SQL o que a pessoa digitou: para isso existem os `%s`, como no resto do projeto.

!!! note "A senha não está na consulta, e é de propósito"
    Repare no que **falta** no `SELECT_USUARIO`: a coluna `senha`. Nenhuma tela do sistema precisa do hash, e o que não é lido do banco não tem como vazar para a página, nem por um descuido em um template. É por isso que o `SELECT *` não é usado nas telas de usuário: ele traria a senha junto. Só o login, no Capítulo 17, vai ler o hash, em uma consulta própria.

### A rota da lista

Agora a rota `listar_usuarios` deixa de ser provisória. Troque-a por esta:

```python
@app.route('/usuarios')
def listar_usuarios():
    # O SELECT_USUARIO já traz o nome do perfil, pelo JOIN
    usuarios = execute_query(SELECT_USUARIO + ' ORDER BY u.nome', fetch=True)

    return render_template('usuarios/usuarios_lista.html', titulo='Usuários', usuarios=usuarios)
```

É o mesmo desenho da `listar_perfis` do Capítulo 12: o `execute_query` com `fetch=True` devolve a lista de linhas, cada uma como um dicionário. A lista ainda mostra o aviso azul, porque o template não mudou: ele é reescrito no Tópico 3, depois que os filtros existirem.

```bash
git add .
git commit -m "Cria o SELECT_USUARIO com JOIN e a consulta da lista de usuários"
git push
```

---

## Tópico 2 — Filtros próprios para a tela

### O que o banco entrega e o que a tela precisa

Três colunas da lista não podem ir para a tela do jeito que o banco as entrega:

| Coluna | O que o banco entrega | O que a tela precisa |
|---|---|---|
| Data de nascimento | Um objeto de data, que o Jinja escreve como `1988-03-14` | `14/03/1988`, e um traço quando a data é `NULL` |
| Cadastro e alteração | Data e hora, `2026-11-03 10:15:42` | `03/11/2026 às 10:15` |
| CPF | O número inteiro, `529.982.247-25` | Na lista, só o meio (`***.982.247-**`) |

O Capítulo 12 formatou o `criado_em` dos perfis direto no template, com o `strftime`, e funcionou porque o `criado_em` nunca é `NULL`. A data de nascimento é opcional: na Ana, ela é `None`, e o `None` não tem o método `strftime`. O template quebraria com `'None' has no attribute 'strftime'`, e seria preciso um `{% if %}` em volta de **cada** data de **cada** tela.

O Flask oferece um jeito melhor: um **filtro próprio**, uma função Python que o template chama com o mesmo `|` dos filtros que você já conhece (o `|upper`, o `|round` do Capítulo 5). A função trata o `None` **uma vez**, e todas as telas se beneficiam.

### Os três filtros

No `app.py`, crie uma seção nova, **FILTROS DO JINJA**, logo depois da constante `SELECT_USUARIO` e antes da seção das páginas principais:

```python
# ==============================================================================
# FILTROS DO JINJA
# ==============================================================================

@app.template_filter('data_br')
def data_br(valor):
    # date ou datetime vira 14/03/1988; um campo vazio vira um traço
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
    # 529.982.247-25 vira ***.982.247-**: a lista mostra só o meio do CPF
    if cpf is None:
        return '—'

    return '***.' + cpf[4:11] + '-**'
```

!!! note "Flask: `@app.template_filter`"
    É um decorador, como o `@app.route` ([Capítulo 3](Capitulo_03_Flask.md)) e o `@app.errorhandler` ([Capítulo 6](Capitulo_06_Heranca_Include_e_Paginas_de_Erro.md)). O `@app.route` liga uma função a um **endereço**. O `@app.template_filter('data_br')` liga uma função a um **nome de filtro**: a partir daí, o template pode escrever `{{ algo|data_br }}`, e o Jinja chama a função, entregando `algo` no parâmetro `valor` e escrevendo o que ela devolve com `return`. O dado original **não muda**, só a exibição. O nome entre aspas é o que se escreve depois do `|`; o nome da função é livre (aqui são iguais, para não confundir).

Filtro por filtro:

- **`data_br`** usa o mesmo `strftime` do [Capítulo 12](Capitulo_12_INSERT_e_SELECT_de_Perfis.md#a-tabela-com-todas-as-colunas), com o modelo do dia, do mês e do ano. Funciona com `date` (a data de nascimento) e com `datetime` (o `criado_em`), porque os dois têm o `strftime`.
- **`data_hora_br`** acrescenta a hora e os minutos (`%H:%M`), para o cadastro e a alteração. A hora que aparece é a de Brasília: o `time_zone` do `db.py` (Capítulo 10) faz o banco e o Python concordarem, em qualquer computador.
- **`cpf_oculto`**: o CPF é um **dado pessoal**, protegido pela LGPD (a lei de proteção de dados), e uma lista que o mostra inteiro para todo mundo expõe mais do que precisa: para escolher em quem clicar, ninguém precisa do número completo. O CPF é gravado como `000.000.000-00` (Capítulo 14), e é isso que a função recebe. Conte as posições, a partir do zero, como nas fatias do [Capítulo 14](Capitulo_14_INSERT_Relacional_de_Usuario.md#as-funcoes-de-apoio): em `529.982.247-25`, o trecho `982.247`, o do meio, ocupa as posições de **4 até antes da 11**, e a fatia `cpf[4:11]` o devolve. O `+` junta os três pedaços. O CPF **inteiro** aparece só na página de detalhe, que se abre por escolha de quem a procura.

Os três começam com `if ... is None: return '—'`: um campo vazio vira um traço, sem erro.

```bash
git add .
git commit -m "Cria os filtros data_br, data_hora_br e cpf_oculto"
git push
```

---

## Tópico 3 — A lista de usuários

### O badge do perfil, em um arquivo próprio

Na lista, o perfil aparece em um **badge**, a etiqueta colorida do Bootstrap (`<span class="badge ...">`). Com ele, o perfil se reconhece de relance, sem ler. Quem decide a cor é um `if/elif/else`, o mesmo do Capítulo 5, que decidia a faixa de preço de um produto. O badge vai aparecer em **duas** páginas, a lista e o detalhe, e por isso ele nasce em um arquivo próprio, para ser **incluído** nas duas com o `{% include %}` do [Capítulo 6](Capitulo_06_Heranca_Include_e_Paginas_de_Erro.md): se uma cor mudar, ou um perfil novo ganhar a sua, há um só lugar para mexer. Crie o `templates/usuarios/_badge_perfil.html`:

```html
{% if usuario.perfil == 'Administrador' %}
  <span class="badge text-bg-danger">Administrador</span>
{% elif usuario.perfil == 'Gerente' %}
  <span class="badge text-bg-warning">Gerente</span>
{% else %}
  <span class="badge text-bg-secondary">{{ usuario.perfil }}</span>
{% endif %}
```

O `text-bg-danger`, o `text-bg-warning` e o `text-bg-secondary` são classes do Bootstrap que escolhem a cor do fundo **e** uma cor de letra que combina com ela: vermelho para o Administrador, amarelo para o Gerente e cinza para os demais. O `_` no começo do nome é uma convenção para dizer "este arquivo não é uma página, é um pedaço que entra em outras".

!!! note "O `else` cobre os perfis que você ainda não conhece"
    O `if` compara o **nome** do perfil, escrito exatamente como foi cadastrado. Um perfil novo (digamos, **Financeiro**) não cai em nenhum `if` nem `elif`, e o `else` o mostra com o badge cinza e o próprio nome, sem quebrar nada. O mesmo acontece se o perfil do administrador tiver sido cadastrado com outra grafia, como `Admin`: ele aparece em cinza, e não em vermelho.

### A tabela, com todas as colunas

Troque o `templates/usuarios/usuarios_lista.html` **inteiro** por esta versão (o aviso azul sai, e a tabela entra no lugar):

```html
{% extends 'layout/base_menu.html' %}

{% block titulo_aba %}{{ titulo }} — Sistema de Gestão{% endblock %}

{% block conteudo %}
  <div class="d-flex justify-content-between align-items-center mb-3">
    <h1 class="h2 mb-0">{{ titulo }}</h1>
    <a href="{{ url_for('inserir_usuario') }}" class="btn btn-primary">Novo usuário</a>
  </div>

  <table class="table table-striped table-hover align-middle">
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
        <td>{{ usuario.cidade if usuario.cidade else '—' }}{% if usuario.estado %}/{{ usuario.estado }}{% endif %}</td>
        <td>{{ usuario.data_nascimento|data_br }}</td>
        <td>{% include 'usuarios/_badge_perfil.html' %}</td>
        <td class="text-end text-nowrap">
          <a href="{{ url_for('usuario_detalhe', id_usuario=usuario.id_usuario) }}" class="btn btn-sm btn-info" title="Ver detalhes"><i class="bi bi-eye"></i></a>
          <a href="#" class="btn btn-sm btn-warning" title="Editar"><i class="bi bi-pencil-square"></i></a>
          <button type="button" class="btn btn-sm btn-danger" title="Excluir"><i class="bi bi-trash"></i></button>
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

É o molde da `perfis_lista.html`: um `{% for %}` com o `{% else %}` para a lista vazia e o `colspan` com o número de colunas (7). Coluna por coluna:

- **Nome**, com o e-mail em letra pequena embaixo (`<small>`).
- **CPF**, com o filtro `cpf_oculto`.
- **Cidade**, com o `if` em uma linha do Capítulo 12 para o traço, e o estado depois da barra só quando existe: o `{% if usuario.estado %}` trata o `None` como falso.
- **Nascimento**, com o filtro `data_br`.
- **Perfil**, com o badge incluído. O arquivo incluído enxerga a variável `usuario` de cada volta do `for`, e é por isso que o badge usa o nome `usuario`.
- **Ações**, com três botões. O **azul-claro** (`btn-info`, ícone de olho) abre a página de detalhe, que o Tópico 4 cria. O `url_for` recebe o nome da **função** da rota e o argumento que preenche o `<int:id_usuario>`: gera `/usuarios/1`, `/usuarios/2` e assim por diante. O **amarelo** e o **vermelho** são os de editar e excluir, como na lista de perfis, e ainda **não fazem nada**: eles ganham as rotas no Capítulo 16.

O botão de olho usa a rota `usuario_detalhe`, que ainda não existe, e o `url_for` quebraria a página. Por isso a lista só é testada depois do Tópico 4: salve o arquivo, mas não recarregue a lista ainda, e siga para o detalhe.

---

## Tópico 4 — A página de detalhe

### A rota

A lista mostra o essencial de todos. O **detalhe** mostra tudo sobre **um** usuário, em um endereço próprio (`/usuarios/2`), que dá para guardar e compartilhar. Os ingredientes você já tem: a variável de rota `<int:id_usuario>` e o `abort(404)` do [Capítulo 13](Capitulo_13_UPDATE_e_DELETE_de_Perfis.md), e o `execute_one`. No `app.py`, acrescente a rota **depois** da `inserir_usuario`:

```python
@app.route('/usuarios/<int:id_usuario>')
def usuario_detalhe(id_usuario):
    usuario = execute_one(SELECT_USUARIO + ' WHERE u.id_usuario = %s', (id_usuario,))

    if usuario is None:
        abort(404)

    return render_template('usuarios/usuario_detalhe.html', usuario=usuario)
```

A rota **reaproveita** o `SELECT_USUARIO`: o mesmo `JOIN`, as mesmas colunas e, de novo, nenhuma senha. O `WHERE` leva um `%s`, e o código vem na tupla `(id_usuario,)`. O `if usuario is None: abort(404)` é o mesmo da `perfil_editar`: um código que não existe é um pedido por algo que não está lá, e o certo é responder **404**. Sem ele, o template tentaria ler os campos de um usuário que não existe, e a página quebraria com o erro 500.

### O template

Crie o `templates/usuarios/usuario_detalhe.html`:

```html
{% extends 'layout/base_menu.html' %}

{% block titulo_aba %}{{ usuario.nome }} — Sistema de Gestão{% endblock %}

{% block conteudo %}
  <div class="d-flex justify-content-between align-items-center mb-3">
    <h1 class="h2 mb-0">{{ usuario.nome }}</h1>
    <a href="{{ url_for('listar_usuarios') }}" class="btn btn-outline-secondary">Voltar à lista</a>
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
              {% include 'usuarios/_badge_perfil.html' %}
              <span class="text-body-secondary">{{ usuario.perfil_descricao or '' }}</span>
            </dd>

            <dt class="col-sm-4">Celular</dt>
            <dd class="col-sm-8">{{ usuario.celular if usuario.celular else '—' }}</dd>
          </dl>

          <h2 class="h5 mb-3">Dados pessoais</h2>
          <dl class="row">
            <dt class="col-sm-4">Data de nascimento</dt>
            <dd class="col-sm-8">{{ usuario.data_nascimento|data_br }}</dd>

            <dt class="col-sm-4">CPF</dt>
            <dd class="col-sm-8">{{ usuario.cpf if usuario.cpf else '—' }}</dd>
          </dl>

          <h2 class="h5 mb-3">Endereço</h2>
          <dl class="row">
            <dt class="col-sm-4">CEP</dt>
            <dd class="col-sm-8">{{ usuario.cep if usuario.cep else '—' }}</dd>

            <dt class="col-sm-4">Endereço</dt>
            <dd class="col-sm-8">{{ usuario.endereco if usuario.endereco else '—' }}</dd>

            <dt class="col-sm-4">Número</dt>
            <dd class="col-sm-8">{{ usuario.numero if usuario.numero else '—' }}</dd>

            <dt class="col-sm-4">Complemento</dt>
            <dd class="col-sm-8">{{ usuario.complemento if usuario.complemento else '—' }}</dd>

            <dt class="col-sm-4">Cidade</dt>
            <dd class="col-sm-8">{{ usuario.cidade if usuario.cidade else '—' }}</dd>

            <dt class="col-sm-4">Estado</dt>
            <dd class="col-sm-8">{{ usuario.estado if usuario.estado else '—' }}</dd>
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

A página é um **cartão** com quatro blocos. Cada dado fica em uma linha de uma **lista de descrição** (`<dl>`), em que o `<dt>` é o rótulo e o `<dd>` é o valor. O `row` e o `col-sm-4`/`col-sm-8` do Bootstrap alinham os dois lado a lado. O que cada bloco usa:

- **O perfil** mostra o badge (o mesmo `include` da lista: aqui, a variável `usuario` é a que a rota entregou) **e a descrição do perfil**, que veio do `JOIN` (`p.descricao AS perfil_descricao`). A descrição pode ser `NULL`, e o `or ''` do Capítulo 12 a deixa em branco.
- **Os opcionais** (celular, CPF, CEP, endereço...) usam o `if` em uma linha: o valor quando existe, um traço quando é `NULL`.
- **O CPF aparece inteiro**, sem o `cpf_oculto`: quem chegou ao detalhe escolheu ver aquele usuário.
- **As datas** usam os filtros: `data_br` no nascimento e `data_hora_br` no cadastro e na última alteração.

Em nenhum lugar aparece a senha: ela nem foi lida do banco.

### O menu continua aceso

No detalhe, o menu **Usuários** precisa continuar aceso, como nas outras páginas de usuários. No `base_menu.html`, procure o botão do menu suspenso **Usuários** e acrescente a nova página à lista do `request.endpoint`. Troque só o trecho do `{% if %}`:

```html
{% if request.endpoint in ['listar_usuarios', 'inserir_usuario'] %}active{% endif %}
```

por:

```html
{% if request.endpoint in ['listar_usuarios', 'inserir_usuario', 'usuario_detalhe'] %}active{% endif %}
```

### Testando a lista e o detalhe

Salve tudo e abra **http://127.0.0.1:5000/usuarios**:

1. **A lista**: o Bruno mostra `***.982.247-**`, `Jaú/SP`, `14/03/1988` e um badge **amarelo**; a Ana, um badge **vermelho**; a Carla, um **cinza**. Os campos vazios da Ana e da Carla mostram `—`, e não `None`. Nenhuma data no formato do banco, nenhum CPF exposto.
2. **O detalhe**: clique no botão de olho do Bruno. O CPF aparece inteiro, `529.982.247-25`, o celular formatado, o complemento (que ele não preencheu) como `—`, e o registro com data e hora, algo como `03/11/2026 às 10:15`. Volte e abra o detalhe da Ana: seis traços no endereço e, ao lado do badge, a descrição do perfil Administrador. O menu **Usuários** continua aceso.
3. **Os botões amarelo e vermelho** não fazem nada, por enquanto.
4. **Um código que não existe**: abra **http://127.0.0.1:5000/usuarios/99999**: a página 404 do projeto. O endereço `/usuarios/abc` também responde 404, sem chegar à função: o `<int:id_usuario>` só aceita número.
5. **O caminho completo**: **Novo usuário**, cadastre um, e o redirect já cai na lista de verdade, com a faixa verde.

| Situação | Quem trata | O que a pessoa vê |
|---|---|---|
| Usuário sem CPF, sem nascimento ou sem cidade | Filtros `cpf_oculto` e `data_br` e o `if` em uma linha | Um traço (`—`) |
| Perfil que não é Administrador nem Gerente | O `else` do `_badge_perfil.html` | Badge cinza com o nome do perfil |
| Código de usuário que não existe | `SELECT` + `abort(404)` | A página 404 |
| Endereço com letras (`/usuarios/abc`) | O `<int:id_usuario>` | A página 404 |

```bash
git add .
git commit -m "Adiciona a lista de usuários com badge e a página de detalhe"
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
from werkzeug.security import generate_password_hash

from db import execute_insert, execute_one, execute_query
from validacoes.validacoes_perfil import validar_perfil
from validacoes.validacoes_usuario import UFS, formatar_cep, formatar_celular, formatar_cpf, validar_usuario

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Liga a proteção CSRF: todo formulário POST do sistema vai precisar do token
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


# ==============================================================================
# FILTROS DO JINJA
# ==============================================================================

@app.template_filter('data_br')
def data_br(valor):
    # date ou datetime vira 14/03/1988; um campo vazio vira um traço
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
    # 529.982.247-25 vira ***.982.247-**: a lista mostra só o meio do CPF
    if cpf is None:
        return '—'

    return '***.' + cpf[4:11] + '-**'


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
    perfis = execute_one('SELECT COUNT(*) AS total FROM perfis')
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
    # Busca a lista de perfis na tabela do banco
    perfis = execute_query(
        'SELECT id_perfil, nome, descricao, criado_em FROM perfis ORDER BY nome',
        fetch=True,
    )

    return render_template('perfis/perfis_lista.html', titulo='Perfis', perfis=perfis)


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
    # Busca o perfil pelo código que veio no endereço
    perfil = execute_one(
        'SELECT id_perfil, nome, descricao FROM perfis WHERE id_perfil = %s',
        (id_perfil,),
    )

    # Código que não existe: mostra a página 404
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
    # Busca o perfil: confirma que ele existe e traz o nome para a mensagem
    perfil = execute_one(
        'SELECT id_perfil, nome FROM perfis WHERE id_perfil = %s',
        (id_perfil,),
    )

    # Código que não existe: mostra a página 404
    if perfil is None:
        abort(404)

    # Conta os usuários do perfil: um perfil em uso não pode ser excluído
    usuarios = execute_one(
        'SELECT COUNT(*) AS total FROM usuarios WHERE perfil_id = %s',
        (id_perfil,),
    )

    if usuarios['total'] > 0:
        flash(f'O perfil "{perfil["nome"]}" tem {usuarios["total"]} usuário(s) e não pode ser excluído.', 'danger')
        return redirect(url_for('listar_perfis'))

    try:
        # O WHERE garante que só este perfil seja excluído
        execute_query('DELETE FROM perfis WHERE id_perfil = %s', (id_perfil,))
        flash(f'Perfil "{perfil["nome"]}" excluído.', 'success')

    # Trata concorrência (um usuário cadastrado no perfil entre a contagem e o DELETE)
    except Error as erro:
        if erro.errno == 1451:
            flash(f'O perfil "{perfil["nome"]}" está em uso e não pode ser excluído.', 'danger')
        else:
            raise

    return redirect(url_for('listar_perfis'))


# ==============================================================================
# USUÁRIOS
# ==============================================================================

@app.route('/usuarios')
def listar_usuarios():
    # O SELECT_USUARIO já traz o nome do perfil, pelo JOIN
    usuarios = execute_query(SELECT_USUARIO + ' ORDER BY u.nome', fetch=True)

    return render_template('usuarios/usuarios_lista.html', titulo='Usuários', usuarios=usuarios)


@app.route('/usuarios/inserir', methods=['GET', 'POST'])
def inserir_usuario():
    # Com muitos campos, o formulário inteiro fica em um dicionário (vazio no GET)
    dados = {}

    if request.method == 'POST':
        # 1. Coleta os dados do formulário (os opcionais com 'or None')
        dados = {
            'nome': request.form.get('nome', '').strip(),
            'email': request.form.get('email', '').strip().lower(),
            'senha': request.form.get('senha', ''),  # a senha não leva strip: espaço pode fazer parte dela
            'confirmacao': request.form.get('confirmacao', ''),
            'perfil_id': request.form.get('perfil_id', ''),
            'celular': request.form.get('celular', '').strip() or None,
            'data_nascimento': request.form.get('data_nascimento', '').strip() or None,
            'cpf': request.form.get('cpf', '').strip() or None,
            'cep': request.form.get('cep', '').strip() or None,
            'endereco': request.form.get('endereco', '').strip() or None,
            'numero': request.form.get('numero', '').strip() or None,
            'complemento': request.form.get('complemento', '').strip() or None,
            'cidade': request.form.get('cidade', '').strip() or None,
            'estado': request.form.get('estado', '') or None,
        }

        # 2. A validação recebe o dicionário inteiro
        erros = validar_usuario(dados)

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
                        dados['nome'],
                        dados['email'],
                        generate_password_hash(dados['senha']),  # grava o hash, nunca a senha
                        formatar_celular(dados['celular']),      # celular, CPF e CEP vão formatados
                        dados['data_nascimento'],
                        formatar_cpf(dados['cpf']),
                        dados['perfil_id'],
                        formatar_cep(dados['cep']),
                        dados['endereco'],
                        dados['numero'],
                        dados['complemento'],
                        dados['cidade'],
                        dados['estado'],
                    ),
                )

                flash(f'Usuário "{dados["nome"]}" cadastrado (código {novo_id}).', 'success')
                return redirect(url_for('listar_usuarios'))

            # Duas colunas UNIQUE: o 1062 pode ser do e-mail ou do CPF
            except Error as erro:
                if erro.errno == 1062:
                    flash('Já existe um usuário com este e-mail ou este CPF.', 'danger')
                else:
                    raise

    # As opções do <select> de perfil vêm da tabela perfis
    perfis = execute_query('SELECT id_perfil, nome FROM perfis ORDER BY nome', fetch=True)

    return render_template('usuarios/usuario_form.html', dados=dados, perfis=perfis, ufs=UFS)


@app.route('/usuarios/<int:id_usuario>')
def usuario_detalhe(id_usuario):
    usuario = execute_one(SELECT_USUARIO + ' WHERE u.id_usuario = %s', (id_usuario,))

    if usuario is None:
        abort(404)

    return render_template('usuarios/usuario_detalhe.html', usuario=usuario)


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

O `templates/usuarios/usuarios_lista.html`:

```html
{% extends 'layout/base_menu.html' %}

{% block titulo_aba %}{{ titulo }} — Sistema de Gestão{% endblock %}

{% block conteudo %}
  <div class="d-flex justify-content-between align-items-center mb-3">
    <h1 class="h2 mb-0">{{ titulo }}</h1>
    <a href="{{ url_for('inserir_usuario') }}" class="btn btn-primary">Novo usuário</a>
  </div>

  <table class="table table-striped table-hover align-middle">
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
        <td>{{ usuario.cidade if usuario.cidade else '—' }}{% if usuario.estado %}/{{ usuario.estado }}{% endif %}</td>
        <td>{{ usuario.data_nascimento|data_br }}</td>
        <td>{% include 'usuarios/_badge_perfil.html' %}</td>
        <td class="text-end text-nowrap">
          <a href="{{ url_for('usuario_detalhe', id_usuario=usuario.id_usuario) }}" class="btn btn-sm btn-info" title="Ver detalhes"><i class="bi bi-eye"></i></a>
          <a href="#" class="btn btn-sm btn-warning" title="Editar"><i class="bi bi-pencil-square"></i></a>
          <button type="button" class="btn btn-sm btn-danger" title="Excluir"><i class="bi bi-trash"></i></button>
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

O `templates/usuarios/usuario_detalhe.html`:

```html
{% extends 'layout/base_menu.html' %}

{% block titulo_aba %}{{ usuario.nome }} — Sistema de Gestão{% endblock %}

{% block conteudo %}
  <div class="d-flex justify-content-between align-items-center mb-3">
    <h1 class="h2 mb-0">{{ usuario.nome }}</h1>
    <a href="{{ url_for('listar_usuarios') }}" class="btn btn-outline-secondary">Voltar à lista</a>
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
              {% include 'usuarios/_badge_perfil.html' %}
              <span class="text-body-secondary">{{ usuario.perfil_descricao or '' }}</span>
            </dd>

            <dt class="col-sm-4">Celular</dt>
            <dd class="col-sm-8">{{ usuario.celular if usuario.celular else '—' }}</dd>
          </dl>

          <h2 class="h5 mb-3">Dados pessoais</h2>
          <dl class="row">
            <dt class="col-sm-4">Data de nascimento</dt>
            <dd class="col-sm-8">{{ usuario.data_nascimento|data_br }}</dd>

            <dt class="col-sm-4">CPF</dt>
            <dd class="col-sm-8">{{ usuario.cpf if usuario.cpf else '—' }}</dd>
          </dl>

          <h2 class="h5 mb-3">Endereço</h2>
          <dl class="row">
            <dt class="col-sm-4">CEP</dt>
            <dd class="col-sm-8">{{ usuario.cep if usuario.cep else '—' }}</dd>

            <dt class="col-sm-4">Endereço</dt>
            <dd class="col-sm-8">{{ usuario.endereco if usuario.endereco else '—' }}</dd>

            <dt class="col-sm-4">Número</dt>
            <dd class="col-sm-8">{{ usuario.numero if usuario.numero else '—' }}</dd>

            <dt class="col-sm-4">Complemento</dt>
            <dd class="col-sm-8">{{ usuario.complemento if usuario.complemento else '—' }}</dd>

            <dt class="col-sm-4">Cidade</dt>
            <dd class="col-sm-8">{{ usuario.cidade if usuario.cidade else '—' }}</dd>

            <dt class="col-sm-4">Estado</dt>
            <dd class="col-sm-8">{{ usuario.estado if usuario.estado else '—' }}</dd>
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

O `templates/usuarios/_badge_perfil.html`:

```html
{% if usuario.perfil == 'Administrador' %}
  <span class="badge text-bg-danger">Administrador</span>
{% elif usuario.perfil == 'Gerente' %}
  <span class="badge text-bg-warning">Gerente</span>
{% else %}
  <span class="badge text-bg-secondary">{{ usuario.perfil }}</span>
{% endif %}
```

No `base_menu.html`, a única mudança é o `usuario_detalhe` na lista do menu **Usuários**. Os demais arquivos (`db.py`, a pasta `validacoes`, `login.html`, `dashboard.html`, `perfil_form.html`, `usuario_form.html`, `404.html`, `500.html`, `estilo.css`, `testar_conexao.py`) são os do Capítulo 14.

---

## 📦 Código deste capítulo

Compare com o seu projeto, ou use como ponto de partida do próximo capítulo. O zip tem o `app.py`, o `db.py`, a pasta `validacoes`, o `testar_conexao.py`, o `banco.sql`, o `.env.example`, o `.gitignore`, o `requirements.txt`, a pasta `templates` (`layout/base_menu.html`, `layout/base_limpa.html`, `login.html`, `dashboard.html`, `perfis/perfis_lista.html`, `perfis/perfil_form.html`, `usuarios/usuarios_lista.html`, `usuarios/usuario_form.html`, `usuarios/usuario_detalhe.html`, `usuarios/_badge_perfil.html`, `404.html` e `500.html`) e a pasta `static` (`estilo.css`). O ambiente virtual e o `.env` **não** vão no zip: depois de descompactar, crie o ambiente com os três comandos do Capítulo 3 e rode `copy .env.example .env`, trocando os marcadores `SUA_SENHA_AQUI` e `NOME_BANCO_DADOS` como no Capítulo 11. O banco também não vai dentro do zip: importe o `banco.sql`, cadastre os três perfis e alguns usuários pelo formulário.

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

??? question "Como o detalhe mostra um traço nos campos opcionais vazios?"
    Com o `if` em uma linha do Capítulo 12: `{{ usuario.cep if usuario.cep else '—' }}`. O `NULL` do banco chega como `None`, que conta como falso, e aparece o traço. Nas datas e no CPF da lista, quem faz isso são os filtros próprios, que começam com `if valor is None: return '—'`.

??? question "Por que o CPF aparece mascarado na lista e inteiro no detalhe?"
    Porque o CPF é um dado pessoal (LGPD), e a lista é vista por quem só quer escolher um usuário: para isso o número completo não faz falta. O detalhe é aberto por quem escolheu ver aquele usuário, e mostra o CPF inteiro. O filtro `cpf_oculto` esconde as pontas, com `'***.' + cpf[4:11] + '-**'`.

---

## ✅ Quiz de Fixação

<quiz>
Uma lista que lesse só a tabela `usuarios` mostraria `1`, `2` e `3` na coluna do perfil. O que traz o nome do perfil?
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
Num `JOIN` sem o `AS perfil`, os nomes das pessoas sumiriam e a coluna **Nome** passaria a mostrar `Administrador`, `Gerente` e `Usuário`. Por quê?
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
Se a célula da cidade fosse escrita só como `{{ usuario.cidade }}`, a Ana, que não tem cidade, mostraria a palavra `None`. Qual destas células mostra um traço no lugar?
- [ ] `{{ usuario.cidade|upper }}`
> Não. O `upper` põe o texto em maiúsculas e não trata valor vazio: mostraria `NONE`.
- [x] `{{ usuario.cidade if usuario.cidade else '—' }}`
> Correto. É o `if` em uma linha do Capítulo 12: o `None` conta como falso, e aparece o traço.
- [ ] `{{ usuario.cidade|data_br }}`
> Não. O `data_br` é para datas: com um texto, ele tentaria chamar o `strftime` e quebraria a página.
- [ ] Nenhuma: o navegador mostra o `None` e não tem como mudar
> Não. O texto vem do servidor, e o template decide o que escrever.
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

A lista de usuários lê o banco com um `JOIN`, que traz o nome do perfil, e o `AS` evita que duas colunas `nome` se sobrescrevam no dicionário. Os filtros `data_br`, `data_hora_br` e `cpf_oculto`, registrados com `@app.template_filter`, escrevem as datas à brasileira, mostram o mínimo do CPF na lista e tratam o `NULL` em um lugar só. A constante `SELECT_USUARIO` guarda a consulta para a lista e o detalhe, e deixa a senha de fora de propósito. O badge do perfil fica em um arquivo incluído na lista e no detalhe, os campos vazios viram um traço com o `if` em uma linha, e o `abort(404)` responde corretamente a um código que não existe. A coluna de ações já tem os botões de editar e excluir, que o Capítulo 16 liga às suas rotas.

---

## 🔗 Navegação

⬅️ [Capítulo 14 — INSERT relacional de usuário](Capitulo_14_INSERT_Relacional_de_Usuario.md) · ➡️ [Capítulo 16 — UPDATE e DELETE de usuário](Capitulo_16_UPDATE_e_DELETE_de_Usuario.md)

---

*Fatec Jahu · ILP951 · Prof. Ronan Adriel Zenatti · 2026*
