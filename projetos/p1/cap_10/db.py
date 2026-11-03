from mysql.connector import Error, pooling

# Senha e dados de conexão no código são provisórios, só para o projeto de sala.
# Num sistema de verdade, ficam fora do código (o .env aparece no Capítulo 11).
CONFIGURACAO = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '',
    'database': 'catalogo',
    'charset': 'utf8mb4',
    'sql_mode': 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION',
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
