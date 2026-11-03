-- produtos_exemplo.sql — Capítulo 10 · Programação para Internet (ILP951)
--
-- Cria o banco "catalogo" e a tabela "produtos", com os sete produtos do catálogo.
-- Pode ser importado de novo a qualquer momento: a tabela é apagada e refeita,
-- e os produtos voltam a ser os sete originais.

SET NAMES utf8mb4;

-- utf8mb4: acentos, cedilha e emojis. unicode_ci: a busca ignora maiúsculas e acentos.
CREATE DATABASE IF NOT EXISTS catalogo
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE catalogo;

DROP TABLE IF EXISTS produtos;

CREATE TABLE produtos (
    id_produto BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nome       VARCHAR(100) NOT NULL,
    categoria  VARCHAR(50),
    preco      DECIMAL(14,2) NOT NULL
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

INSERT INTO produtos (nome, categoria, preco) VALUES
    ('Caneta esferográfica azul',       'Papelaria',   2.50),
    ('Caderno universitário 96 folhas', 'Papelaria',  18.90),
    ('Mouse sem fio',                   'Informática', 59.90),
    ('Teclado USB',                     'Informática', 89.90),
    ('Garrafa térmica 500 ml',          'Casa',        49.90),
    ('Mochila escolar',                 'Acessórios', 129.00),
    ('Fone de ouvido',                  'Informática', 79.90);
