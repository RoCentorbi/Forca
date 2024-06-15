from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'

# Lista de palavras e dicas
palavras = [("python", "Linguagem de programação"), ("tkinter", "Biblioteca de GUI para Python"), ("forca", "Jogo clássico")]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'nova_palavra' in request.form:
            escolher_nova_palavra()
        else:
            letra = request.form['letra'].lower()
            processar_letra(letra)
        return redirect(url_for('index'))
    else:
        if 'palavra_secreta' not in session:
            escolher_nova_palavra()
        return render_template('index.html')

def escolher_nova_palavra():
    palavra_secreta, dica = random.choice(palavras)
    session['palavra_secreta'] = palavra_secreta
    session['dica'] = dica
    session['palavra_display'] = ['_' for _ in palavra_secreta]
    session['tentativas'] = 8
    session['letras_erradas'] = []

def processar_letra(letra):
    if letra in session['palavra_secreta']:
        for index, char in enumerate(session['palavra_secreta']):
            if char == letra:
                session['palavra_display'][index] = letra
    else:
        session['tentativas'] -= 1
        session['letras_erradas'].append(letra)

@app.route('/reiniciar')
def reiniciar():
    escolher_nova_palavra()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)