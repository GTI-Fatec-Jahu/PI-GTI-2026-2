"""Gera os zips de cada etapa em docs/arquivos/.

Uso (na raiz do repositório):
    python projetos/gerar_zips.py              # todas as etapas
    python projetos/gerar_zips.py p1/cap_01    # só uma

A pasta projetos/p1/cap_01/ vira docs/arquivos/p1_cap_01.zip. Dentro do zip, os arquivos
ficam em uma pasta com o mesmo nome do zip (p1_cap_01/). Nunca entram .env, .venv,
__pycache__ nem .git.
"""

import sys
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PROJETOS = RAIZ / "projetos"
DESTINO = RAIZ / "docs" / "arquivos"

PASTAS_IGNORADAS = {".venv", "__pycache__", ".git"}
ARQUIVOS_IGNORADOS = {".env"}


def deve_ignorar(caminho, base):
    partes = caminho.relative_to(base).parts
    for parte in partes:
        if parte in PASTAS_IGNORADAS:
            return True
    return caminho.name in ARQUIVOS_IGNORADOS or caminho.suffix == ".pyc"


def gera_zip(etapa):
    pasta = PROJETOS / etapa
    nome = etapa.replace("/", "_")
    destino = DESTINO / (nome + ".zip")
    DESTINO.mkdir(parents=True, exist_ok=True)

    quantos = 0
    with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as zf:
        for caminho in sorted(pasta.rglob("*")):
            if caminho.is_dir() or deve_ignorar(caminho, pasta):
                continue
            dentro_do_zip = Path(nome) / caminho.relative_to(pasta)
            zf.write(caminho, dentro_do_zip.as_posix())
            quantos += 1
    print(destino.name, "->", quantos, "arquivos")


def todas_as_etapas():
    etapas = []
    for projeto in sorted(PROJETOS.glob("p*")):
        for cap in sorted(projeto.glob("cap_*")):
            etapas.append(projeto.name + "/" + cap.name)
    return etapas


if __name__ == "__main__":
    if len(sys.argv) > 1:
        etapas = sys.argv[1:]
    else:
        etapas = todas_as_etapas()
    for etapa in etapas:
        gera_zip(etapa)
