# Capítulo 2.1 — Python essencial (opcional)

**Disciplina:** Programação para Internet (ILP951)
**Professor:** Ronan Adriel Zenatti · ronan.zenatti@cps.sp.gov.br
**Fatec Jahu — 2º Semestre/2026**

---

## 🎯 Objetivos do Capítulo

Ao final deste capítulo você deverá ser capaz de:

- Executar um script Python pelo terminal e mostrar resultados com `print`
- Guardar valores em variáveis (texto, número inteiro, número decimal e verdadeiro/falso) e converter um tipo em outro
- Montar textos com f-strings e formatar um preço no padrão brasileiro
- Tomar decisões com `if`, `elif` e `else`, usando comparações, `and`, `in` e `None`
- Criar funções com parâmetros e `return`, inclusive a que devolve uma mensagem de erro ou `None`
- Guardar vários valores em uma lista e percorrê-la com `for`
- Representar um produto com um dicionário e procurar um produto em uma lista de dicionários
- Tratar um erro previsível com `try` e `except`
- Usar o `import` com módulos do Python e com um módulo seu

Este capítulo é **opcional**. Se você já escreve funções, listas, dicionários e `try/except` com tranquilidade, pode seguir direto para o Capítulo 3: nada daqui é pré-requisito, e todo conceito de Python aparece explicado de novo no primeiro uso. Ele serve a quem fez o curso básico de Python há algum tempo e quer relembrar, com exemplos do próprio catálogo, o Python que vai aparecer daqui em diante. Não há navegador nem Flask neste capítulo: tudo roda no terminal.

## 📦 Ponto de partida

Este capítulo parte do **seu** repositório `catalogo-produtos`, como ele ficou no fim do Capítulo 2. Os scripts de Python deste capítulo ficam dentro da pasta `treino`, o laboratório que já existe no projeto, e não mudam o catálogo.

Se o seu projeto não está funcionando, baixe o código do Capítulo 2 e descompacte na Área de Trabalho:

➡️ [Baixar p1_cap_02.zip](../arquivos/p1_cap_02.zip)

---

## Tópico 1 — O primeiro script e as variáveis

### Antes de começar

Abra a pasta `catalogo-produtos` no VS Code (se ela estiver em outro computador, ou se você apagou a pasta, use o `git clone` do Capítulo 2). Abra o terminal com `Ctrl + '` e rode:

```bash
git pull
git status
```

O `git status` deve dizer `nothing to commit, working tree clean`. Agora confira se o Python está instalado:

```bash
python --version
```

Deve aparecer algo como `Python 3.12.4` (qualquer versão 3.10 ou mais nova serve). Se aparecer um erro, ou se o Windows abrir a Microsoft Store, baixe o instalador em **python.org** e, na primeira tela, marque a caixa **Add python.exe to PATH** antes de clicar em **Install Now**. Depois feche o VS Code, abra de novo e repita o comando.

Crie a pasta onde ficarão os scripts, dentro de `treino`:

```bash
mkdir treino\python
```

### O que é um script

Um **script** é um arquivo de texto com a extensão `.py`, cheio de instruções que o Python executa **de cima para baixo, uma linha por vez**. No VS Code, crie o arquivo `treino/python/ola.py` com uma única linha:

```python
print('Olá, Python!')
```

Salve e rode no terminal, a partir da pasta do projeto:

```bash
python treino/python/ola.py
```

O terminal mostra:

```text
Olá, Python!
```

O `print(...)` escreve na tela o que estiver entre os parênteses. O texto entre aspas (simples ou duplas, tanto faz) é um valor do tipo **texto**. Neste curso, usaremos aspas simples.

### Variáveis

Uma **variável** é um nome que guarda um valor. Acrescente, depois da primeira linha:

```python
# Uma variável guarda um valor com um nome
nome = 'Caneta esferográfica azul'
print(nome)
```

Salve e rode de novo. A segunda linha da saída é o nome do produto. O `=` **não é uma comparação**: ele diz "guarde o valor da direita no nome da esquerda". A linha que começa com `#` é um **comentário**, que o Python ignora e serve para explicar o código. Os nomes de variável usam letras minúsculas, sem espaço e sem acento, com `_` para separar palavras (`valor_em_estoque`).

Acrescente mais três variáveis, cada uma de um tipo diferente, e mostre-as:

```python
preco = 2.50
estoque = 40
ativo = True

print(preco)
print(estoque)
print(ativo)
```

Salve e rode. Repare que o preço aparece como `2.5`: o Python não mostra o zero final. E o número usa **ponto** para as casas decimais, nunca vírgula.

### Os tipos de valor

Cada valor tem um **tipo**. Peça ao Python que diga o de cada variável:

```python
print(type(nome))
print(type(preco))
print(type(estoque))
print(type(ativo))
```

Salve e rode. As quatro últimas linhas da saída são:

```text
<class 'str'>
<class 'float'>
<class 'int'>
<class 'bool'>
```

| Tipo | O que guarda | Exemplo |
|---|---|---|
| `str` | texto | `'Teclado USB'` |
| `int` | número inteiro | `40` |
| `float` | número com casas decimais | `2.50` |
| `bool` | verdadeiro ou falso | `True` ou `False` (com a inicial maiúscula) |

Com números, o Python faz contas com `+`, `-`, `*` e `/`. Acrescente:

```python
valor_em_estoque = preco * estoque
print(valor_em_estoque)
```

Salve e rode: `100.0`, ou seja, 2,50 vezes 40. Uma conta com `float` sempre dá `float`.

### Texto que parece número

Lembra do `.value` do Capítulo 2, que sempre devolve texto, mesmo em um campo numérico? O mesmo problema existe aqui. Acrescente:

```python
texto_preco = '2.50'
print(texto_preco + texto_preco)
print(float(texto_preco) + float(texto_preco))
```

Salve e rode. A saída é:

```text
2.502.50
5.0
```

Com texto, o `+` **cola** os dois valores (`2.502.50`). Para somar de verdade, é preciso converter antes: `float()` transforma texto em número decimal. Existem três conversões que você vai usar muito:

- `int('40')` transforma texto em número inteiro;
- `float('2.50')` transforma texto em número decimal;
- `str(40)` transforma um número em texto.

Acrescente a última dupla de linhas:

```python
print(int('40') + 1)
print('Estoque: ' + str(estoque))
```

Salve e rode. As duas últimas linhas da saída são `41` e `Estoque: 40`. Sem o `str(...)`, juntar um texto com um número dá erro, porque o Python não mistura os dois tipos. O `ola.py` completo:

```python
print('Olá, Python!')

# Uma variável guarda um valor com um nome
nome = 'Caneta esferográfica azul'
print(nome)

preco = 2.50
estoque = 40
ativo = True

print(preco)
print(estoque)
print(ativo)

print(type(nome))
print(type(preco))
print(type(estoque))
print(type(ativo))

valor_em_estoque = preco * estoque
print(valor_em_estoque)

texto_preco = '2.50'
print(texto_preco + texto_preco)
print(float(texto_preco) + float(texto_preco))

print(int('40') + 1)
print('Estoque: ' + str(estoque))
```

Registre no Git e envie:

```bash
git add .
git commit -m "Adiciona o primeiro script em Python"
git push
```

---

## Tópico 2 — Texto e f-strings

### O problema: montar frases com `+`

Quase toda página que você vai criar mistura texto fixo com valores de variáveis. Crie o arquivo `treino/python/texto.py`:

```python
nome = 'Mouse sem fio'
preco = 59.9

print('Produto: ' + nome + ' custa R$ ' + str(preco))
```

Salve e rode (`python treino/python/texto.py`). A saída é `Produto: Mouse sem fio custa R$ 59.9`. Funciona, mas olhe o código: aspas abrindo e fechando, `+` por todo lado e um `str(...)` para o número. Qualquer frase maior vira uma bagunça.

### A f-string

A **f-string** resolve isso. Acrescente depois da última linha:

```python
print(f'Produto: {nome} custa R$ {preco}')
```

Salve e rode: a segunda linha da saída é igual à primeira, escrita com muito menos ruído. O `f` colado antes das aspas avisa que o texto tem **buracos**, e o que está entre chaves `{ }` é trocado pelo valor da variável, de qualquer tipo, sem precisar do `str()`.

### Formatando o preço

O preço `59.9` está esquisito, e sabemos que o certo é `59,90`. Dentro das chaves dá para dizer **como** mostrar o valor. Acrescente:

```python
print(f'Preço com duas casas: {preco:.2f}')
```

Salve e rode: `Preço com duas casas: 59.90`. O `:.2f` significa "decimal (`f`) com 2 casas depois do ponto". Falta trocar o ponto pela vírgula, e para isso o texto tem o método `.replace('.', ',')`, que troca um pedaço por outro. Acrescente:

```python
preco_br = f'{preco:.2f}'.replace('.', ',')
print(f'Preço no padrão brasileiro: R$ {preco_br}')
```

Salve e rode: `Preço no padrão brasileiro: R$ 59,90`. Guarde essa receita (`:.2f` e `.replace`), porque ela vai virar uma função no Tópico 4.

### Limpando o que o usuário digita

Quem digita em um formulário deixa espaços sobrando e mistura maiúsculas e minúsculas. O texto tem métodos para arrumar isso. Acrescente:

```python
digitado = '   Teclado USB  '
print(digitado)
print(digitado.strip())
print(digitado.strip().lower())
print(digitado.strip().upper())
print(len(digitado.strip()))
```

Salve e rode. As cinco últimas linhas da saída são:

```text
   Teclado USB  
Teclado USB
teclado usb
TECLADO USB
11
```

- `.strip()` remove os espaços do começo e do fim;
- `.lower()` deixa tudo em minúsculas e `.upper()` em maiúsculas;
- `len(...)` conta quantos caracteres o texto tem (aqui, 11);
- dá para **encadear**: `digitado.strip().lower()` limpa e depois baixa as letras.

Repare que a primeira linha, `print(digitado)`, ainda mostra os espaços: os métodos não alteram a variável, eles **devolvem um texto novo**. Se quiser guardar o resultado, atribua a uma variável (`digitado = digitado.strip()`). O `texto.py` completo:

```python
nome = 'Mouse sem fio'
preco = 59.9

print('Produto: ' + nome + ' custa R$ ' + str(preco))

print(f'Produto: {nome} custa R$ {preco}')

print(f'Preço com duas casas: {preco:.2f}')

preco_br = f'{preco:.2f}'.replace('.', ',')
print(f'Preço no padrão brasileiro: R$ {preco_br}')

digitado = '   Teclado USB  '
print(digitado)
print(digitado.strip())
print(digitado.strip().lower())
print(digitado.strip().upper())
print(len(digitado.strip()))
```

Registre no Git e envie:

```bash
git add .
git commit -m "Adiciona o script de textos e f-strings"
git push
```

---

## Tópico 3 — Decisões com `if`

### O primeiro `if`

Um programa útil precisa **escolher** o que fazer. Crie o arquivo `treino/python/decisao.py`:

```python
preco = 59.9

if preco < 20:
    print('Produto barato')
```

Salve e rode (`python treino/python/decisao.py`). **Nada aparece**: o preço não é menor que 20, então o bloco do `if` foi pulado. Troque o `59.9` por `10`, salve e rode de novo: agora aparece `Produto barato`. Volte o valor para `59.9`.

Duas regras do Python aparecem aqui, e vão se repetir em todo o curso:

- a linha do `if` termina com **dois-pontos** (`:`);
- o que está **dentro** do `if` fica **indentado**, com 4 espaços (o VS Code põe isso quando você pressiona `Tab`). A indentação, e não chaves ou palavras de fechamento, é o que diz onde o bloco começa e termina.

### `elif` e `else`

Dá para encadear mais de uma condição. Troque o bloco do `if` por este (mantenha a linha `preco = 59.9`):

```python
if preco < 20:
    faixa = 'barato'
elif preco < 100:
    faixa = 'médio'
else:
    faixa = 'caro'

print(f'Faixa de preço: {faixa}')
```

Salve e rode: `Faixa de preço: médio`. O Python testa de cima para baixo e executa **só o primeiro** bloco cuja condição for verdadeira. O `elif` (de "senão, se") testa outra condição, e o `else` (de "senão") pega tudo o que sobrou e não tem condição. Experimente `10`, `59.9` e `150` no preço: `barato`, `médio` e `caro`. É exatamente a faixa de preços que o Capítulo 5 vai montar no template.

### Os operadores de comparação

Cada condição é uma pergunta cuja resposta é `True` ou `False`:

| Operador | Pergunta |
|---|---|
| `==` | é igual a? |
| `!=` | é diferente de? |
| `<` e `>` | é menor que? é maior que? |
| `<=` e `>=` | é menor ou igual? é maior ou igual? |

!!! warning "`=` e `==` são coisas diferentes"
    Um só `=` **guarda** um valor (`preco = 59.9`). Dois (`==`) **comparam** (`preco == 59.9`). Escrever `if preco = 59.9:` dá erro de sintaxe.

### Combinando condições com `and` e `in`

Acrescente, depois do `print` da faixa:

```python
estoque = 0
nome = 'Teclado USB'

if preco > 0 and estoque > 0:
    print('Disponível para venda')
else:
    print('Indisponível')

if 'USB' in nome:
    print('É um produto USB')
```

Salve e rode. As duas últimas linhas da saída são `Indisponível` e `É um produto USB`. O `and` exige que as **duas** condições sejam verdadeiras (existe também o `or`, em que basta **uma**, e o `not`, que inverte). Como o estoque é 0, a segunda condição falhou. O `in` pergunta se um pedaço de texto aparece dentro de outro. Troque o `estoque = 0` por `estoque = 5` e rode de novo para ver o `Disponível para venda`. Depois volte para `estoque = 0`.

### O `None`

O `None` é o valor do Python para **"nada"**: uma variável que ainda não tem valor. Para testá-lo, usa-se `is None`. Acrescente:

```python
categoria = None

if categoria is None:
    print('Sem categoria')
else:
    print(f'Categoria: {categoria}')

if nome == 'Teclado USB':
    print('Achei o teclado')
```

Salve e rode: `Sem categoria` e `Achei o teclado`. O `None` não é o texto vazio `''` nem o número `0`: é a ausência de valor. Ele aparece o tempo todo, por exemplo quando uma busca não encontra nada. O `decisao.py` completo (com `estoque = 0`):

```python
preco = 59.9

if preco < 20:
    faixa = 'barato'
elif preco < 100:
    faixa = 'médio'
else:
    faixa = 'caro'

print(f'Faixa de preço: {faixa}')

estoque = 0
nome = 'Teclado USB'

if preco > 0 and estoque > 0:
    print('Disponível para venda')
else:
    print('Indisponível')

if 'USB' in nome:
    print('É um produto USB')

categoria = None

if categoria is None:
    print('Sem categoria')
else:
    print(f'Categoria: {categoria}')

if nome == 'Teclado USB':
    print('Achei o teclado')
```

Registre no Git e envie:

```bash
git add .
git commit -m "Adiciona o script de decisões com if"
git push
```

---

## Tópico 4 — Funções

### O problema: o mesmo código repetido

Crie o arquivo `treino/python/funcoes.py` e formate três preços com a receita do Tópico 2:

```python
print('R$ ' + f'{2.5:.2f}'.replace('.', ','))
print('R$ ' + f'{18.9:.2f}'.replace('.', ','))
print('R$ ' + f'{129:.2f}'.replace('.', ','))
```

Salve e rode (`python treino/python/funcoes.py`):

```text
R$ 2,50
R$ 18,90
R$ 129,00
```

Funciona, mas a mesma receita foi escrita três vezes. Se o formato mudar (um `R$` sem espaço, por exemplo), é preciso achar e corrigir cada linha, e esquecer uma é erro certo. Um catálogo com 500 produtos tornaria isso impraticável.

### A função

Uma **função** é um bloco de código com um **nome**, que você escreve uma vez e **chama** quantas vezes quiser. Troque as três linhas por:

```python
def formata_preco(valor):
    texto = f'{valor:.2f}'.replace('.', ',')
    return 'R$ ' + texto


print(formata_preco(2.5))
print(formata_preco(18.9))
print(formata_preco(129))
```

Salve e rode: a saída é a mesma de antes, mas a receita agora existe em um único lugar. Veja as peças:

- `def formata_preco(valor):` **define** a função. O nome vem depois do `def`, e entre parênteses fica o **parâmetro** (`valor`), o dado que a função recebe para trabalhar. A linha termina com `:` e o corpo fica indentado, como no `if`;
- `return` **devolve** o resultado para quem chamou a função e encerra a função;
- `formata_preco(2.5)` **chama** a função. O `2.5` é o **argumento**, e vira o `valor` lá dentro;
- a variável `texto` só existe **dentro** da função. Fora dela, o Python não a conhece.

(As duas linhas em branco antes do código que chama a função são uma convenção do Python para separar a função do resto, e não uma obrigação.)

### `print` e `return` não são a mesma coisa

Este é um engano comum. Acrescente, ao final do arquivo:

```python
def mostra_preco(valor):
    print(formata_preco(valor))


resultado = mostra_preco(10)
print(resultado)
```

Salve e rode. As duas últimas linhas da saída são `R$ 10,00` e `None`. A função `mostra_preco` **escreveu** na tela com o `print`, mas não tem `return`, então devolveu `None` (o "nada" do Tópico 3), e a variável `resultado` ficou sem valor. Resumindo: o `print` **mostra** um valor na tela, o `return` **entrega** um valor a quem chamou. Uma rota do Flask, por exemplo, precisa de `return`, e não de `print`.

### Valor padrão e argumento nomeado

Um parâmetro pode ter um **valor padrão**, usado quando a chamada não informa nada. Troque a primeira função (`formata_preco`) por esta versão, e acrescente a última linha ao final do arquivo:

```python
def formata_preco(valor, simbolo='R$'):
    texto = f'{valor:.2f}'.replace('.', ',')
    return simbolo + ' ' + texto
```

```python
print(formata_preco(2.5, simbolo='US$'))
```

Salve e rode. As linhas anteriores continuam iguais (`R$ 2,50` e as outras), porque sem o segundo argumento vale o padrão `'R$'`. A última linha da saída é `US$ 2,50`: o `simbolo='US$'` é um **argumento nomeado**, em que você diz o nome do parâmetro na chamada. Ele deixa a chamada legível e permite pular parâmetros opcionais.

### A função de validação: a mensagem ou `None`

Há um tipo de função que você vai escrever dezenas de vezes: a que **valida um campo**. O padrão do curso é devolver a **mensagem de erro** quando o valor é inválido e `None` quando está tudo certo. Acrescente ao final do arquivo:

```python
def valida_nome(nome):
    if nome == '':
        return 'Informe o nome.'
    if len(nome) < 3:
        return 'O nome deve ter pelo menos 3 caracteres.'
    return None


print(valida_nome(''))
print(valida_nome('ab'))
print(valida_nome('Caneta'))
```

Salve e rode. As três últimas linhas da saída são:

```text
Informe o nome.
O nome deve ter pelo menos 3 caracteres.
None
```

Repare que há vários `return` e que **o primeiro que for executado encerra a função**: com o nome vazio, a função devolve a primeira mensagem e nem chega ao segundo `if`. Quem chama a função só precisa perguntar `if mensagem is None:` (tudo certo) ou tratar a mensagem como erro. É assim que o Capítulo 9 valida o formulário. O `funcoes.py` completo:

```python
def formata_preco(valor, simbolo='R$'):
    texto = f'{valor:.2f}'.replace('.', ',')
    return simbolo + ' ' + texto


print(formata_preco(2.5))
print(formata_preco(18.9))
print(formata_preco(129))


def mostra_preco(valor):
    print(formata_preco(valor))


resultado = mostra_preco(10)
print(resultado)
print(formata_preco(2.5, simbolo='US$'))


def valida_nome(nome):
    if nome == '':
        return 'Informe o nome.'
    if len(nome) < 3:
        return 'O nome deve ter pelo menos 3 caracteres.'
    return None


print(valida_nome(''))
print(valida_nome('ab'))
print(valida_nome('Caneta'))
```

Registre no Git e envie:

```bash
git add .
git commit -m "Adiciona o script de funções"
git push
```

---

## Tópico 5 — Listas e `for`

### A lista

Um catálogo tem muitos produtos, e não faz sentido ter uma variável para cada um. A **lista** guarda vários valores em sequência, entre colchetes, separados por vírgula. Crie o arquivo `treino/python/listas.py`:

```python
categorias = ['Papelaria', 'Informática', 'Casa']

print(categorias)
print(categorias[0])
print(categorias[2])
print(len(categorias))
```

Salve e rode (`python treino/python/listas.py`). A saída é:

```text
['Papelaria', 'Informática', 'Casa']
Papelaria
Casa
3
```

Cada item tem uma **posição**, chamada de **índice**, e a contagem começa em **0**: `categorias[0]` é o primeiro item e `categorias[2]` é o terceiro. O `len(...)` conta quantos itens a lista tem. Pedir um índice que não existe (`categorias[3]`) dá erro.

### Acrescentando e procurando

Acrescente ao final do arquivo:

```python
categorias.append('Acessórios')
print(categorias)

print('Casa' in categorias)
print('Beleza' in categorias)
```

Salve e rode. As três últimas linhas da saída são:

```text
['Papelaria', 'Informática', 'Casa', 'Acessórios']
True
False
```

O `.append(...)` coloca um item **no final** da lista. O `in`, o mesmo do Tópico 3, agora pergunta se o valor está na lista, e `not in` pergunta se **não** está.

### Percorrendo com `for`

O poder da lista aparece quando você faz algo com **cada** item. Acrescente:

```python
for categoria in categorias:
    print(categoria)
```

Salve e rode: as quatro categorias aparecem, uma por linha, ao final da saída. O `for categoria in categorias:` repete o bloco indentado **uma vez para cada item**, e a cada volta a variável `categoria` guarda um deles. O nome da lista fica no plural e o da variável do `for` no singular, o que faz a linha ser lida quase como uma frase.

### Somando e filtrando

Dentro do `for` dá para acumular valores e tomar decisões. Acrescente:

```python
precos = [2.50, 18.90, 59.90, 89.90, 49.90, 129.00]
total = 0

for preco in precos:
    total = total + preco

print(f'Soma dos preços: R$ {total:.2f}')
```

Salve e rode: `Soma dos preços: R$ 350.10`. A variável `total` começa em 0, e a cada volta recebe ela mesma mais o preço da vez. Agora um `if` **dentro** do `for`, que filtra:

```python
print('Preços acima de R$ 50:')
for preco in precos:
    if preco > 50:
        print(preco)
```

Salve e rode. A saída, ao final, é `Preços acima de R$ 50:` seguido de `59.9`, `89.9` e `129.0`. Cada nível de indentação é um bloco dentro do outro: o `print` só roda quando o `if` é verdadeiro, e o `if` roda a cada volta do `for`.

### Repetindo um número de vezes

Para repetir algo um certo número de vezes, o `for` usa o `range(...)`. Acrescente:

```python
for numero in range(1, 4):
    print(f'Página {numero}')
```

Salve e rode: `Página 1`, `Página 2` e `Página 3`. O `range(1, 4)` produz os números de 1 até **antes** do 4. O primeiro valor entra, o último não. Com um número só, `range(3)`, ele conta a partir do 0 (0, 1 e 2). O `listas.py` completo:

```python
categorias = ['Papelaria', 'Informática', 'Casa']

print(categorias)
print(categorias[0])
print(categorias[2])
print(len(categorias))

categorias.append('Acessórios')
print(categorias)

print('Casa' in categorias)
print('Beleza' in categorias)

for categoria in categorias:
    print(categoria)

precos = [2.50, 18.90, 59.90, 89.90, 49.90, 129.00]
total = 0

for preco in precos:
    total = total + preco

print(f'Soma dos preços: R$ {total:.2f}')

print('Preços acima de R$ 50:')
for preco in precos:
    if preco > 50:
        print(preco)

for numero in range(1, 4):
    print(f'Página {numero}')
```

Registre no Git e envie:

```bash
git add .
git commit -m "Adiciona o script de listas e for"
git push
```

---

## Tópico 6 — Dicionários

### O problema: um produto tem várias informações

Uma lista guarda itens **por posição**. Mas um produto tem `id`, `nome`, `categoria` e `preco`, e lembrar que o nome é o item 1 e o preço é o item 3 é pedir para errar. O **dicionário** guarda cada informação com um **nome** (a **chave**), em pares `chave: valor` entre chaves `{ }`. Crie o arquivo `treino/python/dicionarios.py`:

```python
produto = {'id': 1, 'nome': 'Caneta esferográfica azul', 'categoria': 'Papelaria', 'preco': 2.50}

print(produto)
print(produto['nome'])
print(produto['preco'])
```

Salve e rode (`python treino/python/dicionarios.py`). A saída é:

```text
{'id': 1, 'nome': 'Caneta esferográfica azul', 'categoria': 'Papelaria', 'preco': 2.5}
Caneta esferográfica azul
2.5
```

Para ler uma informação, escreve-se a chave entre colchetes: `produto['nome']`. As chaves são textos, por isso levam aspas.

### Mudando e acrescentando

Acrescente ao final:

```python
produto['preco'] = 2.75
produto['estoque'] = 40
print(produto)
```

Salve e rode. A última linha da saída mostra o dicionário com `'preco': 2.75` e um par novo, `'estoque': 40`, no final. Atribuir a uma chave que **existe** troca o valor, e atribuir a uma chave que **não existe** cria o par.

### Quando a chave não existe

Acrescente uma linha que pede uma chave inexistente:

```python
print(produto['cor'])
```

Salve e rode. O programa **para** com um erro:

```text
Traceback (most recent call last):
  File "...\treino\python\dicionarios.py", line 11, in <module>
    print(produto['cor'])
          ~~~~~~~^^^^^^^
KeyError: 'cor'
```

Leia a mensagem de baixo para cima: a última linha diz **qual** foi o erro (`KeyError`, "erro de chave") e qual chave faltou (`'cor'`), e as de cima dizem o arquivo e a linha (o começo do caminho e o número da linha podem ser diferentes no seu computador). Esse erro é comum quando um dado pode não existir, como um campo que o formulário não enviou. A solução é o método `.get()`, que não dá erro. **Apague** a linha com `produto['cor']` e acrescente no lugar:

```python
print(produto.get('cor'))
print(produto.get('cor', 'sem cor'))
```

Salve e rode. As duas últimas linhas da saída são `None` e `sem cor`. O `.get('cor')` devolve `None` quando a chave não existe, e o segundo argumento, `'sem cor'`, é o **valor padrão** que ele devolve no lugar do `None`.

### Uma lista de dicionários

Um catálogo é uma **lista de dicionários**: cada dicionário é um produto. Acrescente ao final do arquivo, com os mesmos seis produtos que o catálogo já mostra:

```python
produtos = [
    {'id': 1, 'nome': 'Caneta esferográfica azul', 'categoria': 'Papelaria', 'preco': 2.50},
    {'id': 2, 'nome': 'Caderno universitário 96 folhas', 'categoria': 'Papelaria', 'preco': 18.90},
    {'id': 3, 'nome': 'Mouse sem fio', 'categoria': 'Informática', 'preco': 59.90},
    {'id': 4, 'nome': 'Teclado USB', 'categoria': 'Informática', 'preco': 89.90},
    {'id': 5, 'nome': 'Garrafa térmica 500 ml', 'categoria': 'Casa', 'preco': 49.90},
    {'id': 6, 'nome': 'Mochila escolar', 'categoria': 'Acessórios', 'preco': 129.00},
]

for item in produtos:
    print(f"{item['id']} - {item['nome']} ({item['categoria']})")
```

Salve e rode. Seis linhas novas aparecem ao final da saída, como `3 - Mouse sem fio (Informática)`. O `for` do Tópico 5 agora percorre dicionários, e a cada volta `item` é um produto inteiro, de onde se tira cada informação pela chave.

!!! note "Aspas dentro da f-string"
    Dentro das chaves da f-string aparece `item['id']`, que tem aspas simples. Por isso o texto da f-string usa aspas **duplas**: se as aspas de fora e as de dentro fossem iguais, o Python acharia que o texto terminou no meio. É a única situação em que o curso usa aspas duplas.

Combine o `for` com o `if` para filtrar por categoria:

```python
print('Produtos de Informática:')
for item in produtos:
    if item['categoria'] == 'Informática':
        print(item['nome'])
```

Salve e rode: `Produtos de Informática:`, `Mouse sem fio` e `Teclado USB`.

### Procurando um produto

Para fechar, junte tudo em uma função que procura um produto pelo `id`: percorre a lista com o `for`, compara com o `if` e devolve com o `return`. Acrescente:

```python
def busca_produto(id_produto):
    for item in produtos:
        if item['id'] == id_produto:
            return item
    return None


print(busca_produto(3))
print(busca_produto(99))
```

Salve e rode. As duas últimas linhas da saída são o dicionário do mouse (`{'id': 3, 'nome': 'Mouse sem fio', 'categoria': 'Informática', 'preco': 59.9}`) e `None`. Se o `return item` é executado, a função termina ali. Se o `for` acaba sem encontrar ninguém, o último `return None` entrega o "nada". É o mesmo raciocínio da página de detalhe do Capítulo 3. O `dicionarios.py` completo:

```python
produto = {'id': 1, 'nome': 'Caneta esferográfica azul', 'categoria': 'Papelaria', 'preco': 2.50}

print(produto)
print(produto['nome'])
print(produto['preco'])

produto['preco'] = 2.75
produto['estoque'] = 40
print(produto)

print(produto.get('cor'))
print(produto.get('cor', 'sem cor'))

produtos = [
    {'id': 1, 'nome': 'Caneta esferográfica azul', 'categoria': 'Papelaria', 'preco': 2.50},
    {'id': 2, 'nome': 'Caderno universitário 96 folhas', 'categoria': 'Papelaria', 'preco': 18.90},
    {'id': 3, 'nome': 'Mouse sem fio', 'categoria': 'Informática', 'preco': 59.90},
    {'id': 4, 'nome': 'Teclado USB', 'categoria': 'Informática', 'preco': 89.90},
    {'id': 5, 'nome': 'Garrafa térmica 500 ml', 'categoria': 'Casa', 'preco': 49.90},
    {'id': 6, 'nome': 'Mochila escolar', 'categoria': 'Acessórios', 'preco': 129.00},
]

for item in produtos:
    print(f"{item['id']} - {item['nome']} ({item['categoria']})")

print('Produtos de Informática:')
for item in produtos:
    if item['categoria'] == 'Informática':
        print(item['nome'])


def busca_produto(id_produto):
    for item in produtos:
        if item['id'] == id_produto:
            return item
    return None


print(busca_produto(3))
print(busca_produto(99))
```

Registre no Git e envie:

```bash
git add .
git commit -m "Adiciona o script de dicionários"
git push
```

---

## Tópico 7 — Tratando erros com `try` e `except`

### O problema: o erro derruba o programa

No Tópico 6, o `KeyError` parou o programa. Um erro que **pode acontecer** (e que é culpa de quem digitou, e não do código) não deveria derrubar tudo. Crie o arquivo `treino/python/erros.py` e converta um preço que não é número:

```python
texto = 'abc'
preco = float(texto)
print(f'Preço lido: {preco}')
```

Salve e rode (`python treino/python/erros.py`):

```text
Traceback (most recent call last):
  File "...\treino\python\erros.py", line 2, in <module>
    preco = float(texto)
            ^^^^^^^^^^^^
ValueError: could not convert string to float: 'abc'
```

Quando o `float()` recebe um texto que não é número, ele levanta o erro `ValueError`, e o programa morre antes de chegar ao `print`. Em um site, isso seria uma página de erro para o visitante que digitou uma letra no campo de preço.

### `try` e `except`

O `try` ("tente") executa o bloco, e se aparecer o erro nomeado no `except` ("exceto se"), o Python **desvia** para o bloco do `except` em vez de parar. Troque todo o conteúdo do arquivo por:

```python
texto = 'abc'

try:
    preco = float(texto)
    print(f'Preço lido: {preco}')
except ValueError:
    print('Preço inválido.')

print('O programa continua.')
```

Salve e rode:

```text
Preço inválido.
O programa continua.
```

O `float('abc')` falhou, o `print` de dentro do `try` foi pulado, o `except` assumiu e o programa seguiu para a última linha. Troque `'abc'` por `'12.5'` e rode de novo: o bloco do `except` não executa, e aparece `Preço lido: 12.5`. Depois volte para `'abc'`.

!!! note "Por que `except ValueError` e não só `except`"
    Dizer **qual** erro você espera (`ValueError`) evita esconder erros que você não previu, como um nome de variável escrito errado, que apareceria como um falso "preço inválido". Capture só o que faz sentido tratar.

### O preço com vírgula

Agora um caso real do Brasil. Troque `'abc'` por `'59,90'` (a vírgula que o usuário digita) e rode:

```python
texto = '59,90'
```

A saída volta a ser `Preço inválido.`: o `float` só entende o **ponto**. A solução é trocar a vírgula por ponto antes de converter, com o `.replace` do Tópico 2. Troque a linha da conversão por:

```python
    preco = float(texto.replace(',', '.'))
```

Salve e rode: `Preço lido: 59.9` e `O programa continua.`. O arquivo agora está assim:

```python
texto = '59,90'

try:
    preco = float(texto.replace(',', '.'))
    print(f'Preço lido: {preco}')
except ValueError:
    print('Preço inválido.')

print('O programa continua.')
```

### Dentro de uma função

O `try` fica ainda melhor dentro de uma função que **devolve o número ou `None`**, o mesmo padrão do Tópico 4. Acrescente ao final do arquivo:

```python
def le_preco(texto):
    try:
        return float(texto.replace(',', '.'))
    except ValueError:
        return None


print(le_preco('59,90'))
print(le_preco('2.5'))
print(le_preco('abc'))
print(le_preco(''))
```

Salve e rode. As quatro últimas linhas da saída são `59.9`, `2.5`, `None` e `None`. A função aceita vírgula ou ponto e devolve `None` para qualquer coisa que não seja um número, inclusive o texto vazio. Quem a chama só precisa testar `if preco is None:`. O `erros.py` completo:

```python
texto = '59,90'

try:
    preco = float(texto.replace(',', '.'))
    print(f'Preço lido: {preco}')
except ValueError:
    print('Preço inválido.')

print('O programa continua.')


def le_preco(texto):
    try:
        return float(texto.replace(',', '.'))
    except ValueError:
        return None


print(le_preco('59,90'))
print(le_preco('2.5'))
print(le_preco('abc'))
print(le_preco(''))
```

Registre no Git e envie:

```bash
git add .
git commit -m "Adiciona o script de tratamento de erros"
git push
```

---

## Tópico 8 — Módulos e `import`

### Módulos do próprio Python

O Python vem com uma biblioteca enorme de funções prontas, guardadas em **módulos**. Para usar um, você o **importa**. Crie o arquivo `treino/python/modulos.py`. Um exemplo útil para o catálogo: com 23 produtos e 10 por página, quantas páginas são necessárias? Dividir dá 2,3, e o resultado precisa ser **arredondado para cima**, o que o módulo `math` faz com `ceil`:

```python
import math

total_produtos = 23
por_pagina = 10
paginas = math.ceil(total_produtos / por_pagina)

print(f'{total_produtos} produtos, {por_pagina} por página: {paginas} páginas')
```

Salve e rode (`python treino/python/modulos.py`): `23 produtos, 10 por página: 3 páginas`. O `import math` traz o módulo, e `math.ceil(...)` usa a função `ceil` que está **dentro** dele. É a conta que o Capítulo 12.1 usa para paginar a lista.

### Importando só uma peça

Outra forma é trazer só o que se precisa, com `from ... import ...`. Atenção a uma convenção: os `import` ficam **no topo** do arquivo. Acrescente a linha do `from` logo abaixo do `import math`, e o restante no final do arquivo:

```python
from datetime import datetime
```

```python
data = datetime.strptime('25/12/2026', '%d/%m/%Y')
print(data)
print(data.year)
print(data.strftime('%d/%m/%Y'))
```

Salve e rode. As três últimas linhas da saída são:

```text
2026-12-25 00:00:00
2026
25/12/2026
```

O `strptime` **lê** um texto como data, e o segundo argumento diz o formato em que o texto está: `%d` é o dia, `%m` é o mês e `%Y` é o ano com 4 dígitos. O `.year` pega o ano, e o `strftime` faz o caminho inverso, **escrevendo** a data no formato que você pedir. É a base da validação de data de nascimento do Capítulo 14.

### Um erro que o `try` resolve

E se o texto não for uma data de verdade? Acrescente ao final:

```python
try:
    datetime.strptime('31/02/2026', '%d/%m/%Y')
    print('Data válida')
except ValueError:
    print('Data inválida')
```

Salve e rode: `Data inválida`. Não existe 31 de fevereiro, então o `strptime` levanta um `ValueError`, o mesmo erro do Tópico 7, e o `except` o trata.

### O seu próprio módulo

Todo arquivo `.py` é um módulo. Isso permite **separar** o código em arquivos, e foi o que fizemos com as funções `formata_preco` e `le_preco`, que são úteis em vários lugares. Crie o arquivo `treino/python/formatacao.py` com as duas funções, copiadas dos Tópicos 4 e 7:

```python
def formata_preco(valor, simbolo='R$'):
    texto = f'{valor:.2f}'.replace('.', ',')
    return simbolo + ' ' + texto


def le_preco(texto):
    try:
        return float(texto.replace(',', '.'))
    except ValueError:
        return None
```

No `modulos.py`, importe-as. A linha vai no topo, logo depois do `from datetime ...`, separada por uma linha em branco, e o uso vai no final do arquivo:

```python
from formatacao import formata_preco, le_preco
```

```python
preco = le_preco('59,90')
print(formata_preco(preco))
print(formata_preco(preco, simbolo='US$'))
```

Salve os dois arquivos e rode o `modulos.py`. As duas últimas linhas da saída são `R$ 59,90` e `US$ 59,90`. O nome depois do `from` é o nome do **arquivo, sem o `.py`**, e os dois arquivos precisam estar na mesma pasta. Nos Capítulos 10 e 11 você vai criar o seu `db.py` desse mesmo jeito, e importá-lo no `app.py`.

!!! note "Bibliotecas de outras pessoas"
    Os módulos `math` e `datetime` já vêm com o Python. Os de **outras pessoas**, como o Flask, precisam ser instalados antes com o `pip`, o que você fará no Capítulo 3. Depois de instalados, o `import` funciona do mesmo jeito.

### A pasta `__pycache__`

Olhe o explorador do VS Code: apareceu a pasta `treino/python/__pycache__`. Quando um arquivo é importado, o Python guarda uma versão pré-processada dele ali, só para carregar mais rápido na vez seguinte. É lixo que o Python recria quando precisa e **não deve ir para o GitHub**. Rode `git status` e você a verá na lista. Acrescente ao final do `.gitignore`:

```text
# Arquivos temporários que o Python cria sozinho
__pycache__/
*.pyc
```

Salve e rode `git status` de novo: a `__pycache__` **sumiu** da lista. O `modulos.py` completo:

```python
import math
from datetime import datetime

from formatacao import formata_preco, le_preco

total_produtos = 23
por_pagina = 10
paginas = math.ceil(total_produtos / por_pagina)

print(f'{total_produtos} produtos, {por_pagina} por página: {paginas} páginas')

data = datetime.strptime('25/12/2026', '%d/%m/%Y')
print(data)
print(data.year)
print(data.strftime('%d/%m/%Y'))

try:
    datetime.strptime('31/02/2026', '%d/%m/%Y')
    print('Data válida')
except ValueError:
    print('Data inválida')

preco = le_preco('59,90')
print(formata_preco(preco))
print(formata_preco(preco, simbolo='US$'))
```

Registre no Git e envie:

```bash
git add .
git commit -m "Adiciona o módulo de formatação e os exemplos de import"
git push
```

---

## 📦 Código deste capítulo

Compare com o seu projeto. O zip tem o catálogo do Capítulo 2 e a pasta `treino/python` com os oito scripts e o `formatacao.py`. O Capítulo 3 **não** parte deste zip, e sim do zip do Capítulo 2, porque este capítulo não muda o catálogo.

➡️ [Baixar p1_cap_02_1.zip](../arquivos/p1_cap_02_1.zip)

---

## 🃏 Flashcards de Revisão

Tente responder mentalmente antes de abrir.

??? question "Qual é a diferença entre `print` e `return`?"
    O `print` **mostra** um valor na tela e não entrega nada a quem chamou a função (que recebe `None`). O `return` **entrega** o valor a quem chamou e encerra a função. Rotas e funções de validação precisam de `return`.

??? question "Por que `'2.50' + '2.50'` dá `2.502.50` em vez de `5.0`?"
    Porque entre textos o `+` **cola**, e não soma. Para somar é preciso converter antes com `float()` (ou `int()`), como em `float('2.50') + float('2.50')`.

??? question "Qual a vantagem do `.get()` em relação aos colchetes em um dicionário?"
    Com `dicionario['chave']`, uma chave inexistente dá `KeyError` e derruba o programa. O `.get('chave')` devolve `None` (ou o valor padrão que você informar, como em `.get('chave', 'padrão')`).

??? question "O que `range(1, 4)` produz, e por que o 4 não aparece?"
    Produz 1, 2 e 3. O `range` vai do primeiro número até **antes** do último: o início entra e o fim fica de fora.

??? question "Quando faz sentido usar `try` e `except`?"
    Quando existe um erro **previsível** causado por um dado de fora, como um texto digitado onde se esperava um número ou uma data inexistente. Capture o erro específico (por exemplo, `ValueError`) e trate-o, em vez de deixar o programa parar.

??? question "Por que uma função de validação devolve `None` quando o valor é válido?"
    Porque assim ela tem **duas respostas possíveis**: a mensagem de erro (um texto) ou `None` ("sem erro"). Quem chama só precisa perguntar `if mensagem is None:` para saber se está tudo certo.

---

## 📝 Resumo

Você relembrou, com exemplos do catálogo, o Python que o resto do curso usa: variáveis e tipos, f-strings para montar textos e formatar preços, `if/elif/else` para decidir, funções com `return` (inclusive a que devolve uma mensagem ou `None`), listas e `for`, dicionários e a lista de dicionários que representa os produtos, `try/except` para os erros previsíveis e `import` para usar módulos do Python e criar os seus. Nada disso altera o catálogo: tudo ficou em `treino/python`. No Capítulo 3, o Flask aproveita esses mesmos elementos para fazer o catálogo ser servido por um programa.

---

## 🔗 Navegação

⬅️ [Capítulo 2 — Clone, pull, formulário, CSS e JavaScript](Capitulo_02_Clone_Pull_Formulario_CSS_e_JS.md) · ➡️ [Capítulo 3 — Flask](Capitulo_03_Flask.md)

---

*Fatec Jahu · ILP951 · Prof. Ronan Adriel Zenatti · 2026*
