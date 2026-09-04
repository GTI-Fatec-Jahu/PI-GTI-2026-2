# Aula 05 — Conexão MySQL e Python

**Disciplina:** Programação para Internet (ILP951)
**Professor:** Ronan Adriel Zenatti · ronan.zenatti@cps.sp.gov.br
**Fatec Jahu — 2º Semestre/2026**

> **Pré-requisitos:** Aula 04 concluída — formulários GET/POST funcionando, padrão PRG aplicado.

---

## 🎯 Objetivos da Aula

Ao final desta aula você deverá ser capaz de:

- Explicar a diferença entre dado volátil e dado persistente, e por que um banco de dados relacional é a solução correta para sistemas web.
- Escolher o tipo de coluna SQL adequado para cada tipo de dado (`VARCHAR`, `TEXT`, `INT`, `DECIMAL`, `TINYINT`, `TIMESTAMP`).
- Instalar e configurar o MySQL Community Server e criar um banco de dados pelo MySQL Workbench.
- Conectar uma aplicação Python ao MySQL com `mysql-connector-python`, seguindo o ciclo conectar → cursor → executar → confirmar/ler → fechar.
- Configurar parâmetros de conexão robustos (`sql_mode`, `time_zone`, `use_pure`, timeout, pool de conexões).
- Centralizar o acesso ao banco em um módulo `db.py` reutilizável por toda a aplicação.
- Executar os comandos SQL fundamentais (`SELECT`, `INSERT`, `UPDATE`, `DELETE`) e identificar por que a concatenação de strings em SQL é perigosa.

Até aqui, todos os dados do sistema existiam apenas enquanto a aplicação estava rodando — listas Python que desapareciam ao reiniciar o servidor. Hoje isso muda permanentemente. Você vai instalar e configurar o MySQL, entender como bancos de dados relacionais funcionam e por que são a escolha certa para sistemas web, conectar o Python ao banco usando a biblioteca `mysql-connector-python`, criar a primeira tabela via script Python, e executar os primeiros comandos SQL diretamente do código. Ao final desta aula, os dados cadastrados pelo seu sistema sobreviverão a qualquer reinicialização do servidor — pela primeira vez, sua aplicação terá memória permanente.

---

## 🗺️ Mapa Mental da Aula

```mermaid
flowchart LR
    ROOT(("MySQL e<br/>Persistencia de Dados"))

    ROOT --> T1
    subgraph T1["💾 Persistencia"]
        direction TB
        T1A["Dado volatil x persistente"]
        T1B["Banco relacional: tabelas e chaves"]
    end

    ROOT --> T2
    subgraph T2["🔤 Tipos SQL"]
        direction TB
        T2A["VARCHAR, TEXT, INT"]
        T2B["DECIMAL, TINYINT, TIMESTAMP"]
    end

    ROOT --> T3
    subgraph T3["🔌 Conexao Python-MySQL"]
        direction TB
        T3A["connect() e cursor()"]
        T3B["execute() e commit()/fetchall()"]
        T3C["close() sempre no finally"]
    end

    ROOT --> T4
    subgraph T4["⚙️ Parametros do conector"]
        direction TB
        T4A["sql_mode e time_zone"]
        T4B["use_pure e connection_timeout"]
        T4C["pool de conexoes"]
    end

    ROOT --> T5
    subgraph T5["🗂️ db.py central"]
        direction TB
        T5A["execute_query()"]
        T5B["execute_one()"]
    end

    ROOT --> T6["🛡️ SQL Injection"]
```

---

## Parte 1 — Persistência de dados: o problema que o banco resolve

### Dados voláteis versus dados persistentes

Quando o servidor Flask é encerrado — seja porque você fechou o terminal, o computador foi reiniciado, ou houve uma queda de energia — toda informação armazenada em variáveis Python simplesmente desaparece. Isso é chamado de **dado volátil**: existe apenas enquanto o programa está em execução na memória RAM. Para desenvolvimento e testes é aceitável, mas para um sistema real é inviável. Imagine um sistema de vendas que perde todos os pedidos cada vez que o servidor é reiniciado.

A solução profissional é gravar os dados em um **sistema de armazenamento persistente** que mantém as informações independentemente do estado do servidor. Arquivos de texto são uma opção simples, mas ineficientes para buscas e completamente inadequados para múltiplos usuários simultâneos. A solução correta para sistemas web é o **banco de dados relacional**.

![Sem banco de dados os dados são voláteis; com MySQL eles persistem mesmo após reiniciar o servidor](../imgs/Aula_05_img_01.png)

### O que é um banco de dados relacional

Um **banco de dados relacional** organiza os dados em **tabelas** — estruturas bidimensionais compostas por linhas (registros) e colunas (atributos). As tabelas se relacionam entre si por meio de **chaves**, permitindo consultas que cruzam dados de múltiplas fontes com eficiência. Toda essa estrutura é governada pela linguagem **SQL** (Structured Query Language), criada nos anos 1970 e ainda hoje o padrão universal para bancos de dados.

A analogia mais próxima de uma tabela de banco de dados é uma planilha Excel: cada aba seria uma tabela, cada linha seria um registro (um produto, um cliente), e cada coluna seria um atributo (nome, preço, data). A diferença fundamental está em quatro capacidades: **integridade** (o banco garante que os dados seguem as regras definidas), **relacionamentos** (tabelas se conectam por chaves), **concorrência** (múltiplos usuários acessam e modificam dados simultaneamente sem conflito), e **performance** (consultas complexas em milhões de registros em milissegundos).

### Onde o MySQL se encaixa na arquitetura

O MySQL se posiciona como a camada de persistência que sustenta o servidor Flask. O diagrama abaixo mostra exatamente como os três componentes se comunicam:

```mermaid
graph LR
    A["🌐 Navegador"] -->|"requisição HTTP"| B["⚙️ Flask (Python)"]
    B -->|"execute SQL"| C["🗄️ MySQL"]
    C -->|"retorna dados"| B
    B -->|"HTML via Jinja2"| A
    style A fill:#4A90D9,color:#fff,stroke:#2C6FAC
    style B fill:#F5A623,color:#fff,stroke:#C07D0F
    style C fill:#27AE60,color:#fff,stroke:#1A7A43
```

O Flask atua como intermediário: recebe a requisição do navegador, consulta o MySQL, e usa os dados retornados para renderizar o HTML via Jinja2. O navegador nunca se comunica diretamente com o banco — toda interação passa pelo código Python.

### 🔎 Verifique seu Entendimento

Um app de mobilidade urbana registra cada corrida de bike-sharing (usuário, estação de saída, estação de chegada, horário) em uma lista Python dentro do `app.py`.

**Desafio:** Explique, em termos de dado volátil versus persistente, o que acontece com o histórico de corridas se o servidor Flask reiniciar sem um banco de dados, e por que isso é inaceitável para um app desse tipo em produção.

> 💬 Tente por conta própria antes de seguir. A solução comentada está no gabarito desta aula (link na última seção da página).

---

## Parte 2 — Tipos de dados SQL essenciais

Antes de criar a primeira tabela, é fundamental entender os tipos de dados disponíveis no MySQL, pois cada coluna deve ter um tipo declarado. Isso garante integridade e permite ao banco otimizar armazenamento e consultas.

Para texto curto (nomes, e-mails, títulos) usa-se `VARCHAR(n)`, onde `n` é o tamanho máximo em caracteres — por exemplo, `VARCHAR(200)` para um nome de produto. Para textos longos sem limite fixo (descrições, conteúdo de artigos) usa-se `TEXT`. Para números inteiros (quantidades, IDs, idades) usa-se `INT`. Para valores decimais com precisão controlada (preços, medidas) usa-se `DECIMAL(p, d)`, onde `p` é o total de dígitos e `d` quantos ficam após a vírgula — `DECIMAL(10, 2)` suporta valores como `99999999.99`. Para valores verdadeiro/falso usa-se `TINYINT(1)`, onde `1` significa verdadeiro e `0` significa falso. Para datas e horas usa-se `DATE`, `DATETIME` ou `TIMESTAMP` — este último pode ser preenchido automaticamente com a data e hora atuais.

O diagrama de entidade abaixo mostra a estrutura que vamos criar:

```mermaid
erDiagram
    PRODUTO {
        int id PK "AUTO_INCREMENT"
        varchar_200 nome "NOT NULL"
        text descricao "nullable"
        decimal_10_2 preco "NOT NULL"
        int estoque "DEFAULT 0"
        tinyint_1 ativo "DEFAULT 1"
        timestamp criado_em "DEFAULT CURRENT_TIMESTAMP"
    }
```

O campo `id` com `AUTO_INCREMENT` e `PRIMARY KEY` é especial: o banco gera automaticamente um número único para cada novo registro, garantindo que nenhum produto tenha o mesmo ID jamais.

### 🔎 Verifique seu Entendimento

Uma cooperativa quer uma tabela `ponto_coleta` para pontos de coleta seletiva: nome do ponto, endereço, quantos quilos de material já foram coletados, se o ponto está ativo, e quando foi cadastrado.

**Desafio:** Para cada um desses cinco atributos, escolha o tipo SQL mais adequado entre `VARCHAR(n)`, `TEXT`, `INT`, `DECIMAL(p,d)`, `TINYINT(1)` e `TIMESTAMP`, justificando a escolha de `quilos coletados` especificamente (por que não `INT`?).

> 💬 Tente por conta própria antes de seguir. A solução comentada está no gabarito desta aula (link na última seção da página).

---

## Parte 3 — Instalando e configurando o MySQL

### Instalação do MySQL Community Server

Acesse **dev.mysql.com/downloads/mysql** e baixe o **MySQL Community Server** para Windows. Durante a instalação, selecione a opção **"Developer Default"** para instalar o servidor, o **MySQL Workbench** (interface gráfica), o shell e os conectores em um único processo.

Na tela de configuração de senha, defina uma senha para o usuário `root`. **Anote essa senha em um lugar seguro** — ela será necessária em todos os momentos que você precisar conectar ao banco. Mantenha a porta padrão **3306** sem alteração.

Após a instalação, abra um novo terminal e verifique:

```
mysql --version
```

A resposta esperada é algo como `mysql  Ver 8.0.xx for Win64`. Se o comando não for reconhecido, execute pelo MySQL Command Line Client instalado no menu Iniciar.

### MySQL Workbench

O **MySQL Workbench** é a ferramenta gráfica oficial para administrar instâncias MySQL. Com ele você cria bancos e tabelas, escreve e executa queries SQL, e visualiza dados em grade sem precisar usar o terminal. Abra o Workbench, clique em **"Local instance MySQL80"** e insira a senha do `root` quando solicitado.

### Criando o banco de dados do projeto

No Workbench, abra um novo editor SQL (ícone de folha com raio) e execute o seguinte código com `Ctrl+Enter`:

```sql
-- Cria o banco de dados do projeto
-- IF NOT EXISTS: não gera erro se o banco já existir
CREATE DATABASE IF NOT EXISTS projeto_web
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;
-- CHARACTER SET utf8mb4: suporte completo a acentos, cedilha e emojis
-- COLLATE utf8mb4_unicode_ci: ordenação case-insensitive (João = joão)

-- Seleciona o banco para uso nas próximas queries
USE projeto_web;
```

O banco `projeto_web` deve aparecer no painel Navigator. Clique com o botão direito nele e selecione **"Set as Default Schema"** para que o Workbench o utilize automaticamente.

### 🔎 Verifique seu Entendimento

Uma organizadora de campeonatos de e-sports de 2026 precisa de um banco próprio, separado de qualquer outro projeto na mesma instância MySQL, chamado `campeonatos_esports`, também com suporte completo a acentos e emojis (nomes de times costumam usar caracteres especiais).

**Desafio:** Escreva o comando `CREATE DATABASE` completo para esse cenário, incluindo `IF NOT EXISTS`, `CHARACTER SET` e `COLLATE`, seguindo exatamente o padrão desta seção.

> 💬 Tente por conta própria antes de seguir. A solução comentada está no gabarito desta aula (link na última seção da página).

---

## Parte 4 — Conectando Python ao MySQL

### Instalando o conector

Com o ambiente virtual ativo, instale a biblioteca oficial:

```
pip install mysql-connector-python
pip freeze > requirements.txt
```

### O ciclo de vida de uma conexão

Toda operação com banco de dados em Python segue o mesmo ciclo de cinco etapas. Entender esse ciclo é essencial para evitar os dois erros mais comuns: esquecer de fechar a conexão (o que esgota o pool de conexões do banco) e esquecer de chamar `commit()` após operações de escrita (o que faz os dados parecerem salvos mas não estarem).

```mermaid
flowchart LR
    A["1️⃣ Conectar
    connect(host, user, pwd, db)"] --> B["2️⃣ Obter Cursor
    conn.cursor()"]
    B --> C["3️⃣ Executar SQL
    cursor.execute(sql, params)"]
    C --> D{"SELECT
    ou escrita?"}
    D -->|"SELECT"| E["4️⃣ Ler
    fetchall()"]
    D -->|"INSERT/UPDATE/DELETE"| F["4️⃣ Confirmar
    conn.commit()"]
    E --> G["5️⃣ Fechar
    cursor.close() + conn.close()"]
    F --> G
    style A fill:#4A90D9,color:#fff
    style G fill:#E74C3C,color:#fff
```

O **cursor** é o objeto que executa as queries SQL — pense nele como um ponteiro que navega pelos resultados de um `SELECT` ou confirma a execução de um `INSERT`. Sempre abra o cursor, use-o, e feche tanto o cursor quanto a conexão, preferencialmente usando `try/finally` para garantir o fechamento mesmo em caso de erro.

### Parâmetros importantes do MySQL Connector

O `mysql-connector-python` aceita muito mais do que `host`, `user`, `password` e `database`. Entender os parâmetros abaixo é essencial para conexões robustas, corretas e seguras — do desenvolvimento local até a nuvem.

#### `sql_mode` — Modo de validação SQL

O MySQL pode operar em diferentes níveis de rigor na validação dos dados. Sem o modo estrito, ele aceita silenciosamente datas inválidas (`0000-00-00`), trunca textos longos sem aviso e arredonda decimais sem gerar erro. Com o modo estrito, qualquer dado inválido causa um erro explícito, forçando o código a tratar os problemas na origem:

```python
'sql_mode': (
    'STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,'
    'ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION'
)
```

Cada flag ativa uma regra independente:

| Flag | O que faz sem ela | O que faz com ela |
|---|---|---|
| `STRICT_TRANS_TABLES` | Dados inválidos são corrigidos silenciosamente (VARCHAR truncado, DECIMAL arredondado, NOT NULL vira `0`) | Qualquer dado inválido gera erro e aborta o INSERT/UPDATE — é a flag mais importante |
| `NO_ZERO_IN_DATE` | Aceita datas com mês ou dia zero, como `2026-00-15` ou `2026-04-00` | Rejeita datas com mês ou dia zerado, que são malformadas e causam bugs difíceis de rastrear |
| `NO_ZERO_DATE` | Aceita `0000-00-00` como data válida (valor "vazio" legado do MySQL antigo) | Rejeita `0000-00-00` — datas devem ser reais ou `NULL` |
| `ERROR_FOR_DIVISION_BY_ZERO` | Uma divisão por zero em SQL (`10 / 0`) retorna `NULL` silenciosamente | Uma divisão por zero gera erro — torna o bug visível em vez de propagar `NULL` pelo sistema |
| `NO_ENGINE_SUBSTITUTION` | Se o storage engine pedido não existir, o MySQL troca por outro sem avisar | Se o engine não existir, gera erro — evita criar tabelas com engine diferente do esperado sem perceber |

O MySQL 8.0 já usa modo estrito por padrão no servidor, mas declarar explicitamente garante comportamento idêntico independentemente da versão do servidor ou da configuração da máquina de produção.

#### `time_zone` — Fuso horário da sessão

Controla o fuso horário que o MySQL usa em funções como `NOW()` e `CURRENT_TIMESTAMP`, e em colunas `DATETIME` e `TIMESTAMP`. Sem configurar, o servidor usa o fuso do sistema operacional — o que causa inconsistências em servidores em nuvem (geralmente UTC) versus máquinas de desenvolvimento (horário local):

```python
'time_zone': '-03:00'   # Horário de Brasília (BRT, sem horário de verão)
# ou
'time_zone': '+00:00'   # UTC — recomendado para produção e ambientes em nuvem
```

> **Regra prática:** Use `'+00:00'` em produção e armazene tudo em UTC. Converta para o fuso do usuário apenas na camada de interface.

#### `use_pure` — Python puro vs extensão C

O conector tem dois modos internos: a extensão C (mais rápida, padrão quando instalada) e a implementação em Python puro (mais compatível). Normalmente o conector escolhe automaticamente.

**Porém:** se você configurou tudo corretamente, a conexão funciona perfeitamente no Workbench, mas o código Python continua falhando com erros como `Authentication plugin 'caching_sha2_password' is not supported` ou `Lost connection to MySQL server`, a causa provável é uma **incompatibilidade entre a extensão C instalada e a versão do MySQL Server**. Nesses casos, forçar `use_pure=True` resolve o problema:

```python
'use_pure': True   # força a implementação em Python puro
```

O desempenho com `use_pure=True` é ligeiramente menor que a extensão C, mas a diferença é irrelevante para aplicações de pequeno e médio porte. É preferível ter a conexão funcionando de forma confiável a otimizar algo que nem está funcionando.

#### Tratamento de Falhas e Tempo

```python
'connection_timeout': 10,    # segundos para desistir de uma conexão que não responde
'autocommit':         False,  # False = exige commit() explícito (recomendado)
```

Sem `connection_timeout`, um servidor MySQL lento ou inacessível deixa a aplicação travada indefinidamente aguardando resposta. Com `10` segundos, o código recebe um erro em tempo razoável e pode apresentar uma mensagem amigável ao usuário em vez de congelar.

`autocommit=False` (padrão) significa que toda operação de escrita (`INSERT`, `UPDATE`, `DELETE`) precisa de um `commit()` explícito para ser efetivada no banco. Isso dá controle preciso sobre transações: se uma etapa de uma operação composta falhar, você pode chamar `rollback()` e desfazer tudo que havia sido escrito até ali.

#### Pool de Conexões — Essencial para Aplicações Web

Em uma aplicação web, cada requisição HTTP que acessa o banco precisa de uma conexão. Sem pool, cada requisição abre uma nova conexão TCP com o MySQL (alguns milissegundos de handshake e autenticação) e a fecha ao terminar. Com 50 usuários simultâneos, isso representa 50 pares de abertura/fechamento por segundo — um desperdício crescente de recursos do servidor.

Um **pool de conexões** cria um conjunto fixo de conexões antecipadamente e as **reutiliza** entre as requisições. Quando uma requisição termina, a conexão volta ao pool em vez de ser fisicamente fechada:

```mermaid
graph LR
    A["Req. 1"] --> P["Pool
    5 conexões abertas"]
    B["Req. 2"] --> P
    C["Req. 3"] --> P
    D["Req. 4
    (aguarda liberação)"] -.-> P
    P --> M["🗄️ MySQL"]
    style P fill:#F5A623,color:#fff,stroke:#C07D0F
    style M fill:#27AE60,color:#fff,stroke:#1A7A43
```

```python
'pool_name':          'webapp_pool',  # nome identificador do pool
'pool_size':          5,              # conexões abertas permanentemente (típico: 3–10)
'pool_reset_session': True,           # limpa variáveis de sessão ao reutilizar conexão
```

> **Atenção:** `pool_size` define o máximo de conexões simultâneas ao banco. Se todas estiverem ocupadas e uma nova requisição chegar, ela aguarda uma ser liberada. Aumentar `pool_size` indefinidamente consome memória e conexões no servidor MySQL. Para a maioria das aplicações web de pequeno a médio porte, `5` é suficiente.

> **Como o pool funciona com `conn.close()`:** quando você chama `conn.close()` em uma conexão do pool, ela **não é fisicamente fechada** — é devolvida ao pool para reutilização. O código de fechamento permanece idêntico; o pool gerencia o ciclo de vida por baixo dos panos.

#### Segurança — SSL/TLS

Em produção, especialmente com banco em servidor remoto, a conexão deve ser criptografada para evitar que credenciais e dados trafeguem em texto claro pela rede:

```python
'ssl_disabled':    False,                        # False = usa SSL quando disponível
'ssl_verify_cert': True,                         # verifica o certificado do servidor
'ssl_ca':          '/caminho/para/ca-cert.pem',  # certificado da autoridade certificadora
```

Para desenvolvimento local, SSL é opcional (banco e aplicação estão na mesma máquina). Para qualquer ambiente de produção ou banco em nuvem, SSL deve ser **obrigatório**.

### Exemplo completo com todos os parâmetros — Azure Database for MySQL

> **Este exemplo não é testável em aula** — depende de um recurso provisionado na nuvem Microsoft Azure. Serve como referência de como seria uma conexão de produção real com todos os parâmetros configurados corretamente, por isso ele é apresentado de uma vez, sem a divisão em incrementos que usamos nos exemplos que você de fato executa.

O Azure Database for MySQL é um serviço de banco de dados gerenciado. Ele exige SSL, usa credenciais no formato `usuario@servidor`, e tipicamente opera em UTC. Este é o exemplo de uma configuração completa para esse ambiente:

```python
# conexao_azure.py — Exemplo de referência (não testável localmente)
# Demonstra como todos os parâmetros se combinam em um cenário de produção real.

import mysql.connector
from mysql.connector import Error, pooling

AZURE_CONFIG = {
    # —— Identificação do servidor ——————————————————————————————
    'host':     'meu-servidor.mysql.database.azure.com',
    'port':     3306,
    'user':     'adminuser@meu-servidor',   # formato obrigatório no Azure
    'password': 'SenhaForte@2026!',
    'database': 'projeto_web',

    # —— Codificação —————————————————————————————————————————————
    'charset':  'utf8mb4',

    # —— Comportamento SQL ———————————————————————————————————————
    'sql_mode': (
        'STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,'
        'ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION'
    ),
    'time_zone':   '+00:00',   # UTC — padrão recomendado para nuvem

    # —— Compatibilidade —————————————————————————————————————————
    'use_pure':    True,       # recomendado em ambientes de nuvem

    # —— Tempo e falhas ——————————————————————————————————————————
    'connection_timeout': 30,  # nuvem pode ter latência maior que local
    'autocommit':         False,

    # —— SSL (obrigatório no Azure) ——————————————————————————————
    'ssl_disabled':    False,
    'ssl_verify_cert': True,
    'ssl_ca':          'DigiCertGlobalRootG2.crt.pem',  # baixado do portal Azure
}

# Pool para uso em produção — mais conexões para suportar maior tráfego
pool = pooling.MySQLConnectionPool(
    pool_name='azure_pool',
    pool_size=10,
    pool_reset_session=True,
    **AZURE_CONFIG
)

try:
    conn = pool.get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT VERSION() AS versao')
    resultado = cursor.fetchone()
    print(f"Conectado ao Azure MySQL: {resultado['versao']}")
except Error as e:
    print(f'Erro ao conectar ao Azure: {e}')
finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()   # devolve ao pool, não fecha fisicamente
```

A estrutura do código é idêntica à conexão local — o que muda são os parâmetros de configuração. Essa é exatamente a vantagem de centralizar tudo no `db.py`: para migrar do ambiente local para o Azure, você altera apenas o dicionário de configuração, sem tocar em nenhuma rota do `app.py`.

### Exemplo prático 1 — Script de setup do banco

Vamos criar `db_setup.py`, que será executado **uma única vez** para preparar a estrutura inicial e inserir dados de exemplo. Em vez de escrever o script inteiro de uma vez, vamos montá-lo por partes, testando cada uma no terminal antes de seguir.

**Passo 1 — só conectar.** Crie `db_setup.py` na raiz do projeto com apenas a conexão e o fechamento, para confirmar que as credenciais estão certas antes de criar qualquer coisa:

```python
# db_setup.py — Script de configuração inicial do banco de dados
# Execute com: python db_setup.py

import mysql.connector
from mysql.connector import Error

CONFIGURACAO = {
    'host':               'localhost',
    'user':               'root',
    'password':           'SUA_SENHA_AQUI',  # substitua pela sua senha do MySQL
    'database':           'projeto_web',
    'charset':            'utf8mb4',
    'sql_mode':           ('STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,'
                           'ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION'),
    'time_zone':          '-03:00',   # Horário de Brasília
    'use_pure':           True,       # Python puro — compatível com todos os ambientes
    'connection_timeout': 10,         # desiste após 10s sem resposta
    'autocommit':         False,      # exige commit() explícito
}

try:
    conn = mysql.connector.connect(**CONFIGURACAO)
    # O ** "desempacota" o dicionário como argumentos nomeados
    cursor = conn.cursor()
    print('✅ Conectado ao MySQL com sucesso!')

except Error as e:
    print(f'❌ Erro MySQL: {e}')
    print('   Verifique: senha correta? MySQL rodando? Banco "projeto_web" criado?')

finally:
    # finally SEMPRE executa — garante que a conexão seja fechada mesmo com erro
    if 'cursor' in locals() and cursor:
        cursor.close()
    if 'conn' in locals() and conn.is_connected():
        conn.close()
    print('🔌 Conexão encerrada.')
```

Rode `python db_setup.py` no terminal. Se aparecer `✅ Conectado ao MySQL com sucesso!` seguido de `🔌 Conexão encerrada.`, as credenciais estão corretas e podemos seguir. Se aparecer um erro, ajuste a senha em `CONFIGURACAO` antes de continuar.

**Passo 2 — criar a tabela.** Adicione o `CREATE TABLE` logo após a mensagem de conexão bem-sucedida, ainda dentro do `try`:

```python
    # Cria a tabela de produtos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produto (
            id         INT            AUTO_INCREMENT PRIMARY KEY,
            nome       VARCHAR(200)   NOT NULL,
            descricao  TEXT,
            preco      DECIMAL(10, 2) NOT NULL,
            estoque    INT            NOT NULL DEFAULT 0,
            ativo      TINYINT(1)     NOT NULL DEFAULT 1,
            criado_em  TIMESTAMP      DEFAULT CURRENT_TIMESTAMP
        ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
    ''')
    # AUTO_INCREMENT: MySQL gera o id automaticamente (1, 2, 3, ...)
    # NOT NULL: campo obrigatório — INSERT sem esse campo gera erro
    # DEFAULT 0: valor padrão quando o campo não é informado no INSERT
    # DECIMAL(10,2): até 10 dígitos no total, 2 após a vírgula (ideal para preço)
    # TIMESTAMP DEFAULT CURRENT_TIMESTAMP: preenchido automaticamente

    conn.commit()
    print('✅ Tabela "produto" criada (ou já existia).')
```

Rode `python db_setup.py` de novo. No Workbench, atualize o painel Navigator (botão direito → Refresh All) e confirme que a tabela `produto` aparece dentro de `projeto_web`, mesmo sem nenhuma linha ainda.

**Passo 3 — verificar se já existem dados.** Antes de inserir exemplos, precisamos saber se a tabela já está populada (para não duplicar a cada execução do script). Adicione:

```python
    # Insere dados de exemplo apenas se a tabela estiver vazia
    cursor.execute('SELECT COUNT(*) FROM produto')
    total_existente = cursor.fetchone()[0]
    # fetchone() retorna a próxima linha do resultado como tupla; [0] pega o valor

    print(f'ℹ️  A tabela já contém {total_existente} registro(s).')
```

Rode novamente: como a tabela está vazia, a mensagem mostra `0 registro(s)`.

**Passo 4 — inserir os dados de exemplo.** Substitua a linha de `print` do Passo 3 pela lógica condicional que insere cinco produtos apenas na primeira execução:

```python
    if total_existente == 0:
        produtos_exemplo = [
            ('Notebook Dell Inspiron',    'i5, 8GB RAM, 256GB SSD',         3499.90, 15),
            ('Mouse Logitech MX Master',  'Sem fio ergonômico, 7 botões',    299.90, 42),
            ('Teclado Mecânico Redragon', 'Switches Red, retroiluminado',    189.90,  3),
            ('Monitor LG 24"',            'Full HD, 75Hz, painel IPS',      1199.90,  0),
            ('Headset HyperX Cloud',      'Som surround 7.1, microfone',     349.90, 27),
        ]
        cursor.executemany(
            'INSERT INTO produto (nome, descricao, preco, estoque) VALUES (%s, %s, %s, %s)',
            produtos_exemplo
        )
        # executemany: insere múltiplos registros com eficiência
        # %s são placeholders — NUNCA use f-strings ou concatenação em SQL
        # O conector trata cada %s como dado puro, nunca como código SQL
        conn.commit()
        print(f'✅ {len(produtos_exemplo)} produtos inseridos.')
    else:
        print(f'ℹ️  Tabela já contém {total_existente} registro(s).')
```

Rode `python db_setup.py` uma última vez: agora aparece `✅ 5 produtos inseridos.`. Rode de novo (uma segunda vez): a mensagem muda para `ℹ️ Tabela já contém 5 registro(s).` — a checagem do Passo 3 evita duplicar os dados.

**Consolidação — `db_setup.py` completo:**

```python
# db_setup.py — Script de configuração inicial do banco de dados
# Execute com: python db_setup.py
# Cria a tabela e insere dados de exemplo para testes.

import mysql.connector
from mysql.connector import Error

CONFIGURACAO = {
    'host':               'localhost',
    'user':               'root',
    'password':           'SUA_SENHA_AQUI',  # substitua pela sua senha do MySQL
    'database':           'projeto_web',
    'charset':            'utf8mb4',
    'sql_mode':           ('STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,'
                           'ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION'),
    'time_zone':          '-03:00',   # Horário de Brasília
    'use_pure':           True,       # Python puro — compatível com todos os ambientes
    'connection_timeout': 10,         # desiste após 10s sem resposta
    'autocommit':         False,      # exige commit() explícito
}

try:
    # Passo 1: estabelece a conexão
    conn = mysql.connector.connect(**CONFIGURACAO)
    # O ** "desempacota" o dicionário como argumentos nomeados
    cursor = conn.cursor()
    print('✅ Conectado ao MySQL com sucesso!')

    # Passo 2: cria a tabela de produtos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produto (
            id         INT            AUTO_INCREMENT PRIMARY KEY,
            nome       VARCHAR(200)   NOT NULL,
            descricao  TEXT,
            preco      DECIMAL(10, 2) NOT NULL,
            estoque    INT            NOT NULL DEFAULT 0,
            ativo      TINYINT(1)     NOT NULL DEFAULT 1,
            criado_em  TIMESTAMP      DEFAULT CURRENT_TIMESTAMP
        ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
    ''')
    # AUTO_INCREMENT: MySQL gera o id automaticamente (1, 2, 3, ...)
    # NOT NULL: campo obrigatório — INSERT sem esse campo gera erro
    # DEFAULT 0: valor padrão quando o campo não é informado no INSERT
    # DECIMAL(10,2): até 10 dígitos no total, 2 após a vírgula (ideal para preço)
    # TIMESTAMP DEFAULT CURRENT_TIMESTAMP: preenchido automaticamente

    conn.commit()
    print('✅ Tabela "produto" criada (ou já existia).')

    # Passo 3: insere dados de exemplo apenas se a tabela estiver vazia
    cursor.execute('SELECT COUNT(*) FROM produto')
    total_existente = cursor.fetchone()[0]
    # fetchone() retorna a próxima linha do resultado como tupla; [0] pega o valor

    if total_existente == 0:
        produtos_exemplo = [
            ('Notebook Dell Inspiron',    'i5, 8GB RAM, 256GB SSD',         3499.90, 15),
            ('Mouse Logitech MX Master',  'Sem fio ergonômico, 7 botões',    299.90, 42),
            ('Teclado Mecânico Redragon', 'Switches Red, retroiluminado',    189.90,  3),
            ('Monitor LG 24"',            'Full HD, 75Hz, painel IPS',      1199.90,  0),
            ('Headset HyperX Cloud',      'Som surround 7.1, microfone',     349.90, 27),
        ]
        cursor.executemany(
            'INSERT INTO produto (nome, descricao, preco, estoque) VALUES (%s, %s, %s, %s)',
            produtos_exemplo
        )
        # executemany: insere múltiplos registros com eficiência
        # %s são placeholders — NUNCA use f-strings ou concatenação em SQL
        # O conector trata cada %s como dado puro, nunca como código SQL
        conn.commit()
        print(f'✅ {len(produtos_exemplo)} produtos inseridos.')
    else:
        print(f'ℹ️  Tabela já contém {total_existente} registro(s).')

except Error as e:
    print(f'❌ Erro MySQL: {e}')
    print('   Verifique: senha correta? MySQL rodando? Banco "projeto_web" criado?')

finally:
    # finally SEMPRE executa — garante que a conexão seja fechada mesmo com erro
    if 'cursor' in locals() and cursor:
        cursor.close()
    if 'conn' in locals() and conn.is_connected():
        conn.close()
    print('🔌 Conexão encerrada.')
```

No Workbench, clique com o botão direito em `produto` → **"Select Rows"**: os cinco produtos aparecem. Reinicie o servidor, desligue o computador — os dados continuam lá.

![Workbench confirmando os dados inseridos pelo script Python — os registros estão persistidos no banco](../imgs/Aula_05_img_03.png)

> ⚠️ A imagem acima ainda não está disponível em `docs/imgs/`. Ela será adicionada em um passo posterior — o link já fica pronto para quando o arquivo existir.

### 🔎 Verifique seu Entendimento

Um painel de créditos de uso de IA generativa, hospedado na nuvem, precisa de uma conexão MySQL com fuso horário em UTC e com um pool de 8 conexões (o app espera tráfego maior que o normal de um sistema acadêmico).

**Desafio:** Escreva o dicionário de parâmetros com `time_zone`, `pool_name` e `pool_size` corretos para esse cenário, seguindo o padrão das seções "time_zone" e "Pool de Conexões" desta parte.

> 💬 Tente por conta própria antes de seguir. A solução comentada está no gabarito desta aula (link na última seção da página).

---

## Parte 5 — Centralizando a conexão com db.py

Se as credenciais e a lógica de conexão estivessem repetidas em cada rota do `app.py`, para mudar a senha ou o banco você precisaria editar dezenas de lugares. Além disso, o código de cada rota ficaria poluído com detalhes de infraestrutura. A solução é criar um módulo dedicado `db.py` que encapsula tudo e expõe uma interface simples para o resto do sistema. Vamos construí-lo também em incrementos.

**Passo 1 — parâmetros e pool.** Comece só com a configuração e a criação do pool, sem nenhuma função ainda:

```python
# db.py — Módulo central de acesso ao banco de dados
# Qualquer arquivo que precise do banco importa apenas este módulo

import mysql.connector
from mysql.connector import Error, pooling

# Parâmetros de conexão — editados apenas aqui, usados em todo o sistema
_DB_PARAMS = {
    'host':               'localhost',
    'user':               'root',
    'password':           'SUA_SENHA_AQUI',
    'database':           'projeto_web',
    'charset':            'utf8mb4',
    'sql_mode':           ('STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,'
                           'ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION'),
    'time_zone':          '-03:00',   # Horário de Brasília
    'use_pure':           True,       # Python puro — compatível com todos os ambientes
    'connection_timeout': 10,         # desiste após 10s sem resposta
    'autocommit':         False,      # exige commit() explícito
}

# Pool criado uma única vez quando o módulo é carregado pela primeira vez.
# conn.close() devolve a conexão ao pool — não fecha fisicamente.
_pool = pooling.MySQLConnectionPool(
    pool_name='webapp_pool',
    pool_size=5,           # conexões abertas permanentemente
    pool_reset_session=True,
    **_DB_PARAMS
)
```

Salve `db.py` e rode `python -c "import db; print('db.py carregado com sucesso')"` no terminal. Se aparecer a mensagem sem erro, o pool foi criado corretamente — o módulo já é importável, mesmo sem nenhuma função útil ainda.

**Passo 2 — `get_connection()`.** Adicione a função que pega uma conexão do pool:

```python
def get_connection():
    """Retorna uma conexão do pool. Levanta Exception em caso de falha."""
    try:
        return _pool.get_connection()
    except Error as e:
        raise Exception(f'Não foi possível obter conexão do pool: {e}')
```

Teste no terminal: `python -c "from db import get_connection; c = get_connection(); print(c.is_connected()); c.close()"`. Deve imprimir `True`.

**Passo 3 — `execute_query()`.** Esta é a função que o resto do sistema vai usar para todo `SELECT`, `INSERT`, `UPDATE` e `DELETE`:

```python
def execute_query(sql, params=None, fetch=False):
    """
    Executa uma query SQL de forma segura.

    Parâmetros:
        sql    — string SQL com %s como placeholders
        params — tupla ou lista com os valores dos placeholders
        fetch  — True para SELECT (retorna lista de dicts); False para INSERT/UPDATE/DELETE

    Retorna:
        fetch=True  — lista de dicionários (cada linha = {'coluna': valor})
        fetch=False — número de linhas afetadas
    """
    conn = get_connection()
    try:
        # dictionary=True: cada linha retorna como dicionário — produto['nome'] em vez de produto[0]
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, params or ())

        if fetch:
            return cursor.fetchall()   # retorna todas as linhas
        else:
            conn.commit()              # confirma a transação
            return cursor.rowcount     # número de linhas afetadas

    except Error as e:
        conn.rollback()  # desfaz alterações parciais em caso de erro
        raise Exception(f'Erro ao executar query: {e}')
    finally:
        cursor.close()
        conn.close()   # devolve ao pool, não fecha fisicamente
```

Teste: `python -c "from db import execute_query; print(execute_query('SELECT * FROM produto', fetch=True))"`. Deve imprimir a lista com os cinco produtos inseridos na Parte 4.

**Passo 4 — `execute_one()`.** Por fim, uma função de conveniência para quando você só precisa de uma linha (por exemplo, buscar um produto por ID):

```python
def execute_one(sql, params=None):
    """
    Executa um SELECT e retorna apenas a primeira linha (ou None).
    Útil para buscar um registro por ID.
    """
    resultados = execute_query(sql, params, fetch=True)
    return resultados[0] if resultados else None
```

![Arquitetura em camadas: app.py usa db.py que acessa o MySQL — cada camada tem uma responsabilidade clara](../imgs/Aula_05_img_04.png)

Com `db.py` pronto, o `app.py` para listar produtos fica assim:

```python
from flask import Flask, render_template, flash
from db import execute_query

app = Flask(__name__)
app.secret_key = 'chave-secreta-fatec-2026'


@app.route('/produtos')
def lista_produtos():
    try:
        # Toda a complexidade de conexão está em execute_query
        # O app.py só precisa saber o SQL e o que fazer com os dados
        produtos = execute_query(
            'SELECT * FROM produto WHERE ativo = 1 ORDER BY nome',
            fetch=True
        )
    except Exception as e:
        flash(f'Erro ao carregar produtos: {e}', 'danger')
        produtos = []

    return render_template('produtos.html', produtos=produtos, total=len(produtos))
```

Salve e acesse `http://localhost:5000/produtos`: a página agora lista os produtos que vieram do MySQL, não mais de uma lista fixa no Python.

### 🔎 Verifique seu Entendimento

Um app de mobilidade urbana precisa de uma rota `/estacoes` que mostre só as estações de bike-sharing com pelo menos uma bicicleta livre.

**Desafio:** Escreva a chamada a `execute_query` (com `fetch=True`) que busca essas estações na tabela `estacao`, assumindo que ela tem uma coluna `bicicletas_livres`, seguindo exatamente o padrão usado na rota `/produtos` desta seção.

> 💬 Tente por conta própria antes de seguir. A solução comentada está no gabarito desta aula (link na última seção da página).

---

## Parte 6 — SQL fundamental no Workbench

Antes de avançar para o CRUD completo, é essencial dominar os comandos SQL que o Python vai executar por baixo dos panos. Execute cada bloco no Workbench (`Ctrl+Enter`) e observe o resultado na grade antes de passar para o próximo:

```sql
-- ─── SELECT ──────────────────────────────────────────────────────
SELECT * FROM produto;
SELECT nome, preco, estoque FROM produto ORDER BY preco DESC;
SELECT * FROM produto WHERE estoque = 0;
SELECT * FROM produto WHERE preco BETWEEN 200 AND 500;
```

Rode esse primeiro bloco e observe: cada `SELECT` muda o que aparece na grade de resultados, do jeito que a cláusula pede.

```sql
-- LIKE com % busca texto em qualquer posição
SELECT * FROM produto WHERE nome LIKE '%mouse%';

-- Funções de agregação
SELECT COUNT(*)             AS total    FROM produto;
SELECT ROUND(AVG(preco), 2) AS media    FROM produto;
SELECT SUM(estoque)         AS estoque_total FROM produto;
```

Rode este segundo bloco: note que as funções de agregação (`COUNT`, `AVG`, `SUM`) devolvem uma única linha com o resultado calculado, diferente dos `SELECT` anteriores que devolviam várias linhas.

```sql
-- ─── INSERT ──────────────────────────────────────────────────────
INSERT INTO produto (nome, descricao, preco, estoque)
VALUES ('Webcam Logitech C920', 'Full HD 1080p, microfone duplo', 449.90, 18);
```

Rode o `INSERT` e depois repita `SELECT * FROM produto;`: a Webcam aparece como um sexto registro, com um novo `id` gerado automaticamente pelo `AUTO_INCREMENT`.

```sql
-- ─── UPDATE ──────────────────────────────────────────────────────
-- ATENÇÃO: sem WHERE o UPDATE afeta TODOS os registros!
UPDATE produto SET estoque = 10 WHERE id = 4;
UPDATE produto SET ativo   = 0  WHERE estoque = 0;
```

Rode o `UPDATE` e confira com um novo `SELECT` que só o produto de `id = 4` mudou de estoque — o `WHERE` é o que garante que a alteração fique restrita à linha certa.

```sql
-- ─── DELETE ──────────────────────────────────────────────────────
-- ATENÇÃO: sem WHERE o DELETE apaga TODOS os registros!
-- Sempre use WHERE com id específico:
DELETE FROM produto WHERE id = 99;
```

Como não existe produto com `id = 99`, esse `DELETE` não apaga nada — é proposital, para você rodá-lo sem risco de perder dados reais nesta prática.

Cada um desses comandos SQL tem um equivalente direto em Python via `execute_query`. Praticar no Workbench antes de codificar no Python é uma estratégia fundamental: você vê o resultado imediatamente, sem a variável do código Python adicionando complexidade ao diagnóstico.

### 🔎 Verifique seu Entendimento

A tabela `ponto_coleta` da Parte 2 (nome, endereço, quilos coletados, ativo, cadastrado_em) já tem alguns registros.

**Desafio:** Escreva o `SELECT` que lista os pontos com mais de 100 quilos coletados, ordenados do maior para o menor volume, e o `UPDATE` que desativa (`ativo = 0`) um ponto específico pelo `id`, seguindo o padrão desta seção (incluindo o comentário de atenção sobre o `WHERE`).

> 💬 Tente por conta própria antes de seguir. A solução comentada está no gabarito desta aula (link na última seção da página).

---

## Parte 7 — SQL Injection: o risco que você precisa conhecer desde o início

**SQL Injection** é a vulnerabilidade de segurança mais comum em sistemas web e uma das mais destrutivas. Ela ocorre quando dados do usuário são inseridos diretamente em uma string SQL por concatenação, permitindo que um atacante manipule a query:

```python
# ❌ CÓDIGO VULNERÁVEL — NUNCA faça isso
usuario = request.form['usuario']
sql = f"SELECT * FROM usuario WHERE login='{usuario}'"
cursor.execute(sql)
# Se o atacante digitar: ' OR '1'='1' --
# A query vira: SELECT * FROM usuario WHERE login='' OR '1'='1' --
# Como '1'='1' é sempre verdadeiro, TODOS os usuários são retornados
```

Variantes mais agressivas usam `'; DROP TABLE usuario; --` para destruir tabelas inteiras com um único envio de formulário.

![SQL Injection: concatenação abre brechas devastadoras — placeholders %s eliminam completamente o risco](../imgs/Aula_05_img_05.png)

A solução é simples e inviolável: **sempre use queries parametrizadas com placeholders `%s`**. O conector MySQL trata os valores passados como dados puros — nunca os interpreta como código SQL:

```python
# ✅ CÓDIGO SEGURO — sempre assim, sem exceção
sql = "SELECT * FROM usuario WHERE login = %s AND senha = %s"
cursor.execute(sql, (usuario, senha))
# Mesmo que usuario contenha ' OR '1'='1', ele será tratado como texto literal
```

Esta é a regra mais importante desta aula: **jamais concatene dados do usuário em strings SQL**. Repare que a função `execute_query` do `db.py`, construída na Parte 5, já força esse hábito: o parâmetro `params` é sempre passado separado do `sql`, nunca colado dentro da string.

### 🔎 Verifique seu Entendimento

Um sistema de venda de ingressos para shows de 2026 tem uma busca de eventos por nome, implementada com `sql = f"SELECT * FROM evento WHERE nome LIKE '%{termo}%'"` seguido de `cursor.execute(sql)`.

**Desafio:** Explique qual valor um atacante poderia digitar no campo de busca para que a query retorne todos os eventos independentemente do termo, e reescreva o trecho de código usando placeholder `%s` para eliminar a vulnerabilidade.

> 💬 Tente por conta própria antes de seguir. A solução comentada está no gabarito desta aula (link na última seção da página).

---

## 🃏 Flashcards de Revisão

Tente responder mentalmente antes de clicar para revelar.

??? question "Qual a diferença entre dado volátil e dado persistente?"
    Dado **volátil** existe só enquanto o programa está rodando na memória RAM — some se o servidor reiniciar. Dado **persistente** é gravado em um armazenamento durável (como um banco de dados) e sobrevive a reinicializações, quedas de energia e reinícios do servidor.

??? question "Por que `DECIMAL(10, 2)` é melhor que `INT` ou tipos de ponto flutuante para armazenar preços?"
    `DECIMAL(p, d)` guarda um número exato de casas decimais sem os erros de arredondamento típicos de ponto flutuante binário — essencial para valores monetários. `INT` não suporta centavos, e `FLOAT`/`DOUBLE` podem introduzir imprecisões perigosas em cálculos financeiros.

??? question "Quais são as cinco etapas do ciclo de vida de uma conexão MySQL em Python?"
    1) Conectar (`connect()`), 2) obter o cursor (`conn.cursor()`), 3) executar o SQL (`cursor.execute()`), 4) confirmar a escrita (`conn.commit()`) ou ler o resultado (`fetchall()`), 5) fechar cursor e conexão — idealmente dentro de um `finally`.

??? question "Para que serve um pool de conexões, e o que `conn.close()` realmente faz quando a conexão vem de um pool?"
    O pool mantém um conjunto fixo de conexões abertas e reutilizáveis, evitando o custo de abrir/fechar uma conexão TCP a cada requisição. Quando a conexão vem de um pool, `conn.close()` não a fecha fisicamente — apenas a devolve ao pool para a próxima requisição reutilizar.

??? question "Por que centralizar o acesso ao banco em um módulo `db.py` em vez de repetir a conexão em cada rota?"
    Porque credenciais e configuração de conexão ficam em um único lugar — mudar a senha ou migrar de servidor exige editar um arquivo, não dezenas de rotas. Além disso, as rotas do `app.py` ficam livres de detalhes de infraestrutura, só chamando `execute_query`.

??? question "Por que `cursor.execute(sql, (usuario, senha))` é seguro contra SQL Injection, mas `f\"...{usuario}...\"` não é?"
    Com placeholders `%s` e uma tupla de parâmetros, o conector MySQL sempre trata os valores como **dados**, nunca como parte do comando SQL — mesmo que o valor contenha aspas ou palavras-chave SQL. Com f-string, o valor é colado na string antes de virar SQL, permitindo que um atacante injete código.

---

## ✅ Quiz de Fixação

<quiz>
Qual tipo SQL é mais adequado para armazenar o preço de um produto, como `1199.90`?
- [ ] INT
> Não. `INT` só armazena números inteiros — perderia os centavos.
- [x] DECIMAL(10, 2)
> Correto. `DECIMAL(p, d)` guarda um número exato de casas decimais, ideal para valores monetários.
- [ ] VARCHAR(10)
> Não. Armazenar preço como texto impede cálculos e ordenações numéricas corretas.
- [ ] TINYINT(1)
> Não. `TINYINT(1)` é usado para valores booleanos (0 ou 1), não para preços.
</quiz>

<quiz>
Sobre o ciclo de vida de uma conexão MySQL em Python, marque TODAS as afirmações corretas:
- [x] O cursor é o objeto usado para executar comandos SQL
> Sim — `cursor.execute(sql, params)` é como o comando chega ao banco.
- [x] `conn.commit()` é obrigatório após um INSERT, UPDATE ou DELETE para a alteração ser salva
> Sim — com `autocommit=False`, sem `commit()` a alteração fica pendente e pode ser perdida.
- [x] Fechar a conexão dentro de um bloco `finally` garante o fechamento mesmo se ocorrer um erro
> Sim — é exatamente por isso que `db.py` usa `try/except/finally`.
- [ ] `fetchall()` deve ser chamado após um INSERT para confirmar a escrita
> Não. `fetchall()` é para ler resultados de um `SELECT`; escritas usam `commit()`, não `fetchall()`.
</quiz>

<quiz>
Qual é a principal vantagem de um pool de conexões em uma aplicação web com muitos usuários simultâneos?
- [ ] Ele impede erros de sintaxe SQL
> Não. Erros de sintaxe SQL não têm relação com pool de conexões.
- [x] Ele reutiliza conexões já abertas, evitando o custo de abrir e fechar uma conexão a cada requisição
> Correto. Abrir uma conexão TCP nova a cada requisição é caro; o pool mantém conexões prontas para reuso.
- [ ] Ele criptografa automaticamente a senha do banco
> Não. Criptografia é responsabilidade de SSL/TLS (`ssl_disabled`, `ssl_ca`), um parâmetro separado.
- [ ] Ele elimina a necessidade de `commit()`
> Não. `commit()` continua sendo necessário para cada operação de escrita, com ou sem pool.
</quiz>

<quiz>
Por que o código `sql = f"SELECT * FROM usuario WHERE login='{usuario}'"` seguido de `cursor.execute(sql)` é perigoso?
- [ ] Porque f-strings são mais lentas que concatenação com +
> Não é uma questão de performance — é uma questão de segurança.
- [x] Porque permite SQL Injection: um valor malicioso digitado pelo usuário pode alterar o comando SQL executado
> Correto. Sem placeholders, o valor do usuário vira parte literal do comando SQL, podendo ser manipulado por um atacante.
- [ ] Porque o Flask bloqueia f-strings dentro de rotas
> Não. O Flask não tem essa restrição; o problema é específico de como o SQL é montado.
- [ ] Porque MySQL não aceita aspas simples em nenhuma situação
> Não. MySQL aceita aspas simples normalmente — o problema é a falta de parametrização, não as aspas em si.
</quiz>

<quiz>
Qual das opções abaixo é a forma segura e correta de executar uma query com um valor vindo do usuário?
- [ ] `cursor.execute(f"SELECT * FROM produto WHERE id={id_produto}")`
> Não. Concatenar o valor diretamente na string abre brecha para SQL Injection.
- [x] `cursor.execute("SELECT * FROM produto WHERE id = %s", (id_produto,))`
> Correto. O placeholder `%s` com o valor passado separadamente garante que o dado nunca seja interpretado como código SQL.
- [ ] `cursor.execute("SELECT * FROM produto WHERE id = " + str(id_produto))`
> Não. Concatenação com `+` tem exatamente o mesmo risco que a f-string.
- [ ] `cursor.execute("SELECT * FROM produto WHERE id = {}".format(id_produto))`
> Não. `.format()` também concatena o valor diretamente na string SQL, sem proteção contra injection.
</quiz>

---

## 📝 Resumo

Hoje você conectou o Python ao mundo da persistência. Instalou e configurou o MySQL, criou o banco `projeto_web` e a tabela principal via script Python com `executemany`, construído em incrementos pequenos e testados um a um. Aprendeu o ciclo de vida de uma conexão (conectar → cursor → executar → commit/fetchall → fechar) e por que o `finally` é essencial.

Conheceu os parâmetros avançados do conector: `sql_mode` (valida os dados com rigor), `time_zone` (garante consistência de datas entre ambientes), `use_pure` (Python puro resolve incompatibilidades de autenticação quando tudo parece correto mas a conexão falha), `connection_timeout` (evita travamentos por servidor inacessível) e `autocommit=False` (exige `commit()` explícito para controle de transações).

Configurou um **pool de conexões** no `db.py` com `MySQLConnectionPool` — fundamental para aplicações web, onde reutilizar conexões existentes é muito mais eficiente do que abrir e fechar uma por requisição. Viu como esse mesmo padrão se aplica a bancos em nuvem, como o Azure Database for MySQL, com a adição de SSL e parâmetros específicos do ambiente.

Criou o módulo `db.py` que centraliza tudo e expõe `execute_query` e `execute_one`, substituindo os dados estáticos por dados reais do banco. Aprendeu o que é SQL Injection, como funciona e por que placeholders `%s` eliminam completamente o risco.

![Mapa mental da Aula 05: MySQL, SQL básico, conexão Python e segurança contra SQL Injection](../imgs/Aula_05_img_06.png)

Na próxima aula, o CRUD começa de verdade: você vai construir o **Create** conectando o formulário da Aula 04 diretamente ao `INSERT INTO`, e o **Read** completo com filtros dinâmicos usando `WHERE 1=1` e `LIKE`. Metade do sistema ficará funcional de ponta a ponta.

---

## Parte 8 — Atividade da Aula

Crie o `db_setup.py` adaptado para o domínio do seu sistema (produtos, livros, clientes, consultas, filmes — o que você escolheu). Defina a tabela principal com pelo menos seis colunas de tipos variados: `INT AUTO_INCREMENT PRIMARY KEY`, `VARCHAR(n)`, `TEXT`, `DECIMAL(10,2)`, `TINYINT(1)` e `TIMESTAMP DEFAULT CURRENT_TIMESTAMP`. Insira pelo menos cinco registros de exemplo representativos. Execute o script e confirme no Workbench. Crie o `db.py` com `execute_query` e `execute_one`. Atualize a rota de listagem no `app.py` para buscar dados do MySQL em vez da lista estática.

```
git add .
git commit -m "Aula 05: MySQL conectado, tabela criada, listagem via banco real"
git push
```

---

## 🏆 Conquista da Aula

!!! success "Selo desbloqueado: 🔌 Integrador(a) de Dados"
    Você completou a Aula 05. Sua aplicação agora tem memória permanente: os dados sobrevivem a qualquer reinicialização do servidor, e o acesso ao banco está centralizado em um módulo seguro contra SQL Injection. Na próxima aula, você une tudo: formulários da Aula 04 gravando direto no banco, e o Read completo do CRUD.

---

## 🔗 Navegação

⬅️ [Aula 04 — Formulários e HTTP](Aula_04_Formularios_e_HTTP.md) · 🔒 Aula 06 — em breve.

---

## Referências e Leitura Complementar

A documentação oficial do `mysql-connector-python` está em `dev.mysql.com/doc/connector-python/en`. O manual completo do MySQL 8.0 com todas as funções SQL está em `dev.mysql.com/doc/refman/8.0`. O guia definitivo sobre SQL Injection do OWASP está em `owasp.org/www-community/attacks/SQL_Injection`.

---

## 📋 Gabarito dos Exercícios

Os mini-desafios de "🔎 Verifique seu Entendimento" espalhados ao longo desta aula têm as soluções comentadas reunidas em um único arquivo, organizado por bloco de conteúdo. Tente resolver cada desafio por conta própria antes de conferir.

➡️ [Gabarito — Aula 05](gabaritos/Aula_05_gabarito.md)

---

*Fatec Jahu · ILP951 · Prof. Ronan Adriel Zenatti · 2026*
