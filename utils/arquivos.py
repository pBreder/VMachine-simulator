def criar_estoque(cursor, conexao):
    cursor.execute(""" CREATE TABLE IF NOT EXISTS estoque (
                   
                   produto TEXT,
                   preco REAL,
                   quantidade INTEGER,
                   id INTEGER PRIMARY KEY
                   
    )
                    
    """)
    
    conexao.commit()

def registrar_pedido(cursor, conexao, produto, preco, quantidade, data, hora):
    cursor.execute(""" CREATE TABLE IF NOT EXISTS pedidos (

        produto TEXT,
        preco REAL,
        quantidade INTEGER,
        data TEXT,
        hora TEXT
    
    )

    """)

    cursor.execute("""INSERT INTO pedidos (produto, preco, quantidade, data, hora) VALUES (?,?,?,?,?)""",
                   (produto, preco, quantidade, data, hora))
    
    conexao.commit()