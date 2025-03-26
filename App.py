from flask import Flask, jsonify, request, render_template, redirect, url_for, session
from db_utils import carregar_vendas, registrar_saida, adicionar_venda

app = Flask(__name__)

@app.route('/detalhes_venda')
def detalhes_venda():
    vendas = carregar_vendas()
    print(vendas)
    return render_template('index.html', vendas=vendas)

@app.route('/adicionar_venda', methods=['POST'])
def adicionar_venda_route():
    data = request.get_json()
    result = adicionar_venda(data)
    return jsonify({"message": result})

@app.route('/registrar_saida', methods=['POST'])
def registrar_saida_route():
    data = request.get_json()
    order_id = data.get('orderid')
    
    result = registrar_saida(order_id)
    
    return jsonify({"message": result})

@app.route('/')
def index():
    return redirect(url_for('detalhes_venda'))

if __name__ == '__main__':
    app.run(debug=True)
