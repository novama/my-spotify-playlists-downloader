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
- Export **liked songs** (saved tracks) collection.
- Option to **split output** into individual JSON files for each playlist.
- **Flexible export combinations**: export liked songs and/or specific playlists.
- **HTML report generation** with modern, responsive design showing export statistics and file paths.
- Includes **track position in playlist**, user who added it, and date added.
- **Logging** to both console and a log file for traceability.
- **Portable** – works on Windows, macOS, and Linux.
- Simple setup with minimal dependencies.

---

## Getting Started: Step-by-Step Guide

Follow these steps to set up and use the tool. Don't worry if you're not familiar with programming – I'll guide you through everything.

### Step 1: Check Python Installation

First, make sure you have Python installed on your computer.

**Check if Python is installed:**

Open your terminal (Command Prompt on Windows, Terminal on Mac/Linux) and type:

```shell
python --version
```

You should see something like `Python 3.10.x` or higher. If you see an error or a version lower than 3.10, you need to install or update Python:

- **Download Python:** Visit [python.org/downloads](https://www.python.org/downloads/) and download Python 3.10 or newer.
- **During installation:** Make sure to check the box that says "Add Python to PATH".

### Step 2: Set Up a Spotify Developer Account

To access your Spotify data, you need to create a Spotify Developer account and get special credentials (like keys to access your account).

**Follow this detailed guide:** [SPOTIFY_DEVELOPER_SETUP.md](SPOTIFY_DEVELOPER_SETUP.md)

This guide will walk you through:

- Creating a Spotify Developer account (it's free!)
- Creating an app in the Spotify Dashboard
- Getting your **Client ID** and **Client Secret**
- Setting up the **Redirect URI**

**Important:** Keep your Client ID and Client Secret handy – you'll need them in the next steps!

### Step 3: Download the Script

#### Option A: Download as ZIP (easiest for beginners)

In this GitHub repository page, go to the top and:

1. Click the green "Code" button
2. Select "Download ZIP"
3. Extract the ZIP file to a folder on your computer (e.g., `Documents/spotify-downloader`)

#### Option B: Using Git (if you have Git installed)

Open your terminal and run:

```shell
git clone https://github.com/novama/my_spotify_playlists_downloader.git
cd my_spotify_playlists_downloader
```

### Step 4: Install Required Dependencies

The script needs some additional Python packages to work. Let's install them.

1. **Open your terminal** and navigate to the folder where you extracted/cloned the script:

   ```shell
   cd path/to/my_spotify_playlists_downloader
   ```

   Replace `path/to/` with the actual location (e.g., `cd Downloads/spotify-downloader`).

2. **Install dependencies:**

   ```shell
   pip install -r requirements.txt
   ```

   Wait for the installation to complete. You should see messages indicating that packages are being installed.

### Step 5: Configure Your Credentials

Now you need to tell the script your Spotify credentials.

1. **Find the `.env.example` file** in the script folder.

2. **Make a copy and rename it to `.env`** (without the `.example` part):

   - **Windows:** Right-click the file → "Copy" → Paste → Rename to `.env`
   - **Mac/Linux:** In terminal, run: `cp .env.example .env`

3. **Open the `.env` file** with a text editor (Notepad on Windows, TextEdit on Mac, or any code editor).

4. **Fill in your credentials** from Step 2:

   ```env
   SPOTIFY_CLIENT_ID=your_client_id_here
   SPOTIFY_CLIENT_SECRET=your_client_secret_here
   SPOTIFY_REDIRECT_URI=http://127.0.0.1:8000/callback
   ```

   Replace `your_client_id_here` and `your_client_secret_here` with the actual values from your Spotify Developer Dashboard.

   **Important:** The `SPOTIFY_REDIRECT_URI` must match exactly what you set in your Spotify app settings!

5. **Optional settings** (you can leave these as default or customize them):

   ```env
   OUTPUT_DIR=./output
   LOG_LEVEL=INFO
   ```

6. **Save the file** and close it.

### Step 6: Run Your First Export

Now, you're ready to export your playlists. Here are some common scenarios:

#### Basic Export: All Playlists

Export all your playlists to a single JSON file:

```shell
python my_spotify_playlists_downloader.py
```

**What happens:**

- A browser window will open asking you to log in to Spotify (first time only)
- After you authorize the app, your playlists will be exported
- Files will be saved in the `output` folder (or wherever you specified in `.env`)

#### Export Everything with a Nice Report

Export all playlists AND liked songs, with a beautiful HTML report:

```shell
python my_spotify_playlists_downloader.py --all_playlists --liked_songs --html_report
```

**What you get:**

- All your playlists exported as JSON files
- Your liked songs exported as a separate JSON file
- A pretty HTML report you can open in your browser with statistics and file locations

#### Export Each Playlist as Separate Files

Keep each playlist in its own file:

```shell
python my_spotify_playlists_downloader.py --split
```

#### Export Just Your Liked Songs

Only export your saved tracks:

```shell
python my_spotify_playlists_downloader.py --liked_songs
```

#### Export a Specific Playlist

Only export one playlist by name:

```shell
python my_spotify_playlists_downloader.py --playlist_name "My Favorite Playlist"
```

Replace `"My Favorite Playlist"` with the actual name of your playlist.

#### Clean Start (Delete Old Exports First)

Delete old exports before creating new ones:

```shell
python my_spotify_playlists_downloader.py --clean_output --all_playlists --html_report
```

#### The Complete Package (Recommended!)

Export everything with all features enabled:

```shell
python my_spotify_playlists_downloader.py --split --all_playlists --liked_songs --html_report --clean_output
```

This will:

1. Delete old export files (clean start)
2. Export each playlist as a separate JSON file
3. Export your liked songs
4. Generate a beautiful HTML report
5. Show you exactly where everything was saved

---

## Understanding the Options

Here's what each option does:

| Option | What It Does |
|--------|-------------|
| `--split` | Creates separate JSON files for each playlist (instead of one big file) |
| `--liked_songs` | Exports your liked/saved songs collection |
| `--all_playlists` | Exports all playlists (use with `--liked_songs` to export everything) |
| `--html_report` | Creates a beautiful HTML report with statistics and file locations |
| `--clean_output` | Deletes old JSON and HTML files before exporting new ones |
| `--playlist_name "Name"` | Only exports the playlist with this specific name |
| `--output_dir ./folder` | Saves files to a specific folder |

**Tip:** You can combine multiple options, just add them one after another, separated by spaces.

---

## Additional Notes

- Playlist names used for filenames are sanitized: invalid filename characters and emoji are removed, but accents and
  original case are preserved.
- When using `--playlist_name`, the script logs the normalized filter and the number of playlists to be exported.
- When using `--clean_output`, the script logs each deleted JSON and HTML file and confirms the cleaning action.
- When using `--liked_songs` alone (without `--playlist_name` or `--all_playlists`), only liked songs will be exported.
- The HTML report provides a professional overview of your export with modern styling, responsive design, and direct file paths for easy access to exported files.
- All export combinations are flexible: you can export liked songs, specific playlists, all playlists, or any combination thereof.

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
