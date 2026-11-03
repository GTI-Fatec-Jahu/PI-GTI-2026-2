from mysql.connector import Error, pooling

# Troque SUA_SENHA_AQUI e NOME_BANCO_DADOS pelos valores do seu computador.
# Senha e dados de conexão no código são provisórios, só para o projeto de sala.
# Num sistema de verdade, ficam fora do código (o .env aparece no Capítulo 11).
CONFIGURACAO = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'SUA_SENHA_AQUI',
    'database': 'NOME_BANCO_DADOS',
    'charset': 'utf8mb4',
    'sql_mode': (
        'STRICT_TRANS_TABLES,NO_ZERO_DATE,'
        'ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION'
    ),
    'time_zone': '-03:00',  # horário de Brasília, igual em qualquer computador
    'use_pure': True,  # conector em Python puro, evita erros com XAMPP e MySQL juntos
}

pool = pooling.MySQLConnectionPool(pool_name='catalogo_pool', pool_size=5, **CONFIGURACAO)


def execute_query(sql, params=None, fetch=False):
    if params is None:
        params = ()

    conexao = pool.get_connection()
    cursor = conexao.cursor(dictionary=True)

    try:
        cursor.execute(sql, params)

        if fetch:
            resultado = cursor.fetchall()
        else:
            conexao.commit()
            resultado = cursor.rowcount

        return resultado
    except Error:
        conexao.rollback()
        raise
    finally:
        cursor.close()
        conexao.close()


def execute_one(sql, params=None):
    linhas = execute_query(sql, params, fetch=True)

    if len(linhas) > 0:
        return linhas[0]

    return None
