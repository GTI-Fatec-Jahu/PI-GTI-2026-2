# 🌐 Programação para Internet — ILP951 — 2º Semestre/2026

<div align="center">

![Fatec Jahu](https://img.shields.io/badge/Fatec-Jahu-blue?style=for-the-badge)
![Semestre](https://img.shields.io/badge/2º%20Semestre-2026-green?style=for-the-badge)
![Carga Horária](https://img.shields.io/badge/Carga%20Horária-80%20horas--aula-orange?style=for-the-badge)

### 🌐 [Acesse o site da disciplina →](https://gti-fatec-jahu.github.io/PI-GTI-2026-2/)

</div>

---

Este repositório é a **fonte** do guia de estudos da disciplina Programação para Internet (ILP951) — Fatec Jahu, curso de Tecnologia em Gestão da Tecnologia da Informação (GTI), 2º semestre de 2026.

> **Para estudar, use o [site publicado](https://gti-fatec-jahu.github.io/PI-GTI-2026-2/).**
> Ele é gerado automaticamente a partir destes mesmos arquivos Markdown, com flashcards e quizzes funcionais, recursos que o GitHub não renderiza ao abrir um `.md` isolado (é por isso que este README não usa esses recursos).

## 📚 Como o material está organizado

O conteúdo é dividido em **capítulos**, cada um pensado como base para uma aula de 180 minutos, e em dois projetos:

- **Projeto 1 — Catálogo de Produtos (Capítulos 1 a 10):** Git, HTML, CSS e JavaScript, depois Flask, Bootstrap, Jinja2, formulários, `session`, validação e a primeira conexão com o MySQL.
- **Projeto 2 — Sistema de Gestão (Capítulos 11 a 19):** um sistema com perfis, usuários e produtos, com banco de dados completo, login, controle de permissão e relatórios.

Alguns capítulos têm **subcapítulos opcionais** (por exemplo, 12.1). Ao final de cada capítulo há um **zip com o código do projeto** naquele ponto, que serve de ponto de partida do capítulo seguinte. Os arquivos ficam em `docs/arquivos/`.

> O conteúdo da versão anterior do curso está arquivado em `old/`, fora do site.

## 🛠️ Rodando o site localmente

```bash
python -m venv .venv
.venv\Scripts\activate        # no Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve
```

Acesse `http://127.0.0.1:8000`. A publicação é automática: todo push na branch `main` builda e publica no GitHub Pages via Actions.

⚠️ **Configuração única necessária:** em `Settings → Pages`, defina **Source: GitHub Actions**.

## 💬 Contato

📧 [ronan.zenatti@cps.sp.gov.br](mailto:ronan.zenatti@cps.sp.gov.br)

---

*Fatec Jahu · ILP951 · Prof. Ronan Adriel Zenatti · 2026*
