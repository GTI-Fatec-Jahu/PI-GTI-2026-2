def formata_preco(valor, simbolo='R$'):
    texto = f'{valor:.2f}'.replace('.', ',')
    return simbolo + ' ' + texto


def le_preco(texto):
    try:
        return float(texto.replace(',', '.'))
    except ValueError:
        return None
