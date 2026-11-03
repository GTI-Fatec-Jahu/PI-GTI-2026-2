-- perfis_30.sql — Capítulo 12.1 · Programação para Internet (ILP951)
--
-- Acrescenta perfis ao banco "gestao" até chegar a 30, para a lista ter o que buscar,
-- filtrar e dividir em páginas. Nada é apagado: o INSERT IGNORE pula qualquer linha cujo
-- nome já exista (a coluna "nome" é UNIQUE), então os perfis que você cadastrou no
-- Capítulo 12 ficam como estão. Pode ser importado de novo sem efeito.
--
-- Alguns perfis ficam sem descrição (NULL) de propósito, para o filtro "sem descrição"
-- ter o que mostrar. As datas de criação são espalhadas pelo ano para a ordenação por
-- "mais recentes" fazer diferença.

SET NAMES utf8mb4;

USE gestao;

INSERT IGNORE INTO perfis (nome, descricao, criado_em) VALUES
    ('Administrador',          'Acesso total ao sistema',                          '2026-01-05 09:00:00'),
    ('Gerente',                'Gerencia usuários e produtos',                     '2026-01-05 09:05:00'),
    ('Usuário',                'Acesso básico ao sistema',                         '2026-01-05 09:10:00'),
    ('Analista de Sistemas',   'Acompanha o funcionamento e os erros do sistema',  '2026-01-19 10:30:00'),
    ('Analista de Dados',      'Consulta os relatórios e exporta informações',     '2026-02-02 14:15:00'),
    ('Analista Financeiro',    'Confere valores, preços e fechamentos',            '2026-02-16 08:45:00'),
    ('Atendente',              'Atende clientes e consulta o cadastro',            '2026-03-02 11:00:00'),
    ('Auditor',                'Consulta o histórico sem poder alterar nada',      '2026-03-16 16:20:00'),
    ('Almoxarife',             'Controla o estoque dos produtos',                  '2026-03-30 09:40:00'),
    ('Comprador',              NULL,                                               '2026-04-13 13:10:00'),
    ('Contador',               'Acompanha os valores do estoque e dos produtos',   '2026-04-27 15:00:00'),
    ('Convidado',              NULL,                                               '2026-05-11 10:00:00'),
    ('Coordenador',            'Coordena a equipe e distribui as tarefas',         '2026-05-25 08:30:00'),
    ('Consultor',              'Acesso temporário para consultoria externa',       '2026-06-08 17:05:00'),
    ('Desenvolvedor',          'Mantém o código e o banco de dados',               '2026-06-22 09:50:00'),
    ('Designer',               NULL,                                               '2026-07-06 14:40:00'),
    ('Diretor',                'Acompanha os resultados de toda a empresa',        '2026-07-20 11:25:00'),
    ('Estagiário',             'Acesso limitado, em fase de treinamento',          '2026-08-03 08:15:00'),
    ('Estoquista',             'Cadastra a entrada e a saída de produtos',         '2026-08-10 13:35:00'),
    ('Financeiro',             'Cuida de preços, pagamentos e recebimentos',       '2026-08-17 10:10:00'),
    ('Fiscal',                 NULL,                                               '2026-08-24 16:00:00'),
    ('Moderador',              'Revisa e aprova o que outros usuários cadastram',  '2026-08-31 09:20:00'),
    ('Operador de Caixa',      'Registra as vendas no balcão',                     '2026-09-07 12:00:00'),
    ('Recepcionista',          NULL,                                               '2026-09-14 08:05:00'),
    ('Redator',                'Escreve e edita as descrições dos produtos',       '2026-09-21 15:45:00'),
    ('Revisor',                NULL,                                               '2026-09-28 10:55:00'),
    ('Supervisor',             'Supervisiona o atendimento e a equipe de vendas',  '2026-10-05 14:20:00'),
    ('Técnico de Suporte',     'Resolve problemas de acesso dos usuários',         '2026-10-12 09:30:00'),
    ('Vendedor',               'Consulta produtos e preços para vender',           '2026-10-19 11:50:00'),
    ('Gestor de Projetos',     'Acompanha os prazos e os responsáveis de cada projeto', '2026-10-26 16:35:00');
