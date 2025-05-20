from flask import Flask, render_template, request
import requests
import locale

app = Flask(__name__)

# Configura locale para pt_BR (tenta Unix, depois Windows)
try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except locale.Error:
    locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil.1252')

def formatar_valor(valor):
    """Formata float para string com separador de milhar ponto e decimal vírgula"""
    return locale.format_string('%.2f', valor, grouping=True)

def buscar_cotacoes():
    url = "https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,GBP-BRL,BTC-BRL"
    resposta = requests.get(url)
    if resposta.status_code != 200:
        return None
    dados = resposta.json()
    try:
        cotacoes = {
            'USD': float(dados['USDBRL']['bid']),
            'EUR': float(dados['EURBRL']['bid']),
            'GBP': float(dados['GBPBRL']['bid']),
            'BTC': float(dados['BTCBRL']['bid']),
        }
        return cotacoes
    except KeyError:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    cotacoes = buscar_cotacoes()
    resultado = None

    # Formata as cotações para exibição
    cotacoes_formatadas = {}
    if cotacoes:
        for moeda, valor in cotacoes.items():
            cotacoes_formatadas[moeda] = formatar_valor(valor)
    else:
        cotacoes_formatadas = None

    if request.method == 'POST':
        moeda = request.form.get('moeda', '').upper()
        valor_str = request.form.get('valor', '')
        if cotacoes and moeda in cotacoes:
            try:
                valor = float(valor_str.replace(',', '.'))  # aceita vírgula ou ponto na entrada
                convertido = valor * cotacoes[moeda]
                resultado = f'{formatar_valor(valor)} {moeda} = R$ {formatar_valor(convertido)}'
            except ValueError:
                resultado = 'Valor inválido.'
        else:
            resultado = 'Moeda inválida ou cotação indisponível.'

    return render_template('index.html', cotacoes=cotacoes_formatadas, resultado=resultado)

if __name__ == '__main__':
    # Host 0.0.0.0 para Render e debug True para desenvolvimento local
    app.run(debug=True, host='0.0.0.0')
