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
