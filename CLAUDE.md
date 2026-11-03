# CLAUDE.md — Programação para Internet (ILP951) — 2º Semestre/2026

Este repositório é o guia de estudos da disciplina ILP951 (Fatec Jahu), servido como site
estático via **MkDocs Material + GitHub Pages**. O professor (Ronan) é a única autoridade
sobre conteúdo pedagógico; este arquivo governa como o Claude Code se comporta ao lidar com
o repositório, não substitui o julgamento dele.

> ⚠️ **Regra inegociável: nunca corte ou resuma conteúdo original para economizar
> espaço/tempo/tokens.** Texto que o professor entregar é preservado por completo ao ser
> remodelado: só se adicionam seções ao redor. O mesmo vale para qualquer trecho de `old/` que
> você **decidir aproveitar** (ver "Conteúdo anterior em `old/`"): entra inteiro ou fica de
> fora, nunca pela metade. Edições no texto original só com autorização explícita do
> professor, e mesmo assim para corrigir, nunca para encurtar. Se não for possível fazer algo
> com qualidade completa, **diga isso explicitamente** em vez de entregar uma versão resumida,
> incompleta ou malfeita.

## Sobre a disciplina

- **Sigla:** ILP951 · **Curso:** Tecnologia em Gestão da Tecnologia da Informação (GTI)
- **Carga horária:** 80 horas-aula. Cada capítulo é a base de **uma aula de 180 minutos**.
- **Papel do site:** **guia de estudos** do conteúdo. **Nunca mencione trabalhos, avaliações,
  provas, notas, simulados ou recuperação** em nenhum texto.
- **Público:** alunos com **pouca habilidade de programação**. Fizeram um curso básico de
  Python antes (não dominam funções, listas, dicionários, `try/except`) e aprenderam banco
  de dados em outro semestre (SQL, `JOIN`, DDL). O objetivo **não é formar excelentes
  programadores**, e sim alunos que consigam fazer pequenos projetos sozinhos.
- **Stack:** Python, Flask, Jinja2, Bootstrap 5, MySQL (MariaDB do **XAMPP**, gerenciado
  pelo phpMyAdmin), **`mysql-connector-python` com pool de conexões**, `Flask-WTF` (somente
  `CSRFProtect`, sem WTForms), `python-dotenv` (a partir do Capítulo 11), Git/GitHub.
- **Não há deploy.** O Capítulo 20 (publicação) aparece como "🔒 Em breve", sem arquivo e sem
  entrada no `nav`. Fotos de produto são gravadas em disco.

## Terminologia

- **Capítulo** é a unidade de conteúdo (1 a 20 e os subcapítulos: 2.1, 12.1, 13.1, 17.1,
  18.1 a 18.4). **Tópico** é cada seção interna de um capítulo (`## Tópico 3 — ...`).
- Nunca use "aula", "parte" nem "passo" no texto para o aluno. "Horas-aula" (carga
  horária) continua valendo.
- **Projeto 1** (Catálogo de Produtos, Capítulos 1 a 10) e **Projeto 2** (Sistema de Gestão,
  Capítulos 11 a 19). Os projetos são independentes: o Projeto 2 é criado **do zero**.
- **Nunca diga no texto que o aluno fará um capítulo sozinho** (isso vale para o 18). O
  professor diz isso em sala. O Capítulo 18 e seus subcapítulos são tutoriais completos,
  que **ensinam tudo de novo**, sem "veja o Capítulo 12" no lugar da explicação.

## Estilo do texto e do código

- Mantenha o código **simples e fácil**: funções curtas, `if/else` explícito, uma função de
  validação por campo (devolve a mensagem de erro ou `None`), nomes em português claro. Evite
  classes, compreensões de lista/dicionário/conjunto, `lambda`, type hints, `*args`,
  Blueprints e filtros Jinja encadeados. Cada conceito Python é **explicado no primeiro uso**,
  numa caixa curta (o Capítulo 2.1 é uma revisão opcional, não pré-requisito).
- **Ensino incremental:** uma mudança pequena por vez (uma tag, uma rota, um campo). Depois
  de cada incremento, peça para o aluno salvar, rodar e observar o que mudou antes do
  próximo. Só consolide em um bloco completo ao final do tópico, nunca como única forma de
  apresentar o conteúdo.
- **Dor antes do alívio:** onde fizer sentido, deixe o aluno sentir o problema (menu copiado em
  cada página, `if` repetido em cada rota protegida, lista que some ao reiniciar) antes de
  apresentar a solução (herança de template, decorador, banco).
- **Commits:** todo tópico que muda o código termina com um bloco de commit, em português e no
  imperativo:
  ```bash
  git add .
  git commit -m "Adiciona a rota de listagem de produtos"
  ```
  O **primeiro** commit de cada projeto é só local. O **segundo** tópico cria o repositório no
  GitHub e faz `git remote add origin ...` e `git push -u origin main`. Do segundo em diante,
  todo bloco de commit inclui `git push`.
- **JavaScript (Capítulos 1 e 2):** o escopo é só como acionar JS: `<script>` inline e arquivo
  externo, `document.getElementById`, `.value`, `console.log` e disparo por `onclick` ou
  `onsubmit`. A validação fica com os atributos do HTML5 (`required`, `pattern`, `type`). **Não
  entram** `addEventListener` nem condicionais em JS. Única exceção, autorizada pelo professor:
  `evento.preventDefault()` no `onsubmit` do Capítulo 2 (o formulário envia para `#`, e o
  recarregamento limparia o console).
- **Instalação de pacotes:** sempre `pip install pacote`, **sem número de versão** (ex.:
  `pip install mysql-connector-python`). Quem instala é o aluno, e quem fixa as versões é o
  `pip freeze > requirements.txt`. A versão em que o material foi escrito e testado pode ser
  **citada** numa nota ("Versão usada como base"), só para facilitar o diagnóstico de erros
  futuros. Exceção autorizada: o MySQL Workbench, instalado por `winget` com `-v "8.0.47"`
  (a série 26 não é compatível com o MariaDB do XAMPP).
- **Conexão MySQL (Capítulo 10 em diante):** o `db.py` mantém `use_pure: True` (alunos com
  XAMPP e MySQL da Oracle instalados juntos tiveram erros com a extensão C), `time_zone:
  '-03:00'` e `sql_mode` estrito.
- **Segredos:** até o Capítulo 10, a senha do banco e a `secret_key` ficam no código, com aviso
  de que é provisório. O `.env` entra no Capítulo 11. São projetos de sala, sem dados reais.

## Sequência dos capítulos

Cada capítulo lista o que **ensina**. Os subcapítulos são **opcionais**, têm zip próprio, **não
têm quiz** e **nunca são pré-requisito**: o capítulo seguinte parte do zip do número inteiro
(ex.: o 13 parte do zip do 12, e não do 12.1). A única exceção é o 18: o 19 parte do zip do
**18 completo**, que já inclui o que 18.1 a 18.4 produzem.

### Projeto 1 — Catálogo de Produtos (Capítulos 1 a 10)

Produto do Projeto 1: `nome`, `categoria`, `preco`. A lista que começa em memória (7) passa
pela `session` (8) e termina no MySQL (10).

| Cap. | Tema | O que ensina |
|---|---|---|
| 1 | Git, GitHub, HTML5 e CSS | Revisão, parte 1: configurar Git, `init`, `add`, `commit`, `push`, `.gitignore`; HTML5 semântico e CSS básico na página estática do catálogo |
| 2 | Clone, pull, formulário, CSS e JS | Revisão, parte 2: o aluno apaga a pasta do Capítulo 1 e a clona de novo; edita um arquivo no GitHub (pelo site) e faz `git pull`; formulário de produto com CSS e JS mínimo (ver "Estilo") |
| 2.1 | Python essencial (opcional) | Funções, listas, dicionários, `try/except`, f-strings, `import` |
| 3 | Flask | Pasta, venv, `pip install`, **`requirements.txt` com `pip freeze`**, `.gitignore`, rotas, variável de rota (`/produto/<id>`), `render_template`; produtos numa lista Python; `@app.route` como primeiro decorador |
| 4 | Bootstrap com Flask | Navbar, `url_for` (inclusive `static`), `redirect`. O menu é copiado em cada página |
| 5 | Variáveis, filtros, `if`, `for` | Jinja2: lista de produtos com `for`, faixas de preço com `if/elif/else`, filtros. O menu continua duplicado |
| 6 | Templates | `base.html` com `extends` e `block`, `include`, páginas 404 e 500. É o alívio da duplicação |
| 7 | Formulários | GET e POST, `request.form`, tipos de input (text, number, select, radio, checkbox, textarea, date, password, email), PRG. O produto entra numa lista global |
| 8 | Session | `secret_key`, cookie assinado, `session` como **banco temporário**: minicrud de produtos (nome, categoria, preço) com formulário, listagem e exclusão. CSRF com `Flask-WTF`: ativar `CSRFProtect`, ver o erro 400 e acrescentar o `<input type="hidden">` aos formulários |
| 9 | Validação e flash | Validação no servidor (uma função por campo), `flash` com alertas do Bootstrap, formulário que mantém os valores digitados, validação no navegador x no servidor |
| 10 | Banco de dados | XAMPP, phpMyAdmin, importar `produtos_exemplo.sql`, `mysql-connector-python`, `db.py` com pool (`execute_query`, `execute_one`), `SELECT` na lista e `INSERT` pelo formulário |

### Projeto 2 — Sistema de Gestão (Capítulos 11 a 19)

| Cap. | Tema | O que ensina |
|---|---|---|
| 11 | Projeto novo e banco | Checklist do projeto do zero, **enxuto e com links para os capítulos onde cada etapa foi ensinada** (pasta, venv, um único `pip install` com todos os pacotes do projeto, `.gitignore`, `git init`, commit, novo repositório); importar `banco.sql` (**só as três tabelas, sem dados**); `.env` com `python-dotenv` e `.env.example`; `db.py` explicado em detalhe, já com `execute_query`, `execute_one` e `execute_insert` (só escrito, sem inserir dados); `testar_conexao.py`; layout base com Bootstrap e 404/500 |
| 12 | INSERT e SELECT de perfis | Módulos simples (`db.py` com `execute_*`, `validacoes.py`), consultas parametrizadas (`%s`), `flash`, PRG, CSRF, erro `1062` (duplicado). Os alunos criam os perfis **Administrador, Gerente e Usuário** |
| 12.1 | Busca, filtro e paginação (opcional) | `LIKE`, `WHERE 1=1`, `LIMIT`/`OFFSET`, com `perfis_30.sql` (único capítulo em que se popula o banco para ensinar) |
| 13 | UPDATE e DELETE de perfis | Rotas de edição e exclusão por POST, modal de confirmação do Bootstrap, erro `1451` (perfil em uso) demonstrado com um `INSERT` de usuário rodado no phpMyAdmin |
| 13.1 | Soft-delete (opcional) | `deletado_em` (a coluna já existe desde o `banco.sql` do 11, sem `ALTER TABLE`): excluir vira `UPDATE`, restaurar, filtrar os não excluídos |
| 14 | INSERT relacional de usuário | `<select>` de perfis vindo do banco, hash de senha (`generate_password_hash`), validação de CPF, celular, CEP e data em `validacoes.py`, opcionais vazios viram `NULL`, e-mail e CPF únicos |
| 15 | SELECT relacional de usuário | `JOIN` com `perfis`, badges por perfil, página de detalhe, filtros Jinja de data e CPF. A senha nunca é selecionada |
| 16 | UPDATE e DELETE de usuário | Edição com senha opcional, unicidade ignorando o próprio registro, exclusão com modal |
| 17 | Login | `check_password_hash`, `session`, logout, `if 'usuario_id' not in session` em cada rota protegida, menu que muda se logado |
| 17.1 | Controle de permissão (opcional) | `@login_required` e `@perfil_required('Administrador')`, página 403, menu por perfil |
| 18 | CRUD de produtos | Campos que `usuarios` não cobriu: preço (`DECIMAL`, `Decimal`, "1.234,56", filtro `moeda`), estoque, textarea, `ativo` (checkbox), foto (upload, `secure_filename`, extensão e tamanho, gravada em disco, caminho no banco) |
| 18.1 a 18.4 | INSERT, SELECT, UPDATE, DELETE de produtos | Quatro arquivos que dividem o capítulo 18; cada um com zip intermediário |
| 19 | Relatórios | Só tabelas: usuários por perfil (`LEFT JOIN` + `GROUP BY`), por UF, cadastros por mês (`DATE_FORMAT`), `SUM` do estoque e do valor, preço médio, estoque baixo. Usa `relatorios_dados.sql` |
| 20 | Publicação | 🔒 **Em breve** (sem arquivo e fora do `nav`) |

## Banco de dados do Projeto 2

O banco se chama `gestao` (Projeto 1: `catalogo`). O `banco.sql` do Capítulo 11 **só cria as
tabelas**, com `perfis` antes de `usuarios` por causa da chave estrangeira. **Não popula nada:**
os alunos criam perfis e usuários pelo próprio sistema.

```sql
-- DROP DATABASE IF EXISTS gestao;   -- o aluno tira o "--" só se quiser recomeçar do zero

CREATE DATABASE IF NOT EXISTS gestao
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE gestao;

CREATE TABLE IF NOT EXISTS perfis (
    id_perfil     BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nome          VARCHAR(100) NOT NULL UNIQUE,
    descricao     VARCHAR(255),
    criado_em     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deletado_em   DATETIME NULL                         -- soft-delete (Capítulo 13.1)
);

CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario      BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nome            VARCHAR(255) NOT NULL,
    email           VARCHAR(255) NOT NULL UNIQUE,
    senha           VARCHAR(255) NOT NULL,      -- guarda o HASH, nunca a senha
    celular         VARCHAR(20),
    data_nascimento DATE,
    cpf             VARCHAR(14) UNIQUE,         -- gravado como 000.000.000-00
    perfil_id       BIGINT UNSIGNED NOT NULL,
    cep             VARCHAR(9),
    endereco        VARCHAR(255),
    numero          VARCHAR(20),
    complemento     VARCHAR(100),
    cidade          VARCHAR(100),
    estado          CHAR(2),
    criado_em       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em   TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deletado_em     DATETIME NULL,                      -- soft-delete (Capítulo 13.1)
    CONSTRAINT fk_usuarios_perfis
        FOREIGN KEY (perfil_id) REFERENCES perfis (id_perfil)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS produtos (
    id_produto    BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nome          VARCHAR(255) NOT NULL,
    descricao     TEXT,
    categoria     VARCHAR(100),
    preco         DECIMAL(10,2) NOT NULL,
    estoque       INT UNSIGNED NOT NULL DEFAULT 0,
    foto          VARCHAR(255),                 -- caminho do arquivo gravado em disco
    ativo         TINYINT(1) NOT NULL DEFAULT 1,
    criado_em     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

`ativo` existe **só em `produtos`**; `deletado_em` só em `perfis` e `usuarios`. No caminho
principal a exclusão é `DELETE` de verdade; `deletado_em` só é usado no Capítulo 13.1.

> ⚠️ **Nunca use `ALTER TABLE` em nenhum ponto do material do curso.** O `banco.sql` do
> Capítulo 11 já traz todas as colunas que qualquer capítulo vá usar (inclusive `deletado_em`),
> e os capítulos seguintes só fazem `INSERT`, `SELECT`, `UPDATE` e `DELETE`. Se um capítulo
> precisar de uma coluna nova, ela entra no `banco.sql`, não num `ALTER`.

O `banco.sql` usa `CREATE ... IF NOT EXISTS` (importar de novo **não apaga nada**) e traz, na
primeira linha, `-- DROP DATABASE IF EXISTS gestao;` comentado: o aluno tira o `--` só se
quiser recomeçar do zero.

**Dados prontos para baixar** (únicos casos em que o banco é populado, todos em
`docs/arquivos/`): `produtos_exemplo.sql` (Capítulo 10, banco `catalogo` com a tabela mínima
`produtos` com `nome`, `categoria` e `preco`, e algumas linhas), `perfis_30.sql` (12.1) e
`relatorios_dados.sql` (19, usuários e produtos com datas de cadastro espalhadas por vários
meses). Os `.sql` de dados usam `INSERT IGNORE` e buscam o `id_perfil` pelo nome, para
funcionarem seja qual for o `id` que o aluno gerou.

**Convenções (mantenha em todo capítulo do Projeto 2):**

- Tabelas no **plural**, chave primária `id_<singular>`, chave estrangeira `<singular>_id`.
  Rotas `/perfis`, `/perfis/novo`, `/perfis/<int:perfil_id>`, `.../editar`, `.../excluir`;
  funções `lista_perfis`, `perfil_novo`, `perfil_editar`, `perfil_excluir`; templates
  `perfis.html`, `perfil_form.html`. O mesmo molde para `usuarios` e `produtos`.
- **Senha: sempre hash** (`werkzeug.security`). Nunca em texto puro, nunca em `print` ou log,
  nunca devolvida ao formulário. As telas leem usuários por um `SELECT_USUARIO` que **deixa
  `senha` de fora**; só o login lê o hash.
- **O que é `NOT NULL` no banco é obrigatório no formulário**; o que aceita `NULL` é opcional,
  mas validado se preenchido (campo opcional vazio vira `NULL`, não `''`).
- `UNIQUE` (nome do perfil, e-mail, CPF): o app confere por `SELECT` (mensagem amigável) e o
  banco continua sendo a barreira final. Na edição, ignore o próprio registro.
- O `<select>` de perfil sempre vem de `SELECT ... FROM perfis`, e o servidor valida o valor.
- Organização: `app.py` (rotas), `db.py` (pool e `execute_query`, `execute_one`,
  `execute_insert`, no padrão do conteúdo antigo), `validacoes.py` (CPF, celular, CEP, preço).
- SQL sempre parametrizado (`%s`). Nunca monte SQL com f-string.

## Conteúdo anterior em `old/`

`old/` guarda o curso anterior (um projeto único `usuarios`/`perfis`): `old/docs/aulas/`
(Aulas 01 a 05, 07 e 08, gabaritos e apoio), `old/docs/atividades/`, `old/docs/imgs/`,
`old/mkdocs.yml`, `old/CLAUDE_antigo.md`, `old/templates/` e `old/commands/`. **Não é
publicado** (fica fora de `docs_dir`) e **não é editado**: serve de matéria-prima.

> ⚠️ **`old/` é base, não fonte a copiar.** Se o conteúdo saiu de lá, é porque não foi bom o
> bastante para a nova sequência. Os capítulos novos são escritos **para a nova pegada** (estilo,
> terminologia, projeto e ordem deste arquivo), e `old/` só entra quando **poupa trabalho sem
> perder essa pegada**: um bloco de código que já está certo, uma analogia que funcionou, uma
> lista de comandos. Na dúvida, escreva de novo em vez de adaptar. Aproveitar um trecho é opcional;
> o que for aproveitado segue a regra inegociável (inteiro, nunca pela metade), e **o que ficar
> de fora, ou for reescrito, é dito ao professor** no relatório da Fase 3.

Ao aproveitar texto de `old/`, respeite o estilo e a terminologia deste arquivo (o texto antigo
fala em "Tópico NN", "Passo", selos,
mini-desafios e gabaritos, que **não** entram nos capítulos novos) e use o `db.py` com pool
da `old/docs/aulas/Aula_05_Conexao_MySQL_e_Python.md` como referência de padrão. Para as
imagens antigas, siga a seção "Imagens" (validar a necessidade antes de reaproveitar).

## Stack e comandos

- **MkDocs Material** (`mkdocs.yml` na raiz, `docs_dir: docs`).
- **mkdocs-quiz** (série 1.x, plugin registrado como `mkdocs_quiz`), sintaxe `<quiz>...</quiz>`,
  feedback **por alternativa**, em linhas de citação (`>`) logo após cada `- [ ]`/`- [x]`.
- Flashcards: admonition colapsável nativa do Material (`??? question "..."`).
- Mermaid está habilitado (`pymdownx.superfences`) e serve para diagramas pontuais (ex.:
  `erDiagram` no Capítulo 11). **Não há "mapa mental"** nos capítulos.
- Deploy do site: `.github/workflows/deploy-docs.yml` roda `mkdocs build` e publica no GitHub
  Pages a cada push em `main`.

```bash
python -m venv .venv && source .venv/bin/activate   # no Windows: .venv\Scripts\activate
pip install -r requirements.txt
mkdocs build          # rode SEMPRE antes de considerar um capítulo pronto
mkdocs serve          # preview em http://127.0.0.1:8000
```

## Estrutura

```
templates/CAPITULO_TEMPLATE.md   # gabarito estrutural, fora de docs_dir, não vai para o site
docs/
  index.md                       # home: ementa e sumário por projeto
  capitulos/Capitulo_NN_Titulo.md        # um capítulo por arquivo (subcapítulos: Capitulo_12_1_Titulo.md)
  arquivos/                      # zips (p1_cap_03.zip, p2_cap_12_1.zip) e .sql para download
  imgs/                          # Capitulo_NN_img_NN.png, referenciadas como ../imgs/arquivo.png
projetos/                        # código-fonte de cada etapa (fora do site) e o script que gera os zips
old/                             # curso anterior, só consulta
mkdocs.yml                       # nav EXPLÍCITO: arquivo novo não aparece no site sozinho
```

## Imagens

Imagem é exceção, não regra. Para cada figura que o rascunho ou o texto de `old/` pedir, decida
**nesta ordem**:

1. **É realmente necessária?** Teste: o aluno entende o conceito sem ela? Se um parágrafo, uma
   tabela, um bloco de código ou um diagrama Mermaid explicam igual, **não use imagem**. Prints
   do que o aluno vai ver na própria tela (navegador, terminal, VS Code) em geral dispensam
   figura: o texto diz o que observar. Fica a figura que mostra algo que não se enxerga rodando
   o código (arquitetura, fluxo, relação entre peças).
2. **Alguma imagem de `old/docs/imgs/` serve?** Só serve se o que está **escrito nela** (rótulos,
   comandos, termos) bate com o capítulo, com a terminologia e com a stack atuais (ex.: uma figura
   que cita `git checkout` ou "CRUD completo" não serve para o Capítulo 1). Servindo, **copie**
   para `docs/imgs/` já com o nome padrão e **comprimida** (as originais têm 5 a 7 MB; largura
   máxima de 1400 px, ideal abaixo de ~400 KB). O arquivo em `old/` nunca é alterado.
3. **Nenhuma serve?** Gere o prompt para o **Nano Banana** (ver abaixo) e deixe a imagem já
   inserida no capítulo, com o nome final, mesmo que o arquivo ainda não exista.

**Nome padrão:** `Capitulo_NN_img_NN.png`, em ordem de aparição no capítulo, sem lacunas
(`Capitulo_01_img_01.png`; subcapítulos: `Capitulo_12_1_img_01.png`). Inserção no texto:

```markdown
![Descrição objetiva do que a figura mostra](../imgs/Capitulo_01_img_01.png)
```

O texto alternativo descreve a figura (acessibilidade), nunca é "imagem 1".

**Prompts para o Nano Banana:** um arquivo por capítulo, `projetos/imagens/Capitulo_NN_prompts.md`
(fora do site), com um bloco por imagem pendente:

```markdown
## Capitulo_01_img_03.png
- **Aparece em:** Tópico 2, depois do parágrafo "..."
- **Alt:** Descrição objetiva da figura
- **Prompt:**
  > [ESTILO BASE] + [conteúdo específico, com os textos em português do Brasil entre aspas,
  > na grafia exata, e a proporção 16:9]
```

O **estilo base**, igual em todas as figuras para o site ter um só visual (derivado das imagens
de `old/`): *"Diagrama didático em estilo flat vetorial, fundo branco, traço limpo e uniforme,
sem sombras nem gradientes, setas simples, tipografia sans-serif grande e legível, paleta azul
#1F6FB8, laranja #EE7F1D e verde #5AA23C com cinza neutro, proporção 16:9, sem nenhum texto além
dos indicados."* O prompt lista cada rótulo literalmente, porque o gerador erra acentos quando o
texto fica livre.

**Imagem pendente e `mkdocs build`:** a referência a um arquivo que ainda não existe gera
warning. Esses warnings são **esperados**: liste-os no relatório da Fase 3 (nome do arquivo e
onde entra) para separar do que é erro de verdade. Quando o professor colocar o arquivo em
`docs/imgs/` com o nome indicado, o warning some sozinho, sem editar o capítulo.

## Zips de cada etapa

- Cada capítulo termina com **"📦 Código deste capítulo"** (link para o zip) e o seguinte começa
  com **"📦 Ponto de partida"**, apontando para **o mesmo arquivo**. O Capítulo 1 não tem ponto
  de partida; o 3 parte do zip do 2 (o HTML vira template); o 11 não tem (projeto novo).
- Nomes: `p1_cap_03.zip`, `p2_cap_12_1.zip`. Subcapítulos têm zip próprio.
- Fonte: `projetos/p1/cap_03/`, `projetos/p2/cap_12_1/` etc. Cada pasta é um **retrato completo**
  da etapa (não um diff). Um script em `projetos/` gera os zips; **teste cada etapa antes** de
  empacotar (instalar `requirements.txt`, rodar, abrir as páginas).
- O zip leva `requirements.txt`, `.env.example` e os `.sql` da etapa. **Nunca** leva `.env`,
  `.venv`, `__pycache__` nem a pasta `.git`.

---

## O pipeline: escrevendo ou alterando um capítulo

O professor pede um capítulo diretamente na conversa ou por `/novo-capitulo NN`. Siga as três
fases **nesta ordem**. Não pule a Fase 1.

> ⚠️ **Capítulo e subcapítulos nascem juntos.** Ao pedir o Capítulo X, **todos** os subcapítulos
> X.Y da tabela "Sequência dos capítulos" são processados no mesmo pedido (2 → 2.1; 12 → 12.1;
> 13 → 13.1; 17 → 17.1; 18 → 18.1 a 18.4). Eles entram juntos na Fase 1 (resumo e perguntas
> cobrem cada arquivo), são escritos na Fase 2 e verificados na Fase 3, cada um com o seu zip e
> o seu commit. **Nunca entregue o capítulo deixando o subcapítulo como "🔒 Em breve"**; se não
> for possível entregá-lo com qualidade completa, diga isso explicitamente. Um pedido só do
> subcapítulo (ex.: `/novo-capitulo 2.1`) vale apenas para ele.

### Fase 1 — Validar e perguntar antes de escrever

**Não escreva nada ainda.** Leia a linha do capítulo em "Sequência dos capítulos", o que o
professor tiver enviado, o capítulo anterior já publicado (para calibrar tom e nomes), os
trechos úteis de `old/` e `docs/index.md`. Depois resuma o que entendeu e pergunte, sem
assumir, sempre que houver:

- ambiguidade ou lacuna conceitual (etapa pulada, termo sem definição prévia);
- inconsistência com capítulos anteriores (nomes, convenções, nível de profundidade);
- pré-requisito ainda não coberto;
- imagens: aplique a seção "Imagens" (necessidade, reaproveitamento de `old/`, prompt para o
  Nano Banana) e **apresente a decisão por figura** (usar, reaproveitar ou gerar). Nunca invente
  caminho nem remova a referência em silêncio;
- trecho de `old/` que precisaria ser fatiado, adaptado ou deixado de fora;
- objetivos de aprendizagem pouco claros.

Só avance depois das respostas ou de um "pode aplicar sem ajustes".

### Fase 2 — Escrever

Use `templates/CAPITULO_TEMPLATE.md`. Todo capítulo tem, nesta ordem:

1. Cabeçalho padrão (disciplina, professor, semestre)
2. 🎯 Objetivos do capítulo
3. 📦 Ponto de partida (zip do capítulo anterior)
4. Tópicos numerados, com código em incrementos pequenos e bloco de commit
5. 📦 Código deste capítulo (zip)
6. 🃏 Flashcards (3 a 6)
7. ✅ Quiz (3 a 5 perguntas, ao menos uma de múltipla resposta)
8. 📝 Resumo
9. 🔗 Navegação. **Só linke o capítulo seguinte se o arquivo já existir**; senão escreva
   `🔒 Capítulo NN+1 — em breve.` Ao criar o seguinte, volte e troque o placeholder. O capítulo
   que tem subcapítulo linka os dois (`➡️ Capítulo 2.1 (opcional) · ➡️ Capítulo 3`), e o
   subcapítulo linka o capítulo-pai e o próximo número inteiro.

Subcapítulos omitem o quiz. Depois de escrever, atualize `docs/index.md` (status e link no
sumário) e `mkdocs.yml` (entrada no `nav`, obrigatória).

### Fase 3 — Verificar, empacotar, commitar

1. Rode `mkdocs build` e confirme que **não surgiu** warning novo de link ou imagem.
2. Confira: `md_in_html` continua habilitado (**nunca remova**); todo `<quiz>` tem pelo menos
   um `- [x]` e feedback por alternativa em linhas `>`; toda imagem `../imgs/...` existe, **ou**
   consta em `projetos/imagens/Capitulo_NN_prompts.md` (pendente de geração, ver "Imagens"); o
   zip existe, abre e o projeto roda a partir dele.
3. **Execute o código**, não só leia: no mínimo `ast.parse` dos blocos Python e, para rotas e
   templates, o cliente de teste do Flask contra um banco simulado (SQLite em memória serve
   para rotas, templates e validações). O DDL e o SQL do MySQL/MariaDB são conferidos à mão.
4. **Faça o commit** do capítulo pronto, com mensagem que o identifique (ex.: `Adiciona o
   Capítulo 03 — Flask, com quiz e zip`). Um commit por capítulo e um por subcapítulo.
5. **Não faça `git push` sem avisar.** Pergunte: "o Capítulo NN (e os subcapítulos NN.Y) estão
   commitados, posso enviar para o GitHub?" e só envie depois de um sim claro.

---

## Armadilhas já conhecidas

- **`md_in_html` ausente** faz blocos `<div markdown>` aparecerem como código cru.
- **O plugin de quiz é `mkdocs_quiz` (série 1.x), não `quiz`.** `plugins: - quiz` faz o build
  abortar. Mantenha `plugins: - mkdocs_quiz` e `mkdocs-quiz>=1.7,<2` no `requirements.txt`.
- **O `nav` é explícito.** Arquivo novo não aparece no site até entrar no `nav`.
- **Caminhos de imagem e de zip são relativos** (`../imgs/x.png`, `../arquivos/x.zip` a partir
  de `docs/capitulos/`). Ao mover ou renomear, rode `mkdocs build`.
- **A `.venv` do repositório pode apontar para um Python que não existe mais.** Se
  `mkdocs build` falhar com "did not find executable", recrie o venv.
- Para ver o aviso de fim de vida do Material sumir do log: `NO_MKDOCS_2_WARNING=1`.
