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
