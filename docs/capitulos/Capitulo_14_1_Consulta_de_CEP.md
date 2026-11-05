# Capítulo 14.1 — Consulta de CEP (opcional)

**Disciplina:** Programação para Internet (ILP951)
**Professor:** Ronan Adriel Zenatti · ronan.zenatti@cps.sp.gov.br
**Fatec Jahu — 2º Semestre/2026**

---

## 🎯 Objetivos do Capítulo

Ao final deste capítulo você deverá ser capaz de:

- Explicar o que é uma **API** e o que é o formato **JSON**, usando o serviço ViaCEP como exemplo
- Consultar o ViaCEP pelo navegador e ler a resposta
- Acionar, com o `onclick` de um botão, uma função JavaScript que consulta a API com `fetch` e `await`
- Preencher campos do formulário pelo JavaScript, com `.value`
- Tratar os três desfechos da consulta: CEP encontrado, CEP que não existe e falha na consulta
- Explicar por que o servidor continua conferindo os campos que o JavaScript preencheu

Este capítulo é **opcional**: o Capítulo 15 continua do código do Capítulo 14, e não deste. No Capítulo 14, quem cadastra um usuário com endereço digita tudo à mão: CEP, rua, cidade e estado. Só que o CEP **já determina** a rua, a cidade e o estado, e existe um serviço gratuito que informa esses dados a quem pergunta. Aqui o formulário ganha um botão **Buscar**, que consulta o serviço e preenche o endereço.

Este capítulo usa um pouco mais de JavaScript que o Capítulo 2: aparecem o `if`, o `try/catch`, o `fetch` e o `await`, cada um explicado no primeiro uso. A função continua sendo chamada pelo `onclick` de um botão, como a do modal do Capítulo 13.

## 📦 Ponto de partida

Este capítulo continua do **seu** repositório `sistema-gestao`, como ficou no fim do Capítulo 14, com o cadastro de usuário funcionando.

Se o seu projeto não está funcionando, baixe o código do Capítulo 14 e descompacte. Depois de descompactar, crie o ambiente virtual e o `.env`, como no [Capítulo 11, Tópico 4](Capitulo_11_Projeto_Novo_e_Banco.md#topico-4-o-arquivo-env), importe o `banco.sql` no phpMyAdmin e cadastre os três perfis pelo formulário:

➡️ [Baixar p2_cap_14.zip](../arquivos/p2_cap_14.zip)

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Este capítulo precisa de **acesso à internet** no computador, porque a consulta vai a um serviço de fora.

---

## Tópico 1 — O ViaCEP: um serviço que responde com dados

### Uma "página" feita para programas

Você já conhece dois tipos de resposta de um servidor: uma página HTML, que o navegador desenha, e um arquivo, como o CSS. Existe um terceiro tipo, feito para **programas** lerem: os **dados puros**. Um endereço da internet que, em vez de uma página, devolve dados, chama-se **API**. O **ViaCEP** é uma API pública e gratuita que recebe um CEP e devolve o endereço dele.

Abra, em uma aba do navegador, o endereço abaixo (é o CEP `17201-000`, de Jaú):

```text
https://viacep.com.br/ws/17201000/json/
```

A resposta tem este formato:

```json
{
  "cep": "17201-000",
  "logradouro": "Rua Lourenço Prado",
  "complemento": "",
  "unidade": "",
  "bairro": "Centro",
  "localidade": "Jaú",
  "uf": "SP",
  "estado": "São Paulo",
  "regiao": "Sudeste",
  "ibge": "3525300",
  "gia": "4017",
  "ddd": "14",
  "siafi": "6607"
}
```

Esse formato é o **JSON**. Ele é uma lista de pares `"nome": "valor"` entre chaves, e se parece muito com um dicionário do Python: a chave `"localidade"` guarda `"Jaú"`. O JavaScript lê o JSON e o transforma em um objeto, e o valor de cada campo é acessado com um ponto (`dados.localidade`), como o `perfil.nome` do Jinja.

Troque o CEP no endereço por outro, o da sua casa, e veja a resposta mudar. O ViaCEP devolve muita coisa, e o formulário só precisa de três campos:

| Campo da resposta | Campo do formulário | Observação |
|---|---|---|
| `logradouro` | Endereço | A rua, avenida ou praça |
| `localidade` | Cidade | |
| `uf` | Estado | A sigla, como `SP` |
| `bairro` | (nenhum) | A tabela `usuarios` não tem coluna de bairro, e o projeto não altera a estrutura das tabelas, então o bairro fica de fora |

### Os três desfechos

Nem toda consulta dá certo, e a função precisa saber lidar com cada resultado. Teste no navegador:

| O que se pergunta | Endereço de teste | O que o ViaCEP responde |
|---|---|---|
| Um CEP que existe | `https://viacep.com.br/ws/17201000/json/` | O JSON com o endereço |
| Um CEP com 8 números que **não existe** | `https://viacep.com.br/ws/99999999/json/` | `{"erro": "true"}` |
| Algo que **não é um CEP** (letras, ou tamanho errado) | `https://viacep.com.br/ws/abcdefgh/json/` | Uma página de erro (**400**), que não é um JSON |

O terceiro caso é o que mais atrapalha: a resposta **não é um JSON**, e tentar lê-la como JSON falha. Por isso a função, no Tópico 3, confere o tamanho do CEP antes de perguntar, e ainda protege a leitura contra uma resposta inesperada.

!!! note "Um serviço de fora pode falhar"
    O ViaCEP é mantido por terceiros: ele pode ficar fora do ar, ou o computador pode estar sem internet. Por isso o botão **Buscar** é só uma **ajuda**, e nunca uma exigência. O formulário continua funcionando com o endereço digitado à mão, e o servidor continua conferindo tudo, como no Capítulo 14.

!!! note "Por que a consulta funciona de dentro da sua página"
    Um navegador, por segurança, não deixa uma página consultar dados de outro site, a menos que o outro site **permita**. O ViaCEP permite (a resposta dele traz o aviso `Access-Control-Allow-Origin: *`), e é por isso que a consulta vai funcionar a partir do seu `http://127.0.0.1:5000`.

---

## Tópico 2 — O botão e a função

### O botão e o espaço do aviso

No `templates/usuarios/usuario_form.html`, o CEP e o endereço dividiam uma linha, logo abaixo do título **Endereço (opcional)**. Procure este bloco, o `<div class="row">` que abre com o campo `cep` e fecha depois do campo `endereco`:

```html
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
```

E troque o bloco **inteiro** por este trecho:

```html
<div class="row">
  <div class="col-md-5 mb-3">
    <label for="cep" class="form-label">CEP</label>
    <div class="input-group">
      <input type="text" class="form-control" id="cep" name="cep" placeholder="00000-000" value="{{ dados.cep or '' }}" maxlength="9">
      <button type="button" class="btn btn-outline-secondary" onclick="buscarCep()">Buscar</button>
    </div>
  </div>
  <div class="col-md-7 mb-3 d-flex align-items-end">
    <div id="avisoCep" class="form-text mb-2"></div>
  </div>
</div>

<div class="mb-3">
  <label for="endereco" class="form-label">Endereço</label>
  <input type="text" class="form-control" id="endereco" name="endereco" value="{{ dados.endereco or '' }}" maxlength="255">
</div>
```

Os dois campos continuam com o `or ''` do Capítulo 14. Três detalhes: o botão é `type="button"`, e **não** `type="submit"`, para não enviar o formulário; o `onclick="buscarCep()"` chama uma função que ainda não existe; e o `<div id="avisoCep">` é onde a função vai escrever as mensagens. O endereço ganhou uma linha própria, porque o aviso ocupa o lado do CEP. Salve, recarregue **http://127.0.0.1:5000/usuarios/inserir** e clique em **Buscar**. Nada aparece na tela. Aperte `F12`, abra a aba **Console** e clique de novo: o navegador mostra um erro em vermelho, algo como `buscarCep is not defined`. É esperado: o botão chama uma função que ainda não foi escrita.

### Uma função que lê o CEP

Escreva a função. O `base_menu.html` já tem o `{% block scripts %}`, que o Capítulo 13 usou. No **final** do `usuario_form.html`, **depois** do `{% endblock %}` do conteúdo, acrescente:

```html
{% block scripts %}
<script>
  function buscarCep() {
    const cep = document.getElementById('cep').value.replace('-', '').trim();
    document.getElementById('avisoCep').textContent = 'CEP digitado: ' + cep;
  }
</script>
{% endblock %}
```

!!! note "JavaScript: `const`, `.replace` e `.trim`"
    O `const` cria uma variável que **não muda** depois de receber o valor, como o `nome` do Capítulo 13. O `document.getElementById('cep').value` lê o que está no campo (o `.value` do Capítulo 2). O `.replace('-', '')` troca o hífen por nada, e o `.trim()` tira os espaços das pontas: o CEP `17201-000` vira `17201000`, o formato que o ViaCEP aceita. Um `.metodo()` seguido de outro, em cadeia, aplica um depois do outro, da esquerda para a direita. O `.textContent` escreve texto puro dentro do `<div>` do aviso.

Salve, recarregue, digite `17201-000` no CEP e clique em **Buscar**: ao lado do botão aparece `CEP digitado: 17201000`. A função já lê o campo e fala com a página. Falta perguntar ao ViaCEP.

### Perguntar ao ViaCEP: `fetch` e `await`

Troque a função inteira por esta versão, que faz a consulta e **só mostra o resultado no Console**:

```html
{% block scripts %}
<script>
  async function buscarCep() {
    const cep = document.getElementById('cep').value.replace('-', '').trim();

    const resposta = await fetch('https://viacep.com.br/ws/' + cep + '/json/');
    const dados = await resposta.json();

    console.log(dados);
  }
</script>
{% endblock %}
```

!!! note "JavaScript: `fetch`, `await` e `async`"
    O `fetch(endereço)` faz um pedido a um endereço da internet, como o navegador faz ao abrir uma página. Ele **demora**: a resposta chega depois, pela rede. O `await` diz "espere a resposta chegar antes de seguir para a próxima linha", sem travar a página. Para usar o `await`, a função precisa ser declarada com `async` na frente. O `resposta.json()` lê o corpo da resposta como JSON e o transforma em um objeto, e também precisa de um `await`, porque a leitura também leva um instante. O `'https://viacep.com.br/ws/' + cep + '/json/'` junta pedaços de texto com o `+`, e monta o mesmo endereço que você abriu no navegador no Tópico 1.

Salve, recarregue, abra o **Console** (`F12`), digite `17201-000` e clique em **Buscar**. No Console aparece um objeto (clique na setinha para abri-lo), com `logradouro: 'Rua Lourenço Prado'`, `localidade: 'Jaú'` e `uf: 'SP'`. A consulta funciona, e o formulário ainda não muda.

```bash
git add .
git commit -m "Adiciona o botão Buscar e a consulta do CEP no ViaCEP"
git push
```

---

## Tópico 3 — Preencher o formulário e tratar os erros

### Preencher os campos

Agora a função usa o objeto. Troque o `console.log(dados);` por quatro linhas que escrevem nos campos, e foque o campo do número (que o ViaCEP não sabe):

```html
{% block scripts %}
<script>
  async function buscarCep() {
    const cep = document.getElementById('cep').value.replace('-', '').trim();

    const resposta = await fetch('https://viacep.com.br/ws/' + cep + '/json/');
    const dados = await resposta.json();

    document.getElementById('endereco').value = dados.logradouro;
    document.getElementById('cidade').value = dados.localidade;
    document.getElementById('estado').value = dados.uf;
    document.getElementById('numero').focus();
  }
</script>
{% endblock %}
```

O `.value = ...` **escreve** no campo, o mesmo `.value` que lia o CEP. Em um `<select>`, escrever a sigla (`'SP'`) marca a opção que tem esse `value`. O `.focus()` leva o cursor para o campo do número, para a pessoa continuar digitando. Salve, recarregue e busque `17201-000`: o endereço, a cidade e o estado se preenchem sozinhos, e o cursor pula para o **Número**. Os campos continuam **editáveis**: se a rua estiver diferente, a pessoa corrige.

### Um aviso para quem usa

A pessoa precisa ver o que está acontecendo. Acrescente uma variável para o `<div>` do aviso, logo no começo da função, e as mensagens de "Buscando..." e de sucesso:

```html
{% block scripts %}
<script>
  async function buscarCep() {
    const aviso = document.getElementById('avisoCep');
    const cep = document.getElementById('cep').value.replace('-', '').trim();

    aviso.textContent = 'Buscando...';

    const resposta = await fetch('https://viacep.com.br/ws/' + cep + '/json/');
    const dados = await resposta.json();

    document.getElementById('endereco').value = dados.logradouro;
    document.getElementById('cidade').value = dados.localidade;
    document.getElementById('estado').value = dados.uf;
    aviso.textContent = 'Endereço preenchido. Confira e informe o número.';
    document.getElementById('numero').focus();
  }
</script>
{% endblock %}
```

Salve e busque de novo: aparece `Buscando...` por um instante, e depois `Endereço preenchido. Confira e informe o número.`

### CEP incompleto

E se a pessoa clicar em **Buscar** com o campo vazio, ou com o CEP pela metade? Teste: digite `1720` e clique em **Buscar**. A função pergunta ao ViaCEP mesmo assim, recebe uma resposta que **não é JSON** (o terceiro desfecho do Tópico 1), e o `await resposta.json()` falha. Abra o Console: aparece um erro em vermelho (`Unexpected token '<'`, algo assim), e a página fica com `Buscando...` para sempre. A saída é conferir o tamanho **antes** de perguntar. Acrescente, logo depois da linha do `const cep`:

```javascript
    if (cep.length != 8) {
      aviso.textContent = 'Digite os 8 números do CEP.';
      return;
    }
```

!!! note "JavaScript: `if`, `.length` e `return`"
    O `if (condição) { ... }` executa o bloco só quando a condição é verdadeira, como o `if` do Python, mas com a condição entre parênteses e o bloco entre chaves (sem os dois-pontos). O `cep.length` é o **tamanho** do texto, e o `!=` quer dizer "diferente de". O `return;` **encerra** a função na hora: o que vem depois, a consulta ao ViaCEP, não roda.

Salve e teste `1720`: a mensagem `Digite os 8 números do CEP.` aparece, e a função para antes de consultar. Deixe o campo vazio e clique: a mesma mensagem.

### CEP que não existe

Digite `99999999` e clique em **Buscar**. O CEP tem 8 números, a consulta é feita, e o ViaCEP responde `{"erro": "true"}`. Como esse JSON não traz `logradouro`, os campos recebem o texto `undefined`, e a mensagem de sucesso aparece por engano. Confira o erro **antes** de preencher. Acrescente, logo depois da linha do `const dados`:

```javascript
    if (dados.erro) {
      aviso.textContent = 'CEP não encontrado.';
      return;
    }
```

O `if (dados.erro)` é verdadeiro quando o campo `erro` existe na resposta, e falso quando ele não existe (o caso de um CEP encontrado). Salve e teste `99999999`: `CEP não encontrado.`, e os campos de endereço não são tocados.

### Falha na consulta

Resta a falha de verdade: um CEP com 8 **letras** (`abcdefgh`) passa na conferência do tamanho, mas o ViaCEP responde com o erro 400 e a página de erro, que não é um JSON. O mesmo acontece se a internet cair no meio da consulta. Teste `abcdefgh`: no Console, o mesmo erro vermelho de antes, e o aviso fica em `Buscando...`. O `try/catch` captura o erro e deixa a função responder com uma mensagem. Embrulhe a **consulta e o preenchimento** em um `try`, e acrescente o `catch` no final. A função completa, no seu estado final:

```html
{% block scripts %}
<script>
  async function buscarCep() {
    const aviso = document.getElementById('avisoCep');
    const cep = document.getElementById('cep').value.replace('-', '').trim();

    if (cep.length != 8) {
      aviso.textContent = 'Digite os 8 números do CEP.';
      return;
    }

    aviso.textContent = 'Buscando...';

    try {
      const resposta = await fetch('https://viacep.com.br/ws/' + cep + '/json/');
      const dados = await resposta.json();

      if (dados.erro) {
        aviso.textContent = 'CEP não encontrado.';
        return;
      }

      document.getElementById('endereco').value = dados.logradouro;
      document.getElementById('cidade').value = dados.localidade;
      document.getElementById('estado').value = dados.uf;
      aviso.textContent = 'Endereço preenchido. Confira e informe o número.';
      document.getElementById('numero').focus();
    } catch (erro) {
      aviso.textContent = 'Não foi possível consultar o CEP agora. Preencha o endereço à mão.';
    }
  }
</script>
{% endblock %}
```

!!! note "JavaScript: `try` e `catch`"
    É o `try/except` do Python. O JavaScript executa o bloco do `try`, e, se **qualquer** linha dele der erro (a internet caiu, a resposta não é um JSON), pula para o bloco do `catch` em vez de parar a função. O `(erro)` é o nome dado ao erro capturado, e aqui a função não precisa dele: só avisa a pessoa e a deixa preencher à mão.

Salve e teste os quatro casos, nesta ordem:

1. `17201-000`: o endereço é preenchido.
2. `1720`: `Digite os 8 números do CEP.`
3. `99999999`: `CEP não encontrado.`
4. `abcdefgh`: `Não foi possível consultar o CEP agora. Preencha o endereço à mão.`

Para o último caso de falha, simule a **falta de internet**: no `F12`, abra a aba **Network** (Rede), troque `No throttling` por `Offline`, digite um CEP certo e clique em **Buscar**. A mensagem de falha aparece, e o formulário continua utilizável. Volte a opção para `No throttling`.

### O servidor continua mandando

Cadastre um usuário usando o botão: nome `Diego Alves`, e-mail `diego@exemplo.com`, uma senha, um perfil, o CEP `17201-000`, **Buscar**, o número `25`. No phpMyAdmin, confira que o usuário foi gravado com o CEP `17201-000`, o endereço, a cidade `Jaú` e o estado `SP`. Para o servidor, esses campos são iguais aos que a pessoa digitaria: as mesmas funções de `validacoes/validacoes_usuario.py` do Capítulo 14 conferem tudo, e o `app.py` **não mudou** neste capítulo. Quem desligar o JavaScript, ou usar um navegador sem ele, preenche o endereço à mão e cadastra do mesmo jeito. O JavaScript é uma **comodidade**, e a conferência de verdade continua no servidor.

```bash
git add .
git commit -m "Preenche o endereço pelo CEP e trata CEP incompleto, inexistente e falha na consulta"
git push
```

---

## O arquivo completo do capítulo

Só o formulário mudou neste capítulo. O `app.py`, a pasta `validacoes` e os demais arquivos são os do Capítulo 14.

O `templates/usuarios/usuario_form.html`:

```html
{% extends 'layout/base_menu.html' %}

{% block titulo_aba %}Novo usuário — Sistema de Gestão{% endblock %}

{% block conteudo %}
  <h1 class="h2 mb-4">Novo usuário</h1>

  <div class="row justify-content-center">
    <div class="col-lg-8">
      <div class="card">
        <div class="card-body">

          <form action="{{ url_for('inserir_usuario') }}" method="post">
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
                <label for="senha" class="form-label">Senha</label>
                <input type="password" class="form-control" id="senha" name="senha" required minlength="8" maxlength="128" autocomplete="new-password">
                <div class="form-text">Mínimo de 8 caracteres, com letras e números.</div>
              </div>
              <div class="col-md-6 mb-3">
                <label for="confirmacao" class="form-label">Confirmar a senha</label>
                <input type="password" class="form-control" id="confirmacao" name="confirmacao" required minlength="8" maxlength="128" autocomplete="new-password">
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
              <div class="col-md-5 mb-3">
                <label for="cep" class="form-label">CEP</label>
                <div class="input-group">
                  <input type="text" class="form-control" id="cep" name="cep" placeholder="00000-000" value="{{ dados.cep or '' }}" maxlength="9">
                  <button type="button" class="btn btn-outline-secondary" onclick="buscarCep()">Buscar</button>
                </div>
              </div>
              <div class="col-md-7 mb-3 d-flex align-items-end">
                <div id="avisoCep" class="form-text mb-2"></div>
              </div>
            </div>

            <div class="mb-3">
              <label for="endereco" class="form-label">Endereço</label>
              <input type="text" class="form-control" id="endereco" name="endereco" value="{{ dados.endereco or '' }}" maxlength="255">
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
              <button type="submit" class="btn btn-primary">Salvar usuário</button>
            </div>

          </form>

        </div>
      </div>
    </div>
  </div>
{% endblock %}

{% block scripts %}
<script>
  async function buscarCep() {
    const aviso = document.getElementById('avisoCep');
    const cep = document.getElementById('cep').value.replace('-', '').trim();

    if (cep.length != 8) {
      aviso.textContent = 'Digite os 8 números do CEP.';
      return;
    }

    aviso.textContent = 'Buscando...';

    try {
      const resposta = await fetch('https://viacep.com.br/ws/' + cep + '/json/');
      const dados = await resposta.json();

      if (dados.erro) {
        aviso.textContent = 'CEP não encontrado.';
        return;
      }

      document.getElementById('endereco').value = dados.logradouro;
      document.getElementById('cidade').value = dados.localidade;
      document.getElementById('estado').value = dados.uf;
      aviso.textContent = 'Endereço preenchido. Confira e informe o número.';
      document.getElementById('numero').focus();
    } catch (erro) {
      aviso.textContent = 'Não foi possível consultar o CEP agora. Preencha o endereço à mão.';
    }
  }
</script>
{% endblock %}
```

---

## 📦 Código deste capítulo

Compare com o seu projeto. Este capítulo é opcional, então o **Capítulo 15 não parte deste zip**, e sim do zip do Capítulo 14. O zip tem o `app.py`, o `db.py`, a pasta `validacoes`, o `testar_conexao.py`, o `banco.sql`, o `.env.example`, o `.gitignore`, o `requirements.txt`, a pasta `templates` (com o `usuarios/usuario_form.html` novo) e a pasta `static`. O ambiente virtual e o `.env` **não** vão no zip: crie-os como no Capítulo 11.

➡️ [Baixar p2_cap_14_1.zip](../arquivos/p2_cap_14_1.zip)

---

## 🃏 Flashcards de Revisão

Tente responder mentalmente antes de abrir.

??? question "O que é uma API, e o que é JSON?"
    Uma API é um endereço da internet que devolve **dados**, e não uma página, para os programas lerem. O JSON é o formato mais comum desses dados: pares `"nome": "valor"` entre chaves, parecidos com um dicionário do Python.

??? question "O que fazem o `async` e o `await` na função `buscarCep`?"
    O `fetch` demora, porque a resposta chega pela rede. O `await` faz a função **esperar** a resposta antes de seguir para a próxima linha, sem travar a página, e só pode ser usado em uma função declarada com `async`.

??? question "Por que a função confere o tamanho do CEP antes de consultar o ViaCEP?"
    Porque um CEP incompleto faz o ViaCEP responder com uma página de erro que não é JSON, e a leitura falha. Conferir `cep.length != 8` antes poupa a consulta e dá à pessoa uma mensagem clara.

??? question "Para que serve o `try/catch` na função?"
    Para o caso em que algo dá errado e a função não previu: a internet cai, o serviço sai do ar, a resposta não é JSON. Sem ele, a função morre em silêncio e o aviso fica em "Buscando...". Com ele, a pessoa lê uma mensagem e preenche o endereço à mão.

??? question "Se o JavaScript preenche o endereço, por que o servidor ainda valida os campos?"
    Porque o navegador é controlado por quem o usa: o JavaScript pode ser desligado, e os campos podem ser alterados antes do envio. O servidor não sabe se o endereço veio do ViaCEP ou foi digitado, e confere tudo da mesma forma. O botão é uma comodidade, e não uma garantia.

---

## 📝 Resumo

O botão **Buscar** consulta o ViaCEP, uma API pública que responde em JSON, e preenche o endereço, a cidade e o estado do formulário. A função `buscarCep` é chamada pelo `onclick`, usa `fetch` e `await` para perguntar, e confere os três desfechos: o CEP incompleto (antes de consultar), o CEP inexistente (o campo `erro` da resposta) e a falha de rede (o `try/catch`). Como o serviço é de terceiros e o JavaScript pode ser desligado, nada mudou no servidor: o `app.py` e a pasta `validacoes` continuam conferindo o que chega, e o formulário continua funcionando com o endereço digitado à mão.

---

## 🔗 Navegação

⬅️ [Capítulo 14 — INSERT relacional de usuário](Capitulo_14_INSERT_Relacional_de_Usuario.md) · ➡️ [Capítulo 15 — SELECT relacional de usuário](Capitulo_15_SELECT_Relacional_de_Usuario.md)

---

*Fatec Jahu · ILP951 · Prof. Ronan Adriel Zenatti · 2026*
