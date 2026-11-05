# Capítulo 16 — UPDATE e DELETE de usuário

**Disciplina:** Programação para Internet (ILP951)
**Professor:** Ronan Adriel Zenatti · ronan.zenatti@cps.sp.gov.br
**Fatec Jahu — 2º Semestre/2026**

---

## 🎯 Objetivos do Capítulo

Ao final deste capítulo você deverá ser capaz de:

- Abrir o formulário de usuário já preenchido com a linha do banco, e reaproveitá-lo nos dois modos (`'criar'` e `'editar'`) com a variável `acao`
- Adaptar a validação do usuário para ignorar o próprio registro na conferência de e-mail e CPF, com `id_usuario <> %s`
- Tornar a senha opcional na edição: em branco mantém o hash atual, preenchida troca
- Montar um `UPDATE` aos poucos, com `+=` no texto do SQL e `append` na lista de valores, sem nunca juntar o que a pessoa digitou ao SQL
- Excluir um usuário por `POST`, com o modal de confirmação e a função JavaScript que recebe o código

O Capítulo 12 criou o cadastro de perfis, o 13 completou o recurso com a edição e a exclusão, e os Capítulos 14 e 15 fizeram o cadastro e a lista de usuários. Faltam as duas operações que podem estragar dados: **alterar** (`UPDATE`) e **excluir** (`DELETE`). O desenho é o do Capítulo 13, e quase tudo já está pronto: a lista tem os botões de editar e excluir esperando uma rota, a validação inteira está em `validar_usuario`, e o formulário já devolve um dicionário com `or ''`. O que muda é o tamanho do formulário: um usuário tem 12 campos, uma senha que nunca é mostrada e dois valores únicos (e-mail e CPF). Ao final, o recurso `usuarios` fica completo.

## 📦 Ponto de partida

Este capítulo continua do **seu** repositório `sistema-gestao`, como ficou no fim do Capítulo 15: com o cadastro de usuários, a lista com o perfil em um badge e a página de detalhe. Os Capítulos 12.1, 13.1 e 14.1 são opcionais: este capítulo parte do código do 15, e não deles.

Se o seu projeto não está funcionando, baixe o código do Capítulo 15 e descompacte. Depois de descompactar, crie o ambiente virtual e o `.env`, como no [Capítulo 11, Tópico 4](Capitulo_11_Projeto_Novo_e_Banco.md#topico-4-o-arquivo-env), importe o `banco.sql` no phpMyAdmin e cadastre os três perfis e os três usuários pelo formulário (a tabela do [Capítulo 15, Tópico 1](Capitulo_15_SELECT_Relacional_de_Usuario.md#antes-de-comecar) diz o que preencher):

➡️ [Baixar p2_cap_15.zip](../arquivos/p2_cap_15.zip)

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

---

## Tópico 1 — Editar um usuário (UPDATE)

### Antes de começar

Ligue o **Apache** e o **MySQL** no painel do XAMPP. Abra a pasta `sistema-gestao` no VS Code, o terminal (`Ctrl + '`), ative o ambiente virtual e confira o Git:

```bash
venv\Scripts\activate
git status
```

O `git status` deve dizer `nothing to commit, working tree clean`. Ligue o servidor com `python app.py` e deixe esse terminal rodando durante o capítulo (use um segundo terminal, o ícone **+**, para o Git). A lista deve ter a Ana, o Bruno e a Carla do Capítulo 15. Cadastre também um usuário para os testes, que será editado e excluído: nome `Daniel`, e-mail `daniel@exemplo.com`, senha `Senha123`, perfil **Usuário** e nada mais.

### O mapa do recurso, agora completo

| Rota | Métodos | O que faz | Função no `app.py` | Template |
|---|---|---|---|---|
| `/usuarios` | GET | Lista os usuários | `listar_usuarios` | `usuarios/usuarios_lista.html` |
| `/usuarios/inserir` | GET e POST | GET mostra o formulário, POST confere e grava | `inserir_usuario` | `usuarios/usuario_form.html` |
| `/usuarios/<int:id_usuario>` | GET | Detalhe de um usuário | `detalhar_usuario` | `usuarios/usuario_detalhe.html` |
| `/usuarios/<int:id_usuario>/editar` | GET e POST | GET mostra o formulário preenchido, POST confere e atualiza | `editar_usuario` | `usuarios/usuario_form.html` |
| `/usuarios/<int:id_usuario>/excluir` | só POST | Exclui o usuário e volta para a lista | `excluir_usuario` | (nenhum) |

### A validação ignora o próprio usuário

A edição confere os mesmos campos do cadastro, com a `validar_usuario`, e há duas diferenças, as mesmas que você viu na edição de perfis:

1. **E-mail e CPF repetidos**: o **próprio** usuário não conta. Quem abre o Bruno e só corrige o celular envia o e-mail `bruno@exemplo.com`, que já existe, e é dele mesmo. As consultas de e-mail e de CPF passam a ignorar o usuário que está sendo editado, com `id_usuario <> %s`.
2. **A senha é opcional.** O banco guarda o **hash** da senha, e o hash não tem como voltar a ser a senha: não há o que mostrar nos campos de senha, e o sistema também **não deve** mostrá-lo. Quem só quer corrigir o celular de um usuário não pode ser obrigado a digitar uma senha nova. Na edição, campos de senha **em branco** mantêm a senha atual, e campos **preenchidos** trocam a senha, com as mesmas regras do cadastro.

Abra o `validacoes/validacoes_usuario.py`. São seis trocas, todas pequenas.

**1. O `def` da `validar_email`** ganha o código do usuário. Troque:

```python
def validar_email(email):
```

por:

```python
def validar_email(email, id_usuario):
```

**2. A consulta no fim da `validar_email`.** Troque:

```python
    # Formato certo: confere no banco se o e-mail já pertence a outro usuário
    existente = execute_one('SELECT id_usuario FROM usuarios WHERE email = %s', (email,))
```

por:

```python
    # Formato certo: confere no banco se o e-mail já pertence a outro usuário
    # (o id_usuario <> %s ignora o próprio usuário na edição)
    existente = execute_one(
        'SELECT id_usuario FROM usuarios WHERE email = %s AND id_usuario <> %s',
        (email, id_usuario),
    )
```

**3. O `def` da `validar_cpf`.** Troque `def validar_cpf(cpf):` por:

```python
def validar_cpf(cpf, id_usuario):
```

**4. A consulta no fim da `validar_cpf`.** Troque:

```python
    # CPF válido: confere no banco, já no formato em que ele é gravado
    existente = execute_one('SELECT id_usuario FROM usuarios WHERE cpf = %s', (formatar_cpf(cpf),))
```

por:

```python
    # CPF válido: confere no banco, já no formato em que ele é gravado
    existente = execute_one(
        'SELECT id_usuario FROM usuarios WHERE cpf = %s AND id_usuario <> %s',
        (formatar_cpf(cpf), id_usuario),
    )
```

**5. O `def` da função principal**, com o mesmo valor padrão `0` da `validar_perfil` do Capítulo 13. Troque `def validar_usuario(dados):` por:

```python
def validar_usuario(dados, id_usuario=0):
```

**6. As chamadas dentro da `validar_usuario`.** Na seção dos dados principais, troque as duas linhas do e-mail e as três da senha:

```python
    erro = validar_email(dados['email'])
    if erro:
        erros.append(erro)

    erro = validar_senha(dados['senha'], dados['confirmacao'])
    if erro:
        erros.append(erro)
```

por:

```python
    erro = validar_email(dados['email'], id_usuario)
    if erro:
        erros.append(erro)

    # No cadastro (id_usuario 0) a senha é obrigatória; na edição, só é conferida se foi digitada
    if id_usuario == 0 or dados['senha'] or dados['confirmacao']:
        erro = validar_senha(dados['senha'], dados['confirmacao'])
        if erro:
            erros.append(erro)
```

E, na seção dos dados pessoais, troque `erro = validar_cpf(dados['cpf'])` por:

```python
    erro = validar_cpf(dados['cpf'], id_usuario)
```

O cadastro continua chamando `validar_usuario(dados)`, sem o segundo valor, e então o `id_usuario` vale `0`: nenhum usuário tem esse código, as consultas procuram em todos, e a senha é sempre conferida. Na edição, a senha só é conferida quando uma das duas caixas foi preenchida: um texto vazio conta como falso, e o `or` junta as três condições. Salve e cadastre de novo o `daniel@exemplo.com`: `Já existe um usuário com este e-mail.` O cadastro segue igual.

### A rota de edição

Na seção **USUÁRIOS** do `app.py`, acrescente a rota `editar_usuario` **depois** da `detalhar_usuario`. O `abort` já está importado desde o Capítulo 13:

```python
@app.route('/usuarios/<int:id_usuario>/editar', methods=['GET', 'POST'])
def editar_usuario(id_usuario):
    usuario = execute_one(SELECT_USUARIO + ' WHERE u.id_usuario = %s', (id_usuario,))

    if usuario is None:
        abort(404)

    # No GET, o formulário começa com a linha que veio do banco
    dados = usuario

    if request.method == 'POST':
        dados = {
            'nome': request.form.get('nome', '').strip(),
            'email': request.form.get('email', '').strip().lower(),
            'senha': request.form.get('senha', ''),
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

        # O id_usuario faz o próprio usuário não contar como repetido e torna a senha opcional
        erros = validar_usuario(dados, id_usuario)

        if erros:
            for mensagem in erros:
                flash(mensagem, 'danger')
        else:
            # O UPDATE é montado em partes: a senha só entra se uma nova foi digitada
            sql = (
                'UPDATE usuarios SET '
                '    nome = %s, '
                '    email = %s, '
                '    celular = %s, '
                '    data_nascimento = %s, '
                '    cpf = %s, '
                '    perfil_id = %s, '
                '    cep = %s, '
                '    endereco = %s, '
                '    numero = %s, '
                '    complemento = %s, '
                '    cidade = %s, '
                '    estado = %s'
            )
            params = [
                dados['nome'],
                dados['email'],
                formatar_celular(dados['celular']),
                dados['data_nascimento'],
                formatar_cpf(dados['cpf']),
                dados['perfil_id'],
                formatar_cep(dados['cep']),
                dados['endereco'],
                dados['numero'],
                dados['complemento'],
                dados['cidade'],
                dados['estado'],
            ]

            if dados['senha']:
                sql += ', senha = %s'
                params.append(generate_password_hash(dados['senha']))

            sql += ' WHERE id_usuario = %s'
            params.append(id_usuario)

            try:
                execute_query(sql, params)

                flash(f'Usuário "{dados["nome"]}" atualizado.', 'success')
                return redirect(url_for('listar_usuarios'))

            except Error as erro:
                if erro.errno == 1062:
                    flash('Já existe um usuário com este e-mail ou este CPF.', 'danger')
                else:
                    raise

    perfis = execute_query('SELECT id_perfil, nome FROM perfis ORDER BY nome', fetch=True)

    return render_template('usuarios/usuario_form.html', acao='editar', id_usuario=id_usuario,
                           dados=dados, perfis=perfis, ufs=UFS)
```

Compare com a `inserir_usuario` e com a `editar_perfil`: é a junção das duas. Os comentários marcam só o que é novo.

**O começo** é o da `editar_perfil`: busca o usuário pelo código do endereço (com o `SELECT_USUARIO` do Capítulo 15, sem a senha) e responde 404 se ele não existir.

**`dados = usuario`.** No GET, o dicionário do formulário **é a própria linha do banco**: as chaves do `SELECT_USUARIO` têm os mesmos nomes dos campos do formulário (`nome`, `email`, `celular`, `perfil_id`...). O formulário do Capítulo 14 já foi escrito para isso: os opcionais `NULL` chegam como `None`, e o `or ''` os mostra vazios; a data de nascimento chega como data e aparece como `AAAA-MM-DD`, o formato que o `<input type="date">` entende; e o `perfil_id` chega como número, e o `|string` dos dois lados da comparação marca a opção certa do `<select>`.

**O POST** monta o dicionário com o que veio do formulário, igual ao da `inserir_usuario` (copie o bloco de lá), e chama a `validar_usuario` com o `id_usuario`. Com erro, a rota cai no `render_template` do final, com o `dados` do formulário: o que a pessoa digitou volta para a tela, ainda em modo de edição.

**O `UPDATE` montado em partes.** O comando não é mais um texto só: ele é montado em dois lugares, o **texto** do SQL (`sql`) e a **lista dos valores** (`params`, uma lista, na mesma ordem dos `%s`). O começo tem as doze colunas que sempre mudam. Depois, o `if dados['senha']` acrescenta a coluna `senha` **só** quando uma senha nova foi digitada, e, nesse caso, o valor que vai para a lista é o **hash** (nunca a senha digitada), com a mesma função do cadastro. Por último entra o `WHERE`: o comando precisa ficar `UPDATE usuarios SET ..., estado = %s, senha = %s WHERE id_usuario = %s`, e o `WHERE` tem de vir depois de tudo o que está no `SET`.

!!! note "Python: `+=` e `append`"
    O `sql += ' WHERE id_usuario = %s'` acrescenta um pedaço ao final do texto que já está em `sql` (é o mesmo que `sql = sql + ' WHERE...'`). O `params.append(id_usuario)` acrescenta um item ao final da lista `params`. Os dois pedaços acrescentados andam juntos: um `%s` a mais no texto, um valor a mais na lista.

!!! danger "Só junte ao SQL textos fixos, escritos por você"
    O que vai para dentro do texto do SQL (`sql +=`) são pedaços **fixos**, escritos aqui no código. Tudo o que a pessoa digitou, sem exceção, vai na lista `params`, e o conector troca cada `%s` por um valor com segurança, como no resto do projeto. Colocar o que veio do formulário dentro do texto do SQL (com f-string ou com `+`) é a falha de segurança que o `%s` existe para evitar.

Olhe a última peça do comando: **`WHERE id_usuario = %s`**. Sem o `WHERE`, o `UPDATE` alteraria **todos** os usuários da tabela, e todos ficariam com o mesmo nome e o mesmo e-mail. O código vem do **endereço**, e não de um campo do formulário, que a pessoa poderia adulterar. O resto você já conhece: os formatadores do Capítulo 14, o `try/except` com o `1062` como barreira final e o PRG com `redirect` e `flash`. Como no [Capítulo 13](Capitulo_13_UPDATE_e_DELETE_de_Perfis.md#por-que-o-select-vem-antes-e-nao-o-rowcount), a existência do usuário é conferida pelo `SELECT` do começo da rota, e não pelo `rowcount` do `UPDATE`.

### O formulário nos dois modos

O formulário precisa mudar conforme o modo, como o de perfis: o título, o destino do envio, o texto do botão e, aqui, os campos de senha (o rótulo, o `required` e a dica). Primeiro, a rota de cadastro passa a informar o modo. Na `inserir_usuario`, troque a última linha:

```python
    return render_template('usuarios/usuario_form.html', dados=dados, perfis=perfis, ufs=UFS)
```

por:

```python
    return render_template('usuarios/usuario_form.html', acao='criar', id_usuario=None,
                           dados=dados, perfis=perfis, ufs=UFS)
```

Agora o template. As mudanças estão em seis pontos espalhados pelo arquivo, então troque o `templates/usuarios/usuario_form.html` **inteiro** por esta versão:

```html
{% extends 'layout/base_menu.html' %}

{% block titulo_aba %}{{ 'Editar usuário' if acao == 'editar' else 'Novo usuário' }} — Sistema de Gestão{% endblock %}

{% block conteudo %}
  {% if acao == 'editar' %}
    {% set destino = url_for('editar_usuario', id_usuario=id_usuario) %}
  {% else %}
    {% set destino = url_for('inserir_usuario') %}
  {% endif %}

  <h1 class="h2 mb-4">{{ 'Editar usuário' if acao == 'editar' else 'Novo usuário' }}</h1>

  <div class="row justify-content-center">
    <div class="col-lg-8">
      <div class="card">
        <div class="card-body">

          <form action="{{ destino }}" method="post">
            <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">

            <h2 class="h5 mb-3">Dados principais</h2>

            <div class="mb-3">
              <label for="nome" class="form-label">Nome completo</label>
              <input type="text" class="form-control" id="nome" name="nome" placeholder="Ex.: Ana Beatriz Lima" value="{{ dados.nome }}" required minlength="3" maxlength="255">
            </div>

            <div class="mb-3">
              <label for="email" class="form-label">E-mail</label>
              <input type="email" class="form-control" id="email" name="email" placeholder="nome@dominio.com.br" value="{{ dados.email }}" required maxlength="255">
            </div>

            <div class="row">
              <div class="col-md-6 mb-3">
                <label for="senha" class="form-label">{{ 'Nova senha' if acao == 'editar' else 'Senha' }}</label>
                <input type="password" class="form-control" id="senha" name="senha" {% if acao == 'criar' %}required{% endif %} minlength="8" maxlength="128" autocomplete="new-password">
                <div class="form-text">{{ 'Deixe em branco para manter a senha atual.' if acao == 'editar' else 'Mínimo de 8 caracteres, com letras e números.' }}</div>
              </div>
              <div class="col-md-6 mb-3">
                <label for="confirmacao" class="form-label">Confirmar a senha</label>
                <input type="password" class="form-control" id="confirmacao" name="confirmacao" {% if acao == 'criar' %}required{% endif %} minlength="8" maxlength="128" autocomplete="new-password">
              </div>
            </div>

            <div class="mb-4">
              <label for="perfil_id" class="form-label">Perfil</label>
              {% if perfis %}
                <select class="form-select" id="perfil_id" name="perfil_id" required>
                  <option value="">Selecione...</option>
                  {% for perfil in perfis %}
                    <option value="{{ perfil.id_perfil }}" {% if dados.perfil_id|string == perfil.id_perfil|string %}selected{% endif %}>{{ perfil.nome }}</option>
                  {% endfor %}
                </select>
              {% else %}
                <div class="alert alert-warning mb-0" role="alert">
                  Nenhum perfil cadastrado. <a href="{{ url_for('inserir_perfil') }}" class="alert-link">Cadastre um perfil</a> antes de cadastrar usuários.
                </div>
              {% endif %}
            </div>

            <h2 class="h5 mb-3">Dados pessoais (opcionais)</h2>

            <div class="row">
              <div class="col-md-4 mb-3">
                <label for="celular" class="form-label">Celular</label>
                <input type="tel" class="form-control" id="celular" name="celular" placeholder="(14) 99999-9999" value="{{ dados.celular or '' }}" maxlength="20">
              </div>
              <div class="col-md-4 mb-3">
                <label for="data_nascimento" class="form-label">Data de nascimento</label>
                <input type="date" class="form-control" id="data_nascimento" name="data_nascimento" value="{{ dados.data_nascimento or '' }}">
              </div>
              <div class="col-md-4 mb-4">
                <label for="cpf" class="form-label">CPF</label>
                <input type="text" class="form-control" id="cpf" name="cpf" placeholder="000.000.000-00" value="{{ dados.cpf or '' }}" maxlength="14">
              </div>
            </div>

            <h2 class="h5 mb-3">Endereço (opcional)</h2>

            <div class="row">
              <div class="col-md-4 mb-3">
                <label for="cep" class="form-label">CEP</label>
                <input type="text" class="form-control" id="cep" name="cep" placeholder="00000-000" value="{{ dados.cep or '' }}" maxlength="9">
              </div>
              <div class="col-md-8 mb-3">
                <label for="endereco" class="form-label">Endereço</label>
                <input type="text" class="form-control" id="endereco" name="endereco" value="{{ dados.endereco or '' }}" maxlength="255">
              </div>
            </div>

            <div class="row">
              <div class="col-md-4 mb-3">
                <label for="numero" class="form-label">Número</label>
                <input type="text" class="form-control" id="numero" name="numero" value="{{ dados.numero or '' }}" maxlength="20">
              </div>
              <div class="col-md-8 mb-3">
                <label for="complemento" class="form-label">Complemento</label>
                <input type="text" class="form-control" id="complemento" name="complemento" value="{{ dados.complemento or '' }}" maxlength="100">
              </div>
            </div>

            <div class="row">
              <div class="col-md-8 mb-4">
                <label for="cidade" class="form-label">Cidade</label>
                <input type="text" class="form-control" id="cidade" name="cidade" value="{{ dados.cidade or '' }}" maxlength="100">
              </div>
              <div class="col-md-4 mb-4">
                <label for="estado" class="form-label">Estado</label>
                <select class="form-select" id="estado" name="estado">
                  <option value="">--</option>
                  {% for uf in ufs %}
                    <option value="{{ uf }}" {% if dados.estado == uf %}selected{% endif %}>{{ uf }}</option>
                  {% endfor %}
                </select>
              </div>
            </div>

            <div class="d-flex justify-content-between gap-2">
              <a href="{{ url_for('listar_usuarios') }}" class="btn btn-outline-secondary">Cancelar</a>
              <button type="submit" class="btn btn-primary">{{ 'Salvar alterações' if acao == 'editar' else 'Salvar usuário' }}</button>
            </div>

          </form>

        </div>
      </div>
    </div>
  </div>
{% endblock %}
```

As linhas que mudaram em relação ao Capítulo 14:

1. **O título da aba, o `<h1>` e o botão de enviar** usam o `if` em uma linha, como no `perfil_form.html`.
2. **O destino** é escolhido no começo do bloco com o `{% set %}` do Capítulo 13 e usado no `<form action="{{ destino }}">`.
3. **A senha**: o rótulo passa a **Nova senha** na edição, a dica diz `Deixe em branco para manter a senha atual.`, e o `required` dos dois campos só aparece no cadastro (`{% if acao == 'criar' %}required{% endif %}`). O `minlength="8"` continua nos dois modos: o navegador só confere o tamanho quando há texto no campo.

O resto do arquivo (os campos, os `value` com `or ''`, os `<select>`) é o mesmo do Capítulo 14, e funciona nos dois modos sem mudança.

### Os caminhos até a edição

**Na lista.** O botão amarelo existe desde o Capítulo 15, com o `href="#"`. No `usuarios_lista.html`, troque, na célula de ações, a linha do botão de editar:

```html
<a href="#" class="btn btn-sm btn-warning" title="Editar"><i class="bi bi-pencil-square"></i></a>
```

por:

```html
<a href="{{ url_for('editar_usuario', id_usuario=usuario.id_usuario) }}" class="btn btn-sm btn-warning" title="Editar"><i class="bi bi-pencil-square"></i></a>
```

**No menu.** O menu **Usuários** precisa continuar aceso durante a edição. No `base_menu.html`, no botão do menu suspenso **Usuários**, troque só o trecho do `{% if %}`:

```html
{% if request.endpoint in ['listar_usuarios', 'inserir_usuario', 'detalhar_usuario'] %}active{% endif %}
```

por:

```html
{% if request.endpoint in ['listar_usuarios', 'inserir_usuario', 'detalhar_usuario', 'editar_usuario'] %}active{% endif %}
```

### Testando a edição

Salve tudo e teste, sempre entrando pelo botão amarelo da lista:

1. **O formulário preenchido**: abra a edição do **Bruno**. Todos os campos vêm com os dados dele (o CPF, o celular, a data no calendário, o perfil **Gerente** e o estado **SP** marcados), o título é **Editar usuário**, os campos de senha estão vazios e o rótulo diz **Nova senha**. Abra a da **Ana**: os opcionais vêm vazios, e não com a palavra `None`.
2. **Uma alteração simples**: no **Daniel**, troque o nome para `Daniel Silva`, preencha o celular `14 99811 2030` e o estado `SP`, deixe as senhas em branco e salve. Você volta para a lista, com a faixa verde `Usuário "Daniel Silva" atualizado.`
3. **O detalhe**: abra o olho do Daniel. O celular aparece formatado, `(14) 99811-2030`, e a **Última alteração** mostra a hora de agora, enquanto o **Cadastrado em** continua o mesmo. O banco cuida disso (`ON UPDATE CURRENT_TIMESTAMP`, do `banco.sql`), sem nenhuma linha de Python.
4. **Apagar um opcional**: abra a edição do Daniel, apague o celular e salve. No detalhe, o celular mostra `—`. No phpMyAdmin (banco `gestao`, tabela `usuarios`, aba **Procurar**), a coluna aparece como `NULL`.
5. **A senha**: ainda no phpMyAdmin, guarde o começo e o fim do hash da linha do Daniel. Edite o Daniel com `NovaSenha456` nas duas caixas e salve: no phpMyAdmin, o hash é **outro**. Edite de novo, deixe as duas caixas **em branco**, mude só o nome e salve: o hash continua igual. Digite uma senha nova só em uma caixa: a faixa vermelha `A confirmação da senha não confere.`, e o formulário de volta, em modo de edição, com o resto preenchido. (Entrar no sistema com a senha nova só vai ser possível no Capítulo 17, o do login.)
6. **Repetidos**: troque o e-mail do Daniel por `ana@exemplo.com`: `Já existe um usuário com este e-mail.` Mas salvar o Bruno sem mudar nada funciona: o próprio e-mail e o próprio CPF não contam como repetidos.
7. **O perfil**: troque o perfil do Daniel para **Gerente** e salve: o badge na lista fica amarelo.
8. **Um código que não existe**: acesse `/usuarios/99999/editar`: a página 404. E confira, na lista, que **só** o Daniel mudou.

```bash
git add .
git commit -m "Adiciona a edição de usuário com senha opcional e UPDATE montado em partes"
git push
```

---

## Tópico 2 — Excluir um usuário (DELETE)

### A rota que só aceita POST

O comando é o `DELETE`, com os mesmos cuidados do `UPDATE`:

```sql
DELETE FROM usuarios WHERE id_usuario = 3;
```

Sem o `WHERE`, ele apaga **todos** os usuários, sem perguntar e sem "desfazer", e o código apagado nunca é reaproveitado pelo `AUTO_INCREMENT`. A exclusão também **não pode ser um link**: o `GET` deve só consultar, e robôs de busca, o carregamento antecipado de links e a pré-visualização de mensagens fazem `GET` sozinhos. O [Capítulo 13](Capitulo_13_UPDATE_e_DELETE_de_Perfis.md#por-que-excluir-nunca-pode-ser-um-link) explicou isso em detalhe: a rota aceita só `POST`, que só sai de um botão de formulário, com o token CSRF. No `app.py`, acrescente a rota depois da `editar_usuario`:

```python
@app.route('/usuarios/<int:id_usuario>/excluir', methods=['POST'])
def excluir_usuario(id_usuario):
    usuario = execute_one(
        'SELECT id_usuario, nome FROM usuarios WHERE id_usuario = %s',
        (id_usuario,),
    )

    if usuario is None:
        abort(404)

    # Nenhuma tabela depende de usuarios: não há contagem nem erro 1451
    execute_query('DELETE FROM usuarios WHERE id_usuario = %s', (id_usuario,))
    flash(f'Usuário "{usuario["nome"]}" excluído.', 'success')

    return redirect(url_for('listar_usuarios'))
```

O `SELECT` inicial responde 404 para um código que não existe e traz o **nome**, para a mensagem dizer quem foi excluído. Salve e digite, na barra de endereço, `http://127.0.0.1:5000/usuarios/3/excluir` (com qualquer código): o navegador faz um `GET`, e a resposta é **Method Not Allowed** (405). Nada é excluído.

!!! note "Aqui não há contagem nem erro 1451"
    Excluir um **perfil** (Capítulo 13) exigia contar os usuários antes e capturar o erro `1451`, porque a tabela `usuarios` aponta para `perfis` por uma chave estrangeira. Nenhuma outra tabela aponta para `usuarios`: abra o `banco.sql` e confira. Por isso o `DELETE` do usuário não esbarra em nada e não precisa de `try/except`. Se um dia outra tabela passar a apontar para `usuarios` (pedidos, por exemplo), esta rota ganhará as mesmas duas defesas do perfil.

### O modal e a função

O botão vermelho da lista não pode excluir com um clique só. O desenho é o do Capítulo 13: **um único modal** do Bootstrap, reaproveitado por todas as linhas, que uma função JavaScript preenche com o usuário clicado. São quatro alterações no `usuarios_lista.html`.

**Primeira: o modal.** No final do `{% block conteudo %}`, depois da `</table>` e antes do `{% endblock %}`, acrescente:

```html
<div class="modal fade" id="modalExcluir" tabindex="-1" aria-labelledby="tituloModalExcluir" aria-hidden="true">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content">
      <div class="modal-header">
        <h2 class="modal-title h5" id="tituloModalExcluir">Excluir usuário</h2>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Fechar"></button>
      </div>
      <form id="formExcluir" action="" method="post">
        <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
        <div class="modal-body">
          <p class="mb-0">Excluir o usuário <strong id="nomeExcluir"></strong>? Esta ação não pode ser desfeita.</p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">Cancelar</button>
          <button type="submit" class="btn btn-danger">Excluir</button>
        </div>
      </form>
    </div>
  </div>
</div>
```

O **Cancelar** só fecha a janela, e o **Excluir** (`type="submit"`) é o único que envia o `POST`. O `action=""` está vazio de propósito: o endereço depende do usuário clicado.

**Segunda: um `id` no nome.** A função precisa achar o **nome** do usuário, mas a célula do nome traz o nome **e** o e-mail em letra pequena, e a função deve ler só o nome. Por isso o nome ganha uma etiqueta própria, um `<span>` com um `id` que inclui o código. Na célula do nome, troque a linha:

```html
{{ usuario.nome }}<br>
```

por:

```html
<span id="nome_usuario_{{ usuario.id_usuario }}">{{ usuario.nome }}</span><br>
```

Para o usuário de código 3, o HTML gerado é `<span id="nome_usuario_3">Daniel Silva</span>`.

**Terceira: o botão vermelho abre o modal e chama a função.** Na célula de ações, troque a linha do botão de excluir:

```html
<button type="button" class="btn btn-sm btn-danger" title="Excluir"><i class="bi bi-trash"></i></button>
```

por:

```html
<button type="button" class="btn btn-sm btn-danger" title="Excluir" data-bs-toggle="modal" data-bs-target="#modalExcluir" onclick="prepararExclusao({{ usuario.id_usuario }})"><i class="bi bi-trash"></i></button>
```

**Quarta: a função.** No **final** do `usuarios_lista.html`, **depois** do `{% endblock %}` do conteúdo, acrescente:

```html
{% block scripts %}
<script>
  function prepararExclusao(id) {
    const nome = document.getElementById('nome_usuario_' + id).textContent;
    document.getElementById('nomeExcluir').textContent = nome;
    document.getElementById('formExcluir').action = '/usuarios/' + id + '/excluir';
  }
</script>
{% endblock %}
```

!!! note "JavaScript: as três linhas da função"
    É a mesma função do [Capítulo 13](Capitulo_13_UPDATE_e_DELETE_de_Perfis.md#uma-funcao-javascript-que-recebe-o-codigo), com outros nomes. A primeira linha acha o `<span>` do nome (`'nome_usuario_' + id` vira `nome_usuario_3`) e lê o texto dele com `.textContent`. A segunda escreve esse nome no `<strong id="nomeExcluir">` da janela. A terceira troca o `action` do formulário por `/usuarios/3/excluir`, o endereço da rota `excluir_usuario`: se um dia você mudar o endereço da rota, mude aqui também. A função recebe só o **código**, e não o nome, porque um nome com aspas quebraria o atributo `onclick`.

### Testando a exclusão

Salve, recarregue a lista e clique no botão vermelho do **Daniel Silva**: a janela mostra `Excluir o usuário Daniel Silva?`. Clique em **Cancelar**, depois no botão vermelho de **outro** usuário: o nome muda, porque o mesmo modal foi reaproveitado. Cancele, abra o do Daniel de novo e confirme: o Daniel some da lista, com a faixa verde `Usuário "Daniel Silva" excluído.` Confira no phpMyAdmin: a linha dele não está mais na tabela `usuarios`. **Não** exclua a Ana, o Bruno nem a Carla, porque os próximos capítulos usam os três.

Um último teste, o do código que não existe mais. Cadastre um usuário `Teste Duplo` (qualquer e-mail novo e senha `Senha123`), abra a lista em **duas abas** do navegador, exclua o `Teste Duplo` na primeira e, **sem recarregar** a segunda, exclua o mesmo usuário nela. A segunda aba mostra a página 404: o `SELECT` do começo da rota não encontrou o usuário, e o `abort(404)` respondeu, sem tentar apagar nada.

| Situação | Quem trata | O que a pessoa vê |
|---|---|---|
| Endereço da exclusão aberto no navegador (`GET`) | `methods=['POST']` | A página 405, e nada é excluído |
| Clique sem querer no botão vermelho | O modal de confirmação | A janela, com **Cancelar** |
| Usuário que já foi excluído | `SELECT` + `abort(404)` | A página 404 |
| Formulário sem o token CSRF | `CSRFProtect` | O erro 400 |

```bash
git add .
git commit -m "Adiciona a exclusão de usuário por POST com modal de confirmação"
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
def editar_perfil(id_perfil):
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
                    'UPDATE perfis SET '
                    '    nome = %s, '
                    '    descricao = %s '
                    'WHERE id_perfil = %s',
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
def excluir_perfil(id_perfil):
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

    return render_template('usuarios/usuario_form.html', acao='criar', id_usuario=None,
                           dados=dados, perfis=perfis, ufs=UFS)


@app.route('/usuarios/<int:id_usuario>')
def detalhar_usuario(id_usuario):
    usuario = execute_one(SELECT_USUARIO + ' WHERE u.id_usuario = %s', (id_usuario,))

    if usuario is None:
        abort(404)

    return render_template('usuarios/usuario_detalhe.html', usuario=usuario)


@app.route('/usuarios/<int:id_usuario>/editar', methods=['GET', 'POST'])
def editar_usuario(id_usuario):
    usuario = execute_one(SELECT_USUARIO + ' WHERE u.id_usuario = %s', (id_usuario,))

    if usuario is None:
        abort(404)

    # No GET, o formulário começa com a linha que veio do banco
    dados = usuario

    if request.method == 'POST':
        dados = {
            'nome': request.form.get('nome', '').strip(),
            'email': request.form.get('email', '').strip().lower(),
            'senha': request.form.get('senha', ''),
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

        # O id_usuario faz o próprio usuário não contar como repetido e torna a senha opcional
        erros = validar_usuario(dados, id_usuario)

        if erros:
            for mensagem in erros:
                flash(mensagem, 'danger')
        else:
            # O UPDATE é montado em partes: a senha só entra se uma nova foi digitada
            sql = (
                'UPDATE usuarios SET '
                '    nome = %s, '
                '    email = %s, '
                '    celular = %s, '
                '    data_nascimento = %s, '
                '    cpf = %s, '
                '    perfil_id = %s, '
                '    cep = %s, '
                '    endereco = %s, '
                '    numero = %s, '
                '    complemento = %s, '
                '    cidade = %s, '
                '    estado = %s'
            )
            params = [
                dados['nome'],
                dados['email'],
                formatar_celular(dados['celular']),
                dados['data_nascimento'],
                formatar_cpf(dados['cpf']),
                dados['perfil_id'],
                formatar_cep(dados['cep']),
                dados['endereco'],
                dados['numero'],
                dados['complemento'],
                dados['cidade'],
                dados['estado'],
            ]

            if dados['senha']:
                sql += ', senha = %s'
                params.append(generate_password_hash(dados['senha']))

            sql += ' WHERE id_usuario = %s'
            params.append(id_usuario)

            try:
                execute_query(sql, params)

                flash(f'Usuário "{dados["nome"]}" atualizado.', 'success')
                return redirect(url_for('listar_usuarios'))

            except Error as erro:
                if erro.errno == 1062:
                    flash('Já existe um usuário com este e-mail ou este CPF.', 'danger')
                else:
                    raise

    perfis = execute_query('SELECT id_perfil, nome FROM perfis ORDER BY nome', fetch=True)

    return render_template('usuarios/usuario_form.html', acao='editar', id_usuario=id_usuario,
                           dados=dados, perfis=perfis, ufs=UFS)


@app.route('/usuarios/<int:id_usuario>/excluir', methods=['POST'])
def excluir_usuario(id_usuario):
    usuario = execute_one(
        'SELECT id_usuario, nome FROM usuarios WHERE id_usuario = %s',
        (id_usuario,),
    )

    if usuario is None:
        abort(404)

    # Nenhuma tabela depende de usuarios: não há contagem nem erro 1451
    execute_query('DELETE FROM usuarios WHERE id_usuario = %s', (id_usuario,))
    flash(f'Usuário "{usuario["nome"]}" excluído.', 'success')

    return redirect(url_for('listar_usuarios'))


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

O `validacoes/validacoes_usuario.py`:

```python
from datetime import datetime

from db import execute_one

# Siglas dos estados aceitas pelo sistema: o formulário e a validação usam a mesma lista
UFS = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA',
       'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']


# ==============================================================================
# FUNÇÕES DE APOIO
# ==============================================================================

def so_digitos(texto):
    # '(14) 99811-2030' vira '14998112030'
    resultado = ''
    for letra in texto:
        if letra in '0123456789':
            resultado = resultado + letra
    return resultado


def formatar_celular(celular):
    # Devolve o celular no formato que vai para o banco, ou None se o campo veio vazio
    if not celular:
        return None

    digitos = so_digitos(celular)
    if len(digitos) == 11:
        return f'({digitos[0:2]}) {digitos[2:7]}-{digitos[7:11]}'

    return f'({digitos[0:2]}) {digitos[2:6]}-{digitos[6:10]}'


def formatar_cpf(cpf):
    # Devolve o CPF como 000.000.000-00, ou None se o campo veio vazio
    if not cpf:
        return None

    digitos = so_digitos(cpf)
    return f'{digitos[0:3]}.{digitos[3:6]}.{digitos[6:9]}-{digitos[9:11]}'


def formatar_cep(cep):
    # Devolve o CEP como 00000-000, ou None se o campo veio vazio
    if not cep:
        return None

    digitos = so_digitos(cep)
    return f'{digitos[0:5]}-{digitos[5:8]}'


def calcular_digito_cpf(digitos, quantidade):
    # Conta de um dígito verificador do CPF: pesos decrescentes, soma e resto da divisão por 11
    soma = 0
    for posicao in range(quantidade):
        peso = quantidade + 1 - posicao
        soma = soma + int(digitos[posicao]) * peso

    resto = (soma * 10) % 11
    if resto == 10:
        resto = 0

    return resto


# ==============================================================================
# UMA FUNÇÃO POR CAMPO: cada uma devolve a mensagem de erro ou None
# ==============================================================================

# ================ VALIDAÇÕES PARA O CAMPO nome =====================
def validar_nome(nome):
    if not nome:
        return 'Informe o nome do usuário.'

    if len(nome) < 3:
        return 'O nome deve ter pelo menos 3 caracteres.'

    if len(nome) > 255:
        return 'O nome deve ter no máximo 255 caracteres.'

    return None


# ================ VALIDAÇÕES PARA O CAMPO email =====================
def validar_email(email, id_usuario):
    mensagem = 'Informe um e-mail válido, por exemplo nome@dominio.com.br.'

    if not email:
        return 'Informe o e-mail.'

    if len(email) > 255:
        return 'O e-mail deve ter no máximo 255 caracteres.'

    if ' ' in email or email.count('@') != 1:
        return mensagem

    partes = email.split('@')
    antes = partes[0]
    depois = partes[1]

    if antes == '' or '.' not in depois:
        return mensagem

    if depois.startswith('.') or depois.endswith('.'):
        return mensagem

    # Formato certo: confere no banco se o e-mail já pertence a outro usuário
    # (o id_usuario <> %s ignora o próprio usuário na edição)
    existente = execute_one(
        'SELECT id_usuario FROM usuarios WHERE email = %s AND id_usuario <> %s',
        (email, id_usuario),
    )
    if existente:
        return 'Já existe um usuário com este e-mail.'

    return None


# ================ VALIDAÇÕES PARA O CAMPO senha =====================
def validar_senha(senha, confirmacao):
    if len(senha) < 8:
        return 'A senha deve ter pelo menos 8 caracteres.'

    if len(senha) > 128:
        return 'A senha deve ter no máximo 128 caracteres.'

    tem_letra = False
    tem_numero = False
    for caractere in senha:
        if caractere.isalpha():
            tem_letra = True
        if caractere in '0123456789':
            tem_numero = True

    if not tem_letra or not tem_numero:
        return 'A senha deve ter letras e números.'

    if senha != confirmacao:
        return 'A confirmação da senha não confere.'

    return None


# ================ VALIDAÇÕES PARA O CAMPO perfil_id =====================
def validar_perfil_id(perfil_id):
    # Tudo o que chega do formulário é texto: precisa ser um número...
    try:
        numero = int(perfil_id)
    except ValueError:
        return 'Selecione um perfil.'

    # ...e precisa existir na tabela perfis
    perfil = execute_one('SELECT id_perfil FROM perfis WHERE id_perfil = %s', (numero,))
    if perfil is None:
        return 'Selecione um perfil válido.'

    return None


# ================ VALIDAÇÕES PARA O CAMPO celular (opcional) =====================
def validar_celular(celular):
    if not celular:
        return None

    digitos = so_digitos(celular)
    if len(digitos) != 10 and len(digitos) != 11:
        return 'Informe o celular com DDD, com 10 ou 11 dígitos.'

    return None


# ================ VALIDAÇÕES PARA O CAMPO cpf (opcional) =====================
def validar_cpf(cpf, id_usuario):
    if not cpf:
        return None

    digitos = so_digitos(cpf)
    if len(digitos) != 11:
        return 'O CPF deve ter 11 dígitos.'

    if digitos == digitos[0] * 11:
        return 'Informe um CPF válido.'

    if calcular_digito_cpf(digitos, 9) != int(digitos[9]):
        return 'Informe um CPF válido.'

    if calcular_digito_cpf(digitos, 10) != int(digitos[10]):
        return 'Informe um CPF válido.'

    # CPF válido: confere no banco, já no formato em que ele é gravado
    existente = execute_one(
        'SELECT id_usuario FROM usuarios WHERE cpf = %s AND id_usuario <> %s',
        (formatar_cpf(cpf), id_usuario),
    )
    if existente:
        return 'Já existe um usuário com este CPF.'

    return None


# ================ VALIDAÇÕES PARA O CAMPO data_nascimento (opcional) =====================
def validar_data_nascimento(texto):
    if not texto:
        return None

    try:
        data = datetime.strptime(texto, '%Y-%m-%d')
    except ValueError:
        return 'Informe uma data de nascimento válida.'

    if data > datetime.now():
        return 'A data de nascimento não pode estar no futuro.'

    if data.year < 1900:
        return 'A data de nascimento deve ser a partir de 1900.'

    return None


# ================ VALIDAÇÕES PARA O CAMPO cep (opcional) =====================
def validar_cep(cep):
    if not cep:
        return None

    if len(so_digitos(cep)) != 8:
        return 'Informe um CEP com 8 dígitos.'

    return None


# ================ VALIDAÇÕES PARA O CAMPO estado (opcional) =====================
def validar_estado(estado):
    if not estado:
        return None

    if estado not in UFS:
        return 'Selecione um estado válido.'

    return None


# ================ TAMANHO DOS CAMPOS DE TEXTO LIVRE (opcionais) =====================
def validar_tamanho(valor, rotulo, maximo):
    if valor and len(valor) > maximo:
        return f'O campo {rotulo} deve ter no máximo {maximo} caracteres.'

    return None


# ==============================================================================
# FUNÇÃO PRINCIPAL: recebe o dicionário com o formulário e devolve a lista de erros
# ==============================================================================

def validar_usuario(dados, id_usuario=0):
    erros = []

    # ================ DADOS PRINCIPAIS (obrigatórios) =====================
    erro = validar_nome(dados['nome'])
    if erro:
        erros.append(erro)

    erro = validar_email(dados['email'], id_usuario)
    if erro:
        erros.append(erro)

    # No cadastro (id_usuario 0) a senha é obrigatória; na edição, só é conferida se foi digitada
    if id_usuario == 0 or dados['senha'] or dados['confirmacao']:
        erro = validar_senha(dados['senha'], dados['confirmacao'])
        if erro:
            erros.append(erro)

    erro = validar_perfil_id(dados['perfil_id'])
    if erro:
        erros.append(erro)

    # ================ DADOS PESSOAIS (opcionais) =====================
    erro = validar_celular(dados['celular'])
    if erro:
        erros.append(erro)

    erro = validar_cpf(dados['cpf'], id_usuario)
    if erro:
        erros.append(erro)

    erro = validar_data_nascimento(dados['data_nascimento'])
    if erro:
        erros.append(erro)

    # ================ ENDEREÇO (opcional) =====================
    erro = validar_cep(dados['cep'])
    if erro:
        erros.append(erro)

    erro = validar_tamanho(dados['endereco'], 'endereço', 255)
    if erro:
        erros.append(erro)

    erro = validar_tamanho(dados['numero'], 'número', 20)
    if erro:
        erros.append(erro)

    erro = validar_tamanho(dados['complemento'], 'complemento', 100)
    if erro:
        erros.append(erro)

    erro = validar_tamanho(dados['cidade'], 'cidade', 100)
    if erro:
        erros.append(erro)

    erro = validar_estado(dados['estado'])
    if erro:
        erros.append(erro)

    return erros
```

O `templates/usuarios/usuario_form.html`:

```html
{% extends 'layout/base_menu.html' %}

{% block titulo_aba %}{{ 'Editar usuário' if acao == 'editar' else 'Novo usuário' }} — Sistema de Gestão{% endblock %}

{% block conteudo %}
  {% if acao == 'editar' %}
    {% set destino = url_for('editar_usuario', id_usuario=id_usuario) %}
  {% else %}
    {% set destino = url_for('inserir_usuario') %}
  {% endif %}

  <h1 class="h2 mb-4">{{ 'Editar usuário' if acao == 'editar' else 'Novo usuário' }}</h1>

  <div class="row justify-content-center">
    <div class="col-lg-8">
      <div class="card">
        <div class="card-body">

          <form action="{{ destino }}" method="post">
            <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">

            <h2 class="h5 mb-3">Dados principais</h2>

            <div class="mb-3">
              <label for="nome" class="form-label">Nome completo</label>
              <input type="text" class="form-control" id="nome" name="nome" placeholder="Ex.: Ana Beatriz Lima" value="{{ dados.nome }}" required minlength="3" maxlength="255">
            </div>

            <div class="mb-3">
              <label for="email" class="form-label">E-mail</label>
              <input type="email" class="form-control" id="email" name="email" placeholder="nome@dominio.com.br" value="{{ dados.email }}" required maxlength="255">
            </div>

            <div class="row">
              <div class="col-md-6 mb-3">
                <label for="senha" class="form-label">{{ 'Nova senha' if acao == 'editar' else 'Senha' }}</label>
                <input type="password" class="form-control" id="senha" name="senha" {% if acao == 'criar' %}required{% endif %} minlength="8" maxlength="128" autocomplete="new-password">
                <div class="form-text">{{ 'Deixe em branco para manter a senha atual.' if acao == 'editar' else 'Mínimo de 8 caracteres, com letras e números.' }}</div>
              </div>
              <div class="col-md-6 mb-3">
                <label for="confirmacao" class="form-label">Confirmar a senha</label>
                <input type="password" class="form-control" id="confirmacao" name="confirmacao" {% if acao == 'criar' %}required{% endif %} minlength="8" maxlength="128" autocomplete="new-password">
              </div>
            </div>

            <div class="mb-4">
              <label for="perfil_id" class="form-label">Perfil</label>
              {% if perfis %}
                <select class="form-select" id="perfil_id" name="perfil_id" required>
                  <option value="">Selecione...</option>
                  {% for perfil in perfis %}
                    <option value="{{ perfil.id_perfil }}" {% if dados.perfil_id|string == perfil.id_perfil|string %}selected{% endif %}>{{ perfil.nome }}</option>
                  {% endfor %}
                </select>
              {% else %}
                <div class="alert alert-warning mb-0" role="alert">
                  Nenhum perfil cadastrado. <a href="{{ url_for('inserir_perfil') }}" class="alert-link">Cadastre um perfil</a> antes de cadastrar usuários.
                </div>
              {% endif %}
            </div>

            <h2 class="h5 mb-3">Dados pessoais (opcionais)</h2>

            <div class="row">
              <div class="col-md-4 mb-3">
                <label for="celular" class="form-label">Celular</label>
                <input type="tel" class="form-control" id="celular" name="celular" placeholder="(14) 99999-9999" value="{{ dados.celular or '' }}" maxlength="20">
              </div>
              <div class="col-md-4 mb-3">
                <label for="data_nascimento" class="form-label">Data de nascimento</label>
                <input type="date" class="form-control" id="data_nascimento" name="data_nascimento" value="{{ dados.data_nascimento or '' }}">
              </div>
              <div class="col-md-4 mb-4">
                <label for="cpf" class="form-label">CPF</label>
                <input type="text" class="form-control" id="cpf" name="cpf" placeholder="000.000.000-00" value="{{ dados.cpf or '' }}" maxlength="14">
              </div>
            </div>

            <h2 class="h5 mb-3">Endereço (opcional)</h2>

            <div class="row">
              <div class="col-md-4 mb-3">
                <label for="cep" class="form-label">CEP</label>
                <input type="text" class="form-control" id="cep" name="cep" placeholder="00000-000" value="{{ dados.cep or '' }}" maxlength="9">
              </div>
              <div class="col-md-8 mb-3">
                <label for="endereco" class="form-label">Endereço</label>
                <input type="text" class="form-control" id="endereco" name="endereco" value="{{ dados.endereco or '' }}" maxlength="255">
              </div>
            </div>

            <div class="row">
              <div class="col-md-4 mb-3">
                <label for="numero" class="form-label">Número</label>
                <input type="text" class="form-control" id="numero" name="numero" value="{{ dados.numero or '' }}" maxlength="20">
              </div>
              <div class="col-md-8 mb-3">
                <label for="complemento" class="form-label">Complemento</label>
                <input type="text" class="form-control" id="complemento" name="complemento" value="{{ dados.complemento or '' }}" maxlength="100">
              </div>
            </div>

            <div class="row">
              <div class="col-md-8 mb-4">
                <label for="cidade" class="form-label">Cidade</label>
                <input type="text" class="form-control" id="cidade" name="cidade" value="{{ dados.cidade or '' }}" maxlength="100">
              </div>
              <div class="col-md-4 mb-4">
                <label for="estado" class="form-label">Estado</label>
                <select class="form-select" id="estado" name="estado">
                  <option value="">--</option>
                  {% for uf in ufs %}
                    <option value="{{ uf }}" {% if dados.estado == uf %}selected{% endif %}>{{ uf }}</option>
                  {% endfor %}
                </select>
              </div>
            </div>

            <div class="d-flex justify-content-between gap-2">
              <a href="{{ url_for('listar_usuarios') }}" class="btn btn-outline-secondary">Cancelar</a>
              <button type="submit" class="btn btn-primary">{{ 'Salvar alterações' if acao == 'editar' else 'Salvar usuário' }}</button>
            </div>

          </form>

        </div>
      </div>
    </div>
  </div>
{% endblock %}
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
          <span id="nome_usuario_{{ usuario.id_usuario }}">{{ usuario.nome }}</span><br>
          <small class="text-body-secondary">{{ usuario.email }}</small>
        </td>
        <td>{{ usuario.cpf|cpf_oculto }}</td>
        <td>{{ usuario.cidade if usuario.cidade else '—' }}{% if usuario.estado %}/{{ usuario.estado }}{% endif %}</td>
        <td>{{ usuario.data_nascimento|data_br }}</td>
        <td>{% include 'usuarios/_badge_perfil.html' %}</td>
        <td class="text-end text-nowrap">
          <a href="{{ url_for('detalhar_usuario', id_usuario=usuario.id_usuario) }}" class="btn btn-sm btn-info" title="Ver detalhes"><i class="bi bi-eye"></i></a>
          <a href="{{ url_for('editar_usuario', id_usuario=usuario.id_usuario) }}" class="btn btn-sm btn-warning" title="Editar"><i class="bi bi-pencil-square"></i></a>
          <button type="button" class="btn btn-sm btn-danger" title="Excluir" data-bs-toggle="modal" data-bs-target="#modalExcluir" onclick="prepararExclusao({{ usuario.id_usuario }})"><i class="bi bi-trash"></i></button>
        </td>
      </tr>
      {% else %}
      <tr>
        <td colspan="7" class="text-center text-body-secondary py-4">Nenhum usuário cadastrado ainda.</td>
      </tr>
      {% endfor %}
    </tbody>
  </table>

  <div class="modal fade" id="modalExcluir" tabindex="-1" aria-labelledby="tituloModalExcluir" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h2 class="modal-title h5" id="tituloModalExcluir">Excluir usuário</h2>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Fechar"></button>
        </div>
        <form id="formExcluir" action="" method="post">
          <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
          <div class="modal-body">
            <p class="mb-0">Excluir o usuário <strong id="nomeExcluir"></strong>? Esta ação não pode ser desfeita.</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">Cancelar</button>
            <button type="submit" class="btn btn-danger">Excluir</button>
          </div>
        </form>
      </div>
    </div>
  </div>
{% endblock %}

{% block scripts %}
<script>
  function prepararExclusao(id) {
    const nome = document.getElementById('nome_usuario_' + id).textContent;
    document.getElementById('nomeExcluir').textContent = nome;
    document.getElementById('formExcluir').action = '/usuarios/' + id + '/excluir';
  }
</script>
{% endblock %}
```

A única mudança nos layouts é o `'editar_usuario'` na lista do menu **Usuários**, no `base_menu.html` (Tópico 1). Os demais arquivos (`db.py`, `validacoes/validacoes_perfil.py`, `login.html`, `dashboard.html`, `perfis_lista.html`, `perfil_form.html`, `usuario_detalhe.html`, `_badge_perfil.html`, `404.html`, `500.html`, `estilo.css`, `testar_conexao.py`) são os do Capítulo 15.

---

## 📦 Código deste capítulo

Compare com o seu projeto, ou use como ponto de partida do próximo capítulo. O zip tem o `app.py`, o `db.py`, a pasta `validacoes`, o `testar_conexao.py`, o `banco.sql`, o `.env.example`, o `.gitignore`, o `requirements.txt`, a pasta `templates` (`layout/base_menu.html`, `layout/base_limpa.html`, `login.html`, `dashboard.html`, `perfis/perfis_lista.html`, `perfis/perfil_form.html`, `usuarios/usuarios_lista.html`, `usuarios/usuario_form.html`, `usuarios/usuario_detalhe.html`, `usuarios/_badge_perfil.html`, `404.html` e `500.html`) e a pasta `static` (`estilo.css`). O ambiente virtual e o `.env` **não** vão no zip: depois de descompactar, crie o ambiente com os três comandos do Capítulo 3 e rode `copy .env.example .env`, trocando os marcadores `SUA_SENHA_AQUI` e `NOME_BANCO_DADOS` como no Capítulo 11. O banco também não vai dentro do zip: importe o `banco.sql`, cadastre os três perfis e os três usuários pelo formulário.

➡️ [Baixar p2_cap_16.zip](../arquivos/p2_cap_16.zip)

---

## 🃏 Flashcards de Revisão

Tente responder mentalmente antes de abrir.

??? question "Como a linha do banco serve de dicionário para o formulário de edição, sem conversão?"
    As chaves do `SELECT_USUARIO` têm os mesmos nomes dos campos do formulário. Os opcionais `NULL` chegam como `None`, e o `or ''` do template os mostra vazios (sem ele, a palavra "None" iria para dentro do campo). O `perfil_id` chega como número, e o `|string` dos dois lados da comparação marca a opção certa do `<select>`.

??? question "Por que o `SELECT` do e-mail e do CPF repetidos leva `AND id_usuario <> %s`?"
    Porque, ao editar, o usuário já existe com aquele e-mail e aquele CPF. Sem o `<>`, quem corrigisse só o celular do Bruno receberia "Já existe um usuário com este e-mail", barrado por ele mesmo. Com o `<>`, o `SELECT` ignora o registro que está sendo editado. No cadastro, a rota passa `0`, um código que não existe, e a condição não exclui ninguém.

??? question "Como funciona a senha opcional na edição?"
    Os campos de senha em branco significam "manter a atual": a conferência da senha é pulada e a coluna `senha` nem entra no `UPDATE`. Preenchidos, passam por `validar_senha`, e a coluna entra no comando com o **hash** da senha nova (`generate_password_hash`). Nunca se grava a senha digitada, e a senha nunca volta ao formulário.

??? question "Por que montar o `UPDATE` com `sql +=` e `params.append` é seguro?"
    Porque o que se acrescenta ao texto do SQL são pedaços fixos, escritos no código (`', senha = %s'`, `' WHERE id_usuario = %s'`). Tudo o que a pessoa digitou vai na lista `params`, e o conector troca cada `%s` por um valor com segurança. O que nunca se faz é juntar ao texto do SQL o que veio do formulário.

??? question "Por que, no POST da edição, o `dados` deixa de ser a linha do banco e passa a ser o dicionário do formulário?"
    Porque, quando há erro, a rota não faz `redirect`: ela mostra o formulário de novo. Se o `dados` continuasse sendo a linha do banco, quem corrigiu quatro campos e errou o e-mail perderia tudo. Com o dicionário do formulário, ele volta com o que foi digitado, ainda em modo de edição. Quando a edição dá certo, a rota termina no `redirect`.

??? question "Por que a exclusão de usuário não conta nada antes nem captura o erro `1451`, como a de perfil?"
    Porque nenhuma outra tabela aponta para `usuarios` por chave estrangeira. O erro `1451` só acontece quando outras linhas dependem da que se quer apagar, como os usuários dependem do perfil. Sem dependentes, o `DELETE` não tem o que recusar. Os cuidados que continuam são os de toda exclusão: só `POST`, `WHERE id_usuario = %s` e o modal de confirmação.

---

## ✅ Quiz de Fixação

<quiz>
Na edição de um usuário, as duas caixas de senha ficam em branco e a pessoa clica em **Salvar alterações**. O que acontece?
- [ ] O navegador não deixa enviar, porque a senha é obrigatória
> Não. Na edição o `required` das caixas de senha não existe (só no cadastro), justamente porque a senha atual não pode ser mostrada.
- [ ] A senha do usuário é apagada e passa a ser vazia
> Não. A coluna `senha` é `NOT NULL`, e a rota nem a inclui no `UPDATE` quando as caixas estão vazias.
- [x] Os outros campos são atualizados, e o hash da senha atual continua o mesmo
> Correto. A validação só confere a senha quando algo foi digitado, e o `if dados['senha']` da rota só acrescenta `senha = %s` ao comando nesse caso.
- [ ] A rota grava o hash de um texto vazio
> Não. O `generate_password_hash` só é chamado dentro do `if`, quando há senha digitada.
</quiz>

<quiz>
Quais afirmações sobre o `UPDATE` montado com `sql +=` e `params.append` estão corretas? (selecione todas que se aplicam)
- [x] Os pedaços acrescentados ao texto do SQL são fixos, escritos no código
> Correto. `', senha = %s'` e `' WHERE id_usuario = %s'` não dependem do que a pessoa digitou.
- [x] Os valores digitados vão na lista `params`, e o conector troca cada `%s` por um valor com segurança
> Correto. É o mesmo princípio de todas as consultas do projeto.
- [x] O `WHERE` é acrescentado por último, depois do pedaço opcional da senha
> Correto. O `WHERE` tem de vir depois de tudo o que está no `SET`; por isso ele não está no primeiro texto.
- [ ] Como a senha vira hash, ela pode ser colocada direto no texto do SQL com uma f-string
> Não. Nenhum valor do formulário vai para o texto do SQL. O hash vai em `params`, como todos os outros valores.
</quiz>

<quiz>
O Bruno corrige só o celular dele e envia o formulário com o próprio e-mail e o próprio CPF. A conferência de repetidos não usa o `id_usuario <> %s`. O que acontece?
- [ ] A edição é aceita, porque o e-mail é dele
> Não. Sem o `<>`, o `SELECT` encontra a linha do próprio Bruno.
- [x] A rota acusa "Já existe um usuário com este e-mail", barrada pelo próprio registro
> Correto. O `id_usuario <> %s` serve para o `SELECT` ignorar o registro que está sendo editado.
- [ ] O banco apaga o registro antigo e cria um novo
> Não. O `UPDATE` não apaga nada, e o banco nem chega a ser consultado para gravar.
- [ ] A página 500 aparece
> Não. É uma conferência da `validar_usuario`, que devolve uma mensagem de erro na lista de erros.
</quiz>

<quiz>
Por que a rota `excluir_usuario` não conta registros antes do `DELETE` nem trata o erro `1451`, como a `excluir_perfil`?
- [ ] Porque o `DELETE` de usuário ignora as chaves estrangeiras
> Não. O banco sempre respeita as chaves estrangeiras.
- [ ] Porque o erro `1451` só existe no `UPDATE`
> Não. Ele aparece justamente ao tentar excluir uma linha de que outras dependem, como o perfil.
- [x] Porque nenhuma outra tabela aponta para `usuarios`, então não há linhas dependentes que o banco possa recusar
> Correto. O `1451` vem de uma chave estrangeira. Os usuários dependem do perfil, mas nada depende do usuário.
- [ ] Porque a exclusão de usuário é feita por `GET`
> Não. A exclusão aceita só `POST`, pelos mesmos motivos de segurança do perfil.
</quiz>

---

## 📝 Resumo

O recurso `usuarios` ficou completo, com o **Editar** e o **Excluir** na própria lista. A edição reaproveita o `usuario_form.html` com a variável `acao`, e o formulário abre preenchido com a própria linha do banco, graças ao `or ''` e ao `|string` que ele já tinha. A `validar_usuario` ganhou o `id_usuario`, com valor padrão `0`: ele faz o e-mail e o CPF ignorarem o próprio usuário e torna a senha opcional na edição. O `UPDATE` é montado aos poucos: o texto do SQL cresce só com pedaços fixos, os valores vão na lista `params`, e a coluna `senha` entra só quando uma senha nova é digitada, sempre como hash. Quando há erro, o dicionário do formulário devolve o que foi digitado, ainda em modo de edição. A exclusão aceita só `POST` e pede confirmação em um modal preenchido por uma função que recebe o código; como nada depende de `usuarios`, ela não conta registros nem trata o erro `1451`. O Capítulo 17 usa o hash guardado no banco para a pessoa entrar no sistema.

---

## 🔗 Navegação

⬅️ [Capítulo 15 — SELECT relacional de usuário](Capitulo_15_SELECT_Relacional_de_Usuario.md) · ➡️ [Capítulo 17 — Login](Capitulo_17_Login.md)

---

*Fatec Jahu · ILP951 · Prof. Ronan Adriel Zenatti · 2026*
