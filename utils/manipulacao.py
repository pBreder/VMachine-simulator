from utils.output import writing

def add_item(cursor, conexao):

    from utils.extras import mostrar_itens # Chamada dentro da função para evitar circular imports

    nome_prod = input('Qual o nome do novo item? ').capitalize()

    if nome_prod.lower() == 'sair':
        return
    try:                        
        preco_prod = float(input('Digite o valor do novo produto: '))
        quantidade_prod = int(input('Digite a quantidade desse produto adcionado à maquina: '))
    except ValueError:
        writing('Insira somente números')
        return

    cursor.execute("SELECT * FROM estoque WHERE LOWER(produto) = LOWER(?)", (nome_prod,))
    item_existe = cursor.fetchone()

    if item_existe:
        print(f"{nome_prod} já está no estoque")
        return
    else:    
        cursor.execute("INSERT OR IGNORE INTO estoque (produto, preco, quantidade) VALUES (?,?,?)", (nome_prod, preco_prod, quantidade_prod))
        print('Estoque após a alteração:\n')
        mostrar_itens(cursor, conexao)

    conexao.commit()

    writing(f'\nProduto {nome_prod} adcionado com sucesso!')

def deletar_item(cursor, conexao):
    from utils.extras import mostrar_itens

    nome_prod = input('Digite o nome do produto a ser retirado: ').lower()
    print()

    cursor.execute("SELECT * FROM estoque WHERE LOWER(produto) = LOWER(?)", (nome_prod,))
    item_existe = cursor.fetchone()

    if not item_existe:
        print(f"{nome_prod} não existe no estoque.")
        return
    else:
        cursor.execute("DELETE FROM estoque WHERE LOWER(produto) = LOWER(?)", (nome_prod,))
        print('Estoque após a alteração:\n')
        mostrar_itens(cursor, conexao, verificar = False)
    
    conexao.commit()
    
def atualizar_estoque(cursor, conexao):
    from utils.extras import mostrar_itens

    while True:
        nome_prod = input('\nDigite o nome do produto a se alterar o estoque: ').lower()
        
        cursor.execute("SELECT * FROM estoque WHERE LOWER(produto) = LOWER(?)", (nome_prod,))
        item_existe = cursor.fetchone()

        if not item_existe:
            writing("O produto não está no estoque")
        else:
            break
        
    try:
        quant_mod = int(input('Digite a quantidade a se modificar no estoque: '))
    except ValueError:
        writing('Insira somente números inteiros')

    cursor.execute("SELECT quantidade FROM estoque WHERE LOWER(produto) = LOWER(?)", (nome_prod,))
    qtd_atual = cursor.fetchone()[0] # Deve-se acessar o elemento 0 pois fetch retorna uma tuple, e não o numero em si

    nova_qtd = quant_mod + qtd_atual

    if nova_qtd < 0:
        print("O estoque não pode ser negativo.")
    else:
        cursor.execute("UPDATE estoque SET quantidade = ? WHERE LOWER(produto) = LOWER(?)", (nova_qtd, nome_prod))

    conexao.commit()
    writing(f"O valor de {quant_mod} foi modificado na quantidade de {nome_prod} no estoque. Quantidade atual: {nova_qtd}")
    print('Estoque após a alteração:\n')
    mostrar_itens(cursor, conexao)
    