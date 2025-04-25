import time
import sqlite3
from utils.manipulacao import add_item

def verifica_estoque(cursor, conexao):
    cursor.execute("SELECT produto FROM estoque")
    if not cursor.fetchone():
        opcao = input("O estoque está vazio. Deseja cadastrar produtos no estoque? (y/n)").strip().lower()
        if opcao == 'y':
            add_item(cursor, conexao)
        else:
            return

def mostrar_itens(cursor, conexao, verificar = True):
    from utils.output import writing

    imprimir = True
    if verificar == True:
        cursor.execute("SELECT produto FROM estoque")
        if not cursor.fetchone():
            opcao = input("O estoque está vazio. Deseja cadastrar produtos no estoque? (y/n)").strip().lower()
            if opcao == 'y':
                add_item(cursor, conexao)
                imprimir = False
            else:
                return

    if imprimir == True:
        cursor.execute("SELECT produto, preco, quantidade, id FROM estoque")
        estoque = cursor.fetchall()

        print("|---------- Estoque  ----------|\n")

        for nome, preco, quantidade, id in estoque:
            writing(f"{nome} || R$ {preco:.2f} - {quantidade} unidades || codigo: {id}")
            time.sleep(0.01)

def mostrar_pedidos(cursor):
    from utils.output import writing
    try:
        cursor.execute("SELECT produto, preco, quantidade, data, hora FROM pedidos")
        pedidos = cursor.fetchall()

        if not pedidos:
            print("Não há pedidos no histórico.")
        else:
            print("\n|---------- Pedidos  ----------|\n")
            for nome, preco, quantidade, data, hora in pedidos:
                writing(f"{data} {hora} => {nome} || R$ {preco:.2f} - {quantidade} unidades")
                time.sleep(0.01)
    except sqlite3.OperationalError:
        print("A Tabela 'pedidos' não existe no sistema.")