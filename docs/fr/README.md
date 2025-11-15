# My Spotify Playlists Downloader

Exporte les informations de vos playlists Spotify vers des fichiers JSON pour sauvegarde, analyse ou migration.

---

## Description

`my_spotify_playlists_downloader.py` est un script Python en ligne de commande conçu pour vous aider à exporter et
sauvegarder vos playlists Spotify. Il se connecte à votre compte Spotify via OAuth et récupère toutes vos playlists
ainsi que les métadonnées détaillées de chaque piste. Vous pouvez exporter vos playlists sous forme d'un seul fichier
JSON consolidé ou de fichiers JSON individuels par playlist.

Ce script est idéal pour :

- Sauvegarder les données de votre bibliothèque musicale.
- Préparer une migration vers un autre service musical.
- Analyser vos playlists à des fins personnelles ou de recherche.
- Apprendre à intégrer la Web API de Spotify avec Python.

Ce projet est publié sous licence MIT et destiné à un usage éducatif et personnel.

---

## Fonctionnalités

- Exporte **toutes les playlists et métadonnées des pistes**, y compris nom, artistes, album, date de sortie, etc.
- **Exporte les titres aimés** (collection des pistes sauvegardées).
- Option pour **diviser l'export** en fichiers JSON individuels par playlist.
- **Combinaisons flexibles d'export** (titres aimés et/ou playlists).
- **Génération de rapport HTML** avec design moderne et responsive.
- Inclut la **position de la piste dans la playlist**, l'utilisateur qui l'a ajoutée et la date d'ajout.
- **Logging** à la fois dans la console et dans un fichier pour la traçabilité.
- **Portable** – fonctionne sous Windows, macOS et Linux.
- Configuration simple avec des dépendances minimales.

---

## Prérequis

- Python 3.10 ou supérieur
- Un [compte développeur Spotify](SPOTIFY_DEVELOPER_SETUP.md) pour créer une application et obtenir votre Client ID et
  Client Secret

Installez les dépendances avec :

```shell
pip install -r requirements.txt
```

---

## Configuration

1. **Clonez le dépôt**

    ```shell
    git clone https://github.com/yourusername/my_spotify_playlists_downloader.git
    cd my_spotify_playlists_downloader
    ```

2. **Créez votre fichier `.env`**

   Copiez l'exemple fourni:

    ```shell
    cp .env.example .env
    ```

3. **Éditez `.env` et définissez vos variables**

   Obligatoires :

    - `SPOTIFY_CLIENT_ID`
    - `SPOTIFY_CLIENT_SECRET`
    - `SPOTIFY_REDIRECT_URI` (doit correspondre exactement à ce qui est configuré dans votre application Spotify,
      ex. <http://127.0.0.1:8000/callback>)

   Variables optionnelles:

    - `OUTPUT_DIR`: Répertoire où seront enregistrés les fichiers exportés (par défaut : ./playlists)
    - `OUTPUT_PREFIX_SPLIT`: Préfixe pour les fichiers en mode divisé
    - `OUTPUT_PREFIX_SINGLE`: Préfixe pour le fichier unique exporté
    - `LOG_DIR`: Répertoire où seront stockés les logs (par défaut : emplacement du script)
    - `LOG_LEVEL`: Niveau de logging (par défaut : INFO, peut être DEBUG, INFO, WARNING, ERROR, CRITICAL)

### Configuration du compte développeur Spotify

Ce script nécessite un compte développeur Spotify et les identifiants d'une application enregistrée.
Voir [SPOTIFY_DEVELOPER_SETUP.md](SPOTIFY_DEVELOPER_SETUP.md) pour des instructions détaillées.

---

## Utilisation

### Exporter toutes les playlists dans un seul fichier JSON (par défaut)

```shell
python my_spotify_playlists_downloader.py
```

### Exporter chaque playlist en fichier JSON individuel

```shell
python my_spotify_playlists_downloader.py --split
```

### Spécifier un répertoire de sortie personnalisé

```shell
python my_spotify_playlists_downloader.py --output_dir ./my_exports
```

### Exporter uniquement une playlist spécifique par nom

```shell
python my_spotify_playlists_downloader.py --playlist_name "Nom de ma playlist"
```

- Le script exportera uniquement la playlist dont le nom correspond (insensible à la casse, normalisé) à la valeur
  fournie.
- Si aucune playlist ne correspond, une erreur sera enregistrée et aucun fichier ne sera exporté.

### Exporter uniquement les titres aimés (sans playlists)

```shell
python my_spotify_playlists_downloader.py --liked_songs
```

- Exporte votre collection de pistes sauvegardées (titres aimés) dans un fichier JSON dédié.
- Par défaut, le script exporte les playlists. Utilisez ce flag pour exporter uniquement les titres aimés.

### Exporter les playlists et les titres aimés

```shell
python my_spotify_playlists_downloader.py --all_playlists
```

- Exporte à la fois vos playlists et vos titres aimés.
- Équivalent à utiliser `--liked_songs` sans spécifier `--playlist_name`.

### Générer un rapport HTML

```shell
python my_spotify_playlists_downloader.py --html_report
```

- Génère un rapport HTML professionnel et responsive avec le résumé de toute l'exportation.
- Inclut les statistiques, le nombre de playlists/pistes et les chemins des fichiers exportés.
- Le rapport est enregistré dans le répertoire de sortie sous le nom `SpotifyExportReport_YYYYMMDD_HHMMSS.html`.

### Nettoyer le répertoire de sortie avant l'export

```shell
python my_spotify_playlists_downloader.py --clean_output
```

- Tous les fichiers JSON et HTML du répertoire de sortie seront supprimés avant l'export.
- Utile pour éviter de mélanger d'anciennes et de nouvelles exportations.

### Exemples combinés

**Exporter tout avec rapport HTML:**

```shell
python my_spotify_playlists_downloader.py --split --all_playlists --html_report
```

**Nettoyer, exporter uniquement les titres aimés avec rapport:**

```shell
python my_spotify_playlists_downloader.py --liked_songs --html_report --clean_output
```

**Exporter une playlist spécifique en fichier divisé avec nettoyage:**

```shell
python my_spotify_playlists_downloader.py --split --playlist_name "Ma Playlist" --clean_output
```

**Exporter tout en fichiers divisés avec rapport HTML après nettoyage:**

```shell
python my_spotify_playlists_downloader.py --split --all_playlists --html_report --clean_output
```

---

## Notes supplémentaires

- Les noms de playlists utilisés comme noms de fichiers sont assainis: les caractères invalides et les emojis sont
  supprimés, mais les accents et la casse d'origine sont conservés.
- Lors de l'utilisation de `--playlist_name`, le script journalise le filtre normalisé et le nombre de playlists à
  exporter.
- Lors de l'utilisation de `--clean_output`, le script journalise chaque fichier supprimé (JSON et HTML) et confirme le nettoyage du
  répertoire.
- Le comportement par défaut exporte uniquement les playlists. Utilisez `--liked_songs` pour les titres aimés ou `--all_playlists` pour les deux.
- Vous pouvez utiliser `--liked_songs` et `--playlist_name` ensemble pour exporter une playlist spécifique avec vos titres aimés.
- Le rapport HTML (`--html_report`) inclut les chemins des fichiers pour chaque playlist exportée et pour les titres aimés.

---

## Exemple de Sortie

Chaque objet playlist exporté comprend:

- Nom de la playlist, ID, nom affiché et username du propriétaire, description, snapshot_id
- Liste des pistes avec:
  - Position dans la playlist
  - Nom de la piste, artistes, album, date de sortie de l'album
  - URL Spotify
  - Date d'ajout à la playlist et utilisateur l'ayant ajoutée

---

## Avis

Ce script est fourni uniquement à des fins éducatives.
Utilisez-le de manière responsable avec votre propre compte Spotify.
L'auteur n'assume aucune responsabilité en cas de mauvaise utilisation ou de perte de données résultant de son
utilisation.
Le code est propre et exempt de composants malveillants.

## Avis sur la Marque Déposée

Spotify est une marque déposée de Spotify AB.
Ce projet **n'est ni affilié, ni sponsorisé, ni approuvé par Spotify** de quelque manière que ce soit.
Toutes les références à Spotify sont faites uniquement à titre informatif et éducatif.

Les captures d'écran ou images utilisées dans cette documentation sont uniquement à des fins d'illustration pour aider
les utilisateurs à configurer leur compte développeur et n'impliquent aucune association avec Spotify AB.

---

## Licence

Ce projet est sous licence [Licence MIT](../../LICENSE).
