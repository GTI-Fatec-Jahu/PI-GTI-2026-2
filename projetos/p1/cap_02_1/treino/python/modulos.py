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
