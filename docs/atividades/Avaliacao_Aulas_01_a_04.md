# Avaliação — Calculadora de IMC (Aulas 1 a 4)

**Disciplina:** Programação para Internet (ILP951)
**Professor:** Ronan Adriel Zenatti · ronan.zenatti@cps.sp.gov.br
**Fatec Jahu — 2º Semestre/2026**

!!! success "Esta avaliação vale 4 pontos"
    Duração: **19h30 às 21h00**. Todo o código do projeto deve ser desenvolvido **durante este período**.

---

## 🎯 Objetivo

Em dupla, desenvolver uma aplicação Flask que calcula o **Índice de Massa Corporal (IMC)**, classifica o resultado em faixas e apresenta a equipe, partindo de dois arquivos HTML fornecidos.

## 📚 O que está sendo cobrado

- **Aula 01 — Introdução, Git e HTML5:** criar repositório no GitHub, clonar, `commit` e `push`, ambiente virtual (`venv`), `.gitignore`, estrutura básica de uma página HTML.
- **Aula 02 — Flask e Bootstrap:** primeira aplicação Flask, `requirements.txt`, Bootstrap 5 via CDN, pasta `static/`.
- **Aula 03 — Templates Jinja2 e Rotas:** `render_template`, variáveis `{{ }}`, `{% if %}`, `{% for %}` e `url_for`.
- **Aula 04 — Formulários e HTTP:** métodos `GET` e `POST`, `request.form`, conversão de texto para número, validação no servidor.

---

## 📥 Arquivos fornecidos

Baixe os dois arquivos abaixo. Eles são **HTML puro com Bootstrap**: não têm nenhum código Python nem Jinja. Transformá-los em páginas dinâmicas faz parte da avaliação.

- [:material-download: index.html](arquivos/modelo_index.html){ download="index.html" } — página da calculadora, com navbar e o formulário (nome, peso e altura).
- [:material-download: equipe.html](arquivos/modelo_equipe.html){ download="equipe.html" } — página da equipe, com textos de exemplo a serem substituídos pelos dados reais da dupla.

---

## 📅 Como funciona a entrega

1. A avaliação é feita em **dupla**.
2. Crie o repositório **público** no GitHub e desenvolva nele o projeto.
3. **Cada integrante entrega, na atividade correspondente à avaliação no Google Classroom, o mesmo link do repositório**, cada um na sua própria conta.
4. O professor verifica o funcionamento e lança a nota no Classroom para todos que finalizarem dentro do período.
5. **Quem não finalizar até as 20h50** deve fazer o `push` do que produziu no GitHub e enviar o link até as 21h00. A nota será **proporcional ao que estiver funcionando** no repositório. Commits feitos depois das 20h50 não são considerados.

!!! info "Antes das 19h30"
    A **foto da dupla** deve estar pronta no computador antes de começar, pois tirá-la não faz parte do tempo de desenvolvimento.

---

## 🧱 Requisitos obrigatórios

| # | Requisito |
|---|-----------|
| R1 | Aplicação Flask em um arquivo `app.py`, executável com `python app.py`, usando `debug=True`. |
| R2 | **Use `render_template`, mas sem herança.** `index.html` e `equipe.html` ficam na pasta `templates/` como páginas **completas**. **Não use** `{% extends %}` nem `{% block %}`, e não crie um `base.html`. |
| R3 | A rota `/` aceita `GET` e `POST`. No `GET`, exibe o formulário. No `POST`, exibe o resultado **na mesma rota**. O `action` do formulário aponta para `/`. |
| R4 | O cálculo e a classificação acontecem no **back-end**. A classificação usa obrigatoriamente **`if / elif / else`**, com o `else` cobrindo a última faixa. Não use dicionário de faixas, `match/case` nem `if` em linha encadeado. |
| R5 | **Validação no servidor.** Dados inválidos não geram resultado nem erro 500: o usuário vê **todas** as mensagens de erro de uma vez, em alertas Bootstrap. |
| R6 | O resultado aparece em um alerta Bootstrap cuja **cor muda conforme a faixa**, com o formulário visível para calcular de novo. A página deve funcionar em tela de celular. |
| R7 | Segunda rota, `/equipe`, exibindo a **foto da dupla** (guardada em `static/` e exibida com `url_for`) e os dados da equipe. |
| R8 | Repositório **público** no GitHub, com `README.md`, `.gitignore` (sem a pasta `venv/`) e `requirements.txt`. **Os dois integrantes** devem ter commits. |
| R9 | Nenhuma biblioteca além do Flask. Sem banco de dados. |

!!! tip "Dica"
    Sem herança, repetir o `<head>` e a navbar nos dois arquivos é esperado. Nos templates, use apenas o necessário para exibir dados: `{{ variável }}`, `{% if %}`, `{% for %}` e `url_for`. **A classificação continua sendo feita em Python**, no `app.py`.

---

## 🧮 O problema: Calculadora de IMC

### Para quem não conhece o assunto

O **IMC** relaciona o peso de uma pessoa com a sua altura e é usado como um indicador geral de faixa de peso. Sua aplicação receberá os dados pelo formulário, calculará o IMC e dirá em qual faixa a pessoa está.

### Campos do formulário

| Campo | Tipo | Regra de validação |
|-------|------|--------------------|
| Nome | texto | obrigatório (não pode ser vazio nem só espaços) |
| Peso (kg) | número decimal | obrigatório, maior que 0 e até 300 |
| Altura (m) | número decimal | obrigatório, de 0,5 a 2,5 (use ponto como separador decimal) |

### Cálculo

- IMC = peso ÷ altura²
- Exiba o IMC arredondado para **2 casas decimais**.

### Faixas de classificação

| Faixa | IMC | Cor do alerta |
|-------|-----|---------------|
| 🔵 Abaixo do peso | menor que 18,5 | `alert-info` |
| 🟢 Peso normal | de 18,5 até menos de 25 | `alert-success` |
| 🟡 Sobrepeso | de 25 até menos de 30 | `alert-warning` |
| 🔴 Obesidade | 30 ou mais | `alert-danger` |

Os valores **18,5, 25 e 30 pertencem à faixa de cima**. Por exemplo, IMC exatamente 25 é Sobrepeso.

### Exemplo resolvido, para você se orientar

Marina pesa 70 kg e mede 1,75 m.

- Altura²: 1,75 × 1,75 = 3,0625
- IMC: 70 ÷ 3,0625 = **22,86**
- 22,86 está entre 18,5 e 25, então a faixa é **🟢 Peso normal**.

### Valores para testar sua aplicação

Sua aplicação só está certa se devolver exatamente estes resultados.

| # | Peso (kg) | Altura (m) | IMC | Faixa esperada |
|---|-----------|------------|-----|----------------|
| 1 | 50 | 1.70 | 17,30 | 🔵 Abaixo do peso |
| 2 | 70 | 1.75 | 22,86 | 🟢 Peso normal |
| 3 | 85 | 1.75 | 27,76 | 🟡 Sobrepeso |
| 4 | 100 | 1.70 | 34,60 | 🔴 Obesidade |
| 5 | 72.25 | 1.70 | 25,00 | 🟡 Sobrepeso (fronteira) |

E estes valores **inválidos** devem produzir mensagens de erro, sem resultado e sem quebrar a página:

| # | Situação | O que deve acontecer |
|---|----------|----------------------|
| 6 | Nome vazio | erro pedindo o nome |
| 7 | Peso `0` | erro informando que o peso deve ser maior que 0 |
| 8 | Altura `3.0` | erro informando que a altura deve estar entre 0,5 e 2,5 |
| 9 | Todos os campos vazios | os três erros aparecem juntos |

!!! note "Como testar os inválidos"
    Para enviar campos vazios ou fora do intervalo, remova os atributos `required`, `min` e `max` pelo DevTools (`F12`), como feito na Aula 04.

---

## 🛠️ Roteiro sugerido

O tempo é curto: siga a ordem e faça **commits frequentes**, pois o que estiver no GitHub às 20h50 é o que será avaliado.

1. **Repositório e ambiente:** crie o repositório, clone, crie o `venv`, instale o Flask, gere o `requirements.txt` e o `.gitignore`. Primeiro commit.
2. **Páginas no projeto:** crie `app.py` e a pasta `templates/`, coloque os dois HTML fornecidos nela e faça `/` exibir o `index.html` com `render_template`.
3. **`POST` na mesma rota:** faça `/` aceitar `GET` e `POST` e leia os campos com `request.form`.
4. **Validação:** converta os valores para número e acumule **todos** os erros; exiba-os em alertas `alert-danger`.
5. **Cálculo e classificação:** calcule o IMC e classifique com `if / elif / else`.
6. **Resultado:** exiba o IMC e a faixa em um alerta com a cor da faixa, mantendo o formulário visível.
7. **Rota `/equipe`:** exiba a página da equipe com `render_template`, a foto pela pasta `static/` e `url_for`, e os dados reais dos integrantes.
8. **Fechamento:** escreva o `README.md`, confira o checklist e faça o `push` final.

---

## ✅ Checklist de conferência

Use antes de fazer o `push` final. Não é necessário entregar este checklist.

- [ ] `git clone` do seu repositório em uma **pasta nova**, `venv`, `pip install -r requirements.txt` e `python app.py` funcionam do zero.
- [ ] `templates/index.html` e `templates/equipe.html` são exibidos com `render_template`.
- [ ] Não existe `base.html` e nenhum arquivo usa `{% extends %}` ou `{% block %}`.
- [ ] A rota `/` funciona em `GET` e em `POST`, e o resultado aparece na mesma URL.
- [ ] Os 5 testes válidos e os 4 inválidos dão o resultado esperado.
- [ ] A classificação usa `if / elif / else`.
- [ ] Nenhum dado inválido causa erro 500.
- [ ] A rota `/equipe` mostra a foto e os dados de **ambos** os integrantes.
- [ ] O repositório é público, tem `README.md`, `.gitignore` e `requirements.txt`, e os dois integrantes têm commits.
- [ ] O link do repositório foi enviado por **cada integrante** no Classroom.

---

## 📁 Estrutura esperada do repositório

```
seu-repositorio/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── templates/
│   ├── index.html
│   └── equipe.html
└── static/
    └── img/
        └── dupla.jpg      # a foto da dupla (o nome do arquivo pode variar)
```

---

📝 [Voltar à lista de atividades](index.md)
