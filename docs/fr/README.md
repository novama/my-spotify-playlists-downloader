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
- Option pour **diviser l'export** en fichiers JSON individuels par playlist.
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

### ESpécifier un répertoire de sortie personnalisé

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

### Nettoyer le répertoire de sortie avant l'export

```shell
python my_spotify_playlists_downloader.py --clean_output
```

- Tous les fichiers JSON du répertoire de sortie seront supprimés avant l'export des nouvelles playlists.
- Utile pour éviter de mélanger d'anciennes et de nouvelles exportations.

### Combiner les options

Vous pouvez combiner ces options selon vos besoins. Par exemple, pour nettoyer le répertoire de sortie et exporter
uniquement une playlist spécifique en fichier individuel:

```shell
python my_spotify_playlists_downloader.py --split --playlist_name "Nom de ma playlist" --clean_output
```

---

## Notes supplémentaires

- Les noms de playlists utilisés comme noms de fichiers sont assainis: les caractères invalides et les emojis sont
  supprimés, mais les accents et la casse d'origine sont conservés.
- Lors de l'utilisation de --playlist_name, le script journalise le filtre normalisé et le nombre de playlists à
  exporter.
- Lors de l'utilisation de --clean_output, le script journalise chaque fichier supprimé et confirme le nettoyage du
  répertoire.

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
