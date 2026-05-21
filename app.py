from flask import Flask, render_template, request, redirect, url_for
from datetime import date, timedelta
from db import get_connection

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registrazione', methods=['GET', 'POST'])
def registrazione():
    if request.method == 'POST':
        nome = request.form['nome']
        cognome = request.form['cognome']
        data_nascita = request.form['data_nascita']
        email = request.form['email']
        scadenza = date.today() + timedelta(days=365)
        db = get_connection()
        cursore = db.cursor()
        #Inserimento nuovo cliente nel database
        cursore.execute("INSERT INTO CLIENTE (Nome, Cognome, DataNascita, Email, ScadenzaTessera) VALUES (%s, %s, %s, %s, %s)", (nome, cognome, data_nascita, email, scadenza))
        db.commit()
        cursore.close()
        db.close()
        return redirect(url_for('index'))
    return render_template('registrazione.html')


@app.route('/assegnazione-kart', methods=['GET', 'POST'])
def assegnazione():
    db = get_connection()
    cursore = db.cursor()
    if request.method == 'POST':
        id_cliente = request.form['id_cliente']
        id_kart = request.form['id_kart']
        id_turno = request.form['id_turno']
        #Recupero il prezzo del turno per il kart con lo stesso id
        cursore.execute("SELECT CK.PrezzoTurno FROM KART K JOIN CATEGORIA_KART CK ON K.ID_Categoria = CK.ID_Categoria WHERE K.ID_Kart = %s", (id_kart,))
        risultato = cursore.fetchone()
        costo = risultato[0]
        #Inserimento di un nuovo pilota nel turno selezionto
        cursore.execute("INSERT INTO INGRESSO_PISTA (ID_Cliente, ID_Kart, ID_Turno, CostoPagato) VALUES (%s, %s, %s, %s)", (id_cliente, id_kart, id_turno, costo))
        db.commit()
        cursore.close()
        db.close()
        return redirect(url_for('index'))

    #Recupero dei clienti ordinati alfabeticamente per cognome
    cursore.execute("SELECT ID_Cliente, Nome, Cognome FROM CLIENTE ORDER BY Cognome")
    clienti = cursore.fetchall()
    #Recupero dei turni programmati dal più recente al più vecchio
    cursore.execute("SELECT ID_Turno, DataOraInizio, Tipo, DurataMinuti FROM TURNO ORDER BY DataOraInizio DESC")
    turni = cursore.fetchall()
    #Recupero dei kart operativi divisi per categoria
    cursore.execute("SELECT K.ID_Kart, K.NumeroGara, CK.Nome FROM KART K JOIN CATEGORIA_KART CK ON K.ID_Categoria = CK.ID_Categoria WHERE K.Stato = 'Operativo' ORDER BY CK.Nome, K.NumeroGara")
    karts = cursore.fetchall()
    cursore.close()
    db.close()

    return render_template('assegnazione-kart.html', clienti=clienti, turni=turni, karts=karts)


@app.route('/classifiche', methods=['GET'])
def classifiche():
    categoria = request.args.get('categoria', default="")
    id_cliente = request.args.get('id_cliente', default="")
    db = get_connection()
    cursore = db.cursor()
    #Recupero di tutte le categorie di kart per filtrare la classifica
    cursore.execute("SELECT ID_Categoria, Nome FROM CATEGORIA_KART")
    categorie = cursore.fetchall()
    #Recupero dei clienti per visualizzare la classifica per cliente
    cursore.execute("SELECT ID_Cliente, Nome, Cognome FROM CLIENTE ORDER BY Cognome")
    clienti = cursore.fetchall()
    
    #Seleziona i piloti e i rispettivi migliori tempi
    query = "SELECT C.Nome, C.Cognome, MIN(K.NumeroGara), CK.Nome, MIN(IP.MigliorTempo) FROM INGRESSO_PISTA IP JOIN CLIENTE C ON IP.ID_Cliente = C.ID_Cliente JOIN KART K ON IP.ID_Kart = K.ID_Kart JOIN CATEGORIA_KART CK ON K.ID_Categoria = CK.ID_Categoria WHERE IP.MigliorTempo IS NOT NULL"
    parametri = []
    #Condizioni per costruire la query in base ai parametri inseriti dall'utente
    if id_cliente:
        query += " AND C.ID_Cliente = %s"
        parametri.append(id_cliente)
    if categoria:
        query += " AND CK.ID_Categoria = %s"
        parametri.append(categoria)
    #Costruzione della seconda parte della query in base ai parametri inseriti dall'utente
    query += " GROUP BY C.ID_Cliente, CK.ID_Categoria ORDER BY MIN(IP.MigliorTempo) ASC LIMIT 10"
    cursore.execute(query, parametri)
    classifica = cursore.fetchall()
    cursore.close()
    db.close()

    return render_template('classifiche.html', classifica=classifica, categorie=categorie, clienti=clienti, selected_categoria=categoria, selected_cliente=id_cliente)


@app.route('/turni-piloti', methods=['GET'])
def turni_piloti():
    db = get_connection()
    cursore = db.cursor()
    #Recupera i turni programmati dal più recente
    cursore.execute("SELECT ID_Turno, DataOraInizio, Tipo, DurataMinuti, MaxPartecipanti FROM TURNO ORDER BY DataOraInizio DESC")
    tutti_turni = cursore.fetchall()
    lista_turni = []
    for t in tutti_turni:
        #Seleziona dal turno corrente i piloti registrati, i numeri di gara e le categorie dei kart
        cursore.execute("SELECT C.Nome, C.Cognome, K.NumeroGara, CK.Nome FROM INGRESSO_PISTA IP JOIN CLIENTE C ON IP.ID_Cliente = C.ID_Cliente JOIN KART K ON IP.ID_Kart = K.ID_Kart JOIN CATEGORIA_KART CK ON K.ID_Categoria = CK.ID_Categoria WHERE IP.ID_Turno = %s", (t[0],))
        piloti = cursore.fetchall()
        lista_turni.append({'data_ora': t[1], 'tipo': t[2], 'iscritti': piloti})
    cursore.close()
    db.close()
    return render_template('turni-piloti.html', turni=lista_turni)


if __name__ == '__main__':
    app.run(debug=True)