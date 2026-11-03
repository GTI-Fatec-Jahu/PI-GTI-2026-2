---
description: Escreve ou altera um capítulo seguindo o pipeline do CLAUDE.md
argument-hint: número do capítulo (ex.: 3, 12.1) ou caminho do rascunho
---

Leia `CLAUDE.md` na raiz do repositório antes de qualquer outra coisa, se ainda não está no
contexto desta sessão.

Processe `$ARGUMENTS` seguindo exatamente as três fases descritas em `CLAUDE.md`, nesta ordem,
sem pular nenhuma:

1. **Fase 1, Validar e perguntar.** Leia a linha do capítulo em "Sequência dos capítulos", o
   rascunho (se `$ARGUMENTS` for um caminho), o capítulo anterior já publicado em
   `docs/capitulos/` (se existir), os trechos úteis de `old/` e `docs/index.md`. Escreva um
   resumo do que entendeu e faça as perguntas necessárias (ver gatilhos no CLAUDE.md). Pare
   aqui e espere a resposta do professor, a não ser que ele já tenha dito "pode aplicar sem
   ajustes".
2. **Fase 2, Escrever.** Aplique `templates/CAPITULO_TEMPLATE.md`: objetivos, ponto de
   partida, tópicos com código em incrementos pequenos e bloco de commit, código do capítulo
   (zip), flashcards, quiz, resumo e navegação. Siga o estilo, a terminologia e a regra de
   nunca cortar conteúdo reaproveitado de `old/`. Atualize `docs/index.md` e o `nav` do
   `mkdocs.yml`.
3. **Fase 3, Verificar, empacotar e commitar.** Rode `mkdocs build`, confira a checklist do
   CLAUDE.md, execute o código, gere e teste o zip, faça o commit do capítulo e **pergunte ao
   professor antes de qualquer `git push`**.

Nunca mencione trabalhos, avaliações ou que o aluno fará o capítulo sozinho.
