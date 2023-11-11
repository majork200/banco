import psycopg2


conn = psycopg2.connect(
    dbname="cadastropy",
    user="postgres",
    password="192003",
    host="localhost",
    port="5433"
)
cursor = conn.cursor()

cursor.execute("SELECT * FROM eletronicos")
registros = cursor.fetchall()

if registros:
    for registro in registros:
            print(f"Código: {registro[0]}, Nome: {registro[1]}, Preço: {registro[2]}")
else:
    print("A tabela está vazia.")