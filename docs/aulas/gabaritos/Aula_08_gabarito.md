# Gabarito — Tópico 07 — CRUD: Edição e Exclusão

> Soluções comentadas dos mini-desafios de "🔎 Verifique seu Entendimento" do
> [Tópico 07](../Aula_08_CRUD_Edicao_e_Exclusao.md). Tente resolver cada desafio por
> conta própria antes de conferir aqui.

---

## Parte 1 — Edição de patinetes elétricos

**Desafio proposto:** escrever a rota `GET` de edição (com `404` e `acao='editar'`) e o trecho do template que pré-preenche o campo `modelo` e o interruptor `ativo`.

**Solução comentada:**

```python
@app.route('/patinetes/<int:patinete_id>/editar')
def patinete_editar(patinete_id):
    patinete = execute_one('SELECT * FROM patinete WHERE id = %s', (patinete_id,))
    if patinete is None:
        abort(404)   # não existe: não faz sentido mostrar um formulário vazio de edição
    return render_template('patinete_form.html', acao='editar', patinete=patinete)
```

```html
<div class="mb-3">
  <label for="modelo" class="form-label">Modelo</label>
  <input type="text" class="form-control" id="modelo" name="modelo"
         value="{{ patinete.modelo | default('') }}">
</div>

{# O interruptor só aparece na edição: todo patinete novo nasce ativo #}
{% if acao == 'editar' %}
<div class="form-check form-switch mb-3">
  <input class="form-check-input" type="checkbox" role="switch"
         id="ativo" name="ativo" value="1"
         {% if patinete.ativo %}checked{% endif %}>
  <label class="form-check-label" for="ativo">Patinete ativo</label>
</div>
{% endif %}
```

Dois detalhes fazem a diferença. Primeiro, o `value="{{ patinete.modelo | default('') }}"` preenche o campo com o valor do banco (o `default('')` protege o primeiro acesso do cadastro, quando não existe `patinete`). Segundo, o `checked` do interruptor é decidido por `{% if patinete.ativo %}`: o `TINYINT(1)` do banco chega como `1` ou `0`, e `1` é "verdadeiro" para o Jinja2. O `{% if acao == 'editar' %}` em volta é o que reaproveita o mesmo template no cadastro sem mostrar um interruptor sem sentido.

---

## Parte 2 — Corrigir a lotação de um evento

**Desafio proposto:** escrever o `POST` da rota `/eventos/<int:evento_id>/editar` (valida `lotacao`, converte o checkbox `esgotado`, `UPDATE` com `WHERE id`) e explicar por que checar a existência com `SELECT` e não com `rowcount`.

**Solução comentada:**

```python
@app.route('/eventos/<int:evento_id>/editar', methods=['GET', 'POST'])
def evento_editar(evento_id):

    # Existência checada por SELECT, antes de qualquer UPDATE
    atual = execute_one('SELECT * FROM evento WHERE id = %s', (evento_id,))
    if atual is None:
        abort(404)

    if request.method == 'POST':
        lotacao_txt = request.form.get('lotacao', '').strip()
        esgotado    = 1 if request.form.get('esgotado') else 0   # checkbox desmarcado não é enviado

        erros = []
        lotacao = lotacao_txt
        try:
            valor = int(lotacao_txt)
        except ValueError:
            erros.append('A lotação deve ser um número inteiro.')
        else:
            if valor < 1:
                erros.append('A lotação deve ser de pelo menos 1 pessoa.')
            else:
                lotacao = valor

        if erros:
            for erro in erros:
                flash(erro, 'danger')
            evento = {'id': evento_id, 'nome': atual['nome'],
                      'lotacao': lotacao, 'esgotado': esgotado}
            return render_template('evento_form.html', acao='editar', evento=evento)

        execute_query(
            'UPDATE evento SET lotacao = %s, esgotado = %s WHERE id = %s',
            (lotacao, esgotado, evento_id)
        )
        flash('Evento atualizado com sucesso.', 'success')
        return redirect(url_for('lista_eventos'))

    return render_template('evento_form.html', acao='editar', evento=atual)
```

A existência é checada com um `SELECT` porque `rowcount` conta as linhas **modificadas**, e não as **encontradas**. Se a organização abrir o formulário e salvar sem mudar nada (a mesma lotação e o mesmo estado de `esgotado`), o `UPDATE` devolve `rowcount = 0`, igualzinho ao caso de um evento que não existe. Quem decidisse "0 linhas = não achei" mostraria um erro falso ao usuário. O `WHERE id = %s` continua sendo o que restringe a alteração ao evento certo, e o `id` vem da URL, já convertido para `int`.

---

## Parte 3 — Desativar ou apagar pontos de coleta

**Desafio proposto:** escrever o comando SQL adequado para o ponto `7` (fechou, mas tem dois anos de pesagens) e para o ponto `99` (cadastrado por engano ontem, sem pesagens), justificando a diferença.

**Solução comentada:**

```sql
-- Ponto 7: exclusão LÓGICA. Preserva as pesagens e os relatórios de volume coletado
UPDATE ponto_coleta SET ativo = 0 WHERE id = 7;

-- Ponto 99: exclusão FÍSICA. Foi um engano, não há histórico a preservar
DELETE FROM ponto_coleta WHERE id = 99;
```

O ponto `7` **tem história**: as pesagens dos últimos dois anos e os relatórios de volume coletado dependem de que ele continue existindo no banco. Apagá-lo deixaria essas pesagens "órfãs" e distorceria os totais históricos; desativá-lo (`ativo = 0`) apenas o tira das listagens correntes, e ainda é reversível se ele reabrir. O ponto `99` foi cadastrado por engano e não tem nenhum dado associado: manter o registro só poluiria o sistema, então a exclusão física é adequada. Em ambos os comandos, o `WHERE id = ...` é o que garante que só a linha certa seja afetada.

---

## Parte 4 — Revogar uma chave de API

**Desafio proposto:** explicar o risco do link `GET` de revogação e reescrever a rota (`POST`, `404` se a chave não existir, redirect com flash) e o formulário que a aciona.

**Solução comentada:**

O risco: um link `<a href="/chaves/7/revogar">` aciona uma rota `GET` que **altera dados**. Mas `GET` deve ser seguro, e vários programas o disparam sozinhos: robôs de busca que rastreiam a página, navegadores que pré-carregam links, aplicativos que geram pré-visualização. Qualquer um deles poderia revogar chaves de API (e derrubar integrações em produção) sem que ninguém clicasse em nada.

```python
@app.route('/chaves/<int:chave_id>/revogar', methods=['POST'])   # só aceita POST
def chave_revogar(chave_id):

    chave = execute_one('SELECT id, nome FROM chave_api WHERE id = %s', (chave_id,))
    if chave is None:
        abort(404)

    execute_query('UPDATE chave_api SET ativa = 0 WHERE id = %s', (chave_id,))
    flash(f'Chave "{chave["nome"]}" revogada.', 'warning')
    return redirect(url_for('lista_chaves'))   # PRG: redirect depois do POST
```

```html
<form action="{{ url_for('chave_revogar', chave_id=chave.id) }}" method="post" class="d-inline">
  <button type="submit" class="btn btn-sm btn-outline-danger">Revogar chave</button>
</form>
```

Com `methods=['POST']`, digitar a URL na barra de endereços (um `GET`) resulta em `405 Method Not Allowed`. Optei por uma revogação **lógica** (`ativa = 0`), que mantém o histórico de uso da chave para auditoria. Em um sistema real, o ideal é também envolver o botão em um modal de confirmação, como na Parte 4 do tópico, já que revogar uma chave é uma ação de impacto.

---

## Parte 5 — Revisando a rota de cancelamento de inscrições

**Desafio proposto:** listar pelo menos quatro problemas da rota `apagar_inscricao` e reescrevê-la.

**Solução comentada:**

Problemas do código original:

1. **Exclusão por `GET`.** O link `<a href="/inscricoes/apagar/12">` permite que robôs e *prefetch* apaguem inscrições. A rota deve aceitar apenas `POST`.
2. **SQL Injection.** `f'DELETE FROM inscricao WHERE id = {id}'` cola o valor da URL direto no SQL. Como `<id>` não tem conversor, o parâmetro é um texto qualquer, e um valor como `1 OR 1=1` apagaria **todas** as inscrições. É preciso conversor `<int:...>` e placeholder `%s`.
3. **Nenhuma checagem de existência.** Um `id` que não existe não gera `404`; a rota apaga zero linhas em silêncio e responde como se tivesse dado certo.
4. **Sem padrão PRG e sem feedback.** Terminar um `POST` com `render_template` faz o F5 reenviar o pedido, e o usuário não vê nenhuma flash message de resultado.
5. **Sem confirmação.** Um clique acidental já apaga a inscrição, sem volta.
6. **Exclusão física sem critério.** Uma inscrição de um campeonato tem histórico (tabelas, premiações): a exclusão **lógica** (`ativa = 0`) costuma ser a escolha adequada.

Versão corrigida:

```python
@app.route('/inscricoes/<int:inscricao_id>/cancelar', methods=['POST'])
def cancelar_inscricao(inscricao_id):

    inscricao = execute_one('SELECT id, time FROM inscricao WHERE id = %s', (inscricao_id,))
    if inscricao is None:
        abort(404)

    try:
        execute_query('UPDATE inscricao SET ativa = 0 WHERE id = %s', (inscricao_id,))
        flash(f'Inscrição do time "{inscricao["time"]}" cancelada.', 'warning')
    except Exception as e:
        flash(f'Não foi possível cancelar a inscrição: {e}', 'danger')

    return redirect(url_for('lista_inscricoes'))
```

No template, o link vira um botão dentro de um formulário `POST` (preferencialmente aberto a partir de um modal de confirmação):

```html
<form action="{{ url_for('cancelar_inscricao', inscricao_id=inscricao.id) }}" method="post" class="d-inline">
  <button type="submit" class="btn btn-sm btn-outline-danger">Cancelar inscrição</button>
</form>
```

Veja como cada problema da lista corresponde a uma linha do checklist da Parte 5: método `POST`, conversor de inteiro, placeholder, `404`, PRG com flash e exclusão lógica. Um bom exercício é conferir a sua resposta contra esse checklist, item por item.

---

*Fatec Jahu · ILP951 · Prof. Ronan Adriel Zenatti · 2026*
