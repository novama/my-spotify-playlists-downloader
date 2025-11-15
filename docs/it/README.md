# My Spotify Playlists Downloader

Esporta le informazioni delle tue playlist Spotify in file JSON per backup, analisi o migrazione.

---

## Descrizione

`my_spotify_playlists_downloader.py` è uno script Python da riga di comando progettato per aiutarti a esportare e fare
il backup delle tue playlist Spotify. Si connette al tuo account Spotify tramite OAuth e recupera tutte le tue playlist
insieme ai metadati dettagliati di ciascun brano. Puoi esportare le playlist come un singolo file JSON consolidato o
come file JSON individuali per ogni playlist.

Questo script è ideale per:

- Eseguire il backup dei dati della tua libreria musicale.
- Prepararti a migrare verso un altro servizio di musica.
- Analizzare le tue playlist per scopi personali o di ricerca.
- Imparare come integrare la Web API di Spotify usando Python.

Il progetto è rilasciato sotto licenza MIT ed è destinato a un uso educativo e personale.

---

## Funzionalità

- Esporta **tutte le playlist e i metadati dei brani**, inclusi nome, artisti, album, data di rilascio e altro.
- **Esporta i brani preferiti** (collezione dei brani salvati).
- Opzione per **dividere l'output** in file JSON individuali per ogni playlist.
- **Combinazioni flessibili di esportazione** (brani preferiti e/o playlist).
- **Generazione di report HTML** con design moderno e responsive che mostra statistiche e percorsi dei file.
- Include **la posizione del brano nella playlist**, l'utente che lo ha aggiunto e la data di aggiunta.
- **Logging** sia su console che su file per la tracciabilità.
- **Portabile** – funziona su Windows, macOS e Linux.
- Configurazione semplice con dipendenze minime.

---

## Guida Passo-Passo per Iniziare

Segui questi passaggi per configurare e utilizzare lo strumento. Non preoccuparti se non hai familiarità con la programmazione – ti guiderò in tutto.

### Passo 1: Verifica l'Installazione di Python

Per prima cosa, assicurati di avere Python installato sul tuo computer.

**Verifica se Python è installato:**

Apri il tuo terminale (Prompt dei comandi su Windows, Terminale su Mac/Linux) e digita:

```shell
python --version
```

Dovresti vedere qualcosa come `Python 3.10.x` o superiore. Se vedi un errore o una versione inferiore a 3.10, devi installare o aggiornare Python:

- **Scarica Python:** Visita [python.org/downloads](https://www.python.org/downloads/) e scarica Python 3.10 o più recente.
- **Durante l'installazione:** Assicurati di selezionare la casella che dice "Add Python to PATH" (Aggiungi Python al PATH).

### Passo 2: Configurare un Account Sviluppatore Spotify

Per accedere ai tuoi dati Spotify, devi creare un account sviluppatore Spotify e ottenere credenziali speciali (come chiavi per accedere al tuo account).

**Segui questa guida dettagliata:** [SPOTIFY_DEVELOPER_SETUP.md](SPOTIFY_DEVELOPER_SETUP.md)

Questa guida ti spiegherà:

- Creare un account sviluppatore Spotify (è gratuito!)
- Creare un'app nel Dashboard di Spotify
- Ottenere il tuo **Client ID** e **Client Secret**
- Configurare la **Redirect URI**

**Importante:** Tieni a portata di mano il tuo Client ID e Client Secret – ne avrai bisogno nei prossimi passaggi!

### Passo 3: Scaricare lo Script

#### Opzione A: Scarica come ZIP (più facile per i principianti)

In questa pagina del repository GitHub, vai in alto e:

1. Clicca sul pulsante verde "Code"
2. Seleziona "Download ZIP"
3. Estrai il file ZIP in una cartella sul tuo computer (es. `Documenti/spotify-downloader`)

#### Opzione B: Usando Git (se hai Git installato)

Apri il tuo terminale ed esegui:

```shell
git clone https://github.com/novama/my_spotify_playlists_downloader.git
cd my_spotify_playlists_downloader
```

### Passo 4: Installare le Dipendenze Necessarie

Lo script ha bisogno di alcuni pacchetti Python aggiuntivi per funzionare. Installiamoli.

1. **Apri il tuo terminale** e naviga nella cartella dove hai estratto/clonato lo script:

   ```shell
   cd percorso/a/my_spotify_playlists_downloader
   ```

   Sostituisci `percorso/a/` con la posizione effettiva (es. `cd Download/spotify-downloader`).

2. **Installa le dipendenze:**

   ```shell
   pip install -r requirements.txt
   ```

   Attendi il completamento dell'installazione. Vedrai messaggi che indicano che i pacchetti sono in fase di installazione.

### Passo 5: Configurare le tue Credenziali

Ora devi dire allo script le tue credenziali Spotify.

1. **Trova il file `.env.example`** nella cartella dello script.

2. **Fai una copia e rinominala in `.env`** (senza la parte `.example`):

   - **Windows:** Click destro sul file → "Copia" → Incolla → Rinomina in `.env`
   - **Mac/Linux:** Nel terminale, esegui: `cp .env.example .env`

3. **Apri il file `.env`** con un editor di testo (Blocco note su Windows, TextEdit su Mac, o qualsiasi editor di codice).

4. **Compila le tue credenziali** dal Passo 2:

   ```env
   SPOTIFY_CLIENT_ID=tuo_client_id_qui
   SPOTIFY_CLIENT_SECRET=tuo_client_secret_qui
   SPOTIFY_REDIRECT_URI=http://127.0.0.1:8000/callback
   ```

   Sostituisci `tuo_client_id_qui` e `tuo_client_secret_qui` con i valori effettivi dal tuo Dashboard Sviluppatore Spotify.

   **Importante:** La `SPOTIFY_REDIRECT_URI` deve corrispondere esattamente a quello che hai impostato nelle impostazioni della tua app Spotify!

5. **Impostazioni opzionali** (puoi lasciarle predefinite o personalizzarle):

   ```env
   OUTPUT_DIR=./output
   LOG_LEVEL=INFO
   ```

6. **Salva il file** e chiudilo.

### Passo 6: Esegui la tua Prima Esportazione

Ora sei pronto per esportare le tue playlist. Ecco alcuni scenari comuni:

#### Esportazione Base: Tutte le Playlist

Esporta tutte le tue playlist in un singolo file JSON:

```shell
python my_spotify_playlists_downloader.py
```

**Cosa succede:**

- Si aprirà una finestra del browser che ti chiede di accedere a Spotify (solo la prima volta)
- Dopo aver autorizzato l'app, le tue playlist verranno esportate
- I file verranno salvati nella cartella `output` (o dove hai specificato in `.env`)

#### Esporta Tutto con un Bel Report

Esporta tutte le playlist E i brani preferiti, con un bellissimo report HTML:

```shell
python my_spotify_playlists_downloader.py --all_playlists --liked_songs --html_report
```

**Cosa ottieni:**

- Tutte le tue playlist esportate come file JSON
- I tuoi brani preferiti esportati in un file JSON separato
- Un bel report HTML che puoi aprire nel tuo browser con statistiche e posizioni dei file

#### Esporta Ogni Playlist come File Separati

Mantieni ogni playlist nel suo file:

```shell
python my_spotify_playlists_downloader.py --split
```

#### Esporta Solo i tuoi Brani Preferiti

Esporta solo i tuoi brani salvati:

```shell
python my_spotify_playlists_downloader.py --liked_songs
```

#### Esporta una Playlist Specifica

Esporta solo una playlist per nome:

```shell
python my_spotify_playlists_downloader.py --playlist_name "Mia Playlist Preferita"
```

Sostituisci `"Mia Playlist Preferita"` con il nome effettivo della tua playlist.

#### Inizio Pulito (Elimina Prima le Vecchie Esportazioni)

Elimina le vecchie esportazioni prima di crearne di nuove:

```shell
python my_spotify_playlists_downloader.py --clean_output --all_playlists --html_report
```

#### Il Pacchetto Completo (Consigliato!)

Esporta tutto con tutte le funzionalità abilitate:

```shell
python my_spotify_playlists_downloader.py --split --all_playlists --liked_songs --html_report --clean_output
```

Questo farà:

1. Eliminare i vecchi file di esportazione (inizio pulito)
2. Esportare ogni playlist come un file JSON separato
3. Esportare i tuoi brani preferiti
4. Generare un bellissimo report HTML
5. Mostrarti esattamente dove è stato salvato tutto

---

## Comprendere le Opzioni

Ecco cosa fa ogni opzione:

| Opzione | Cosa Fa |
|--------|----------|
| `--split` | Crea file JSON separati per ogni playlist (invece di un file grande) |
| `--liked_songs` | Esporta la tua collezione di brani preferiti/salvati |
| `--all_playlists` | Esporta tutte le playlist (usalo con `--liked_songs` per esportare tutto) |
| `--html_report` | Crea un bellissimo report HTML con statistiche e posizioni dei file |
| `--clean_output` | Elimina i vecchi file JSON e HTML prima di esportare quelli nuovi |
| `--playlist_name "Nome"` | Esporta solo la playlist con questo nome specifico |
| `--output_dir ./cartella` | Salva i file in una cartella specifica |

**Suggerimento:** Puoi combinare più opzioni, aggiungile semplicemente una dopo l'altra, separate da spazi.

---

## Note aggiuntive

- I nomi delle playlist usati come nomi file vengono sanificati: caratteri non validi ed emoji vengono rimossi, ma si
  mantengono accenti e maiuscole/minuscole originali.
- Usando `--playlist_name`, lo script registra il filtro normalizzato e il numero di playlist da esportare.
- Usando `--clean_output`, lo script registra ogni file eliminato (JSON e HTML) e conferma la pulizia della cartella.
- Il comportamento predefinito esporta solo le playlist. Usa `--liked_songs` per i brani preferiti o `--all_playlists` per entrambi.
- Puoi usare `--liked_songs` e `--playlist_name` insieme per esportare una playlist specifica insieme ai tuoi brani preferiti.
- Il report HTML (`--html_report`) include i percorsi dei file per ogni playlist esportata e per i brani preferiti.

---

## Esempio di Output

Ogni oggetto playlist esportato include:

- Nome playlist, ID, display name e username del proprietario, descrizione, snapshot_id
- Lista dei brani con:
  - Posizione nella playlist
  - Nome brano, artisti, album, data di rilascio dell'album
  - URL Spotify
  - Data di aggiunta alla playlist e utente che lo ha aggiunto

---

## Avviso

Questo script è fornito esclusivamente a scopo educativo.
Usalo responsabilmente con il tuo account Spotify.
L'autore non si assume alcuna responsabilità per un uso improprio o per eventuali perdite di dati causate dall'utilizzo.
Il codice è pulito e privo di componenti dannosi.

## Avviso sul Marchio Registrato

Spotify è un marchio registrato di Spotify AB.
Questo progetto **non è affiliato, sponsorizzato o approvato da Spotify** in alcun modo.
Tutti i riferimenti a Spotify sono effettuati esclusivamente a scopo informativo ed educativo.

Eventuali screenshot o immagini utilizzate in questa documentazione hanno solo scopo illustrativo per aiutare gli utenti
a configurare il proprio account sviluppatore e non implicano alcuna associazione con Spotify AB.

---

## Licenza

Questo progetto è rilasciato sotto [Licenza MIT](../../LICENSE).
