import time
import os
import json

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

estoque_arq = "Registro de estoque - VMachine"

def back():
    print('\nRetornando ao menu incial.')
    time.sleep(1)
    main()

def load_estoque(estoque_arq):
    if os.path.exists(estoque_arq):
        with open(estoque_arq,"r") as arquivo:
            estoque = json.load(arquivo)
            return estoque
    else:
        return itens

pre_estoque = load_estoque(estoque_arq)
estoque_real = pre_estoque if pre_estoque else itens

def salvar(estoque):
    with open(estoque_arq,"w") as arquivo:
        json.dump(estoque, arquivo, indent=4)

def writing(string):
    for letra in string:
        print(letra, end = '', flush = True)
        time.sleep(0.01)
    print()

def mostrar_itens():   
    print()                     
    for item, info in estoque_real.items():
        if info['quantidade'] > 0:
            print(f"{item}: R${info['preco']:.2f}, quantidade no estoque: {info['quantidade']}")

def add_item():

    nome_prod = input('Qual o nome do novo item? ')

    if nome_prod.lower() in [item.lower() for item in estoque_real]:
        writing(f'\n{nome_prod} já está na máquina.')
        return

    try:                        
        preco_prod = float(input('Digite o valor do novo produto: '))
        quantidade_prod = int(input('Digite a quantidade desse produto adcionado à maquina: '))
        cod_prod = input("Digite o codigo do novo produto: ")
    except ValueError:
        writing('Insira somente números')
        back()

    estoque_real[nome_prod] = {'preco': preco_prod, 'codigo' : cod_prod ,'quantidade': quantidade_prod}
    writing(f'Produto {nome_prod} adcionado com sucesso!')

    salvar(estoque_real)

def retirar_item():
    nome_prod = input('Digite o nome do produto a ser retirado: ').lower()

    for item in list(estoque_real.keys()):
        if item.lower() == nome_prod:
            del estoque_real[item]
    else:
        writing('O produto não está no estoque')
    
def alterar_estoque():

    while True:
        nome_prod = input('\nDigite o nome do produto a se alterar o estoque: ').lower()
        if nome_prod.lower() not in list(map(lambda x: x.lower(), estoque_real.keys())):
            writing("O produto não está no estoque")
        else:
            break
        
    try:
        quant_mod = int(input('Digite a quantidade a se modificar no estoque: '))
    except ValueError:
        writing('Insira somente números inteiros')

    for item in estoque_real:
        if nome_prod == item.lower():
            estoque_real[item]['quantidade'] += quant_mod
            writing(f"O valor de {quant_mod} foi modificado na quantidade de {item} no estoque. Quantidade atual: {estoque_real[item]['quantidade']}")
            salvar(estoque_real)
            return
        
def main():

    while True:

        menu = [
        '\n***** Menu da Máquina de vendas *****\n',
        '1. Mostrar produtos disponíveis',
        '2. Adicionar item',
        '3. Retirar Item',
        '4. Atualizar estoque',
        '5. Sair\n',
        '***********************************'
    ]

        for frase in menu:
            for letra in frase:
                print(letra, end = '', flush = True)
                time.sleep(0.01)
            print()

        opcao = input('\nEscolha uma opção: ')

        if opcao == '1':
            mostrar_itens()
        elif opcao == '2':
            add_item()
        elif opcao == '3':
            retirar_item()
        elif opcao == '4':
            alterar_estoque()
        elif opcao == '5':
            print('Saindo...')
            break
        else:
            writing('Opção inválida, tente de novo.')
        
main()