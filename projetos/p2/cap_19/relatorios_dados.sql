-- relatorios_dados.sql — Capítulo 19 · Programação para Internet (ILP951)
--
-- Acrescenta ao banco "gestao" 24 usuários e 21 produtos, para os relatórios terem o que
-- contar, somar e agrupar. Pode ser importado de novo sem efeito:
--   * os usuários usam INSERT IGNORE: a coluna "email" é UNIQUE, então uma linha cujo e-mail
--     já existe é pulada;
--   * a tabela "produtos" não tem coluna UNIQUE, então cada produto só entra se ainda não
--     existir um com o mesmo nome (NOT EXISTS).
-- Nada do que você cadastrou é alterado ou apagado.
--
-- Os usuários ficam espalhados de fevereiro a outubro de 2026, com junho de propósito SEM
-- nenhum cadastro, e alguns sem cidade e estado (NULL). Todos têm a senha Senha123, guardada
-- como hash, como em qualquer usuário criado pelo sistema. Os produtos têm categorias
-- diferentes, estoques de 0 a 120, dois deles inativos e um sem categoria (NULL).

SET NAMES utf8mb4;

USE gestao;

-- Os três perfis que o Capítulo 12 pede. Se já existem, o IGNORE pula e a descrição que você
-- escolheu continua valendo. Os usuários abaixo buscam o id de cada perfil pelo nome.
INSERT IGNORE INTO perfis (nome, descricao) VALUES
    ('Administrador', 'Acesso total ao sistema'),
    ('Gerente',       'Gerencia usuários e produtos'),
    ('Usuário',       'Acesso básico ao sistema');

SET @id_administrador = (SELECT id_perfil FROM perfis WHERE nome = 'Administrador');
SET @id_gerente       = (SELECT id_perfil FROM perfis WHERE nome = 'Gerente');
SET @id_usuario       = (SELECT id_perfil FROM perfis WHERE nome = 'Usuário');

-- Hash da senha Senha123 (nunca a senha em texto puro)
SET @senha = 'scrypt:32768:8:1$FPEXcV8lvNZZshsw$f8d37022605b70293fb3fbff06ff91a024351941dd40457857aa53698f209a11e8ae9b084e3536af5b8af9db6fc1042751d6c81b8833e03a3bc257004e98bcd6';

INSERT IGNORE INTO usuarios (nome, email, senha, perfil_id, cidade, estado, criado_em) VALUES
    ('Marcos Oliveira',        'marcos.oliveira@exemplo.com',   @senha, @id_administrador, 'Jaú',            'SP', '2026-02-03 09:15:00'),
    ('Fernanda Castro',        'fernanda.castro@exemplo.com',   @senha, @id_gerente,       'Bauru',          'SP', '2026-02-17 14:40:00'),
    ('Paulo Henrique Ribeiro', 'paulo.ribeiro@exemplo.com',     @senha, @id_usuario,       'Campinas',       'SP', '2026-03-05 10:05:00'),
    ('Juliana Martins',        'juliana.martins@exemplo.com',   @senha, @id_usuario,       'Belo Horizonte', 'MG', '2026-03-12 16:20:00'),
    ('Ricardo Almeida',        'ricardo.almeida@exemplo.com',   @senha, @id_usuario,       NULL,             NULL, '2026-03-26 11:30:00'),
    ('Patrícia Gomes',         'patricia.gomes@exemplo.com',    @senha, @id_gerente,       'Curitiba',       'PR', '2026-04-02 08:50:00'),
    ('Thiago Fernandes',       'thiago.fernandes@exemplo.com',  @senha, @id_usuario,       'São Paulo',      'SP', '2026-04-09 13:25:00'),
    ('Camila Rocha',           'camila.rocha@exemplo.com',      @senha, @id_usuario,       'Rio de Janeiro', 'RJ', '2026-04-16 15:10:00'),
    ('Lucas Barbosa',          'lucas.barbosa@exemplo.com',     @senha, @id_usuario,       'Jaú',            'SP', '2026-04-30 09:45:00'),
    ('Aline Teixeira',         'aline.teixeira@exemplo.com',    @senha, @id_gerente,       'Uberlândia',     'MG', '2026-05-07 10:35:00'),
    ('Rodrigo Nunes',          'rodrigo.nunes@exemplo.com',     @senha, @id_usuario,       NULL,             NULL, '2026-05-14 17:00:00'),
    ('Beatriz Carvalho',       'beatriz.carvalho@exemplo.com',  @senha, @id_usuario,       'Ribeirão Preto', 'SP', '2026-05-28 12:15:00'),
    ('Gustavo Pereira',        'gustavo.pereira@exemplo.com',   @senha, @id_administrador, 'São Paulo',      'SP', '2026-07-01 08:30:00'),
    ('Larissa Moreira',        'larissa.moreira@exemplo.com',   @senha, @id_usuario,       'Porto Alegre',   'RS', '2026-07-08 14:55:00'),
    ('Diego Santana',          'diego.santana@exemplo.com',     @senha, @id_usuario,       'Bauru',          'SP', '2026-07-15 11:10:00'),
    ('Vanessa Duarte',         'vanessa.duarte@exemplo.com',    @senha, @id_gerente,       'Niterói',        'RJ', '2026-07-29 16:45:00'),
    ('Felipe Araújo',          'felipe.araujo@exemplo.com',     @senha, @id_usuario,       'Jaú',            'SP', '2026-08-05 09:20:00'),
    ('Renata Lopes',           'renata.lopes@exemplo.com',      @senha, @id_usuario,       NULL,             NULL, '2026-08-19 13:50:00'),
    ('Bruna Freitas',          'bruna.freitas@exemplo.com',     @senha, @id_usuario,       'Londrina',       'PR', '2026-08-26 15:35:00'),
    ('Eduardo Cardoso',        'eduardo.cardoso@exemplo.com',   @senha, @id_gerente,       'Campinas',       'SP', '2026-09-02 10:25:00'),
    ('Tatiane Ramos',          'tatiane.ramos@exemplo.com',     @senha, @id_usuario,       'Juiz de Fora',   'MG', '2026-09-16 14:05:00'),
    ('André Monteiro',         'andre.monteiro@exemplo.com',    @senha, @id_usuario,       'Marília',        'SP', '2026-09-23 08:40:00'),
    ('Sabrina Costa',          'sabrina.costa@exemplo.com',     @senha, @id_usuario,       NULL,             NULL, '2026-10-07 11:55:00'),
    ('Leonardo Pinto',         'leonardo.pinto@exemplo.com',    @senha, @id_usuario,       'São Paulo',      'SP', '2026-10-21 16:10:00');

-- Produtos: cada linha só entra se ainda não existir um produto com o mesmo nome.
INSERT INTO produtos (nome, categoria, preco, estoque, ativo, criado_em)
SELECT v.nome, v.categoria, v.preco, v.estoque, v.ativo, v.criado_em
FROM (
    SELECT 'Notebook Aurora 15"' AS nome, 'Informática' AS categoria, 3499.90 AS preco, 8 AS estoque, 1 AS ativo, '2026-02-04 09:00:00' AS criado_em
    UNION ALL SELECT 'Notebook Zenith Pro',         'Informática', 5899.00,   3, 1, '2026-02-04 09:10:00'
    UNION ALL SELECT 'Monitor 24" Full HD',         'Informática',  899.90,  14, 1, '2026-02-18 10:30:00'
    UNION ALL SELECT 'Roteador Wi-Fi 6',            'Informática',  449.50,  22, 1, '2026-03-03 14:00:00'
    UNION ALL SELECT 'SSD 480 GB',                  'Informática',  289.90,   0, 1, '2026-03-17 11:20:00'
    UNION ALL SELECT 'Teclado Mecânico RGB',        'Periféricos',  329.90,  17, 1, '2026-04-07 09:45:00'
    UNION ALL SELECT 'Mouse Sem Fio',               'Periféricos',   79.90,  45, 1, '2026-04-07 09:50:00'
    UNION ALL SELECT 'Mouse Gamer 7200 DPI',        'Periféricos',  159.90,   4, 1, '2026-04-21 15:30:00'
    UNION ALL SELECT 'Webcam HD 1080p',             'Periféricos',  199.00,   2, 1, '2026-05-05 13:15:00'
    UNION ALL SELECT 'Impressora Multifuncional',   'Periféricos',  749.00,   6, 1, '2026-05-19 10:00:00'
    UNION ALL SELECT 'Headset Estéreo',             'Áudio',        189.90,  12, 1, '2026-06-02 16:40:00'
    UNION ALL SELECT 'Caixa de Som Bluetooth',      'Áudio',        249.90,   0, 0, '2026-06-16 09:25:00'
    UNION ALL SELECT 'Fone de Ouvido Intra-auricular', 'Áudio',      59.90,  38, 1, '2026-07-07 11:05:00'
    UNION ALL SELECT 'Microfone de Mesa USB',       'Áudio',        279.00,   1, 1, '2026-07-21 14:50:00'
    UNION ALL SELECT 'Cabo HDMI 2 m',               'Acessórios',    29.90,  60, 1, '2026-08-04 10:15:00'
    UNION ALL SELECT 'Hub USB 4 Portas',            'Acessórios',    69.90,   5, 1, '2026-08-18 15:00:00'
    UNION ALL SELECT 'Suporte para Notebook',       'Acessórios',   119.90,   3, 0, '2026-09-01 09:35:00'
    UNION ALL SELECT 'Mousepad Grande',             'Acessórios',    49.90,  25, 1, '2026-09-15 13:40:00'
    UNION ALL SELECT 'Filtro de Linha 6 Tomadas',   'Outros',        54.90,   9, 1, '2026-09-29 11:30:00'
    UNION ALL SELECT 'Cadeira de Escritório',       'Outros',       899.00,   2, 1, '2026-10-13 16:20:00'
    UNION ALL SELECT 'Pilhas AA (4 unidades)',      NULL,            14.90, 120, 1, '2026-10-27 10:45:00'
) AS v
WHERE NOT EXISTS (SELECT 1 FROM produtos p WHERE p.nome = v.nome);
