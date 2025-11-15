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
- **Génération de rapport HTML** avec design moderne et responsive affichant statistiques et chemins des fichiers.
- Inclut la **position de la piste dans la playlist**, l'utilisateur qui l'a ajoutée et la date d'ajout.
- **Logging** à la fois dans la console et dans un fichier pour la traçabilité.
- **Portable** – fonctionne sous Windows, macOS et Linux.
- Configuration simple avec des dépendances minimales.

---

## Guide Étape par Étape pour Commencer

Suivez ces étapes pour configurer et utiliser l'outil. Ne vous inquiétez pas si vous n'êtes pas familier avec la programmation – je vais vous guider à travers tout.

### Étape 1: Vérifier l'Installation de Python

Tout d'abord, assurez-vous d'avoir Python installé sur votre ordinateur.

**Vérifier si Python est installé:**

Ouvrez votre terminal (Invite de commandes sur Windows, Terminal sur Mac/Linux) et tapez:

```shell
python --version
```

Vous devriez voir quelque chose comme `Python 3.10.x` ou supérieur. Si vous voyez une erreur ou une version inférieure à 3.10, vous devez installer ou mettre à jour Python:

- **Télécharger Python:** Visitez [python.org/downloads](https://www.python.org/downloads/) et téléchargez Python 3.10 ou plus récent.
- **Pendant l'installation:** Assurez-vous de cocher la case qui dit "Add Python to PATH" (Ajouter Python au PATH).

### Étape 2: Configurer un Compte Développeur Spotify

Pour accéder à vos données Spotify, vous devez créer un compte développeur Spotify et obtenir des identifiants spéciaux (comme des clés pour accéder à votre compte).

**Suivez ce guide détaillé:** [SPOTIFY_DEVELOPER_SETUP.md](SPOTIFY_DEVELOPER_SETUP.md)

Ce guide vous expliquera:

- Créer un compte développeur Spotify (c'est gratuit!)
- Créer une application dans le Tableau de bord Spotify
- Obtenir votre **Client ID** et **Client Secret**
- Configurer la **Redirect URI**

**Important:** Gardez votre Client ID et Client Secret à portée de main – vous en aurez besoin dans les prochaines étapes!

### Étape 3: Télécharger le Script

#### Option A: Télécharger en ZIP (plus facile pour les débutants)

Sur cette page du dépôt GitHub, allez en haut et:

1. Cliquez sur le bouton vert "Code"
2. Sélectionnez "Download ZIP"
3. Extrayez le fichier ZIP dans un dossier sur votre ordinateur (ex. `Documents/spotify-downloader`)

#### Option B: En utilisant Git (si vous avez Git installé)

Ouvrez votre terminal et exécutez:

```shell
git clone https://github.com/novama/my_spotify_playlists_downloader.git
cd my_spotify_playlists_downloader
```

### Étape 4: Installer les Dépendances Nécessaires

Le script a besoin de quelques paquets Python supplémentaires pour fonctionner. Installons-les.

1. **Ouvrez votre terminal** et naviguez vers le dossier où vous avez extrait/cloné le script:

   ```shell
   cd chemin/vers/my_spotify_playlists_downloader
   ```

   Remplacez `chemin/vers/` par l'emplacement réel (ex. `cd Téléchargements/spotify-downloader`).

2. **Installer les dépendances:**

   ```shell
   pip install -r requirements.txt
   ```

   Attendez que l'installation se termine. Vous verrez des messages indiquant que les paquets sont en cours d'installation.

### Étape 5: Configurer vos Identifiants

Maintenant, vous devez indiquer au script vos identifiants Spotify.

1. **Trouvez le fichier `.env.example`** dans le dossier du script.

2. **Faites une copie et renommez-la en `.env`** (sans la partie `.example`):

   - **Windows:** Clic droit sur le fichier → "Copier" → Coller → Renommer en `.env`
   - **Mac/Linux:** Dans le terminal, exécutez: `cp .env.example .env`

3. **Ouvrez le fichier `.env`** avec un éditeur de texte (Bloc-notes sur Windows, TextEdit sur Mac, ou n'importe quel éditeur de code).

4. **Remplissez vos identifiants** de l'Étape 2:

   ```env
   SPOTIFY_CLIENT_ID=votre_client_id_ici
   SPOTIFY_CLIENT_SECRET=votre_client_secret_ici
   SPOTIFY_REDIRECT_URI=http://127.0.0.1:8000/callback
   ```

   Remplacez `votre_client_id_ici` et `votre_client_secret_ici` par les valeurs réelles de votre Tableau de bord Développeur Spotify.

   **Important:** La `SPOTIFY_REDIRECT_URI` doit correspondre exactement à ce que vous avez configuré dans les paramètres de votre application Spotify!

5. **Paramètres optionnels** (vous pouvez les laisser par défaut ou les personnaliser):

   ```env
   OUTPUT_DIR=./output
   LOG_LEVEL=INFO
   ```

6. **Sauvegardez le fichier** et fermez-le.

### Étape 6: Exécutez votre Premier Export

Maintenant, vous êtes prêt à exporter vos playlists. Voici quelques scénarios courants:

#### Export Basique: Toutes les Playlists

Exportez toutes vos playlists dans un seul fichier JSON:

```shell
python my_spotify_playlists_downloader.py
```

**Ce qui se passe:**

- Une fenêtre de navigateur s'ouvrira vous demandant de vous connecter à Spotify (seulement la première fois)
- Après avoir autorisé l'application, vos playlists seront exportées
- Les fichiers seront sauvegardés dans le dossier `output` (ou là où vous l'avez spécifié dans `.env`)

#### Exporter Tout avec un Beau Rapport

Exportez toutes les playlists ET les titres aimés, avec un beau rapport HTML:

```shell
python my_spotify_playlists_downloader.py --all_playlists --liked_songs --html_report
```

**Ce que vous obtenez:**

- Toutes vos playlists exportées sous forme de fichiers JSON
- Vos titres aimés exportés dans un fichier JSON séparé
- Un beau rapport HTML que vous pouvez ouvrir dans votre navigateur avec des statistiques et des emplacements de fichiers

#### Exporter Chaque Playlist comme Fichiers Séparés

Gardez chaque playlist dans son propre fichier:

```shell
python my_spotify_playlists_downloader.py --split
```

#### Exporter Seulement vos Titres Aimés

Exportez seulement vos pistes sauvegardées:

```shell
python my_spotify_playlists_downloader.py --liked_songs
```

#### Exporter une Playlist Spécifique

Exportez seulement une playlist par nom:

```shell
python my_spotify_playlists_downloader.py --playlist_name "Ma Playlist Préférée"
```

Remplacez `"Ma Playlist Préférée"` par le nom réel de votre playlist.

#### Départ Propre (Supprimer les Anciens Exports D'abord)

Supprimez les anciens exports avant d'en créer de nouveaux:

```shell
python my_spotify_playlists_downloader.py --clean_output --all_playlists --html_report
```

#### Le Pack Complet (Recommandé!)

Exportez tout avec toutes les fonctionnalités activées:

```shell
python my_spotify_playlists_downloader.py --split --all_playlists --liked_songs --html_report --clean_output
```

Cela va:

1. Supprimer les anciens fichiers d'export (départ propre)
2. Exporter chaque playlist comme un fichier JSON séparé
3. Exporter vos titres aimés
4. Générer un beau rapport HTML
5. Vous montrer exactement où tout a été sauvegardé

---

## Comprendre les Options

Voici ce que fait chaque option:

| Option | Ce Qu'elle Fait |
|--------|-----------------|
| `--split` | Crée des fichiers JSON séparés pour chaque playlist (au lieu d'un gros fichier) |
| `--liked_songs` | Exporte votre collection de titres aimés/sauvegardés |
| `--all_playlists` | Exporte toutes les playlists (utilisez avec `--liked_songs` pour tout exporter) |
| `--html_report` | Crée un beau rapport HTML avec statistiques et emplacements des fichiers |
| `--clean_output` | Supprime les anciens fichiers JSON et HTML avant d'exporter les nouveaux |
| `--playlist_name "Nom"` | Exporte seulement la playlist avec ce nom spécifique |
| `--output_dir ./dossier` | Sauvegarde les fichiers dans un dossier spécifique |

**Conseil:** Vous pouvez combiner plusieurs options, ajoutez-les simplement les unes après les autres, séparées par des espaces.

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
