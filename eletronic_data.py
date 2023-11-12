#Aluno: Jhonathan William Matricula: 202202136956
#Aluno: Gabriel Severo Paiva Matricula:202203600397

from tkinter import *
import psycopg2

class PrincipalBD:
    def __init__(self,win):
        self.win=win
        self.obj = AppBD()
        

     # Configuração da interface Tkinter 
        self.label_codigo = Label(win, text="Código:",background="#0A1B2A",foreground="#FFFFFF")
        self.label_codigo.grid(row=0, column=0,padx=50,pady=20)
        self.entry_codigo = Entry(win,background="#5882FA",foreground="#FFFFFF")
        self.entry_codigo.grid(row=0, column=1,padx=50,pady=20)

        self.label_nome = Label(win, text="Nome:",background="#0A1B2A",foreground="#FFFFFF")
        self.label_nome.grid(row=1, column=0,padx=50,pady=20)
        self.entry_nome = Entry(win,background="#5882FA",foreground="#FFFFFF")
        self.entry_nome.grid(row=1, column=1,padx=50,pady=20)

        self.label_preco_juros = Label(win, text="Preço com juros de 10%:", background="#0A1B2A", foreground="#FFFFFF")
        self.label_preco_juros.grid(row=0, column=5, columnspan=2)

        self.label_preco_var = StringVar()
        self.label_preco_var.trace_add("write", self.atualizar_label_preco_juros)
        

        self.label_preco = Label(win, text="Preço:",background="#0A1B2A",foreground="#FFFFFF")
        self.label_preco.grid(row=2, column=0,padx=50,pady=20)
        self.entry_preco = Entry(win,background="#5882FA",foreground="#FFFFFF",textvariable=self.label_preco_var)
        self.entry_preco.grid(row=2, column=1,padx=50,pady=20)

        self.btn_cadastrar = Button(win, text="Cadastrar", command=self.cadastrar,background="#FF8000")
        self.btn_cadastrar.grid(row=3,column=0,ipadx=10)

        #teste para mostra lista sql terminar dps
        self.btn_addtabela = Button(win,text= "tabela",command=self.rtabela,background="#FF8000")
        self.btn_addtabela.grid(row=4,column=1,pady=20,ipadx=10)


        self.btn_atualizar = Button(win, text="Atualizar", command=self.atualizar,background="#FF8000")
        self.btn_atualizar.grid(row=3, column=1,ipadx=10)

        self.btn_excluir = Button(win, text="Excluir", command=self.excluir,background="#FF8000")
        self.btn_excluir.grid(row=4, column=0,ipadx=10)

    # Funções para manipular a interface Tkinter
    
    #novo windowns a ser aplicado
    def rtabela(self):
        self.obj.resultados()

    def atualizar_label_preco_juros(self, *args):
        try:
            preco = float(self.label_preco_var.get())
            preco_com_juros = preco * 1.1
            self.label_preco_juros.config(text=f"Preço com juros de 10%: {preco_com_juros:.2f}")
        except ValueError:
            self.label_preco_juros.config(text="Preço com juros de 10%: sem numero")

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

    def cadastrar_dados(self, nome, preco):
        try:
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS eletronicos (
               codigo SERIAL PRIMARY KEY,
               nome VARCHAR(255),
               preco REAL,
               juros_preco REAL                  
             )
            """)
            self.conn.commit()

            if nome and preco:
                preco = float(preco)  # Convertendo para float
                juros_preco = preco * 1.1
                print(f"Juros preco: {juros_preco}")  # Adicionado para debug
                self.cursor.execute("INSERT INTO eletronicos (nome, preco, juros_preco) VALUES (%s, %s, %s) RETURNING codigo", (nome, preco, juros_preco))
                novo_codigo = self.cursor.fetchone()[0]
                self.conn.commit()
                print("Cadastrado")
                return novo_codigo
            else:
                print("Nome e preço não podem ser vazios. Cadastro não realizado.")
                return None
        except (psycopg2.Error, ValueError) as error:
            print(f"Erro ao cadastrar dados: {error}")
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
    
    
    #resultados em teste terminar dps

    def resultados(self):
       try:
           self.cursor.execute("SELECT nome, preco ,juros_preco FROM eletronicos")
           dados = self.cursor.fetchall()

           self.nwin = Tk()
           self.nwin.title("Resultados do SQL")
           self.nwin.geometry("350x300")

           text_widget = Text(self.nwin, wrap="word")
           text_widget.grid(row=0, column=0, padx=10, pady=10)

           for dado in dados:
               resultado_texto = f"Nome: {dado[0]}, Preço: {dado[1]},Juros: {dado[2]}\n"
               text_widget.insert(END, resultado_texto)

           self.nwin.mainloop()

       except psycopg2.Error as e:
           print(f"Erro ao obter dados do SQL: {e}")


    #Função para excluir os dados na tabela

    def excluir_dados(self, codigo):
        try:
            self.cursor.execute("DELETE FROM eletronicos WHERE codigo=%s", (codigo,))
            print("excluído")
            self.conn.commit()
        except:
            print("Espaço do codigo esta vazio!")







 # Programa principal
janela = Tk()
janela.title("Cadastro de eletronicos")
janela.geometry("600x350")
janela.configure(background="#0A1B2A")

PrincipalBD(janela)

janela.mainloop()
