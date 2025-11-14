# My Spotify Playlists Downloader

Exports your Spotify playlists information to JSON files for backup, analysis, or migration purposes.

---

## Description

`my_spotify_playlists_downloader.py` is a command-line Python script designed to help you export and back up your
Spotify playlists. It connects to your Spotify account via OAuth and retrieves all your playlists along with detailed
metadata for each track. You can export your playlists either as a single consolidated JSON file or as individual JSON
files per playlist.

This script is ideal for:

- Backing up your music library data.
- Preparing for migration to another music service.
- Analyzing your playlists for personal or research purposes.
- Learning about integration with Spotify’s Web API using Python.

The project is released under the MIT License and intended for educational and personal use.

---

## Features

- Exports **all playlists and track metadata** including name, artists, album, release date, and more.
- Option to **split output** into individual JSON files for each playlist.
- Includes **track position in playlist**, user who added it, and date added.
- **Logging** to both console and a log file for traceability.
- **Portable** – works on Windows, macOS, and Linux.
- Simple setup with minimal dependencies.

---

## Requirements

- Python 3.10 or higher
- A [Spotify Developer account](SPOTIFY_DEVELOPER_SETUP.md) to create an app and obtain your Client ID and Client
  Secret

Install dependencies with:

```shell
pip install -r requirements.txt
```

---

## Setup

1. **Clone the repository**

    ```shell
    git clone https://github.com/yourusername/my_spotify_playlists_downloader.git
    cd my_spotify_playlists_downloader
    ```

2. **Create your `.env` file**

   Copy the provided example:

    ```shell
    cp .env.example .env
    ```

3. **Edit `.env` and set your variables**

   **Required:**

    - `SPOTIFY_CLIENT_ID`
    - `SPOTIFY_CLIENT_SECRET`
    - `SPOTIFY_REDIRECT_URI` (must match exactly with what is set in your Spotify app settings,
      e.g. <http://127.0.0.1:8000/callback>)

   **Optional:**

    - `OUTPUT_DIR`: Directory where outputs will be saved (default: ./playlists)
    - `OUTPUT_PREFIX_SPLIT`: Prefix for output files in split mode
    - `OUTPUT_PREFIX_SINGLE`: Prefix for single output file
    - `LOG_DIR`: Directory where logs will be stored (default: script location)
    - `LOG_LEVEL`: Logging level (default: INFO, can be DEBUG, INFO, WARNING, ERROR, CRITICAL)

### Spotify Developer account setup

This script requires a Spotify Developer account and registered app credentials.
See [SPOTIFY_DEVELOPER_SETUP.md](SPOTIFY_DEVELOPER_SETUP.md) for detailed instructions.

---

## Usage

### Export all playlists to a single JSON file (default)

```shell
python my_spotify_playlists_downloader.py
```

### Export each playlist as an individual JSON file

```shell
python my_spotify_playlists_downloader.py --split
```

### Specify a custom output directory

```shell
python my_spotify_playlists_downloader.py --output_dir ./my_exports
```

### Export only a specific playlist by name

```shell
python my_spotify_playlists_downloader.py --playlist_name "My Favorite Playlist"
```

- The script will export only the playlist whose name matches (case-insensitive, normalized) the value provided.
- If no playlist matches, an error will be logged and no file will be exported.

### Clean output directory before exporting

```shell
python my_spotify_playlists_downloader.py --clean_output
```

- All JSON files in the output directory will be deleted before exporting new playlists.
- Useful to avoid mixing old and new exports.

### Combine options

You can combine these options as needed. For example, to clean the output directory and export only a specific playlist
as a split file:

```shell
python my_spotify_playlists_downloader.py --split --playlist_name "My Favorite Playlist" --clean_output
```

---

## Additional Notes

- Playlist names used for filenames are sanitized: invalid filename characters and emoji are removed, but accents and
  original case are preserved.
- When using --playlist_name, the script logs the normalized filter and the number of playlists to be exported.
- When using --clean_output, the script logs each deleted file and confirms the cleaning action.

---

## Output Example

Each exported playlist object includes:

- Playlist name, ID, owner display name and username, description, snapshot_id
- Tracks list with:
  - Position in playlist
  - Track name, artists, album, album release date
  - Spotify URL
  - Date added to playlist and user who added it

---

## Disclaimer

This script is provided for educational purposes only.  
Use it responsibly with your own Spotify account.  
The author assumes no liability for misuse or for any data loss caused by its usage.  
The code is clean and free of malicious components.

## Trademark disclaimer

Spotify is a registered trademark of Spotify AB.  
This project is **not affiliated with, sponsored, or endorsed by Spotify** in any way.  
All references to Spotify are made solely for informational and educational purposes.

Any screenshots or images used in this documentation are for illustrative purposes only to assist users in setting up
their Developer account and do not imply any association with Spotify AB.

---

## License

This project is licensed under the [MIT License](../../LICENSE).
