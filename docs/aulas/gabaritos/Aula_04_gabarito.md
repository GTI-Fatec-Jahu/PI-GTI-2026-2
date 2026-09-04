# Gabarito — Aula 04 — Formulários e HTTP

> Soluções comentadas dos mini-desafios de "🔎 Verifique seu Entendimento" da
> [Aula 04](../Aula_04_Formularios_e_HTTP.md). Tente resolver cada desafio por conta
> própria antes de conferir aqui.

---

## Parte 1 — Status HTTP do painel de créditos de IA

**Desafio proposto:** identificar a categoria e o código de status para uma falha por
sobrecarga no servidor.

**Solução comentada:**

A falha é causada pelo **servidor** (sobrecarga), não por um erro do usuário — por isso
a categoria correta é **5xx**. Dentro do que a aula apresentou, o código mais direto é
o **500 Internal Server Error**, usado quando algo deu errado no código ou na
infraestrutura do servidor. (Em APIs reais existe também o código mais específico
**503 Service Unavailable**, próprio para sobrecarga temporária — mas o raciocínio de
categoria, 5xx = erro do servidor, é o que a aula pede.)

---

## Parte 2 — GET ou POST no app de bike-sharing

**Desafio proposto:** escolher o método certo para a tela de filtro por bairro e para a
tela de desbloqueio de bicicleta.

**Solução comentada:**

A tela de **filtro por bairro** usa **GET** — ela só lê/exibe estações, e faz sentido
poder compartilhar o link já filtrado (`/estacoes?bairro=centro`) com outra pessoa. A
tela de **desbloqueio de bicicleta** usa **POST** — ela executa uma ação que modifica
o estado do sistema (a bicicleta passa a estar em uso), e não faz sentido nenhum
"compartilhar o link" de destravar uma bike específica: isso permitiria que qualquer
pessoa com o link destravasse a bicicleta em nome de outro usuário.

---

## Parte 3 — Campos do cadastro de ponto de coleta seletiva

**Desafio proposto:** escolher entre `<select>`, `radio` e `checkbox` para "tipo de
material aceito" (só um por ponto) e "aceita coleta domiciliar".

**Solução comentada:**

```html
<select name="tipo_material">
  <option value="papel">Papel</option>
  <option value="plastico">Plástico</option>
  <option value="vidro">Vidro</option>
  <option value="metal">Metal</option>
</select>

<input type="checkbox" name="coleta_domiciliar" value="sim">
```

"Tipo de material aceito" permite **apenas uma opção selecionada por vez** — tanto
`<select>` quanto `radio` resolveriam, mas `<select>` é preferível quando há várias
opções (evita ocupar muito espaço vertical na tela, ao contrário do `radio`, mais
indicado para 2-4 opções lado a lado). "Aceita coleta domiciliar" é um valor
independente de verdadeiro/falso — exatamente o caso de uso do `checkbox`, que pode ser
marcado ou não sem depender de nenhuma outra opção.

---

## Parte 4 — request.form no formulário de ingressos

**Desafio proposto:** ler um campo opcional (`cupom`) e um obrigatório (`quantidade`)
com a forma de acesso adequada a cada um.

**Solução comentada:**

```python
cupom = request.form.get('cupom', '')
# Campo opcional: .get() com valor padrão evita erro se o campo não vier

quantidade = request.form['quantidade']
# Campo obrigatório: o acesso com colchetes lança KeyError (erro 400) se o campo
# não existir, o que sinaliza claramente que a requisição está malformada
```

A diferença está em como cada situação deve reagir à ausência do campo: para o cupom,
a ausência é um caso normal e esperado (`.get()` com padrão evita quebrar a aplicação);
para a quantidade, a ausência indica um problema real na requisição, e deixar o
`KeyError` estourar é aceitável nesse ponto — a validação completa de negócio (por
exemplo, quantidade > 0) viria depois, como visto na Parte 5.

---

## Parte 5 — Validação do código promocional

**Desafio proposto:** coletar o campo `codigo` com `.strip()` e validar vazio e
comprimento diferente de 8.

**Solução comentada:**

```python
codigo = request.form.get('codigo', '').strip()

erros = []

if not codigo:
    erros.append('O código promocional é obrigatório.')
elif len(codigo) != 8:
    erros.append('O código promocional deve ter exatamente 8 caracteres.')
```

Segue exatamente o padrão da Parte 5 da aula: primeiro coleta com `.strip()` para
eliminar espaços acidentais, depois valida em cadeia (`if` / `elif`) para não checar o
comprimento de um código que já está vazio.

---

## Parte 6 — PRG na confirmação de aluguel de veículo elétrico

**Desafio proposto:** explicar o que dá errado sem `redirect` e o que o PRG evita.

**Solução comentada:**

Sem o `redirect`, a rota do aluguel processaria o POST e chamaria
`render_template('confirmacao.html')` diretamente. Se o usuário pressionar F5 depois
de ver a confirmação, o navegador reenviaria o mesmo POST (a última requisição feita),
o que processaria o aluguel **uma segunda vez** — cobrando o usuário duas vezes ou
reservando dois veículos para a mesma pessoa. O padrão PRG evita exatamente isso:
como a rota termina com `redirect(url_for(...))` em vez de renderizar direto, o F5
recarrega apenas o **GET** final (a página de confirmação), sem repetir o POST que
processa o pagamento.

---

## Parte 7 — Feedback visual do campo de potência solar

**Desafio proposto:** aplicar `is-invalid`/`invalid-feedback` ao campo de potência em
kWp.

**Solução comentada:**

```html
<input
  type="number"
  step="0.1"
  class="form-control {% if erros.potencia %}is-invalid{% elif potencia %}is-valid{% endif %}"
  id="potencia"
  name="potencia"
  value="{{ potencia | default('') }}"
>

{% if erros.potencia %}
  <div class="invalid-feedback">{{ erros.potencia }}</div>
{% else %}
  <div class="valid-feedback">Potência válida!</div>
{% endif %}
```

O padrão é idêntico ao do campo Nome mostrado na Parte 7: a classe `is-invalid` só
aparece quando `erros.potencia` existe (erro específico desse campo), e o
`invalid-feedback` só é exibido nessa mesma condição — mantendo a mensagem de erro
"colada" visualmente ao campo problemático.

---

## Parte 8 — Busca de campeonatos de e-sports

**Desafio proposto:** rota `/campeonatos` com `request.args` para `jogo` e
`modalidade`, filtrando por modalidade.

**Solução comentada:**

```python
@app.route('/campeonatos')
def campeonatos():
    jogo = request.args.get('jogo', '').strip()
    modalidade = request.args.get('modalidade', 'todas')

    todos_campeonatos = [
        {'nome': 'Copa Regional de Valorant', 'jogo': 'valorant', 'modalidade': 'equipe'},
        {'nome': 'Torneio Solo de Free Fire', 'jogo': 'free fire', 'modalidade': 'individual'},
        {'nome': 'Liga Universitária de LoL', 'jogo': 'league of legends', 'modalidade': 'equipe'},
    ]

    resultados = todos_campeonatos
    if jogo:
        resultados = [c for c in resultados if jogo.lower() in c['jogo'].lower()]
    if modalidade != 'todas':
        resultados = [c for c in resultados if c['modalidade'] == modalidade]

    return render_template('campeonatos.html', resultados=resultados)
```

Segue o mesmo padrão da rota `/busca` da Parte 8: parâmetros lidos com
`request.args.get`, valor padrão `'todas'` para o filtro opcional, e filtragem
progressiva (primeiro por `jogo`, depois por `modalidade`) usando list comprehension.

---

## Parte 9 — Depurando o painel de créditos de IA no Network

**Desafio proposto:** descrever os passos no painel Network para diagnosticar três
hipóteses diferentes de falha.

**Solução comentada:**

Com `F12 → Network` aberto e **Preserve log** marcado, clique em "Resgatar código
promocional" e observe:

1. **A requisição nem está sendo enviada** — nenhuma nova linha aparece na lista de
   requisições do painel Network. Isso indica um problema no JavaScript do botão (ele
   não está de fato submetendo o formulário), não no servidor.
2. **O servidor está respondendo com erro** — a requisição aparece na lista, e a aba
   **Headers** mostra o código de status (por exemplo, `500` ou `400`) em vermelho.
3. **Os dados enviados estão incorretos** — a requisição aparece com status `200` ou
   `302` (o servidor respondeu normalmente), mas a aba **Payload** mostra que o campo
   `codigo` foi enviado vazio ou com um nome diferente do esperado pelo Flask.

---

*Fatec Jahu · ILP951 · Prof. Ronan Adriel Zenatti · 2026*
