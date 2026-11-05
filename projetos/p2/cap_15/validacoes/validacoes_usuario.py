from datetime import datetime

from db import execute_one

# Siglas dos estados aceitas pelo sistema: o formulário e a validação usam a mesma lista
UFS = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA',
       'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']


# ==============================================================================
# FUNÇÕES DE APOIO
# ==============================================================================

def so_digitos(texto):
    # '(14) 99811-2030' vira '14998112030'
    resultado = ''
    for letra in texto:
        if letra in '0123456789':
            resultado = resultado + letra
    return resultado


def formatar_celular(celular):
    # Devolve o celular no formato que vai para o banco, ou None se o campo veio vazio
    if not celular:
        return None

    digitos = so_digitos(celular)
    if len(digitos) == 11:
        return f'({digitos[0:2]}) {digitos[2:7]}-{digitos[7:11]}'

    return f'({digitos[0:2]}) {digitos[2:6]}-{digitos[6:10]}'


def formatar_cpf(cpf):
    # Devolve o CPF como 000.000.000-00, ou None se o campo veio vazio
    if not cpf:
        return None

    digitos = so_digitos(cpf)
    return f'{digitos[0:3]}.{digitos[3:6]}.{digitos[6:9]}-{digitos[9:11]}'


def formatar_cep(cep):
    # Devolve o CEP como 00000-000, ou None se o campo veio vazio
    if not cep:
        return None

    digitos = so_digitos(cep)
    return f'{digitos[0:5]}-{digitos[5:8]}'


def calcular_digito_cpf(digitos, quantidade):
    # Conta de um dígito verificador do CPF: pesos decrescentes, soma e resto da divisão por 11
    soma = 0
    for posicao in range(quantidade):
        peso = quantidade + 1 - posicao
        soma = soma + int(digitos[posicao]) * peso

    resto = (soma * 10) % 11
    if resto == 10:
        resto = 0

    return resto


# ==============================================================================
# UMA FUNÇÃO POR CAMPO: cada uma devolve a mensagem de erro ou None
# ==============================================================================

# ================ VALIDAÇÕES PARA O CAMPO nome =====================
def validar_nome(nome):
    if not nome:
        return 'Informe o nome do usuário.'

    if len(nome) < 3:
        return 'O nome deve ter pelo menos 3 caracteres.'

    if len(nome) > 255:
        return 'O nome deve ter no máximo 255 caracteres.'

    return None


# ================ VALIDAÇÕES PARA O CAMPO email =====================
def validar_email(email):
    mensagem = 'Informe um e-mail válido, por exemplo nome@dominio.com.br.'

    if not email:
        return 'Informe o e-mail.'

    if len(email) > 255:
        return 'O e-mail deve ter no máximo 255 caracteres.'

    if ' ' in email or email.count('@') != 1:
        return mensagem

    partes = email.split('@')
    antes = partes[0]
    depois = partes[1]

    if antes == '' or '.' not in depois:
        return mensagem

    if depois.startswith('.') or depois.endswith('.'):
        return mensagem

    # Formato certo: confere no banco se o e-mail já pertence a outro usuário
    existente = execute_one('SELECT id_usuario FROM usuarios WHERE email = %s', (email,))
    if existente:
        return 'Já existe um usuário com este e-mail.'

    return None


# ================ VALIDAÇÕES PARA O CAMPO senha =====================
def validar_senha(senha, confirmacao):
    if len(senha) < 8:
        return 'A senha deve ter pelo menos 8 caracteres.'

    if len(senha) > 128:
        return 'A senha deve ter no máximo 128 caracteres.'

    tem_letra = False
    tem_numero = False
    for caractere in senha:
        if caractere.isalpha():
            tem_letra = True
        if caractere in '0123456789':
            tem_numero = True

    if not tem_letra or not tem_numero:
        return 'A senha deve ter letras e números.'

    if senha != confirmacao:
        return 'A confirmação da senha não confere.'

    return None


# ================ VALIDAÇÕES PARA O CAMPO perfil_id =====================
def validar_perfil_id(perfil_id):
    # Tudo o que chega do formulário é texto: precisa ser um número...
    try:
        numero = int(perfil_id)
    except ValueError:
        return 'Selecione um perfil.'

    # ...e precisa existir na tabela perfis
    perfil = execute_one('SELECT id_perfil FROM perfis WHERE id_perfil = %s', (numero,))
    if perfil is None:
        return 'Selecione um perfil válido.'

    return None


# ================ VALIDAÇÕES PARA O CAMPO celular (opcional) =====================
def validar_celular(celular):
    if not celular:
        return None

    digitos = so_digitos(celular)
    if len(digitos) != 10 and len(digitos) != 11:
        return 'Informe o celular com DDD, com 10 ou 11 dígitos.'

    return None


# ================ VALIDAÇÕES PARA O CAMPO cpf (opcional) =====================
def validar_cpf(cpf):
    if not cpf:
        return None

    digitos = so_digitos(cpf)
    if len(digitos) != 11:
        return 'O CPF deve ter 11 dígitos.'

    if digitos == digitos[0] * 11:
        return 'Informe um CPF válido.'

    if calcular_digito_cpf(digitos, 9) != int(digitos[9]):
        return 'Informe um CPF válido.'

    if calcular_digito_cpf(digitos, 10) != int(digitos[10]):
        return 'Informe um CPF válido.'

    # CPF válido: confere no banco, já no formato em que ele é gravado
    existente = execute_one('SELECT id_usuario FROM usuarios WHERE cpf = %s', (formatar_cpf(cpf),))
    if existente:
        return 'Já existe um usuário com este CPF.'

    return None


# ================ VALIDAÇÕES PARA O CAMPO data_nascimento (opcional) =====================
def validar_data_nascimento(texto):
    if not texto:
        return None

    try:
        data = datetime.strptime(texto, '%Y-%m-%d')
    except ValueError:
        return 'Informe uma data de nascimento válida.'

    if data > datetime.now():
        return 'A data de nascimento não pode estar no futuro.'

    if data.year < 1900:
        return 'A data de nascimento deve ser a partir de 1900.'

    return None


# ================ VALIDAÇÕES PARA O CAMPO cep (opcional) =====================
def validar_cep(cep):
    if not cep:
        return None

    if len(so_digitos(cep)) != 8:
        return 'Informe um CEP com 8 dígitos.'

    return None


# ================ VALIDAÇÕES PARA O CAMPO estado (opcional) =====================
def validar_estado(estado):
    if not estado:
        return None

    if estado not in UFS:
        return 'Selecione um estado válido.'

    return None


# ================ TAMANHO DOS CAMPOS DE TEXTO LIVRE (opcionais) =====================
def validar_tamanho(valor, rotulo, maximo):
    if valor and len(valor) > maximo:
        return f'O campo {rotulo} deve ter no máximo {maximo} caracteres.'

    return None


# ==============================================================================
# FUNÇÃO PRINCIPAL: recebe o dicionário com o formulário e devolve a lista de erros
# ==============================================================================

def validar_usuario(dados):
    erros = []

    # ================ DADOS PRINCIPAIS (obrigatórios) =====================
    erro = validar_nome(dados['nome'])
    if erro:
        erros.append(erro)

    erro = validar_email(dados['email'])
    if erro:
        erros.append(erro)

    erro = validar_senha(dados['senha'], dados['confirmacao'])
    if erro:
        erros.append(erro)

    erro = validar_perfil_id(dados['perfil_id'])
    if erro:
        erros.append(erro)

    # ================ DADOS PESSOAIS (opcionais) =====================
    erro = validar_celular(dados['celular'])
    if erro:
        erros.append(erro)

    erro = validar_cpf(dados['cpf'])
    if erro:
        erros.append(erro)

    erro = validar_data_nascimento(dados['data_nascimento'])
    if erro:
        erros.append(erro)

    # ================ ENDEREÇO (opcional) =====================
    erro = validar_cep(dados['cep'])
    if erro:
        erros.append(erro)

    erro = validar_tamanho(dados['endereco'], 'endereço', 255)
    if erro:
        erros.append(erro)

    erro = validar_tamanho(dados['numero'], 'número', 20)
    if erro:
        erros.append(erro)

    erro = validar_tamanho(dados['complemento'], 'complemento', 100)
    if erro:
        erros.append(erro)

    erro = validar_tamanho(dados['cidade'], 'cidade', 100)
    if erro:
        erros.append(erro)

    erro = validar_estado(dados['estado'])
    if erro:
        erros.append(erro)

    return erros
