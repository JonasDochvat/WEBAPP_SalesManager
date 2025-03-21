import psycopg2
from psycopg2.extras import RealDictCursor
from db_config import conectar

def carregar_vendas():
    conn = conectar()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    query = """SELECT o.order_id, c.company_name, p.product_name, od.quantity, od.unit_price,  o.ship_city, order_date
        FROM order_details od
        JOIN orders o ON od.order_id = o.order_id
        JOIN customers c ON o.customer_id = c.customer_id
        JOIN products p ON od.product_id = p.product_id;"""  # Seleciona todos os pedidos da tabela Orders
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

