"""Copia o código de cada etapa para a seção "Os arquivos completos do capítulo".

Uso (na raiz do repositório):
    python projetos/sincronizar_arquivos_completos.py            # todos os capítulos do Projeto 2
    python projetos/sincronizar_arquivos_completos.py --conferir # só mostra o que está diferente

Dentro da seção final de cada capítulo, toda linha de texto que termina em ":" e cita um
arquivo entre crases (por exemplo  O `templates/perfis/perfil_form.html`:) é seguida de um
bloco de código. Se esse arquivo existe na pasta da etapa (projetos/p2/cap_12/...), o bloco
recebe o conteúdo dele. Linhas que começam com "A rota" ou "As rotas" (trechos parciais) são
puladas: esses blocos são mantidos à mão.
"""

import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CAPITULOS = RAIZ / 'docs' / 'capitulos'
PROJETOS = RAIZ / 'projetos'

TITULOS_DA_SECAO = ('## Os arquivos completos', '## As mudanças completas', '## O arquivo completo')


def pasta_da_etapa(arquivo_md):
    # Capitulo_12_1_Busca... -> p2/cap_12_1 ; Capitulo_12_INSERT... -> p2/cap_12
    partes = arquivo_md.stem.split('_')
    numero = partes[1]
    if partes[2].isdigit():
        numero = numero + '_' + partes[2]
    return PROJETOS / 'p2' / ('cap_' + numero)


def sincroniza(arquivo_md, so_conferir):
    pasta = pasta_da_etapa(arquivo_md)
    linhas = arquivo_md.read_text(encoding='utf-8').split('\n')
    dentro = False
    diferentes = []
    i = 0
    while i < len(linhas):
        linha = linhas[i]
        if linha.startswith('## '):
            dentro = linha.startswith(TITULOS_DA_SECAO)
        citados = re.findall(r'`([^`]+)`', linha)
        anuncia = (dentro and linha.rstrip().endswith(':') and citados
                   and not linha.startswith(('A rota', 'As rotas', 'Na rota')))
        if anuncia:
            caminho = pasta / citados[-1]
            # procura o bloco de código logo abaixo
            j = i + 1
            while j < len(linhas) and linhas[j].strip() == '':
                j += 1
            if caminho.is_file() and j < len(linhas) and linhas[j].startswith('```'):
                k = j + 1
                while not linhas[k].startswith('```'):
                    k += 1
                novo = caminho.read_text(encoding='utf-8').replace('\r\n', '\n').rstrip('\n').split('\n')
                if linhas[j + 1:k] != novo:
                    diferentes.append(citados[-1])
                    if not so_conferir:
                        linhas[j + 1:k] = novo
                        k = j + 1 + len(novo)
                i = k
        i += 1
    if diferentes and not so_conferir:
        arquivo_md.write_text('\n'.join(linhas), encoding='utf-8', newline='\n')
    for nome in diferentes:
        print(arquivo_md.name, '->', nome, '(diferente)' if so_conferir else '(atualizado)')


if __name__ == '__main__':
    so_conferir = '--conferir' in sys.argv
    for md in sorted(CAPITULOS.glob('Capitulo_1[1-9]*.md')):
        sincroniza(md, so_conferir)
