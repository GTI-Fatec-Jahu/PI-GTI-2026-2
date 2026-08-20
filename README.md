# 🌐 Programação para Internet — ILP951

Material didático da disciplina **Programação para Internet** (ILP951), do curso de
Tecnologia em Gestão da Tecnologia da Informação (GTI) da **Fatec Jahu**, 2º
Semestre/2026.

O conteúdo é publicado como um site estático com [MkDocs Material][mkdocs-material] e
fica disponível em:

**📖 [gti-fatec-jahu.github.io/PI-GTI-2026-2](https://gti-fatec-jahu.github.io/PI-GTI-2026-2/)**

[mkdocs-material]: https://squidfunk.github.io/mkdocs-material/

---

## Sobre a disciplina

- **Sigla:** ILP951 · **Curso:** Tecnologia em Gestão da Tecnologia da Informação (GTI)
- **Carga horária:** 80 aulas presenciais (20 encontros de 4 horas-aula)
- **Professor:** Ronan Adriel Zenatti
- **Stack ensinada:** Python, Flask, Jinja2, Bootstrap 5, MySQL, Git/GitHub

Ao longo do semestre, os alunos constroem um sistema web completo — do primeiro
"Olá, mundo" em Flask até um CRUD relacional com login e relatórios gerenciais,
apresentado em banca ao final do curso.

## 🗂️ Estrutura do repositório

```
docs/
  index.md              # home do site: ementa, trilha e sumário de aulas
  aulas/
    Aula_NN_Titulo.md    # uma aula por arquivo, publicada progressivamente
  imgs/                  # imagens usadas nas aulas
templates/
  AULA_TEMPLATE.md       # gabarito estrutural usado ao remodelar cada aula
mkdocs.yml               # configuração do site (nav é explícito)
requirements.txt         # dependências Python do site
.github/workflows/
  deploy-docs.yml         # publica o site no GitHub Pages a cada push em main
```

## 🚀 Rodando localmente

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

mkdocs serve                     # preview local em http://127.0.0.1:8000
mkdocs build                     # build de produção, gera a pasta site/
```

## 📦 Publicação

O deploy é automático: todo push na branch `main` dispara o workflow
[`deploy-docs.yml`](.github/workflows/deploy-docs.yml), que builda o site com MkDocs e
publica o resultado no GitHub Pages.

## 🛠️ Tecnologias do site

[MkDocs Material](https://squidfunk.github.io/mkdocs-material/) como gerador de site
estático, [Mermaid](https://mermaid.js.org/) para diagramas (mapas mentais das aulas)
e [mkdocs-quiz](https://pypi.org/project/mkdocs-quiz/) para os quizzes interativos de
fixação.

---

*Fatec Jahu · ILP951 · Prof. Ronan Adriel Zenatti · 2º Semestre/2026*
