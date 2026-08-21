# Gabarito — Aula 02 — Flask e Bootstrap

> Soluções comentadas dos mini-desafios de "🔎 Verifique seu Entendimento" da
> [Aula 02](../Aula_02_Flask_e_Bootstrap.md). Tente resolver cada desafio por conta
> própria antes de conferir aqui.

---

## Parte 1 — Estática ou dinâmica: as duas telas do assistente de estudos

**Desafio proposto:** classificar a tela de "Termos de Uso" e a tela "Meu histórico
de perguntas" como estática ou dinâmica.

**Solução comentada:**

A tela de **Termos de Uso** é **estática**: o texto é sempre o mesmo, para qualquer
aluno, em qualquer momento — pode ser um arquivo HTML fixo, sem nenhum processamento
por trás. A tela **"Meu histórico de perguntas"** é **dinâmica**: o conteúdo depende
de quem está logado e muda a cada nova pergunta feita, então precisa ser gerado no
momento da requisição, buscando os dados daquele aluno específico no banco de dados.

---

## Parte 2 — Instalando o `requests` e atualizando o requirements.txt

**Desafio proposto:** instalar uma nova biblioteca, atualizar o `requirements.txt` e
commitar a mudança.

**Solução comentada:**

```
pip install requests
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Aula 02: adiciona requests ao requirements.txt"
```

`pip install requests` baixa e instala a biblioteca no ambiente virtual ativo.
`pip freeze > requirements.txt` regrava o arquivo com **todas** as dependências
atuais (incluindo o Flask que já estava lá e o requests recém-instalado) — por isso
não é preciso editar o arquivo manualmente.

---

## Parte 3 — MVC aplicado ao app de coleta seletiva

**Desafio proposto:** mapear Controller, View e Model para um app de agendamento de
coleta seletiva.

**Solução comentada:**

- **Controller:** recebe o pedido de agendamento vindo do navegador (ex.: "quero
  agendar a coleta de eletrônicos para quinta-feira") e decide o que fazer com ele —
  é o garçom que anota o pedido e leva para a cozinha.
- **Model:** guarda e processa os dados — os dias de coleta disponíveis por rua, os
  tipos de material aceitos, os agendamentos já feitos — é a cozinha com o estoque.
- **View:** a página que confirma o agendamento para o morador, com data, horário e
  material combinados — é o prato finalizado que chega à mesa.

---

## Parte 4 — Estrutura de pastas da loja do criador de conteúdo

**Desafio proposto:** comandos `mkdir` para criar a estrutura padrão de pastas.

**Solução comentada:**

```
mkdir templates
mkdir static
mkdir static\css
mkdir static\js
mkdir static\imgs
```

A ordem não muda o resultado, mas `static` precisa existir antes de criar as
subpastas `static\css`, `static\js` e `static\imgs` dentro dela.

---

## Parte 5 — Rota `/creditos/<usuario>`

**Desafio proposto:** nova rota Flask com variável na URL, devolvendo os créditos de
IA de um usuário.

**Solução comentada:**

```python
@app.route('/creditos/<usuario>')
def creditos_ia(usuario):
    # <usuario> captura o que vier nessa posição da URL e chega como parâmetro
    return f'<p>{usuario} ainda tem 12 créditos de IA hoje.</p>'
```

Acessar `/creditos/joao` devolve "joao ainda tem 12 créditos de IA hoje." — o mesmo
mecanismo de `/usuario/<nome>` visto no exemplo anterior, só que aplicado a um dado
diferente (créditos em vez de perfil).

---

## Parte 6 — Rota e template para a linha ativa

**Desafio proposto:** criar `templates/rota_ativa.html` e uma rota `/rota-ativa` que
o serve com `render_template`.

**Solução comentada:**

`templates/rota_ativa.html`:

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Rota Ativa</title>
</head>
<body>
  <h1>Linha Ativa Agora</h1>
  <p>Linha 12 — Ônibus Elétrico Circular Centro</p>
</body>
</html>
```

No `app.py`:

```python
@app.route('/rota-ativa')
def rota_ativa():
    return render_template('rota_ativa.html')
```

---

## Parte 7 — Quarto card do evento na página `/sobre`

**Desafio proposto:** adicionar um card Bootstrap anunciando um show, seguindo a
estrutura dos três cards já existentes.

**Solução comentada:**

```html
<div class="col-md-4 mb-4">
  <div class="card h-100">
    <div class="card-body">
      <h5 class="card-title">🎤 Show de Encerramento 2026</h5>
      <p class="card-text">
        Nossa equipe está patrocinando o show de encerramento do festival de
        música deste ano — acompanhe as novidades por aqui.
      </p>
    </div>
  </div>
</div>
```

Basta copiar a estrutura `col-md-4` → `card` → `card-body` → `card-title` /
`card-text` já usada nos três cards de tecnologia e adicioná-la dentro da mesma
`<div class="row">`, depois do terceiro card — o grid de 12 colunas continua
funcionando porque `4 + 4 + 4 = 12` fecha a primeira linha, e o quarto card quebra
para a linha seguinte automaticamente.

---

## Parte 8 — Classes responsivas do painel solar

**Desafio proposto:** escolher as classes `col-*` para 4-lado-a-lado (telas grandes),
2-por-linha (tablets) e 1-por-linha (celular).

**Solução comentada:**

```html
<div class="col-12 col-md-6 col-lg-3">
  <!-- card do indicador aqui -->
</div>
```

`col-12` (padrão, sem prefixo) faz o card ocupar a linha inteira no celular.
`col-md-6` faz cada card ocupar metade da linha a partir de telas médias (tablet) —
dois cards por linha. `col-lg-3` faz cada card ocupar um quarto da linha a partir de
telas grandes (notebook/desktop) — quatro cards lado a lado, já que `3 × 4 = 12`.

---

## Parte 9 — CSS e JS próprios do app de mobilidade

**Desafio proposto:** criar `static/css/mobilidade.css` e `static/js/mapa.js`, e
vinculá-los ao template na ordem correta.

**Solução comentada:**

`static/css/mobilidade.css`:

```css
.rota-ativa {
    color: green;
}
```

`static/js/mapa.js`:

```javascript
// Script do mapa de rotas ativas — em construção
```

No `<head>` do template, depois do Bootstrap CSS:

```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/mobilidade.css') }}">
```

No fim do `<body>`, depois do Bootstrap JS:

```html
<script src="{{ url_for('static', filename='js/mapa.js') }}"></script>
```

A ordem importa pelo mesmo motivo do `estilo.css` visto na aula: o CSS próprio precisa
vir depois do Bootstrap para poder sobrescrevê-lo, e o JS próprio precisa vir depois
do Bootstrap JS para poder usar a API dele, se precisar.

---

*Fatec Jahu · ILP951 · Prof. Ronan Adriel Zenatti · 2026*
