from tkinter import *
import psycopg2

class PrincipalBD:
    def __init__(self,win):
        self.win=win
        self.obj = AppBD()
        self.objr = MyApp()
        

     # Configuração da interface Tkinter
        self.label_codigo = Label(win, text="Código:")
        self.label_codigo.grid(row=0, column=0,padx=50,pady=20)
        self.entry_codigo = Entry(win)
        self.entry_codigo.grid(row=0, column=1,padx=50,pady=20)

        self.label_nome = Label(win, text="Nome:")
        self.label_nome.grid(row=1, column=0,padx=50,pady=20)
        self.entry_nome = Entry(win)
        self.entry_nome.grid(row=1, column=1,padx=50,pady=20)

        self.label_preco = Label(win, text="Preço:")
        self.label_preco.grid(row=2, column=0,padx=50,pady=20)
        self.entry_preco = Entry(win)
        self.entry_preco.grid(row=2, column=1,padx=50,pady=20)

        self.btn_cadastrar = Button(win, text="Cadastrar", command=self.cadastrar)
        self.btn_cadastrar.grid(row=3,column=0)

        self.btn_addjuros = Button(win,text= "juros",command=self.juros)
        self.btn_addjuros.grid(row=4,column=0)

        self.btn_addtabela = Button(win,text= "tabela",command=self.rtabela)
        self.btn_addtabela.grid(row=4,column=1,pady=20)


        self.btn_atualizar = Button(win, text="Atualizar", command=self.atualizar)
        self.btn_atualizar.grid(row=3, column=1)

        self.btn_excluir = Button(win, text="Excluir", command=self.excluir)
        self.btn_excluir.grid(row=3, column=2)

    # Funções para manipular a interface Tkinter

    def rtabela(self):
        self.objr.resultados()

    def cadastrar(self):  
        self.nome = self.entry_nome.get()
        self.preco = self.entry_preco.get()
        self.obj.cadastrar_dados(self.nome, self.preco)

    def atualizar(self):
        self.codigo = self.entry_codigo.get()
        self.nome = self.entry_nome.get()
        self.preco = self.entry_preco.get()
        self.obj.atualizar_dados(self.codigo, self.nome, self.preco)

    def excluir(self):
        try:
            self.codigo = self.entry_codigo.get()
            self.obj.excluir_dados(self.codigo)
        except:
            print("Insira um codigo na tabela")
    def juros(self):
        self.codigo = self.entry_codigo.get()
        self.nome = self.entry_nome.get()
        self.preco = self.entry_preco.get()
        self.obj.adicionar_juros(self.codigo, self.nome, self.preco)


class AppBD:
    def __init__(self):
        
        print("metodo construtor")  
   
    # Conectar ao PostgreSQL

        self.conn = psycopg2.connect(
        dbname="cadastropy",
        user="postgres",
        password="192003",
        host="localhost",
        port="5433"
    )
        self.cursor = self.conn.cursor()

    # Chamar a função para criar a tabela
    # Funções para interagir com o banco de dados

    def cadastrar_dados(self,nome, preco):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS eletronicos (
               codigo SERIAL PRIMARY KEY,
               nome VARCHAR(255),
               preco FLOAT
             )
            """)
        self.conn.commit()
        if nome and preco:
            # Função para verificar e criar a tabela se não existir

            self.cursor.execute("INSERT INTO eletronicos (nome, preco) VALUES (%s, %s) RETURNING codigo", (nome, preco))
            novo_codigo = self.cursor.fetchone()[0]
            self.conn.commit()
            print("cadastrado")
            return novo_codigo
        else:
            print("Nome e preço não podem ser vazios. Cadastro não realizado.")
            return None

    #Função para atualizar os dados na tabela
    def atualizar_dados(self, codigo, nome, preco):
       try:
           # Verificar se todos os valores são não vazios
           if nome and preco and codigo:
               self.cursor.execute("UPDATE eletronicos SET nome=%s, preco=%s WHERE codigo=%s", (nome, preco, codigo))
               print("atualizado")
               self.conn.commit()
           else:
               print("Erro: Nome, preço e código não podem ser vazios.")
       except psycopg2.Error as erros:
           self.conn.rollback()
           print(f"Erro ao atualizar dados: {erros}")



    #Função para adicionar juros os dados na tabela

    def adicionar_juros(self, codigo, nome, preco):
        try:
            # Recuperar os registros existentes
            self.cursor.execute("SELECT codigo, preco FROM eletronicos")
            registros = self.cursor.fetchall()

            if registros:
                for codigo, preco in registros:
                    # Calcular novo preço com juros de 10%
                    novo_preco = preco * 1.1

                    # Atualizar registro com o novo preço
                    self.cursor.execute("UPDATE eletronicos SET preco=%s WHERE codigo=%s", (novo_preco, codigo))

                print("Juros adicionados a todos os registros")
                self.conn.commit()
            else:
                print("A tabela está vazia.")
        except psycopg2.Error as e:
            print(f"Erro ao adicionar juros: {e}")
            self.conn.rollback()

    #Função para excluir os dados na tabela

    def excluir_dados(self, codigo):
        try:
            self.cursor.execute("DELETE FROM eletronicos WHERE codigo=%s", (codigo,))
            print("excluído")
            self.conn.commit()
        except:
            print("Espaço do codigo esta vazio!")






class MyApp():
    def __init__(self):
        super().__init__()

    def app(self):
         #Programa principal
        self.janela = Tk()
        self.janela.title("Cadastro de eletronicos")
        self.janela.geometry("600x400")

        PrincipalBD(self.janela)

        self.janela.mainloop()
        pass
    def resultados(self):

        self.janela_result = Tk()
        self.janela_result.title("resultado")
        self.janela_result.mainloop()

        pass
