<!--
GABARITO ESTRUTURAL DE CAPÍTULO, vive fora de docs/, não é publicado no site.
Use como referência das seções obrigatórias (ver CLAUDE.md). Apague este comentário no
arquivo real.

Regras que valem o capítulo inteiro:
- "Capítulo" é a unidade; "Tópico" é a seção interna. Nunca "aula", "parte" ou "passo".
- Nunca mencione trabalhos, avaliações, provas ou notas, nem que o aluno fará o capítulo sozinho.
- Código simples, em incrementos pequenos: um trecho novo por vez, e depois dele o pedido
  explícito para salvar, rodar e observar o que mudou antes do próximo trecho. Só consolide
  tudo em um bloco ao final do tópico.
- Todo conceito Python novo é explicado no primeiro uso, numa caixa curta (!!! note).
- Todo tópico que muda o código termina com o bloco de commit. O primeiro commit do projeto é
  só local; do segundo em diante inclui `git push`.
- Subcapítulos (2.1, 12.1, 13.1, 14.1, 17.1, 18.x) omitem o quiz.
- Nomes: tabela no plural, PK `id_<singular>`, FK `<singular>_id`. A variável ou o parâmetro de rota que
  guarda o valor de uma PK leva o nome da PK (`id_perfil`). SQL em MAIÚSCULAS (comandos, cláusulas,
  funções, tipos); nomes de banco, tabela, coluna e apelido em minúsculas.
-->

# Capítulo NN — [Título do Capítulo]

**Disciplina:** Programação para Internet (ILP951)
**Professor:** Ronan Adriel Zenatti · ronan.zenatti@cps.sp.gov.br
**Fatec Jahu — 2º Semestre/2026**

---

## 🎯 Objetivos do Capítulo

Ao final deste capítulo você deverá ser capaz de:

- [objetivo 1, com verbo de ação: criar, implementar, conectar, identificar...]
- [objetivo 2]
- [objetivo 3]

## 📦 Ponto de partida

Este capítulo continua do código do capítulo anterior. Se o seu projeto não está funcionando,
baixe o ponto de partida, descompacte, crie o ambiente virtual e instale as dependências:

➡️ [Baixar p1_cap_NN-1.zip](../arquivos/p1_cap_NN-1.zip)

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## Tópico 1 — [Título do primeiro tópico]

[Parta de uma situação ou problema concreto antes de nomear o conceito (problema → conceito →
exemplo). Apresente o código em incrementos pequenos.]

```python
# primeiro incremento, só o que é novo
```

Salve o arquivo, recarregue a página e observe [o que deve mudar na tela].

!!! note "Python: [conceito novo]"
    Explicação curta, no primeiro uso do conceito.

[próximo incremento, só depois de o aluno ter rodado o anterior]

Para registrar este ponto no Git:

```bash
git add .
git commit -m "Mensagem curta, em português, no imperativo"
```

## Tópico 2 — [Título do segundo tópico]

[...]

Para registrar e enviar:

```bash
git add .
git commit -m "Outra mensagem"
git push
```

---

## 📦 Código deste capítulo

Compare com o seu projeto, ou use como ponto de partida do próximo capítulo.

➡️ [Baixar p1_cap_NN.zip](../arquivos/p1_cap_NN.zip)

---

## 🃏 Flashcards de Revisão

Tente responder mentalmente antes de abrir. De 3 a 6 flashcards.

??? question "Pergunta objetiva sobre o conceito A?"
    Resposta direta e curta, de 1 a 3 frases.

??? question "Erro típico sobre este tema?"
    Por que é um erro e qual o raciocínio correto.

---

## ✅ Quiz de Fixação

De 3 a 5 perguntas, com pelo menos uma de múltipla resposta. O feedback é por alternativa,
em linhas de citação logo abaixo dela.

<quiz>
[Pergunta 1]?
- [ ] Alternativa incorreta
> Não. [Por que está errada.]
- [x] Alternativa correta
> Correto. [Por que está certa, e não só "Correto!".]
- [ ] Alternativa incorreta
> Não. [Por que está errada.]
</quiz>

---

## 📝 Resumo

[De 3 a 5 frases amarrando o que o aluno leva deste capítulo. Não repita o conteúdo.]

---

## 🔗 Navegação

⬅️ [Capítulo NN-1 — Título anterior](Capitulo_NN-1_Titulo.md) · 🔒 Capítulo NN+1 — em breve.

<!-- Troque o placeholder por ➡️ [Capítulo NN+1 — Título](Capitulo_NN+1_Titulo.md) quando
     o arquivo seguinte existir. -->

---

*Fatec Jahu · ILP951 · Prof. Ronan Adriel Zenatti · 2026*
