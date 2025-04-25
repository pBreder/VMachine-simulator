import sqlite3
import time
from utils.extras import *
from utils.manipulacao import *
from utils.arquivos import criar_estoque
from utils.output import writing
    
def main():

    conn = sqlite3.connect('registros/registro_estoque_VM.db')
    cursor = conn.cursor()

    criar_estoque(cursor, conn)

    while True:

        menu = [
        '\n***** Menu da Máquina de vendas (ADM) *****\n',
        '1. Mostrar produtos disponíveis',
        '2. Mostrar histórico de pedidos',
        '3. Adicionar item',
        '4. Retirar Item',
        '5. Atualizar estoque',
        '6. Sair\n',
        '***********************************'
    ]

        for frase in menu:
            for letra in frase:
                print(letra, end = '', flush = True)
                time.sleep(0.01)
            print()

        opcao = input('\nEscolha uma opção: ')
        print()

        if opcao == '1':
            mostrar_itens(cursor, conn)
        elif opcao == '2':
            mostrar_pedidos(cursor)
        elif opcao == '3':
            add_item(cursor, conn)
        elif opcao == '4':
            deletar_item(cursor, conn)
        elif opcao == '5':
            atualizar_estoque(cursor, conn)
        elif opcao == '6':
            conn.close()
            print('Saindo...')
            break
        else:
            writing('Opção inválida, tente de novo.')
        
main()