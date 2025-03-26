import psycopg2
from psycopg2.extras import RealDictCursor
from db_config import conectar

def carregar_vendas():
    conn = conectar()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    query = """SELECT 
        sod.salesorderid, 
        CASE
            WHEN c.storeid IS NOT NULL THEN s.name  -- Quando for uma loja, usa o nome da loja
            WHEN c.personid IS NOT NULL THEN CONCAT(pp.FirstName, ' ', pp.LastName)  -- Quando for uma pessoa, usa o nome da pessoa
            ELSE 'Desconhecido' -- Caso não tenha storeid nem personid
        END AS buyer_name,
        soh.status,
        p.name,
        sod.orderqty, 
        ROUND(sod.unitprice,2) AS unitprice,  
        soh.territoryid, 
        TO_CHAR(soh.orderdate, 'DD/MM/YYYY') AS orderdate
    FROM sales.salesorderdetail sod
    JOIN sales.salesorderheader soh ON sod.salesorderid = soh.salesorderid
    JOIN sales.customer c ON soh.customerid = c.customerid
    LEFT JOIN production.product p ON sod.productid = p.productid
    LEFT JOIN sales.store s ON c.storeid = s.businessentityid
    LEFT JOIN person.person pp ON c.personid = pp.businessentityid 
    LIMIT 100;
"""  # Seleciona todos os pedidos da tabela Orders
    cursor.execute(query)
    
    vendas = cursor.fetchall()  # Pega todos os resultados da query
    
    conn.close()
    
    return vendas

def adicionar_venda(dados_venda):
    conn = conectar()
    cursor = conn.cursor()
    
    query = """
        INSERT INTO orders (customerid, employeeid, orderdate, shipcity)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (dados_venda['customerid'], dados_venda['employeeid'], dados_venda['orderdate'], dados_venda['shipcity']))
    
    conn.commit()  # Confirma a transação
    conn.close()
    
    return "Venda adicionada com sucesso"

def registrar_saida(order_id):
    conn = conectar()
    cursor = conn.cursor()
    
    query = """
        UPDATE orders
        SET shipdate = CURRENT_DATE
        WHERE orderid = %s
    """
    cursor.execute(query, (order_id,))
    
    conn.commit()
    conn.close()
    
    return "Saída registrada com sucesso"

