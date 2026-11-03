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
