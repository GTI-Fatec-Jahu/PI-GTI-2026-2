---
description: Processa uma aula nova ou alterada em docs/aulas/ seguindo o pipeline do CLAUDE.md
argument-hint: caminho/do/arquivo.md
---

Leia `CLAUDE.md` na raiz do repositório antes de qualquer outra coisa, se ainda não
está no contexto desta sessão.

Processe o arquivo `$ARGUMENTS` seguindo exatamente as três fases descritas em
`CLAUDE.md`, nesta ordem, sem pular nenhuma:

1. **Fase 1, Validar e perguntar.** Leia o arquivo indicado por completo, leia 1-2
   aulas já publicadas em `docs/aulas/` para calibrar padrão (se já existir alguma), e
   leia `docs/index.md`. Escreva um resumo do que entendeu e faça as perguntas
   necessárias (ver lista de gatilhos no CLAUDE.md). Pare aqui e espere a resposta do
   professor antes de continuar, a não ser que ele já tenha dito explicitamente "pode
   aplicar sem ajustes".
2. **Fase 2, Remodelar.** Aplique a estrutura de `templates/AULA_TEMPLATE.md`
   (objetivos, mapa mental, conteúdo com código fatiado em incrementos pequenos,
   flashcards, quiz, resumo, selo de conquista conforme a tabela de gamificação do
   CLAUDE.md, navegação). Preserve o conteúdo original por completo, só adicione
   seções ao redor. Atualize `docs/index.md` (status da aula e trilha) e `mkdocs.yml`
   (entrada no `nav`).
3. **Fase 3, Verificar, finalizar e enviar ao GitHub.** Rode `mkdocs build`, confira os
   itens da checklist do CLAUDE.md (md_in_html, mermaid, quiz, imagens), faça o commit
   com mensagem indicando a aula, e pergunte explicitamente ao professor se pode enviar
   com `git push` antes de fazê-lo. Nunca dê push sem essa confirmação.

Se o arquivo `$ARGUMENTS` for um dos arquivos herdados do 1º semestre (ver seção
"Conteúdo herdado do 1º semestre" em `CLAUDE.md`), trate-o como um rascunho normal na
Fase 1, o fato de já ter conteúdo completo não dispensa a validação.
