from db import execute_one


def validar_perfil(nome, descricao, id_perfil=0):
    erros = []

    # ================ VALIDAÇÕES PARA O CAMPO nome =====================
    if not nome:
        erros.append('Informe o nome do perfil.')
    elif len(nome) < 3:
        erros.append('O nome deve ter pelo menos 3 caracteres.')
    elif len(nome) > 100:
        erros.append('O nome deve ter no máximo 100 caracteres.')

    # ================ VALIDAÇÕES PARA O CAMPO descricao =====================
    # Como descricao pode ser None, checamos antes de usar len()
    if descricao and len(descricao) > 255:
        erros.append('A descrição deve ter no máximo 255 caracteres.')

    # ================ NOME REPETIDO (CONSULTA AO BANCO) =====================
    # Se as regras básicas passaram, checa unicidade no banco de dados
    # O id_perfil <> %s ignora o próprio perfil na edição (no cadastro, o id_perfil vale 0)
    if not erros:
        existente = execute_one(
            'SELECT id_perfil, deletado_em FROM perfis WHERE nome = %s AND id_perfil <> %s',
            (nome, id_perfil),
        )

        # O nome pode pertencer a um perfil da lixeira, que não aparece na lista
        if existente:
            if existente['deletado_em'] is None:
                erros.append('Já existe um perfil com este nome.')
            else:
                erros.append('Já existe um perfil excluído com este nome. Restaure-o na lixeira.')

    return erros
