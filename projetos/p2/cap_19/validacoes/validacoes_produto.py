from decimal import Decimal

from werkzeug.utils import secure_filename

# Categorias de produto aceitas pelo sistema: o formulário e a validação leem a mesma lista
CATEGORIAS = ['Informática', 'Periféricos', 'Áudio', 'Acessórios', 'Outros']

# Limite da coluna estoque
ESTOQUE_MAXIMO = 1000000

# Limite da coluna preco, que é DECIMAL(10,2)
PRECO_MAXIMO = Decimal('99999999.99')

# Extensões aceitas para a foto do produto
EXTENSOES_FOTO = ['jpg', 'jpeg', 'png', 'webp']


# ==============================================================================
# FUNÇÕES DE APOIO
# ==============================================================================

def so_digitos(texto):
    resultado = ''
    for letra in texto:
        if letra in '0123456789':
            resultado = resultado + letra
    return resultado


def converter_preco(texto):
    # Aceita 1234,56 e 1.234,56. Devolve um Decimal, ou None se o texto não for um preço.
    partes = texto.split(',')
    if len(partes) > 2:
        return None

    centavos = ''
    if len(partes) == 2:
        centavos = partes[1]
        if len(centavos) == 0 or len(centavos) > 2 or so_digitos(centavos) != centavos:
            return None

    grupos = partes[0].split('.')
    numero = ''
    for posicao in range(len(grupos)):
        grupo = grupos[posicao]
        if grupo == '' or so_digitos(grupo) != grupo:
            return None
        if len(grupos) > 1 and posicao == 0 and len(grupo) > 3:
            return None
        if posicao > 0 and len(grupo) != 3:
            return None
        numero = numero + grupo

    if centavos != '':
        numero = numero + '.' + centavos

    return Decimal(numero)


def extensao_da_foto(nome_arquivo):
    # 'Foto da Ação.PNG' vira 'png'; um nome sem ponto não tem extensão
    nome_seguro = secure_filename(nome_arquivo)

    if '.' not in nome_seguro:
        return ''

    return nome_seguro.rsplit('.', 1)[1].lower()


# ==============================================================================
# UMA FUNÇÃO POR CAMPO: cada uma devolve a mensagem de erro ou None
# ==============================================================================

# ================ VALIDAÇÕES PARA O CAMPO nome =====================
def validar_nome(nome):
    if not nome:
        return 'Informe o nome do produto.'

    if len(nome) < 3:
        return 'O nome deve ter pelo menos 3 caracteres.'

    if len(nome) > 255:
        return 'O nome deve ter no máximo 255 caracteres.'

    return None


# ================ VALIDAÇÕES PARA O CAMPO descricao (opcional) =====================
def validar_descricao(descricao):
    # A coluna é TEXT; o limite de 2000 caracteres é uma regra do sistema
    if descricao and len(descricao) > 2000:
        return 'A descrição deve ter no máximo 2000 caracteres.'

    return None


# ================ VALIDAÇÕES PARA O CAMPO preco =====================
def validar_preco(texto):
    if not texto:
        return 'Informe o preço.'

    preco = converter_preco(texto)
    if preco is None:
        return 'Informe o preço no formato 1.234,56.'

    if preco <= 0:
        return 'O preço deve ser maior que zero.'

    if preco > PRECO_MAXIMO:
        return 'O preço máximo é 99.999.999,99.'

    return None


# ================ VALIDAÇÕES PARA O CAMPO estoque =====================
def validar_estoque(texto):
    if not texto:
        return 'Informe o estoque.'

    if so_digitos(texto) != texto:
        return 'O estoque deve ser um número inteiro, sem sinal nem vírgula.'

    if int(texto) > ESTOQUE_MAXIMO:
        return 'O estoque máximo é 1.000.000.'

    return None


# ================ VALIDAÇÕES PARA O CAMPO categoria (opcional) =====================
def validar_categoria(categoria):
    if not categoria:
        return None

    if categoria not in CATEGORIAS:
        return 'Selecione uma categoria válida.'

    return None


# ================ VALIDAÇÕES PARA A foto (opcional) =====================
def validar_foto(foto):
    if foto is None:
        return None

    if extensao_da_foto(foto.filename) not in EXTENSOES_FOTO:
        return 'A foto deve ser um arquivo jpg, jpeg, png ou webp.'

    return None


# ==============================================================================
# FUNÇÃO PRINCIPAL: recebe o dicionário com o formulário e a foto, e devolve a lista de erros
# ==============================================================================

def validar_produto(dados, foto):
    erros = []

    erro = validar_nome(dados['nome'])
    if erro:
        erros.append(erro)

    erro = validar_descricao(dados['descricao'])
    if erro:
        erros.append(erro)

    erro = validar_preco(dados['preco'])
    if erro:
        erros.append(erro)

    erro = validar_estoque(dados['estoque'])
    if erro:
        erros.append(erro)

    erro = validar_categoria(dados['categoria'])
    if erro:
        erros.append(erro)

    erro = validar_foto(foto)
    if erro:
        erros.append(erro)

    return erros
