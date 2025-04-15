import time
import datetime
import json
import os

while True:
        try:
            dinheiro = float(input("Quanto de dinheiro você tem: "))
            break
        except ValueError:
            print("Insira somente números, por favor.")

print(f'Dinehiro depositado: R${dinheiro:.2f}')

itens = {
    'Snickers': {'preco': 3.50, 'codigo' : '0a','quantidade' : 10},
    'Amendoins': {'preco': 3.00, 'codigo' : '0b','quantidade' : 10},
    'Kitkat\'s': {'preco': 5.00, 'codigo' : '0c','quantidade' : 10},
    'Doritos': {'preco': 4.50, 'codigo' : '1a','quantidade' : 10},
    'Ruffles': {'preco': 4.50, 'codigo' : '1b','quantidade' : 10},
    'Jujubas': {'preco': 1.50, 'codigo' : '1c','quantidade' : 10},
    'Twix\'s': {'preco': 3.00, 'codigo' : '2a','quantidade' : 10},
    'M&M\'s': {'preco': 4.00, 'codigo' : '2b','quantidade' : 10},
    'Mentos': {'preco': 4.00, 'codigo' : '2c','quantidade' : 10}
}

def load_estoque():
    if os.path.exists("Registro de estoque - VMachine"):
        with open("Registro de estoque - VMachine","r") as arquivo:
            estoque = json.load(arquivo)
            return estoque
    else:
        return

pre_estoque = load_estoque()
estoque_real = pre_estoque if pre_estoque else itens

def back():
    print('\nRetornando ao menu incial.')
    time.sleep(1)
    main()

def writing(string):
    for letra in string:
        print(letra, end = '', flush = True)
        time.sleep(0.01)
    print()

def salvar_pedido(pedido):
    with open ("Registro de pedidos - VMachine", "a") as arquivo:
        json.dump(pedido, arquivo, indent = 4)
        arquivo.write("\n" + "-" * 50 + "\n")

    print('Pedido salvo! APAGAR DEPOIS')

def salvar_estoque(estoque):
    with open ("Registro de estoque - VMachine", "w") as arquivo:
        json.dump(estoque, arquivo, indent = 4)

def mostrar_itens():

    print()                     
    for item, info in estoque_real.items():
        if info['quantidade'] > 0:
            print(f"{item}: R${info['preco']:.2f}, codigo: {info['codigo']}")
            time.sleep(0.01)

def comprar_item(dinheiro):

    # Verifica qual o produto desejado e se o codigo está associado à algum item.
    while True:
        cod_prod = input('\nDigite o codigo do produto que quer comprar: ').lower()
        if cod_prod not in [info['codigo'] for info in estoque_real.values()]:
            print("Esse codigo nao corresponde a nenhum porduto do estoque.")
        else:
            break

    # Verifica se há esse item no estoque.
    for item, info in estoque_real.items():
        if cod_prod == info['codigo'] and info['quantidade'] < 1:
                print(f"Produto {item} indisponível no estoque.")
                back()
        else:
            if cod_prod == info['codigo']:
                produto_nome = item

    # Obtem-se a quantidade desejada do produto e verifica se a demanda é maior que a oferta.
    while True:
        try:
            quant = int(input('Digite a quantidade que irá comprar: '))
            for item, info in estoque_real.items():
                if cod_prod == info['codigo'] and quant > info['quantidade']:
                    if info['quantidade'] == 1:
                        choose = input(f'Desculpe, mas há somente {info["quantidade"]} unidade no estoque. Deseja compra-la? (y/n): ')
                        if choose == 'y':
                            quant = info['quantidade']
                        else:
                            back()
                    else:
                        choose = input(f'Desculpe, mas há somente {info["quantidade"]} unidades no estoque. Deseja compra-las? (y/n): ')
                        if choose == 'y':
                            quant = info['quantidade']
                        else:
                            back()                  
            break
        except ValueError:
            print('Insira somente números inteiros')

    # Calcula o custo valoral do pedido.
    for item, info in estoque_real.items():
        if cod_prod == info['codigo']:
            valor = quant * info['preco']

    # Verifica se o cliente tem dinheiro suficiente para a compra.
    if valor > dinheiro:
        writing('\nDinheiro insuficiente para efetuar a compra.')
        back()

    # Abate o valor valoral do valor depositado e atualiza a quantidade do estoque.
    for item, info in estoque_real.items():
        if cod_prod == info['codigo']:
            estoque_real[item]['quantidade'] -= quant

    dinheiro -= valor

    data = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    writing('\nCompra feita com sucesso!')


    if dinheiro > 0:
        writing(f"Devolvendo troco de R${dinheiro:.2f}")
    else:
        dinheiro = 0

    return produto_nome, quant, data, valor, dinheiro

def main():

    while True:

        menu = [
        '\n***** Bem vindo à Vending Machine! *****\n',
        '1. Mostrar produtos disponíveis',
        '2. Comprar Produto.',
        '3. Sair\n',
        '***********************************'
    ]

        for frase in menu:
            writing(frase)

        opcao = input('\nEscolha uma opção: ')

        if opcao == '1':
            mostrar_itens()

        elif opcao == '2':
            nome_produto, quantidade_pedida, data_compra, valor_total, troco_recebido = comprar_item(dinheiro)

            pedido = {

                "Produto" : nome_produto,
                "Quantidade" : quantidade_pedida,
                "Data e hora" : data_compra,
                "Valor" : valor_total,
                "Troco" : troco_recebido,
                "Dinheiro" : dinheiro,
                "Estoque" : estoque_real
            }

            print(nome_produto)
            salvar_pedido(pedido)
            salvar_estoque(estoque_real)

        elif opcao == '3':
            print('Saindo...')
            break

        else:
            print('Opção inválida, tente de novo.')
        
main()