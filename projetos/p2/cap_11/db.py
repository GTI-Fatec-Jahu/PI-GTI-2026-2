import os

from dotenv import load_dotenv
from mysql.connector import Error, pooling

# Lê o arquivo .env e coloca cada linha dele nas variáveis de ambiente do programa.
load_dotenv()

if os.getenv('DB_NAME') is None:
    raise RuntimeError('Não encontrei o arquivo .env. Copie o .env.example para .env e preencha.')

CONFIGURACAO = {
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT', '3306')),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME'),
    'charset': 'utf8mb4',
    'sql_mode': (
        'STRICT_TRANS_TABLES,NO_ZERO_DATE,'
        'ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION'
    ),
    'time_zone': '-03:00',  # horário de Brasília, igual em qualquer computador
    'use_pure': True,  # conector em Python puro, evita erros com XAMPP e MySQL juntos
}

pool = pooling.MySQLConnectionPool(pool_name='gestao_pool', pool_size=5, **CONFIGURACAO)


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


def execute_insert(sql, params=None):
    if params is None:
        params = ()

    conexao = pool.get_connection()
    cursor = conexao.cursor()

    try:
        cursor.execute(sql, params)
        conexao.commit()
        return cursor.lastrowid
    except Error:
        conexao.rollback()
        raise
    finally:
        cursor.close()
        conexao.close()
