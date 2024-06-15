from flask import Flask, render_template, request, redirect, url_for, session
import random
import signal

# Definição do manipulador de sinal
def handler(signum, frame):
    print('Signal handler called with signal', signum)
    # Aqui você pode adicionar qualquer limpeza ou lógica de saída necessária
    exit(0)  # Certifique-se de sair do programa após o tratamento do sinal

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'

palavras = [("lilian", "nome próprio"), ("lilian", "nome próprio"), ("cauã", "nome próprio"), ("laura", "nome próprio"), ("rodrigo", "nome próprio"), ("divino", "nome próprio"), ("sueli", "nome próprio"), ("antonio", "nome próprio"), ("luciene", "nome próprio"), ("benedito", "nome próprio"), ("carolina", "nome próprio"), ("jeferson", "nome próprio"), ("estevão", "nome próprio"), ("erickson", "nome próprio"), ("enrico", "nome próprio"), ("camila", "nome próprio"), ("daniel", "nome próprio"), ("antonela", "nome próprio"), ("fernando", "nome próprio"), ("sophia", "nome próprio"), ("cristina", "nome próprio"), ("renan", "nome próprio"), ("arthur", "nome próprio"), ("tamires", "nome próprio"), ("aline", "nome próprio"), ("alfredo", "nome próprio"), ("roberta", "nome próprio"), ("candida", "nome próprio"), ("gilberto", "nome próprio"), ("gilton", "nome próprio"), ("leticia", "nome próprio"), ("henry", "nome próprio"), ("hugo", "nome próprio"), ("carlos", "nome próprio"), ("lucineide", "nome próprio"), ("marina", "nome próprio"), ("neymar", "nome próprio"), ("messi", "nome próprio"), ("cristiano-ronaldo", "nome próprio"), ("ronaldinho", "nome próprio"), ("joão", "nome próprio"), ("gargamel", "nome próprio"), ("josé", "nome próprio"), ("jesus", "nome próprio"), ("garfo", "objeto"), ("copo", "objeto"), ("faca", "objeto"), ("livro", "objeto"), ("prato", "objeto"), ("lousa", "objeto"), ("smartphone", "objeto"), ("celular", "objeto"), ("camera", "objeto"), ("vaso", "objeto"), ("regua", "objeto"), ("tijolo", "objeto"), ("mesa", "objeto"), ("lampada", "objeto"), ("mouse", "objeto"), ("chinelo", "objeto"), ("sapato", "objeto"), ("mala", "objeto"), ("cadeira", "objeto"), ("ventilador", "objeto"), ("teclado", "objeto"), ("martelo", "objeto"), ("chave", "objeto"), ("agulha", "objeto"), ("linha", "objeto"), ("televisão", "objeto"), ("antena", "objeto"), ("lanterna", "objeto"), ("lampada", "objeto"), ("garrafa", "objeto"), ("geladeira", "objeto"), ("lápis", "objeto"), ("caderno", "objeto"), ("borracha", "objeto"), ("caneta", "objeto"), ("sofa", "objeto"), ("bucha", "objeto"), ("projetor", "objeto"), ("ribeirâo-preto", "cep"), ("brumadinho", "cep"), ("são-paulo", "cep"), ("cravinhos", "cep"), ("rio-de-janeiro", "cep"), ("sertãozinho", "cep"), ("cansas", "cep"), ("brasil", "cep"), ("estados-unidos", "cep"), ("rondonia", "cep"), ("curitiba", "cep"), ("manaus", "cep"), ("brasilia", "cep"), ("piracicaba", "cep"), ("são josé-do-rio-preto", "cep"), ("campinas", "cep"),  ("jardinópolis", "cep"), ("brodoswki", "cep"), ("inglaterra", "cep"),  ("vitória", "cep"), ("florianópolis", "cep"), ("franca", "cep"), ("frança", "cep"), ("argentina", "cep"), ("canadá", "cep"), ("américa-do-sol", "cep"), ("america-do-note", "cep"), ("japão", "cep"), ("china", "cep"), ("perú", "cep"), ("bolivia", "cep"), ("venezuela", "cep"), ("itália", "cep"), ("espanha", "cep"), ("veneza", "cep"), ("africa", "cep"), ("israel", "cep"), ("palestina", "cep"), ("irã", "cep"), ("qatar", "cep"), ("equador", "cep"), ("irlanda", "cep"), ("russia", "cep"), ("madri", "cep"), ("vaticano", "cep"), ("belgica", "cep"), ("amapá", "cep"), ("boston", "cep"), ("são-josé-do-rio-pardo", "cep"), ("itajaí", "cep"), ("mariana", "cep"), ("bahia", "cep"), ("salvador", "cep"), ("natal", "cep"), ("maceió", "cep"), ("jeriquaquara", "cep"), ("araraquara", "cep"), ("são-carlos", "cep"), ("goiania", "cep"), ("planura", "cep"), ("minas-gerais", "cep"), ("ribeirão-pires", "cep"), ("ribeirão-bonito", "cep"), ("jundiaí", "cep"), ("santa-rita-do-passa-quatro", "cep"), ("santo-antônio-da-alebria", "cep"), ("guariba", "cep"), ("guaratinguetá", "cep"), ("pirassununga", "cep"), ("cajuru", "cep"), ("ceará", "cep"), ("catanduva", "cep"), ("olímpia", "cep"), ("divinópolis", "cep"),]

def escolher_nova_palavra():
    escolhida = random.choice(palavras)
    session['palavra_secreta'] = escolhida[0]
    session['dica'] = escolhida[1]
    session['palavra_display'] = ['_' for _ in escolhida[0]]
    session['tentativas'] = 8
    session['letras_erradas'] = []
    session['forca_estado'] = 0

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'palavra_secreta' not in session:
        escolher_nova_palavra()
    
    if request.method == 'POST':
        letra = request.form['letra'].lower()
        processar_letra(letra)
        if '_' not in session['palavra_display'] or session['tentativas'] == 0:
            return redirect(url_for('resultado'))
    return render_template('index.html')

def processar_letra(letra):
    if letra in session['palavra_secreta']:
        for index, char in enumerate(session['palavra_secreta']):
            if char == letra:
                session['palavra_display'][index] = letra
    else:
        session['tentativas'] -= 1
        session['letras_erradas'].append(letra)
        session['forca_estado'] += 1
    session.modified = True

@app.route('/resultado')
def resultado():
    venceu = '_' not in session['palavra_display']
    return render_template('resultado.html', venceu=venceu)

@app.route('/reiniciar', methods=['POST'])
def reiniciar():
    escolher_nova_palavra()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Configuração do manipulador de sinal dentro do bloco correto
    signal.signal(signal.SIGINT, handler)
    print('Servidor iniciado. Pressione Ctrl+C para sair.')
    app.run(debug=True)