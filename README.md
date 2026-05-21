# Progetto Basi di Dati: Kartodromo Punto di Corda

### Gabriel Tavcar - SM3201659

[PDF Del Progetto](progetto_sm3201659.pdf)

![Demo dell'applicazione](demo.gif)

L'applicazione permette di gestire le operazioni quotidiane del kartodromo **Punto di Corda**. Le funzionalità principali includono:

* **Registrazione Nuovo Cliente:** Inserimento dati anagrafici (nome, cognome, data di nascita, email).
* **Assegnazione Turno e Kart:** Gestione delle assegnazioni piloti ai turni e ai kart disponibili.
* **Monitoraggio Pista:** Visualizzazione dei turni programmati e dei piloti iscritti.
* **Classifiche:** Visualizzazione dei 10 migliori tempi assoluti, con possibilità di filtrare i tempi per pilota e categoria.

### Stack Tecnologico e Sicurezza

* **Frontend:** HTML5, CSS.
* **Backend:** Python con framework Flask.
* **Database:** MySQL (gestito tramite XAMPP con server Apache).
* **Sicurezza:** Tutte le operazioni di scrittura nel database (INSERT) e di ricerca (SELECT) utilizzano il parametro %s, proteggendo dalle SQL Injection.


Nota: Tutti i dati mostrati all'interno dell'applicazione (nomi, tempi, ecc.) sono stati generati casualmente e sono inseriti a scopo dimostrativo.