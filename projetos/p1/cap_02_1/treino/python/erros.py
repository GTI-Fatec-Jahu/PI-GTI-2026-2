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
