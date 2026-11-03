from db import execute_one

# Se o .env, o XAMPP ou o banco estiverem errados, o erro aparece já na linha acima,
# quando o db.py cria o pool.
print('Conectado ao banco de dados.')

info = execute_one('SELECT DATABASE() AS banco, VERSION() AS versao, NOW() AS agora')
print('Banco:', info['banco'])
print('Servidor:', info['versao'])
print('Hora do banco:', info['agora'])

perfis = execute_one('SELECT COUNT(*) AS total FROM perfis')
usuarios = execute_one('SELECT COUNT(*) AS total FROM usuarios')
produtos = execute_one('SELECT COUNT(*) AS total FROM produtos')

print('Tabela perfis:', perfis['total'], 'linhas')
print('Tabela usuarios:', usuarios['total'], 'linhas')
print('Tabela produtos:', produtos['total'], 'linhas')
