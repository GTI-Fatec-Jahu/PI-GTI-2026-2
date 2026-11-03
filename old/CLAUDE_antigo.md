# CLAUDE.md — Programação para Internet (ILP951) — 2º Semestre/2026

Este repositório é o material publicado da disciplina ILP951 (Fatec Jahu), servido como
site estático via **MkDocs Material + GitHub Pages**. O professor (Ronan) é a única
autoridade sobre conteúdo pedagógico, este arquivo governa como o Claude Code deve se
comportar ao lidar com o repositório, não substitui o julgamento dele.

> ⚠️ **Regra inegociável: nunca corte ou resuma conteúdo original para economizar
> espaço/tempo/tokens.** Se o texto de uma aula já existe (seja um rascunho novo do
> professor, seja o conteúdo herdado do repositório do 1º semestre, ver seção
> "Conteúdo herdado do 1º semestre" abaixo), ele é preservado por completo ao
> remodelar, só se adicionam seções novas ao redor (mapa mental, flashcards, quiz,
> conquista). Edições no texto original só são permitidas quando o professor autorizar
> explicitamente, e mesmo assim devem ser cautelosas (corrigir, não encurtar). Se em
> algum momento não for possível fazer algo com qualidade completa, **diga isso
> explicitamente ao professor** em vez de entregar uma versão resumida, incompleta ou
> malfeita.

## Sobre esta disciplina

- **Sigla:** ILP951 · **Curso:** Tecnologia em Gestão da Tecnologia da Informação (GTI)
- **Carga horária:** 80 aulas presenciais (20 encontros de 4 horas-aula)
- **Stack ensinada:** Python, Flask, Jinja2, Bootstrap 5, MySQL, Git/GitHub
- **Avaliações:** Trabalho 1 (estrutura de rotas e interface, entregue na Aula 9) e
  Avaliação P1 teórica com apresentação do T1 (Aula 10); Trabalho 2 (validação final e
  deploy, iniciado na Aula 17) e Avaliação P2, projeto final (Aula 18); Avaliação
  Substitutiva (Aula 19), que recupera a nota de P1 ou P2.

## Terminologia nas interfaces dos alunos: "tópico", não "aula"

A turma não acompanhou a programação semanal, então "aula" deixou de fazer sentido para
quem lê o site. **Em tudo que o aluno vê** (site, `nav`, `index.md`, README, páginas de
atividades, gabaritos, mensagens de commit de exemplo dentro do conteúdo) use **"tópico"**,
no masculino ("este tópico", "o próximo tópico", "Tópico 06", "Conquista do Tópico").
"Horas-aula" (carga horária) e "encontros" continuam valendo.

- **Nomes de arquivo, pastas e imagens não mudam:** `docs/aulas/Aula_NN_*.md`,
  `gabaritos/Aula_NN_gabarito.md`, `docs/imgs/Aula_NN_img_*.png`. O prefixo `Aula_` é só
  identificador interno. **A numeração dos tópicos é contínua e independente do número do
  arquivo** (não há lacunas na interface). Mapa atual: Tópicos 1 a 5 = `Aula_01` a
  `Aula_05`; Tópico 6 = `Aula_07_*.md`; Tópico 7 = `Aula_08_*.md`. Os próximos seguem
  a ordem do Sumário do `index.md` (Bloco 2: Tópico 8 = antiga Aula 11, 9 = Aula 12,
  10 = Aula 14, 11 = Aula 15, 12 = Aula 16, 13 = Aula 17, 14 = Aula 20), mas o número
  do arquivo continua o do planejamento.
- Neste arquivo e nos prompts, "aula" segue como atalho para a unidade de conteúdo. A
  regra vale para o **texto produzido** para o aluno, inclusive os templates em
  `templates/`.
- **Trabalhos, simulados e avaliações ficam só em `docs/atividades/`.** Eles não são
  tópicos: não entram na Trilha do `index.md` nem no Sumário de tópicos (as antigas Aulas
  6, 9, 10, 13, 18 e 19 do planejamento). Como a numeração dos tópicos é
  contínua, essas lacunas não aparecem na interface, e os selos associados a elas (ver
  tabela de gamificação, que usa os números do planejamento) não são usados.
- **Sumário sem datas:** a tabela do `index.md` não tem coluna de data.

## Conteúdo herdado do 1º semestre

A disciplina já tem um repositório do 1º semestre de 2026 com 15 aulas escritas em
prosa corrida (sem gamificação, sem mapa mental, sem quiz). Esse conteúdo é a base
real da matéria, o professor já validou a didática e a progressão pedagógica nele.

- **Aulas com base direta a remodelar:** 1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 15.
  O texto teórico e os exemplos de código já existem, o trabalho aqui é aplicar o
  pipeline deste arquivo (mapa mental, flashcards, quiz, conquista) preservando o
  conteúdo original por completo.
- **O domínio dos exemplos herdados muda.** O 1º semestre usava outro domínio nos
  exemplos; no 2º semestre toda aula remodelada usa `usuarios`/`perfis` (seção "Domínio do
  CRUD"). A teoria e a didática herdadas permanecem; o que não couber no novo domínio vai
  para `docs/aulas/apoio/`, e nada é descartado.
- **Aula 14 (2º semestre) funde duas aulas do 1º semestre** (Visualização
  Mestre-Detalhe + Segurança e Registro). Ao processá-la, combine o conteúdo das duas
  fontes sem cortar nenhuma das duas, e pergunte ao professor se a ordem de fusão faz
  sentido antes de aplicar.
- **Aulas sem base no 1º semestre, conteúdo novo:** 6 e 13 (trabalho prático
  individual da Calculadora de IMC, ver "Padrão dos trabalhos práticos individuais"
  abaixo), 16 (IV Congresso de Tecnologia, evento institucional, sem conteúdo de aula
  no sentido tradicional), 17, 18, 19 e 20 (relatórios/T2, avaliação P2, substitutiva
  e encerramento). Para essas, calibre tom e profundidade pelas aulas vizinhas já
  remodeladas, e trate como qualquer rascunho novo na Fase 1 do pipeline.

### Padrão dos trabalhos práticos individuais (Aulas 6 e 13)

O repositório do 1º semestre tem dois exemplos desse formato (`A1_Calculadora_Gorjeta`
e a atividade `P1_Avaliacao`, um simulador de custo de viagem): um enunciado sem dicas
nem código pronto, pedindo uma aplicação Flask com formulário, cálculo no back-end,
classificação do resultado em faixas nomeadas, estilização com Bootstrap e código
versionado no GitHub. As Aulas 6 e 13 do 2º semestre seguem exatamente esse padrão
(calculadora de IMC, e depois sua evolução com histórico em banco de dados). Escreva o
enunciado dessas aulas com o mesmo nível de detalhe e o mesmo tom, como um roteiro de
etapas claras, nunca como uma atividade "menor" ou de preenchimento.

## Domínio do CRUD: `usuarios` e `perfis` (tabela auxiliar)

O sistema que a turma constrói em aula é um **CRUD de usuários, cada um com um perfil**
guardado em uma tabela auxiliar. Todos os exemplos de banco, rotas, templates e
validações do semestre (Tópico 05 em diante) usam esse domínio. O exemplo antigo
(`produto`) saiu do texto principal e vive só em material de apoio (ver abaixo), e na
lista fixa do Tópico 03, que é exemplo de Jinja2 e não usa banco.

**Esquema oficial** (definido pelo professor; criado pelo `db_setup.py` do Tópico 05,
com `perfis` antes de `usuarios` por causa da chave estrangeira):

```sql
CREATE TABLE perfis (
    id_perfil     BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nome          VARCHAR(100) NOT NULL UNIQUE,
    descricao     VARCHAR(255),
    criado_em     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE usuarios (
    id_usuario      BIGINT AUTO_INCREMENT PRIMARY KEY,
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
    CONSTRAINT fk_usuarios_perfil FOREIGN KEY (perfil_id) REFERENCES perfis (id_perfil)
        ON DELETE RESTRICT   -- acrescentado ao DDL original do professor (FK desde o CREATE TABLE)
);
```

A coluna `ativo TINYINT(1) NOT NULL DEFAULT 1` **não** está no `CREATE TABLE`: entra pelo
`ALTER TABLE ... ADD COLUMN ativo ... AFTER estado` do Tópico 06 (Parte 3), que preserva a
lição de evoluir uma tabela sem perder dados. Quem recriar o banco do zero precisa
acrescentá-la (os tópicos avisam).

**Dados de exemplo** (`db_setup.py`): perfis `Administrador` (id 1), `Gerente` (id 2) e
`Usuário` (id 3); cinco usuários fictícios (e-mails `@exemplo.com.br`, CPFs válidos),
todos com a senha de teste `Senha@123`, que vai ao banco já como hash. O último usuário
tem colunas opcionais `NULL` de propósito.

**Convenções (mantenha em todo tópico novo):**

- Nomes de tabela no **plural** (`usuarios`, `perfis`), chave primária `id_<singular>`,
  chave estrangeira `<singular>_id`. Rotas `/usuarios`, `/usuarios/novo`,
  `/usuarios/<int:usuario_id>`, `.../editar`, `.../excluir`, `.../reativar`; funções
  `lista_usuarios`, `usuario_novo`, `usuario_detalhe`, `usuario_editar`,
  `usuario_excluir`, `usuario_reativar`; templates `usuarios.html`, `usuario_form.html`,
  `usuario_detalhe.html`. Para `perfis`, o mesmo molde (`/perfis`, `perfil_*`).
- **Senha: sempre hash** (`werkzeug.security.generate_password_hash` /
  `check_password_hash`). Nunca em texto puro, nunca em `print`/log, nunca devolvida ao
  formulário. As telas leem os usuários por `SELECT_USUARIO`, que lista as colunas e
  **deixa `senha` de fora**; só a rota de login (Tópico 11) lê o hash.
- **O que é `NOT NULL` no banco é obrigatório no formulário**; o que aceita `NULL` é
  opcional, mas validado se preenchido (campo opcional vazio vira `NULL`, não `''`).
- E-mail e CPF são `UNIQUE`: o app confere por `SELECT` (mensagem amigável) e o banco
  continua sendo a barreira final. Na edição, comparar o `id` para ignorar o próprio usuário.
- O `<select>` de perfil sempre vem de `SELECT ... FROM perfis` (nunca uma lista fixa em
  Python) e o servidor valida o valor recebido (`int` + existe na tabela).
- Funções puras de formatação e validação (CPF, celular, CEP) ficam em `validacoes.py`;
  acesso ao banco em `db.py`; o `app.py` guarda rotas, filtros Jinja2 e `validar_usuario`.
- Os **mini-desafios** continuam em temas variados (ver regra abaixo) e **não** usam
  `usuarios`/`perfis`, porque o exemplo da aula já é esse domínio.

**Material de apoio com o domínio antigo.** O que o CRUD de `produto` ensinava e não
existe em `usuarios` (tipo `DECIMAL` e agregações numéricas, `Decimal`/`quantize` e `int`
para preço e estoque, filtro Jinja2 `moeda`, badges por faixa de estoque, `ALTER TABLE`
para criar uma categoria, lista fixa de categorias) ficou em `docs/aulas/apoio/`
(`Aula_05_apoio_produto.md`, `Aula_07_apoio_produtos.md`), publicado mas **fora do `nav`**,
como os gabaritos. A aula que perde conteúdo para o apoio cita o arquivo em uma seção
"📎 Material de Apoio", logo antes da Conquista. Ao adaptar o domínio de uma aula nova,
use o que for interessante para `usuarios`/`perfis`, mova o restante para o apoio com
`produto` como exemplo, e **nunca descarte** conteúdo original.

**Plano para o Bloco 2 (proposta; confirme cada ponto com o professor na Fase 1 do
tópico, ele é a autoridade pedagógica):**

| Tópico | Tema | Como entra o domínio `usuarios`/`perfis` |
|---|---|---|
| 8 | Modelagem relacional 1:N | Formaliza o que o aluno já usou: diagrama ER `perfis` 1:N `usuarios`, PK/FK, `ON DELETE`/`ON UPDATE`, `SHOW CREATE TABLE`, `INNER JOIN` x `LEFT JOIN` (perfil sem usuários). A FK já existe desde o Tópico 05: mostre-a e experimente-a, não a "introduza" |
| 9 | CRUD relacional: implementação | CRUD completo de `perfis` no mesmo molde; contagem de usuários por perfil na lista (`LEFT JOIN` + `GROUP BY`); impedir apagar perfil em uso, com mensagem amigável (erro `1451`/`COUNT` prévio) |
| 10 | Mestre-detalhe e segurança de registro | Mestre-detalhe: página do perfil com a lista dos seus usuários. Segurança de registro: auto-cadastro público (`/registro`) que **fixa** o perfil `Usuário` no servidor, nunca aceita `perfil_id` do formulário público; força de senha; CSRF token |
| 11 | Login e controle de sessão | Login por e-mail e senha (`check_password_hash`), `session`, usuário inativo não entra, decoradores `login_required` e `perfil_required('Administrador')`, protegendo `/usuarios` e `/perfis`, logout. Fecha as lacunas apontadas no checklist do Tópico 07 |
| 13 | Relatórios gerenciais | Usuários por perfil, por UF, cadastros por mês, ativos x inativos (`GROUP BY`, `COUNT`, agregações) |
| 14 | Encerramento | Revisão do sistema completo; Trabalho 2 (validação final e deploy) parte desse CRUD |

## Ensino incremental de código (regra de estilo)

O professor forneceu um material de referência de estilo (uma aula de revisão de HTML5
e CSS3) que ainda aplica blocos grandes de código de uma vez. **Não repita esse
padrão.** Ao escrever ou remodelar qualquer explicação de código:

- Introduza uma mudança pequena por vez (uma tag nova, uma rota nova, um campo novo no
  formulário), nunca uma seção inteira pronta de uma vez.
- Depois de cada incremento, peça explicitamente ao aluno para rodar o código e
  observar o que mudou na tela antes de introduzir o próximo incremento (frases como
  "salve o arquivo e recarregue a página, note que...").
- Só junte tudo em um bloco de código completo ao final da seção, como consolidação,
  nunca como a única forma de apresentar o conteúdo.
- Isso vale tanto para aulas remodeladas a partir do conteúdo herdado (que pode
  precisar ser fatiado se estiver em blocos grandes) quanto para conteúdo novo.

## Exercícios de verificação parcial (mini-desafios)

Regra pedagógica complementar à anterior: nunca deixe o aluno acumular vários
conceitos novos sem checar o próprio entendimento até só o quiz do final da aula.
Todo bloco de conteúdo numerado (`## N. [Bloco]` / `## Parte N`) termina com um
mini-desafio prático "🔎 Verifique seu Entendimento":

- **Um mini-desafio por bloco de conteúdo**, não por subtítulo, não fragmente demais.
- **Sempre prático/aplicado**, mesmo em blocos conceituais sem código: peça para
  aplicar o conceito a um cenário concreto (ex.: mapear Model/View/Controller de um
  app real), nunca "explique X" com as próprias palavras (isso é papel do flashcard).
- **Temas atuais de 2026, nunca o óbvio de livro-texto** (chega de biblioteca e
  cadastro de alunos). Varie entre os blocos da mesma aula, sem repetir o mesmo tema
  duas vezes seguidas:
  - IA generativa no dia a dia (assistente de estudos, painel de créditos de uso)
  - Mobilidade urbana (bike-sharing, veículo elétrico, caronas compartilhadas)
  - Sustentabilidade e clima (coleta seletiva, energia solar residencial, pegada de
    carbono de um evento)
  - Cultura pop / eventos de 2026 e economia criativa (ingressos, e-sports, métricas
    de criador de conteúdo, pequeno negócio local)
- **Nunca traga a resposta junto do desafio, nem um link direto para ela.** O
  mini-desafio só aponta para "o gabarito desta aula, no fim da página" — isso é
  proposital, evita que o aluno resolva o exercício só clicando na resposta.
- **Um arquivo de gabarito por aula**, em `docs/aulas/gabaritos/Aula_NN_gabarito.md`
  (gabarito estrutural em `templates/GABARITO_TEMPLATE.md`), um bloco `## Parte N` por
  mini-desafio, na mesma ordem da aula. Fica dentro de `docs/` (é publicado, o link no
  fim da aula funciona) mas **nunca é adicionado ao `nav` do `mkdocs.yml`** — só quem
  tiver o link da aula chega até ele.
- A aula referencia o gabarito **uma única vez**, na seção "📋 Gabarito dos
  Exercícios", a última seção do arquivo (depois de "🔗 Navegação").

## Stack e comandos

- **MkDocs Material** (`mkdocs.yml` na raiz, `docs_dir: docs`)
- **Mermaid** para diagramas, via `pymdownx.superfences` (fence ` ```mermaid `), sem plugin extra
- **mkdocs-quiz** (série 1.x, plugin registrado como `mkdocs_quiz` no `mkdocs.yml`) para
  quizzes interativos, sintaxe `<quiz>...</quiz>`. O feedback é **por alternativa**, em
  linhas de citação (`>`) logo após cada `- [ ]`/`- [x]` (ver "Armadilhas já conhecidas")
- Flashcards via admonition colapsável nativa do Material (`??? question "..."`), sem dependência nova
- Deploy: `.github/workflows/deploy-docs.yml`, roda `mkdocs build` e publica em GitHub Pages a cada push em `main`

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
mkdocs build          # build de produção, rode SEMPRE antes de considerar uma aula pronta
mkdocs serve           # preview local em http://127.0.0.1:8000
```

## Estrutura

```
templates/
  AULA_TEMPLATE.md       # gabarito estrutural, fora de docs_dir, não entra no site
docs/
  index.md              # home do site, ementa, trilha, sumário de aulas
  aulas/
    Aula_NN_Titulo.md    # uma aula por arquivo, adicionada progressivamente pelo professor
    gabaritos/           # Aula_NN_gabarito.md, publicados mas fora do nav
    apoio/               # Aula_NN_apoio_*.md, material de apoio (domínio produto), fora do nav
  imgs/                  # imagens referenciadas pelas aulas (../imgs/arquivo.png)
mkdocs.yml               # nav é EXPLÍCITO, arquivo novo não aparece no site sozinho
```

---

## O pipeline: processando uma aula nova ou alterada em `docs/aulas/`

As aulas chegam **progressivamente**: o professor adiciona ou edita um `.md` em
`docs/aulas/` (em geral conteúdo cru, seja um rascunho novo, seja um arquivo herdado do
1º semestre ainda não remodelado) e pede para processá-lo, seja diretamente na
conversa ou via `/nova-aula caminho/do/arquivo.md`. Sempre que isso acontecer, siga as
três fases abaixo **nesta ordem**. Não pule a Fase 1 mesmo que o conteúdo pareça óbvio
ou já pareça "pronto" (o conteúdo herdado do 1º semestre também passa pela Fase 1).

### Fase 1 — Validar o conteúdo e perguntar antes de aplicar

**Não edite nada ainda.** Primeiro leia:
- o arquivo novo/alterado, por completo;
- pelo menos 1-2 aulas já publicadas em `docs/aulas/`, para calibrar terminologia,
  convenções de nomenclatura (nomes de rotas, variáveis, comandos SQL em maiúsculas,
  etc.) e nível de profundidade já estabelecido;
- `docs/index.md`, para checar se a aula é coerente com a trilha e o bloco em que está.

Depois, escreva um resumo curto do que entendeu e faça perguntas específicas sempre que
houver qualquer um destes casos, não assuma a resposta:

- **Ambiguidade ou lacuna conceitual**: a explicação pula uma etapa, ou um termo é usado
  sem definição prévia.
- **Inconsistência com aulas anteriores**: nomenclatura, convenção de código, ou nível
  de profundidade diferente do padrão já estabelecido.
- **Imagem referenciada que não existe em `docs/imgs/`**: nunca invente o caminho nem
  remova a referência silenciosamente, pergunte se a imagem vem depois ou se o trecho
  deve ser reescrito sem ela.
- **Pré-requisito ainda não coberto**: a aula assume um conceito que ainda não apareceu
  em nenhuma aula publicada até agora.
- **Domínio do exemplo**: se o rascunho ou o conteúdo herdado usa outro domínio (produto,
  cliente, livro...), diga como pretende levá-lo para `usuarios`/`perfis` (ver "Domínio do
  CRUD") e quais trechos, por não terem equivalente, iriam para o material de apoio.
  Confirme antes de aplicar.
- **Exemplos/dados**: se os exemplos numéricos ou o código do rascunho puderem ser
  adaptados para caber melhor em um mapa mental ou flashcard, confirme antes de
  alterá-los, são escolha pedagógica do professor, não só formatação.
- **Objetivos de aprendizagem ausentes**: se o rascunho não deixar claro o que o aluno
  deve saber fazer ao final, pergunte em vez de inventar objetivos genéricos.
- **Conteúdo herdado do 1º semestre com blocos de código grandes demais**: sinalize
  quais trechos você pretende fatiar em incrementos menores (ver "Ensino incremental de
  código" acima) antes de reescrever, já que fatiar muda a apresentação do conteúdo
  original.

Só depois de receber as respostas (ou uma confirmação explícita de "pode aplicar sem
ajustes") siga para a Fase 2.

### Fase 2 — Remodelar com gamificação e múltiplas formas de aprendizagem

Use `templates/AULA_TEMPLATE.md` como estrutura-base. Toda aula remodelada deve
conter, nesta ordem (pule uma seção só se genuinamente não fizer sentido para o
conteúdo, por exemplo aulas que são só enunciado de trabalho, avaliação, ou evento
institucional não precisam de mapa mental):

1. Cabeçalho padrão (disciplina/professor/semestre)
2. 🎯 Objetivos da aula
3. 🗺️ **Mapa mental** — `flowchart LR` com subgraphs por tópico (NÃO o diagrama
   `mindmap` do Mermaid, e NÃO `flowchart TD`, ver "Armadilhas já conhecidas"
   abaixo), resumindo os conceitos antes do detalhe. Gabarito em
   `templates/AULA_TEMPLATE.md`. Para aulas de front-end/rotas, prefira nós que
   representem requisição, rota e resposta; para aulas de banco de dados, um
   `erDiagram` complementar (fora do mapa mental) pode ajudar a mostrar as tabelas.
4. Conteúdo, mantém a didática problema→conceito→exemplo já usada no conteúdo herdado
   do 1º semestre, aplicando a regra de "Ensino incremental de código" acima. Cada
   bloco de conteúdo termina com um mini-desafio de verificação parcial (ver
   "Exercícios de verificação parcial" abaixo)
5. 🃏 **Flashcards de revisão** (3–6 por aula), sintaxe:
   ```
   ??? question "Pergunta objetiva?"
       Resposta curta e direta.
   ```
6. ✅ **Quiz de fixação** (3–5 perguntas, `mkdocs-quiz`), pelo menos uma de múltipla resposta
7. 📝 Resumo
8. 🏆 **Conquista da aula**, selo temático em `!!! success "Selo desbloqueado: ..."`,
   seguindo o **tema de gamificação do semestre** definido abaixo. Isso é reforço
   motivacional impresso na página, não um sistema de pontos real: o site é estático e
   não tem login nem banco de dados, então não há XP persistido entre sessões. Se o
   professor quiser gamificação com estado real (streak, ranking entre alunos), isso
   exige um backend, fora do escopo deste site, sinalize a ele em vez de simular.

   **Tema de gamificação do semestre — "Trilha do(a) Desenvolvedor(a) Full-Stack":** a
   jornada do aluno é enquadrada como uma progressão de carreira em desenvolvimento
   web, do primeiro contato até a entrega de um sistema completo. Cada bloco tem um
   arco, e cada aula um selo dentro dele, mantenha o tom técnico/profissional, nunca
   infantil.
   - **Bloco 1 (Aulas 1–10) — "Trilha do(a) Arquiteto(a) de Aplicações Web"**: Aula 1
     → `🧭 Explorador(a) da Web`, Aula 2 → `🧱 Construtor(a) de Aplicações`, Aula 3 →
     `🗺️ Navegador(a) de Rotas`, Aula 4 → `📨 Mensageiro(a) HTTP`, Aula 5 → `🔌
     Integrador(a) de Dados`, Aula 6 → `🧮 Desenvolvedor(a) Solo`, Aula 7 → `📝 Escriba
     de Dados`, Aula 8 → `🔧 Mantenedor(a) do Ciclo de Vida`, Aula 9 → `📦
     Entregador(a) do T1`, Aula 10 (P1) → `🎖️ Veterano(a) do Bloco 1`.
   - **Bloco 2 (Aulas 11–20) — "Trilha do(a) Engenheiro(a) Full-Stack"**: Aula 11 →
     `🔗 Modelador(a) Relacional`, Aula 12 → `🧩 Mestre das Relações`, Aula 13 → `📊
     Guardião(ã) do Histórico`, Aula 14 → `🛡️ Guardião(ã) das Credenciais`, Aula 15 →
     `🔐 Sentinela de Acesso`, Aula 16 → `🌐 Embaixador(a) Tecnológico(a)`, Aula 17 →
     `📈 Estrategista de Relatórios`, Aula 18 (P2) → `🏆 Desenvolvedor(a) Full-Stack —
     ILP951` (selo final, o sistema completo foi entregue e apresentado aqui, não na
     Aula 20), Aula 19 → `🔁 Revisor(a) Geral`, Aula 20 → `🎓 Ciclo Completo`.
   - Ao remodelar uma aula fora dessa lista (não deveria acontecer, mas por segurança),
     escolha um nome de selo consistente com o tema (progressão de carreira/habilidade
     em desenvolvimento web full-stack) em vez de inventar temas novos a cada aula.
9. 🔗 Navegação (aula anterior / próxima), **só linke a próxima aula se o arquivo dela
   já existir em `docs/aulas/`.** Como as aulas chegam progressivamente, a mais recente
   deve mostrar `🔒 Aula NN+1 — em breve.` no lugar do link. Ao adicionar essa próxima
   aula depois, volte na aula anterior e troque o placeholder pelo link real.
10. 📋 **Gabarito dos Exercícios**, a última seção do arquivo, um único link para
    `gabaritos/Aula_NN_gabarito.md` (ver "Exercícios de verificação parcial" abaixo).
    Nunca embuta as respostas na própria aula.

Depois de remodelar o conteúdo:
- Atualize `docs/index.md`: mude o status da aula de 🔒 "Em breve" para ✅ "Disponível"
  com link, no bloco correto do Sumário de Aulas e na trilha Mermaid.
- Atualize `mkdocs.yml`: adicione a entrada da aula no `nav`, na seção de bloco correta
  (o nav não descobre arquivos novos sozinho, esse passo é obrigatório).

### Fase 3 — Garantir a exibição completa, finalizar e enviar ao GitHub

O ciclo de uma aula só termina quando ela está construída, verificada, commitada e (com
autorização) publicada. Não deixe uma aula "pronta" apenas na conversa, sem esse
fechamento.

Antes de considerar a aula pronta:

1. Rode `mkdocs build` (sem `--strict`, mas leia os warnings) e confirme que o arquivo
   novo/alterado **não introduziu** nenhum warning novo de link ou imagem quebrada.
2. Confira especificamente:
   - todo bloco `<div ... markdown>` usado (ex. badges centralizados) só funciona
     porque `md_in_html` está habilitado em `markdown_extensions`, **nunca remova essa
     extensão do `mkdocs.yml`**;
   - blocos ` ```mermaid ` fecham corretamente (não há crase/backtick sobrando dentro);
   - blocos `<quiz>...</quiz>` têm pelo menos uma alternativa `- [x]`, e o feedback de
     cada alternativa vem em linhas de citação (`>`) logo abaixo dela (formato da
     mkdocs-quiz 1.x), não como parágrafo solto no fim do bloco;
   - toda imagem referenciada com `../imgs/arquivo.png` existe de fato em `docs/imgs/`;
   - todo mini-desafio "🔎 Verifique seu Entendimento" tem seu par correspondente em
     `gabaritos/Aula_NN_gabarito.md`, e esse arquivo de gabarito **não** foi
     adicionado ao `nav` do `mkdocs.yml`;
   - se a aula tem seção "📎 Material de Apoio", o arquivo em `apoio/` existe, o link
     funciona e o arquivo **não** está no `nav`;
   - o código do domínio `usuarios`/`perfis` foi **executado**, não só lido: no mínimo
     `ast.parse` dos blocos Python e, para rotas e templates, um teste com o cliente de
     teste do Flask contra um banco simulado (sem MySQL local, SQLite em memória serve
     para validar rotas, templates e validações; o DDL do MySQL precisa ser conferido à mão).
3. Se possível, abra `mkdocs serve` e navegue até a página da aula para conferir
   visualmente o mapa mental, os flashcards (clique para expandir) e o quiz.
4. **Faça o commit** assim que a aula passar nas checagens acima. Mensagem de commit
   deve indicar a aula (ex.: `Adiciona Aula 03 — Templates Jinja2 e Rotas, com mapa
   mental, flashcards e quiz`). Um commit por aula finalizada, não acumule várias aulas
   num commit só.
5. **Não dê `git push` automaticamente sem avisar o professor** de que a aula está
   pronta e commitada, ele decide quando publicar. Pergunte explicitamente: "a Aula NN
   está commitada e pronta, posso enviar (`git push`) para o GitHub agora?" Só rode o
   push depois de uma confirmação clara.

---

## Armadilhas já conhecidas neste projeto

- **`md_in_html` ausente** causa badges/imagens dentro de `<div markdown>` sendo
  exibidos como código cru em vez de renderizar. Não esqueça essa extensão ao criar o
  `mkdocs.yml` do zero (ela já vem incluída no arquivo entregue junto com este
  `CLAUDE.md`, mas fique atento se o arquivo for recriado).
- **O plugin de quiz é `mkdocs_quiz` (série 1.x), não `quiz`.** A `mkdocs-quiz`
  publicada no índice é a linha 1.x, cujo entry point registra o nome `mkdocs_quiz`. Se
  o `mkdocs.yml` listar `plugins: - quiz`, o `mkdocs build` aborta com "The 'quiz' plugin
  is not installed" e o site inteiro deixa de publicar. Mantenha `plugins: - mkdocs_quiz`
  e o `requirements.txt` em `mkdocs-quiz>=1.7,<2`. A sintaxe `<quiz>...</quiz>` com
  `- [x]` continua igual; o que mudou foi o feedback, que agora é por alternativa em
  linhas `>` (ver Fase 3).
- **Capturas de tela do domínio antigo.** As imagens `Aula_06_img_01.png` (formulário de
  novo produto), `Aula_06_img_02.png` (diagrama do `WHERE 1=1` com `produto`),
  `Aula_06_img_03.png` (lista e detalhe de produtos) e `Aula_07_img_01.png` (edição de
  produto) não combinam mais com o texto. Estão comentadas (`<!-- IMAGEM PENDENTE ... -->`)
  nos Tópicos 06 e 07 até haver versões com `usuarios`; o diagrama do `WHERE 1=1` foi
  trocado por uma tabela. `Aula_07_img_02.png` e `_03.png` (GET x POST, modal) usam
  produto como ilustração genérica e foram mantidas, com a legenda avisando. Não invente
  capturas: peça ao professor.
- **O `nav` do `mkdocs.yml` é explícito.** Um arquivo `.md` novo em `docs/aulas/` não
  aparece no site até ser adicionado ao `nav`, isso é intencional (permite manter
  aulas "em rascunho" fora do site publicado), mas é fácil esquecer esse passo.
- **Caminhos de imagem são relativos** (`../imgs/arquivo.png` a partir de
  `docs/aulas/*.md`). Ao mover ou renomear arquivos, esses caminhos quebram
  silenciosamente, sempre rode `mkdocs build` depois.
- **Nunca use `mindmap` do Mermaid para o "Mapa Mental da Aula".** O layout desse tipo
  de diagrama é orgânico/de força, sem controle de colisão entre aresta e texto, e a
  versão do Mermaid empacotada pelo Material não inclui o layout `tidy-tree` nem
  plugins de layout tipo ELK que resolveriam isso. Use `flowchart LR` com `subgraph`
  por tópico, mesmo efeito de visão geral, sem sobreposição. Padrão em
  `templates/AULA_TEMPLATE.md`.
- **No mapa mental, use `flowchart LR` (esquerda→direita), nunca `TD`/`TB`.** Com 4-6
  subgraphs irmãos, `TD` os espalha lado a lado, o diagrama fica mais largo que a
  coluna de conteúdo do site, o Material encolhe o SVG inteiro para caber e o texto
  vira ilegível. Em `LR` os mesmos subgraphs empilham na vertical (a página rola, isso
  não é problema); a largura fica controlada porque só cresce com a profundidade da
  árvore, não com o número de ramos. Se o mapa tiver muitos ramos (mais de ~6) mesmo
  assim, considere dividir em dois diagramas menores em vez de forçar tudo em um só.
- **Sempre valide um mapa mental novo visualmente antes de dar por pronto**, não só
  com `mkdocs build` (que não pega problemas de layout/tamanho, só link/imagem
  quebrada). Se houver Playwright disponível no ambiente, renderize o bloco Mermaid
  isolado (`mermaid.min.js` local + HTML mínimo) dentro de um container com a largura
  aproximada da coluna de conteúdo (~760px) e tire um screenshot antes de aplicar.
- **Arquivos de gabarito (`docs/aulas/gabaritos/*.md`) são publicados mesmo fora do
  `nav`.** O `mkdocs build` gera um aviso informativo do tipo "not included in the
  'nav' configuration" para eles, isso é esperado e proposital (ver "Exercícios de
  verificação parcial"), não confunda com um link ou imagem quebrada de verdade.
- **Conteúdo herdado do 1º semestre pode ter blocos de código grandes.** Ao remodelar
  essas aulas, avise na Fase 1 quais trechos serão fatiados em incrementos menores
  (ver "Ensino incremental de código"), isso é uma mudança de apresentação do conteúdo
  original e precisa de confirmação antes de aplicar, mesmo que o conteúdo em si não
  mude.
