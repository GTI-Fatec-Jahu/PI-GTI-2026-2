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
