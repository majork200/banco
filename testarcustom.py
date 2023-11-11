from tkinter import *
import psycopg2

def obter_dados_e_preencher_lista():
    try:
        conn = psycopg2.connect(
            dbname="cadastropy",
            user="postgres",
            password="192003",
            host="localhost",
            port="5433"
        )
        cursor = conn.cursor()

        cursor.execute("SELECT nome, preco FROM eletronicos")
        dados = cursor.fetchall()

        root = Tk()
        root.title("Lista de Dados SQL")

        listbox = Listbox(root, height=10, width=40)
        scrollbar = Scrollbar(root, orient="vertical", command=listbox.yview)

        listbox.config(yscrollcommand=scrollbar.set)

        listbox.grid(row=0, column=0, padx=10, pady=10)
        scrollbar.grid(row=0, column=1, sticky="ns", pady=10)

        for dado in dados:
            listbox.insert(END, f"Nome: {dado[0]}, Preço: {dado[1]}")

        root.mainloop()

    except psycopg2.Error as e:
        print(f"Erro ao obter dados do SQL: {e}")

obter_dados_e_preencher_lista()
