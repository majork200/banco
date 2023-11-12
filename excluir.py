import psycopg2
conn = psycopg2.connect(
    dbname="cadastropy",
    user="postgres",
    password="gabriel789",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS eletronicos")
print("Tabela excluída")
conn.commit()
#Deteletar tababelas Existentes