# Gabarito — Aula 01 — Introdução, Git e HTML5

> Soluções comentadas dos mini-desafios de "🔎 Verifique seu Entendimento" da
> [Aula 01](../Aula_01_Introducao_Git_HTML5.md). Tente resolver cada desafio por conta
> própria antes de conferir aqui.

---

## Parte 1 — As três camadas de um assistente de estudos com IA

**Desafio proposto:** identificar front-end, back-end e banco de dados em um
assistente de estudos com IA.

**Solução comentada:**

- **Front-end:** a tela no navegador onde o aluno digita a pergunta e lê a resposta —
  o campo de texto, o botão de enviar, o histórico da conversa exibido na tela.
- **Back-end:** o código (em Python, por exemplo) que recebe a pergunta enviada pelo
  navegador, decide como processá-la — inclusive, muitas vezes, chamando um modelo de
  IA generativa por trás — e devolve a resposta pronta para ser exibida.
- **Banco de dados:** onde ficam guardados, de forma permanente, o cadastro dos
  alunos que usam o assistente e o histórico de perguntas e respostas de cada um,
  para que a conversa não se perca ao fechar a aba.

O ponto central do desafio é perceber que a mesma arquitetura genérica (front-end/
back-end/banco de dados) se aplica a qualquer aplicação web, inclusive uma com IA por
trás — a IA generativa entra como parte da lógica do back-end, não como uma quarta
camada separada.

---

## Parte 2 — Diagnosticando o PATH não configurado

**Desafio proposto:** prever o erro no terminal quando o PATH não foi configurado e
explicar como resolver sem reinstalar.

**Solução comentada:**

Ao digitar `python --version` sem o PATH configurado, o Windows não sabe onde
encontrar o programa `python`, e o terminal responde com uma mensagem equivalente a:

```
'python' não é reconhecido como um comando interno
ou externo, um programa operável ou um arquivo em lotes.
```

Para resolver sem reinstalar do zero, existem duas saídas: (1) rodar novamente o
instalador do Python e escolher a opção "Modify" (Modificar), marcando "Add Python to
PATH" dessa vez; ou (2) adicionar manualmente o caminho da instalação do Python às
variáveis de ambiente do Windows (Painel de Controle → Sistema → Configurações
avançadas → Variáveis de Ambiente → editar `Path`). A primeira opção é mais simples e
a recomendada para quem está começando.

---

## Parte 3 — Provando que as extensões do VS Code estão ativas

**Desafio proposto:** apontar evidências visuais (fora do menu de extensões) de que
Python e Prettier estão ativas.

**Solução comentada:**

Para a extensão **Python**: (1) ao abrir um arquivo `.py`, o código aparece com
**coloração sintática** — palavras-chave, strings e comentários em cores diferentes,
em vez de tudo em preto e branco; (2) no **canto inferior direito da barra de
status** aparece um seletor de interpretador Python (algo como "Python 3.12.0
64-bit"), e ao digitar código surgem sugestões de autocompletar (IntelliSense).

Para a extensão **Prettier**: a evidência mais direta é comportamental — ao salvar um
arquivo de um tipo que o Prettier formata (como `.html` ou `.js`), o código se
reorganiza sozinho (indentação corrigida, aspas padronizadas) sem que ninguém precise
apertar um botão de formatar manualmente.

---

## Parte 4 — Comandos para criar o projeto do app de ingressos

**Desafio proposto:** escrever a sequência de comandos para criar a pasta
`ingressos-show`, entrar nela e abrir o VS Code.

**Solução comentada:**

```
cd Desktop
mkdir ingressos-show
cd ingressos-show
code .
```

`cd Desktop` navega até a Área de Trabalho, `mkdir ingressos-show` cria a nova pasta,
`cd ingressos-show` entra nela, e `code .` abre o VS Code já dentro dessa pasta (o
`.` significa "a pasta atual").

---

## Parte 5 — Ambiente virtual para o Projeto A

**Desafio proposto:** explicar o conflito de versões entre os dois projetos e criar
um venv só para o Projeto A.

**Solução comentada:**

Se as bibliotecas fossem instaladas direto no Python global do computador, só seria
possível ter **uma** versão da biblioteca de IA generativa instalada por vez. Atualizar
para a versão mais recente (que o Projeto A precisa) quebraria o Projeto B, que trava
com essa versão; manter a versão antiga (que o Projeto B precisa) impediria o Projeto
A de funcionar. Um ambiente virtual próprio para o Projeto A resolve o conflito,
isolando as bibliotecas de cada projeto.

Dentro da pasta do Projeto A, no terminal:

```
python -m venv venv
venv\Scripts\activate
```

Depois de ativar, o prefixo `(venv)` aparece no início da linha do terminal,
confirmando que qualquer biblioteca instalada a partir dali fica isolada nesse
projeto.

---

## Parte 6 — Protegendo a chave de API do app de caronas

**Desafio proposto:** definir o que entra no `.gitignore` antes do primeiro commit e
escrever a sequência completa de comandos Git.

**Solução comentada:**

O `.gitignore` precisa conter a linha `.env` **antes** do primeiro `git add .` —
assim o Git nunca chega a rastrear esse arquivo, e a chave de API nunca entra em
nenhum commit.

```
git init
git add .
git commit -m "Configuração inicial do app de caronas compartilhadas"
git remote add origin https://github.com/SEU-USUARIO/caronas-compartilhadas.git
git push -u origin main
```

O ponto-chave do desafio é a ordem: o `.gitignore` com `.env` listado precisa existir
**antes** do `git add .`, porque o Git só ignora arquivos que ainda não foram
adicionados ao repositório.

---

## Parte 7 — Página HTML5 do mutirão de coleta seletiva

**Desafio proposto:** escrever do zero uma página HTML5 válida com estrutura
obrigatória, `<h1>`, lista de materiais, tabela de horários e link para o Instagram.

**Solução comentada:**

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Mutirão de Coleta Seletiva</title>
</head>
<body>

  <h1>Mutirão de Coleta Seletiva do Bairro</h1>

  <h2>Materiais aceitos</h2>
  <ul>
    <li>Papel e papelão</li>
    <li>Vidro</li>
    <li>Eletrônicos</li>
  </ul>

  <h2>Dias e horários de coleta</h2>
  <table border="1">
    <thead>
      <tr>
        <th>Rua</th>
        <th>Dia</th>
        <th>Horário</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Rua das Flores</td>
        <td>Sábado</td>
        <td>08h — 12h</td>
      </tr>
      <tr>
        <td>Rua dos Ipês</td>
        <td>Domingo</td>
        <td>08h — 12h</td>
      </tr>
    </tbody>
  </table>

  <p>
    Siga a ação no Instagram:
    <a href="https://instagram.com/mutiraodobairro">@mutiraodobairro</a>
  </p>

</body>
</html>
```

O que este desafio verifica é a combinação de várias tags aprendidas na mesma página
— estrutura obrigatória, hierarquia de títulos, lista, tabela com `thead`/`tbody` e
link — sem se apoiar em nenhum exemplo pronto como modelo.

---

*Fatec Jahu · ILP951 · Prof. Ronan Adriel Zenatti · 2026*
