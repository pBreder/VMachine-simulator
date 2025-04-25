import datetime
import sqlite3
import sys
from utils.extras import *
from utils.arquivos import *
from utils.output import writing

def adcionar_saldo(saldo):

    while True:
        try:
            valor_dep = float(input("Quanto de dinheiro você quer depositar: ").strip())
            break
        except ValueError:
            print("Insira somente números, por favor.")

    print(f'Dinheiro depositado: R${valor_dep:.2f}')

    saldo_final = saldo + valor_dep

    print(f"Seu novo saldo é de {saldo_final}")

    return saldo_final

def comprar_item(saldo, cursor, conexao):

    # Verifica qual o produto desejado, se o codigo (ID) está associado à algum item e se há quantidade no estoque.
    while True:
        cod_prod = input('\nDigite o codigo (ID) do produto que quer comprar: ').strip()
        cursor.execute("SELECT * FROM estoque WHERE id = ?", (cod_prod,))
        item_existe = cursor.fetchone()

        if not item_existe:
                print('\nItem não encontrado, digite um código válido.')
                continue
        else:
            cursor.execute("SELECT quantidade FROM estoque WHERE id = ?", (cod_prod,))
            qtd_estoque = cursor.fetchone()[0] # fetch retorna uma tuple, logo é necessario acessar o elemento.
            produto = item_existe[0]
            
            if qtd_estoque < 1:
                print('O produto selecionado esgotou.')
                return saldo
            else:
                while True:
                    try:
                        while True:
                            quantidade_desejada = int(input("Digite a quantidade que deseja comprar: ").strip())
                            if quantidade_desejada >= 1:
                                break

                        if quantidade_desejada > qtd_estoque and qtd_estoque == 1:
                            opcao = input(f"Desculpe, mas há somente {qtd_estoque} unidade no estoque. Deseja comprá-la? (y/n): ").strip().lower()
                            if opcao == 'y':
                                quantidade_desejada = qtd_estoque
                                break
                            else:
                                return saldo
                            
                        elif quantidade_desejada > qtd_estoque and qtd_estoque > 1:
                            opcao = input(f"Desculpe, mas há somente {qtd_estoque} unidades no estoque. Deseja comprá-las? (y/n): ").strip().lower() # Somente para adaptar 'unidade' para o plural
                            if opcao == 'y':
                                quantidade_desejada = qtd_estoque
                                break
                            else:
                                return saldo
                            
                        else:
                            break

                    except ValueError:
                        print("Digite somente valores inteiros.")
        conexao.commit()
        break

    # Calcula o valor total da compra.
    cursor.execute("SELECT preco FROM estoque WHERE id = ?", (cod_prod,))
    preco_desejado = cursor.fetchone()

    if preco_desejado is None:
        print("O codigo digitado não está cadastrado no estoque.")
        return saldo

    
    preco_produto = preco_desejado[0]
    valor_total = quantidade_desejada * preco_produto

    # Verifica se o cliente tem dinheiro suficiente para a compra.
    if valor_total > saldo:
        writing('\nDinheiro insuficiente para efetuar a compra.')
        return saldo

    # Desconta o valor total do valor depositado (saldo) e atualiza o estoque.
    nova_quantidade = qtd_estoque - quantidade_desejada
    cursor.execute("UPDATE estoque SET quantidade = ? WHERE id = ?", (nova_quantidade, cod_prod))
    saldo -= valor_total

    # Obtem a o momento em que se efetua a compra
    data = datetime.datetime.now().strftime("%d/%m/%Y")
    hora = datetime.datetime.now().strftime("%H:%M:%S")

    registrar_pedido(cursor, conexao, produto, preco_produto, quantidade_desejada, data, hora)

    if saldo > 0:
        writing(f"Compra feita com sucesso, devolvendo troco de R${saldo:.2f}")
    else:
        saldo = 0
        print("Compra feita com sucesso, mas seu saldo esgotou.")
    
    return saldo

def main():
    conn = sqlite3.connect('registros/registro_estoque_VM.db')
    cursor = conn.cursor()
    criar_estoque(cursor, conn)
    
    valor_dep = 0

    try:
        cursor.execute("SELECT 1 FROM estoque LIMIT 1")
    except sqlite3.OperationalError:
        sys.exit("O estoque ainda não foi montado, tente novamente mais tarde.")

    while True:

        menu = [
        '\n***** Bem vindo à Vending Machine! *****\n',
        '1. Mostrar produtos disponíveis',
        '2. Comprar Produto.',
        '3. Adicionar saldo.',
        '4. Sair\n',
        '***********************************'
    ]

        for frase in menu:
            writing(frase)

        opcao = input('\nEscolha uma opção: ').strip()

        if opcao == '1':
            mostrar_itens(cursor, conn, verificar = False)

        elif opcao == '2':
            valor_dep = comprar_item(valor_dep, cursor, conn)

        elif opcao == '3':
            valor_dep = adcionar_saldo(valor_dep)

        elif opcao == '4':
            print('Saindo...')
            break

        else:
            print('Opção inválida, tente de novo.')
        
main()