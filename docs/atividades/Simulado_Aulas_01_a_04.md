# Simulado — Preparação para a Avaliação (Aulas 1 a 4)

**Disciplina:** Programação para Internet (ILP951)
**Professor:** Ronan Adriel Zenatti · ronan.zenatti@cps.sp.gov.br
**Fatec Jahu — 2º Semestre/2026**

!!! warning "Atividade não avaliativa — não vale nota"
    Este é um **simulado**. Ele **não vale nota**: existe para você e sua dupla testarem, com calma e sem risco, o que será cobrado na avaliação. Levar a sério é a melhor forma de descobrir o que ainda precisa de revisão **antes** do dia que conta.

> **Pré-requisitos:** Aulas 01 a 04 concluídas (Git/GitHub, ambiente virtual, Flask, Bootstrap, rotas, formulários, GET e POST, validação no servidor).

---

## 🎯 Objetivos da atividade

Ao final, sua dupla deverá ser capaz de:

- Criar do zero um projeto Flask versionado no GitHub, com ambiente virtual e `requirements.txt`.
- Criar **páginas HTML completas** (`<!DOCTYPE html>` até `</html>`), cada uma em seu próprio arquivo da pasta `templates/`, e exibi-las com `render_template`, **sem herança de templates**.
- Receber dados de um formulário e devolver o resultado **na mesma rota**, tratando `GET` e `POST`.
- Validar os dados no servidor e classificar o resultado com `if / elif / else`.
- Construir uma interface responsiva com Bootstrap 5.
- Servir uma imagem a partir da pasta `static/` em uma segunda rota.

## 📅 Como funciona a entrega

1. A atividade é feita em **dupla**.
2. A dupla escolhe **um único tema** entre os dois apresentados abaixo (Tema A ou Tema B).
3. Você recebe este enunciado antes da avaliação para se preparar; o desenvolvimento pode ser feito antes do dia.
4. **No dia da avaliação, a dupla apresenta o projeto funcionando ao professor**, rodando na própria máquina.
5. **Somente depois da apresentação**, a dupla entrega no Google Classroom **o link do repositório no GitHub**. Quem enviar o link sem ter apresentado não cumpriu a atividade.

---

## 🧱 Requisitos obrigatórios

| # | Requisito |
|---|-----------|
| R1 | Aplicação Flask em um arquivo `app.py`, executável com `python app.py`, usando `debug=True` durante o desenvolvimento. |
| R2 | **Use `render_template`, mas sem herança.** Cada página é um arquivo `.html` **completo** na pasta `templates/` (`<!DOCTYPE html>` até `</html>`), com o próprio `<head>` e o Bootstrap. **Não use** `{% extends %}` nem `{% block %}`, e não crie um `base.html`. Cada rota devolve a sua página com `render_template`. |
| R3 | A rota `/` aceita `GET` e `POST`. No `GET`, exibe o formulário. No `POST`, recebe os dados e exibe o resultado **na mesma rota**. O `action` do formulário aponta para a própria rota `/`. |
| R4 | O cálculo e a classificação acontecem no **back-end**. A classificação usa obrigatoriamente **`if / elif / else`**, com o `else` cobrindo a última faixa. Não use dicionário de faixas, `match/case` nem `if` em linha encadeado. |
| R5 | **Validação no servidor.** Dados inválidos não geram resultado nem erro 500: o usuário vê todas as mensagens de erro de uma vez, em alertas Bootstrap. |
| R6 | Interface com **Bootstrap 5** (via CDN): navbar, container, card, campos `form-control`/`form-select`, botão e alerta colorido conforme a faixa do resultado. A página deve funcionar em tela de celular (teste pelo DevTools, `F12`). |
| R7 | Segunda rota, `/equipe`, com **uma foto da dupla** e os **dados da dupla** (detalhes na Etapa 8). |
| R8 | Repositório **público** no GitHub, com `README.md`, `.gitignore` (sem a pasta `venv/`) e `requirements.txt`. **Os dois integrantes** devem ter commits. |
| R9 | Nenhuma biblioteca além do Flask. Sem banco de dados. |

> 💡 Repetir o mesmo trecho de HTML (`<head>`, navbar) nos dois arquivos é esperado: sem herança, cada página é independente. Dentro dos templates, use apenas o necessário para exibir dados: `{{ variável }}`, `{% if %}` para mostrar ou esconder o resultado e os erros, `{% for %}` para listar os erros e `url_for`. **A classificação por faixas continua sendo feita em Python**, no `app.py`.

---

## 🧭 Escolha um tema

=== "Tema A — Pegada de carbono do deslocamento"

    ### 🌱 Calculadora de Pegada de Carbono do Deslocamento

    #### Para quem não conhece o assunto

    **Pegada de carbono** é a quantidade de gases de efeito estufa que uma atividade lança na atmosfera, medida em **quilogramas de CO₂** (dióxido de carbono). No deslocamento diário, ela depende de duas coisas: **quantos quilômetros** você percorre e **qual meio de transporte** usa. Cada meio emite uma quantidade diferente de CO₂ por quilômetro rodado. O ônibus, por exemplo, divide a emissão entre os passageiros, por isso o valor por pessoa é baixo.

    Sua aplicação vai estimar a emissão **mensal** de uma pessoa e dizer em qual faixa de impacto ela está.

    #### Campos do formulário

    | Campo | Tipo | Regra de validação |
    |-------|------|--------------------|
    | Distância percorrida por dia (km, somando ida e volta) | número | obrigatório, maior que 0 |
    | Dias de deslocamento por semana | número inteiro | obrigatório, de 1 a 7 |
    | Meio de transporte | lista de seleção (`select`) | obrigatório, um dos 5 valores da tabela abaixo |

    #### Fatores de emissão

    Valores **aproximados e arredondados para fins didáticos**. Não são valores oficiais de inventário de emissões.

    | Meio de transporte | Fator (kg de CO₂ por km) |
    |--------------------|--------------------------|
    | Bicicleta ou a pé | 0,00 |
    | Carro elétrico | 0,05 |
    | Ônibus (por passageiro) | 0,07 |
    | Moto | 0,10 |
    | Carro a gasolina | 0,20 |

    #### Cálculo

    Considere que o mês tem **4 semanas**.

    - Quilômetros por mês = distância por dia × dias por semana × 4
    - Emissão mensal (kg de CO₂) = quilômetros por mês × fator do meio de transporte

    #### Faixas de classificação (emissão mensal)

    | Faixa | Emissão mensal |
    |-------|----------------|
    | 🟢 Baixo impacto | até 20 kg |
    | 🟡 Impacto moderado | acima de 20 kg até 60 kg |
    | 🟠 Alto impacto | acima de 60 kg até 120 kg |
    | 🔴 Impacto crítico | acima de 120 kg |

    #### Exemplo resolvido, para você se orientar

    Marina vai de moto até a faculdade: 12 km por dia (ida e volta), 5 dias por semana.

    - Quilômetros por mês: 12 × 5 × 4 = **240 km**
    - Emissão mensal: 240 × 0,10 = **24,00 kg de CO₂**
    - 24,00 está acima de 20 e até 60, então a faixa é **🟡 Impacto moderado**.

    #### Valores para testar sua aplicação

    Sua aplicação só está certa se devolver exatamente estes resultados.

    | # | Distância/dia | Dias/semana | Meio de transporte | Km/mês | Emissão mensal | Faixa esperada |
    |---|---------------|-------------|--------------------|--------|----------------|----------------|
    | 1 | 10 | 5 | Bicicleta ou a pé | 200 | 0,00 kg | 🟢 Baixo impacto |
    | 2 | 30 | 5 | Ônibus | 600 | 42,00 kg | 🟡 Impacto moderado |
    | 3 | 25 | 5 | Carro a gasolina | 500 | 100,00 kg | 🟠 Alto impacto |
    | 4 | 40 | 6 | Carro a gasolina | 960 | 192,00 kg | 🔴 Impacto crítico |
    | 5 | 50 | 7 | Carro elétrico | 1400 | 70,00 kg | 🟠 Alto impacto |

    E estes valores **inválidos** devem produzir mensagens de erro, sem resultado e sem quebrar a página:

    | # | Situação | O que deve acontecer |
    |---|----------|----------------------|
    | 6 | Distância `0` (ou negativa) | erro informando que a distância deve ser maior que 0 |
    | 7 | Dias por semana `8` | erro informando que os dias devem estar entre 1 e 7 |
    | 8 | Nenhum meio de transporte selecionado | erro pedindo para selecionar o meio de transporte |
    | 9 | Todos os campos vazios | os três erros aparecem juntos |

=== "Tema B — Monitor de créditos de IA"

    ### 🤖 Monitor de Créditos de IA

    #### Para quem não conhece o assunto

    Muitos assistentes de IA generativa (para estudo, texto, imagem) funcionam com **créditos de uso**. Cada plano dá um número de créditos por mês, e cada pedido feito ao assistente consome alguns deles. Quando os créditos acabam, o usuário fica sem o serviço até o mês seguinte, ou precisa pagar mais. Por isso, os painéis de uso mostram **quanto já foi gasto** e **se o ritmo atual vai durar até o fim do mês**.

    Sua aplicação vai reproduzir esse painel: a partir do que a pessoa já gastou até hoje, calcula uma **projeção** para o fim do mês e classifica a situação.

    Exemplos de planos (fictícios, só para referência ao digitar): **Gratuito** com 100 créditos, **Estudante** com 500, **Pro** com 2000.

    #### Campos do formulário

    | Campo | Tipo | Regra de validação |
    |-------|------|--------------------|
    | Limite do plano (créditos por mês) | número inteiro | obrigatório, maior que 0 |
    | Créditos usados até hoje | número inteiro | obrigatório, maior ou igual a 0 |
    | Dia do mês (hoje) | número inteiro | obrigatório, de 1 a 30 |

    #### Cálculo

    Considere que o mês tem **30 dias**.

    - Percentual usado até hoje = créditos usados ÷ limite × 100
    - Projeção para o fim do mês (créditos) = créditos usados × 30 ÷ dia do mês
    - Percentual projetado = projeção ÷ limite × 100

    #### Faixas de classificação

    A ordem das verificações importa: a situação "esgotado" tem **prioridade** sobre as demais.

    | Faixa | Condição |
    |-------|----------|
    | 🔴 Limite esgotado | créditos usados maiores ou iguais ao limite |
    | 🟠 Risco de estourar | (não esgotado) percentual projetado acima de 100% |
    | 🟡 Atenção | (não esgotado) percentual projetado acima de 70% até 100% |
    | 🟢 Tranquilo | percentual projetado até 70% |

    #### Exemplo resolvido, para você se orientar

    Lucas assina o plano **Estudante** (500 créditos). No dia 10, já usou 120 créditos.

    - Percentual usado até hoje: 120 ÷ 500 × 100 = **24,00%**
    - Projeção para o fim do mês: 120 × 30 ÷ 10 = **360 créditos**
    - Percentual projetado: 360 ÷ 500 × 100 = **72,00%**
    - 72,00% está acima de 70% e até 100%, então a faixa é **🟡 Atenção**.

    #### Valores para testar sua aplicação

    Sua aplicação só está certa se devolver exatamente estes resultados.

    | # | Limite | Usados | Dia | Usado hoje | Projeção | % projetado | Faixa esperada |
    |---|--------|--------|-----|------------|----------|-------------|----------------|
    | 1 | 500 | 100 | 15 | 20,00% | 200 | 40,00% | 🟢 Tranquilo |
    | 2 | 500 | 200 | 15 | 40,00% | 400 | 80,00% | 🟡 Atenção |
    | 3 | 500 | 300 | 15 | 60,00% | 600 | 120,00% | 🟠 Risco de estourar |
    | 4 | 500 | 520 | 20 | 104,00% | 780 | 156,00% | 🔴 Limite esgotado |
    | 5 | 100 | 40 | 6 | 40,00% | 200 | 200,00% | 🟠 Risco de estourar |

    No teste 4 a projeção também passaria de 100%, mas a faixa correta é **Limite esgotado**. Se sua aplicação mostrou "Risco de estourar", a ordem das condições está errada.

    E estes valores **inválidos** devem produzir mensagens de erro, sem resultado e sem quebrar a página:

    | # | Situação | O que deve acontecer |
    |---|----------|----------------------|
    | 6 | Limite `0` (evita divisão por zero) | erro informando que o limite deve ser maior que 0 |
    | 7 | Dia do mês `31` | erro informando que o dia deve estar entre 1 e 30 |
    | 8 | Créditos usados negativos | erro informando que os créditos usados não podem ser negativos |
    | 9 | Todos os campos vazios | os três erros aparecem juntos |

---

## 🛠️ Roteiro de desenvolvimento

Siga as etapas **na ordem**. Ao fim de cada uma há um **ponto de verificação**: só avance quando ele estiver funcionando, e faça um **commit** com uma mensagem que diga o que a etapa entregou. Não escreva tudo de uma vez.

### Etapa 0 — Repositório e ambiente

- Crie o repositório público no GitHub e clone-o na sua máquina.
- Crie e ative o ambiente virtual, instale o Flask e gere o `requirements.txt`.
- Crie o `.gitignore` com a pasta `venv/`.
- Crie o `app.py` com uma aplicação Flask mínima e uma rota `/` que devolve apenas um texto simples.
- Crie a pasta `templates/` ao lado do `app.py`.

🔎 **Ponto de verificação:** `python app.py` sobe o servidor e o texto aparece em `http://localhost:5000`. Faça o primeiro commit e envie ao GitHub.

### Etapa 1 — Página completa com Bootstrap

- Crie o arquivo `templates/index.html` como uma página HTML completa: `<!DOCTYPE html>`, `<html lang="pt-br">`, `<head>` com `charset`, `viewport`, `<title>` e o Bootstrap 5 via CDN, e um `<body>`.
- Faça a rota `/` devolver esse arquivo com `render_template`.
- No corpo, coloque uma navbar (com o nome da aplicação e, por ora, só o link para a própria página inicial) e um `container` com um título.

🔎 **Ponto de verificação:** salve e recarregue. A página deve aparecer com a tipografia e a navbar do Bootstrap. Se ela aparecer "crua", o CDN não carregou: confira o `<head>`.

### Etapa 2 — O formulário (sem processar nada ainda)

- Dentro de um card, monte o formulário do tema escolhido, com os campos da tabela e o tipo de campo adequado a cada um. Use `label` associado a cada campo e o atributo `name` em todos.
- Use `method="post"` e `action` apontando para `/`. Inclua um botão de envio.

🔎 **Ponto de verificação:** preencha o formulário e clique em enviar. Você deve ver uma página de erro **405 Method Not Allowed**. Isso é esperado: o formulário já envia um `POST`, mas a rota ainda só aceita `GET`. Anote no seu README por que isso acontece, você vai precisar explicar na apresentação.

### Etapa 3 — A mesma rota recebendo os dados

- Declare que a rota `/` aceita `GET` e `POST`.
- Separe os dois comportamentos: no `GET`, devolve o formulário; no `POST`, lê os campos enviados.
- Por enquanto, apenas mostre no terminal (`print`) os valores recebidos e devolva o formulário de novo.

🔎 **Ponto de verificação:** envie o formulário e confira no terminal do VS Code que os valores chegaram. O 405 desapareceu.

### Etapa 4 — Conversão e validação no servidor

- Lembre-se: tudo o que chega de um formulário é **texto**. Converta para número antes de calcular.
- Aplique as regras de validação da tabela do seu tema, acumulando **todos** os erros antes de exibir algum.
- Se houver erros, devolva a página com cada erro em um alerta Bootstrap (`alert-danger`) acima do formulário. Se não houver, siga para a próxima etapa.

🔎 **Ponto de verificação:** rode todos os testes **inválidos** da tabela do seu tema. Para conseguir enviar campos vazios ou fora do intervalo, remova os atributos `required`, `min` e `max` pelo DevTools, como fizemos na Aula 04. O servidor não pode quebrar (erro 500) em nenhum deles.

### Etapa 5 — O cálculo

- Com os dados válidos, faça o cálculo da fórmula do seu tema.
- Ainda **sem** classificar: mostre apenas os números calculados (arredondados para 2 casas decimais) em um card de resultado, abaixo do formulário.

🔎 **Ponto de verificação:** confira os números dos testes 1 a 5 da tabela. Se um deles não bater, corrija a fórmula antes de continuar.

### Etapa 6 — Classificação com if / elif / else

Faça esta etapa **em três passos**, testando entre eles:

1. Comece com um `if / else` que separa apenas duas faixas (a primeira e "todo o resto").
2. Acrescente **um** `elif` e teste de novo.
3. Acrescente os `elif` restantes, deixando a última faixa no `else`.

🔎 **Ponto de verificação:** os cinco testes válidos devem cair, cada um, na faixa esperada. Teste também valores **na fronteira** das faixas, por exemplo um resultado exatamente igual ao limite de uma faixa, e confirme se ele caiu onde a tabela manda.

### Etapa 7 — Resultado com cor e clareza

- Exiba o nome da faixa e os números calculados dentro de um alerta Bootstrap cuja **cor muda conforme a faixa** (use as cores contextuais do Bootstrap).
- Mantenha o formulário visível na página, para o usuário poder calcular de novo.

🔎 **Ponto de verificação:** as quatro faixas aparecem com quatro visuais diferentes. Reduza a largura da janela (ou use o modo celular do DevTools) e confirme que nada quebra.

### Etapa 8 — A rota `/equipe`

- Crie o arquivo `templates/equipe.html`, também uma **página completa e independente** (sem `extends`), e a rota `/equipe` que o devolve com `render_template`. Use a mesma navbar, agora com dois links: **Calculadora** (`/`) e **Equipe** (`/equipe`). Atualize a navbar do `index.html` também.
- Guarde a foto da dupla dentro da pasta `static/` do projeto e a exiba com `url_for('static', ...)`, com texto alternativo (`alt`) descritivo e classes do Bootstrap para ficar responsiva.
- A página deve mostrar, para **cada integrante**: nome completo e RA. E, para a dupla: curso e semestre, o **tema escolhido** e o **link do repositório** no GitHub.
- Organize as informações em card(s) do Bootstrap; a página não pode parecer um texto solto.

🔎 **Ponto de verificação:** a foto carrega, os dados aparecem e a navegação entre as duas rotas funciona nos dois sentidos.

### Etapa 9 — Fechamento

- Escreva o `README.md` com: nomes da dupla, tema escolhido, como executar o projeto (criar o `venv`, instalar o `requirements.txt`, rodar) e uma **tabela com os resultados obtidos** nos testes válidos e inválidos do seu tema.
- Confira o **checklist final** abaixo e faça o último commit e o `push`.

---

## ✅ Checklist antes de apresentar

- [ ] `git clone` do seu próprio repositório em uma **pasta nova**, criação do `venv`, `pip install -r requirements.txt` e `python app.py` funcionam do zero.
- [ ] Existem `templates/index.html` e `templates/equipe.html`, cada um uma página completa, e ambos são exibidos com `render_template`.
- [ ] Não existe `base.html` e nenhum arquivo usa `{% extends %}` ou `{% block %}`.
- [ ] A rota `/` funciona em `GET` e em `POST`, e o resultado aparece na mesma URL.
- [ ] Os 5 testes válidos e os 4 inválidos do tema escolhido dão o resultado esperado.
- [ ] A classificação usa `if / elif / else`.
- [ ] Nenhum dado inválido causa erro 500.
- [ ] A rota `/equipe` mostra a foto e os dados de **ambos** os integrantes.
- [ ] O repositório é público, tem README, `.gitignore` e `requirements.txt`, e os dois integrantes têm commits.
- [ ] Cada integrante sabe explicar **qualquer** trecho do código, inclusive o que causa o erro 405 e por que a validação é feita no servidor.

## 🎤 No dia da avaliação

- Traga a aplicação **rodando** na sua máquina. O professor poderá pedir que você:
    - execute os valores de teste que ele ditar;
    - altere uma faixa ou uma regra de validação ao vivo;
    - explique um trecho do código e responda perguntas de cada integrante da dupla.
- **Só depois de apresentar**, entregue no Google Classroom o **link do repositório** no GitHub.

## ⭐ Desafios extras (opcionais)

- Manter no formulário os valores digitados depois do cálculo e depois de um erro. Cuidado: texto digitado pelo usuário nunca deve ser inserido no HTML sem antes ser escapado.
- Acrescentar ao resultado uma recomendação curta específica para cada faixa.
- Página de erro 404 personalizada, com a mesma navbar.

---

## 📁 Estrutura esperada do repositório

```
seu-repositorio/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── templates/
│   ├── index.html         # página completa, sem extends/block
│   └── equipe.html        # página completa, sem extends/block
└── static/
    └── img/
        └── dupla.jpg      # a foto da dupla (o nome do arquivo pode variar)
```

## 🔗 Revisão de apoio

Se algo travar, volte ao conteúdo correspondente:

- [Aula 01 — Introdução, Git e HTML5](../aulas/Aula_01_Introducao_Git_HTML5.md): repositório, commits, `venv`, `.gitignore`.
- [Aula 02 — Flask e Bootstrap](../aulas/Aula_02_Flask_e_Bootstrap.md): primeira aplicação, Bootstrap via CDN, pasta `static/`, `requirements.txt`.
- [Aula 03 — Templates Jinja2 e Rotas](../aulas/Aula_03_Templates_Jinja2_e_Rotas.md): `render_template`, variáveis, `{% if %}`, `{% for %}` e `url_for`. Nesta atividade a **herança** (`extends` e `block`) **não** é usada.
- [Aula 04 — Formulários e HTTP](../aulas/Aula_04_Formularios_e_HTTP.md): GET e POST, `request.form`, validação no servidor, código 405.

---

📝 [Voltar à lista de atividades](index.md)
