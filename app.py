from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def buscar_cotacoes():
    url = "https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,GBP-BRL"
    resposta = requests.get(url)
    if resposta.status_code != 200:
        return None
    dados = resposta.json()
    cotacoes = {
        'USD': float(dados['USDBRL']['bid']),
        'EUR': float(dados['EURBRL']['bid']),
        'GBP': float(dados['GBPBRL']['bid']),
    }
    return cotacoes

@app.route('/', methods=['GET', 'POST'])
def index():
    cotacoes = buscar_cotacoes()
    resultado = None
    if request.method == 'POST':
        moeda = request.form.get('moeda').upper()
        valor = request.form.get('valor')
        if cotacoes and moeda in cotacoes:
            try:
                valor = float(valor)
                convertido = valor * cotacoes[moeda]
                resultado = f'{valor} {moeda} = R$ {convertido:.2f}'
            except ValueError:
                resultado = 'Valor inválido.'
        else:
            resultado = 'Moeda inválida ou cotação indisponível.'
    return render_template('index.html', cotacoes=cotacoes, resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)
