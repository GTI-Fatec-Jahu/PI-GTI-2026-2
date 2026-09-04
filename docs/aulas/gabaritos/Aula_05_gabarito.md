# Gabarito — Aula 05 — Conexão MySQL e Python

> Soluções comentadas dos mini-desafios de "🔎 Verifique seu Entendimento" da
> [Aula 05](../Aula_05_Conexao_MySQL_e_Python.md). Tente resolver cada desafio por
> conta própria antes de conferir aqui.

---

## Parte 1 — Persistência no app de bike-sharing

**Desafio proposto:** explicar o que acontece com o histórico de corridas sem banco de
dados, se o servidor reiniciar.

**Solução comentada:**

Se o histórico de corridas vive apenas em uma lista Python dentro do `app.py`, ele é
**dado volátil**: existe somente enquanto o processo do servidor está rodando na
memória RAM. Ao reiniciar o servidor — por uma atualização de código, uma queda de
energia, ou um simples redeploy — a lista é recriada vazia, e **todo o histórico de
corridas anteriores é perdido para sempre**. Para um app de mobilidade em produção,
isso é inaceitável: o histórico é usado para cobrança, para relatórios de uso das
estações e para o próprio usuário conferir corridas passadas — perder esses dados a
cada reinício quebraria a confiança no sistema e provavelmente violaria obrigações de
cobrança com os usuários.

---

## Parte 2 — Tipos SQL para pontos de coleta seletiva

**Desafio proposto:** escolher o tipo SQL de cada atributo da tabela `ponto_coleta`.

**Solução comentada:**

| Atributo | Tipo SQL |
|---|---|
| nome do ponto | `VARCHAR(200)` |
| endereço | `VARCHAR(255)` ou `TEXT` (se for descrição livre e longa) |
| quilos coletados | `DECIMAL(10, 2)` |
| ativo | `TINYINT(1)` |
| cadastrado em | `TIMESTAMP DEFAULT CURRENT_TIMESTAMP` |

"Quilos coletados" **não** deve ser `INT` porque coleta seletiva é normalmente pesada
com casas decimais (por exemplo, `42.75` kg) — usar `INT` forçaria arredondar ou
truncar esse valor, perdendo precisão real do quanto foi coletado. `DECIMAL(10, 2)`
guarda o valor exato, com até 2 casas decimais, sem os erros de arredondamento que um
tipo de ponto flutuante binário introduziria.

---

## Parte 3 — CREATE DATABASE para o campeonato de e-sports

**Desafio proposto:** escrever o `CREATE DATABASE` para `campeonatos_esports` com
suporte a acentos e emojis.

**Solução comentada:**

```sql
CREATE DATABASE IF NOT EXISTS campeonatos_esports
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE campeonatos_esports;
```

`IF NOT EXISTS` evita erro se o banco já tiver sido criado antes (por exemplo, se você
rodar o script duas vezes). `utf8mb4` é o `CHARACTER SET` necessário para suportar
emojis e caracteres especiais nos nomes dos times, além de acentuação em português —
o `utf8mb4_unicode_ci` (`ci` = case-insensitive) garante que buscas por nome não
diferenciem maiúsculas de minúsculas.

---

## Parte 4 — Parâmetros de conexão do painel de créditos de IA na nuvem

**Desafio proposto:** escrever `time_zone`, `pool_name` e `pool_size` para uma conexão
em nuvem com pool de 8 conexões.

**Solução comentada:**

```python
CONFIGURACAO = {
    # ... host, user, password, database, charset, sql_mode ...
    'time_zone':          '+00:00',            # UTC — padrão recomendado para nuvem
    'pool_name':           'creditos_ia_pool',
    'pool_size':            8,
    'pool_reset_session':   True,
}
```

`time_zone='+00:00'` é a escolha correta para um serviço hospedado na nuvem, evitando
inconsistências entre o fuso do servidor de banco e o fuso da aplicação. `pool_size=8`
atende o tráfego maior esperado sem exagerar no número de conexões simultâneas
mantidas abertas no servidor MySQL (o padrão sugerido na aula é 5, mas o pool pode
crescer conforme a demanda real do sistema).

---

## Parte 5 — Consultando bicicletas livres com execute_query

**Desafio proposto:** rota que busca estações com `bicicletas_livres` disponíveis.

**Solução comentada:**

```python
from flask import Flask, render_template, flash
from db import execute_query

@app.route('/estacoes')
def estacoes():
    try:
        estacoes = execute_query(
            'SELECT * FROM estacao WHERE bicicletas_livres > 0 ORDER BY nome',
            fetch=True
        )
    except Exception as e:
        flash(f'Erro ao carregar estações: {e}', 'danger')
        estacoes = []

    return render_template('estacoes.html', estacoes=estacoes, total=len(estacoes))
```

Segue exatamente o padrão da rota `/produtos` da Parte 5: `execute_query` com
`fetch=True` para um `SELECT`, dentro de um `try/except` que trata falhas de conexão
sem derrubar a página, e o resultado passado ao template junto com a contagem total.

---

## Parte 6 — SQL fundamental para pontos de coleta

**Desafio proposto:** `SELECT` dos pontos com mais de 100 kg coletados (ordenado) e
`UPDATE` que desativa um ponto por `id`.

**Solução comentada:**

```sql
SELECT * FROM ponto_coleta
WHERE quilos_coletados > 100
ORDER BY quilos_coletados DESC;

-- ATENÇÃO: sem WHERE o UPDATE afeta TODOS os registros!
UPDATE ponto_coleta SET ativo = 0 WHERE id = 7;
```

O `SELECT` filtra com `WHERE quilos_coletados > 100` e ordena do maior para o menor
com `ORDER BY quilos_coletados DESC`. O `UPDATE` segue a mesma cautela reforçada na
aula: sempre usar `WHERE` com um `id` específico, nunca um `UPDATE` "solto" que
alteraria todos os pontos de coleta cadastrados.

---

## Parte 7 — Corrigindo SQL Injection na busca de ingressos

**Desafio proposto:** identificar um valor malicioso e reescrever com placeholder.

**Solução comentada:**

Digitando `%' OR '1'='1` no campo de busca, a query montada por concatenação viraria:

```sql
SELECT * FROM evento WHERE nome LIKE '%%' OR '1'='1'%'
```

Como `'1'='1'` é sempre verdadeiro, a condição inteira passa a ser verdadeira para
**todas** as linhas, retornando todos os eventos cadastrados independentemente do
termo digitado — e, em variações mais agressivas, o mesmo tipo de campo poderia ser
usado para comandos ainda mais destrutivos, como visto na Parte 7 da aula.

A correção usa placeholder `%s`, deixando o `%` de "contém" fora da string do usuário:

```python
termo = request.args.get('q', '').strip()
sql = "SELECT * FROM evento WHERE nome LIKE %s"
cursor.execute(sql, (f'%{termo}%',))
# O valor de 'termo' é tratado como dado puro pelo conector,
# mesmo que contenha aspas ou palavras-chave SQL
```

---

*Fatec Jahu · ILP951 · Prof. Ronan Adriel Zenatti · 2026*
