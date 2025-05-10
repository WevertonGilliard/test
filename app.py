from flask import Flask, render_template, request, redirect
import csv
from datetime import date
import os

app = Flask(__name__)
ARQUIVO = 'saldo.csv'

def obter_ultimo_saldo():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, 'r') as f:
            linhas = list(csv.reader(f))
            if len(linhas) > 1:
                return float(linhas[-1][4])
    return 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registrar', methods=['POST'])
def registrar():
    entradas = float(request.form['entradas'])
    saidas = float(request.form['saidas'])
    saldo_do_dia = entradas - saidas
    saldo_anterior = obter_ultimo_saldo()
    saldo_acumulado = saldo_anterior + saldo_do_dia
    data_hoje = date.today().isoformat()

    with open(ARQUIVO, 'a', newline='') as f:
        writer = csv.writer(f)
        if os.stat(ARQUIVO).st_size == 0:
            writer.writerow(["data", "entradas", "saidas", "saldo_do_dia", "saldo_acumulado"])
        writer.writerow([data_hoje, entradas, saidas, saldo_do_dia, saldo_acumulado])

    return redirect('/historico')

@app.route('/historico')
def historico():
    historico = []
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, 'r') as f:
            leitor = csv.reader(f)
            historico = list(leitor)
    return render_template('historico.html', dados=historico)

if __name__ == '__main__':
    app.run(debug=True)
