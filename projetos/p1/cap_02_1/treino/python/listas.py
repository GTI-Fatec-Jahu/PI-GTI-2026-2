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
