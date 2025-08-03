#!/usr/bin/env python3
# -----------------------------------------------------------------------------
# my_spotify_playlists_downloader.py
#
# Exports your Spotify playlists and Liked Songs to JSON files.
#
# License: MIT
# Date: 2025-07-01
#
# This script is provided for educational purposes.
# It is free to use and modify under the MIT License.
# The author provides no warranty and is not responsible for any use or misuse.
# The code is clean and contains no malicious components.
#
# Trademark disclaimer
#
# Spotify is a registered trademark of Spotify AB.
# This project is **not affiliated with, sponsored, or endorsed by Spotify** in any way.
# All references to Spotify are made solely for informational and educational purposes.
# -----------------------------------------------------------------------------

"""
my_spotify_playlists_downloader.py

Usage:
    python my_spotify_playlists_downloader.py [--split] [--output_dir /path/to/dir] [--playlist_name NAME]

Options:
    --split           Export each playlist as an individual JSON file named after the playlist (sanitized).
    --output_dir DIR  Override the output directory path defined in .env or default.
    --playlist_name NAME  Export only the playlist or Liked Songs with this name (case-insensitive, normalized).
    --clean_output    Delete all JSON files in the output directory before exporting.
"""

import argparse
import json
import logging
import os
import re
import sys
import time
from pathlib import Path

import spotipy
import unicodedata
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

# Ensure minimum Python version for compatibility
if sys.version_info < (3, 10):
    print("This script requires Python 3.10 or higher.")
    sys.exit(1)


def load_env():
    """
    Load and validate required and optional environment variables from .env file.

    Returns:
        dict: Dictionary containing configuration variables.
    Raises:
        ValueError: If any required variable is missing or empty.
    """
    load_dotenv()
    required_vars = ["SPOTIFY_CLIENT_ID", "SPOTIFY_CLIENT_SECRET", "SPOTIFY_REDIRECT_URI"]
    config = {}

    for var in required_vars:
        val = os.getenv(var)
        if not val or not val.strip():
            raise ValueError(f"Missing required environment variable: {var}")
        config[var] = val.strip()

    # Optional variables
    config["OUTPUT_DIR"] = os.getenv("OUTPUT_DIR", "").strip()
    config["OUTPUT_PREFIX_SPLIT"] = os.getenv("OUTPUT_PREFIX_SPLIT", "").strip()
    config["OUTPUT_PREFIX_SINGLE"] = os.getenv("OUTPUT_PREFIX_SINGLE", "").strip()
    config["LOG_DIR"] = os.getenv("LOG_DIR", "").strip()
    config["LOG_LEVEL"] = os.getenv("LOG_LEVEL", "INFO").strip().upper() or "INFO"

    return config


def setup_logging(log_dir: Path, log_level: str):
    """
    Configure logging to output to console and to a log file in the specified directory.

    Args:
        log_dir (Path): Directory where the log file will be saved.
        log_level (str): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).

    Returns:
        Logger: Configured logger instance.
    """
    log_dir.mkdir(parents=True, exist_ok=True)
    logfile_path = log_dir / "my_spotify_playlists_downloader.log"

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(logfile_path, encoding='utf-8')
        ]
    )
    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized. Log file: {logfile_path}")
    return logger


def sanitize_filename(name: str) -> str:
    """
    Sanitize a string to create a safe filename by replacing invalid characters.

    Args:
        name (str): Original string.

    Returns:
        str: Sanitized string safe for filenames.
    """
    return re.sub(r'[\\/*?:"<>|]', "_", name)


def normalize_playlist_name(name: str) -> str:
    """
    Normalize a playlist name for comparison: strip, lowercase, remove extra spaces.

    Args:
        name (str): Playlist name to normalize.
    Returns:
        str: Normalized name for matching.
    """
    if not name:
        return ''
    return ' '.join(name.strip().lower().split())


def sanitize_playlist_name(name: str) -> str:
    """
    Sanitize a playlist name to be safe for filenames, removing invalid/emoji characters,
    but keeping accents, original case, and trimming spaces.

    Args:
        name (str): Original playlist name.
    Returns:
        str: Sanitized playlist name.
    """
    def is_valid_char(c):
        cat = unicodedata.category(c)
        # Exclude emoji (So, Sk, Cs, Co, Cn), but keep accents and printable letters/numbers
        return not (cat.startswith('C') or cat.startswith('S'))

    name = ''.join(c for c in name if is_valid_char(c))
    # Remove invalid filename chars (but keep accents)
    name = re.sub(r'[\\/*?:"<>|]', '', name)
    return name.strip()


def get_all_playlists(sp: spotipy.Spotify, logger) -> list:
    """
    Retrieve all playlists from the current user's Spotify account.

    Args:
        sp (spotipy.Spotify): Authenticated Spotify client.
        logger (Logger): Logger instance for logging.

    Returns:
        list: List of playlist objects.
    """
    playlists = []
    results = sp.current_user_playlists()
    while results:
        playlists.extend(results['items'])
        results = sp.next(results) if results['next'] else None
    logger.info(f"Retrieved {len(playlists)} playlists from account.")
    return playlists


def get_playlist_tracks(sp: spotipy.Spotify, playlist_id: str, logger) -> list:
    """
    Retrieve all tracks from a specific playlist by ID.

    Args:
        sp (spotipy.Spotify): Authenticated Spotify client.
        playlist_id (str): Spotify playlist ID.
        logger (Logger): Logger instance for logging.

    Returns:
        list: List of track dictionaries with selected metadata.
    """
    tracks = []
    track_index = 0
    tracks_data = sp.playlist_items(playlist_id)

    while tracks_data:
        for item in tracks_data['items']:
            track = item['track']
            if track:
                tracks.append({
                    'position': track_index,
                    'name': track['name'],
                    'artist': ', '.join([artist['name'] for artist in track['artists']]),
                    'album': track['album']['name'],
                    'album_release_date': track['album']['release_date'],
                    'spotify_url': track['external_urls']['spotify'],
                    'added_at': item['added_at'],
                    'added_by': item['added_by']['id'] if item['added_by'] else None,
                })
                track_index += 1

        tracks_data = sp.next(tracks_data) if tracks_data['next'] else None

    logger.debug(f"Retrieved {len(tracks)} tracks for playlist ID {playlist_id}.")
    return tracks


def get_liked_songs(sp: spotipy.Spotify, logger) -> list:
    """
    Retrieve all liked songs from the current user's Spotify account.

    Args:
        sp (spotipy.Spotify): Authenticated Spotify client.
        logger (Logger): Logger instance for logging.

    Returns:
        list: List of track dictionaries with selected metadata.
    """
    tracks = []
    track_index = 0
    results = sp.current_user_saved_tracks()

    while results:
        for item in results['items']:
            track = item['track']
            if track:
                tracks.append({
                    'position': track_index,
                    'name': track['name'],
                    'artist': ', '.join([artist['name'] for artist in track['artists']]),
                    'album': track['album']['name'],
                    'album_release_date': track['album']['release_date'],
                    'spotify_url': track['external_urls']['spotify'],
                    'added_at': item['added_at'],
                    'added_by': None,  # Liked Songs doesn't provide added_by info
                })
                track_index += 1

        results = sp.next(results) if results['next'] else None

    logger.debug(f"Retrieved {len(tracks)} liked songs.")
    return tracks


def export_playlists(sp: spotipy.Spotify, split: bool, output_dir: Path,
                     output_prefix_split: str, output_prefix_single: str, playlist_name_filter: str, logger):
    """
    Export all playlists and/or Liked Songs to JSON files, either as individual files or a single combined file.
    Optionally filter by normalized playlist name or 'Liked Songs'.

    Args:
        sp (spotipy.Spotify): Authenticated Spotify client.
        split (bool): Whether to export each playlist as a separate file.
        output_dir (Path): Directory to save output files.
        output_prefix_split (str): Prefix for split output filenames.
        output_prefix_single (str): Prefix for single output filename.
        playlist_name_filter (str): Normalized playlist name or 'Liked Songs' to filter.
        logger (Logger): Logger instance for logging.

    Returns:
        tuple: (total_playlists_exported (int), total_tracks_exported (int))
    """
    export = []
    total_tracks = 0
    total_playlists = 0

    output_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Output directory set to: {output_dir}")

    # Normalize filter if provided
    normalized_filter = normalize_playlist_name(playlist_name_filter) if playlist_name_filter else None
    if normalized_filter:
        logger.info(f"Running with playlist_name filter: '{playlist_name_filter}' (normalized: '{normalized_filter}')")

    # Handle Liked Songs if filter matches or no filter is provided
    liked_songs_exported = False
    if not normalized_filter or normalized_filter == normalize_playlist_name("Liked Songs"):
        logger.info("Exporting Liked Songs")
        tracks = get_liked_songs(sp, logger)
        total_tracks += len(tracks)
        liked_songs_obj = {
            'playlist_name': 'Liked Songs',
            'playlist_id': 'liked_songs',
            'owner_id': sp.current_user()['id'],
            'owner': sp.current_user()['display_name'] or 'Unknown',
            'description': 'User\'s Liked Songs collection',
            'snapshot_id': '',
            'tracks': tracks
        }

        if split:
            export_filename = f"{output_prefix_split}{sanitize_playlist_name('Liked Songs')}.json"
            filepath = output_dir / export_filename
            filepath.write_text(json.dumps([liked_songs_obj], ensure_ascii=False, indent=4), encoding='utf-8')
            logger.info(f"Saved Liked Songs to {filepath}")
        else:
            export.append(liked_songs_obj)
        total_playlists += 1
        liked_songs_exported = True

    # Handle playlists
    playlists = get_all_playlists(sp, logger)
    filtered_playlists = []
    for playlist in playlists:
        normalized_name = normalize_playlist_name(playlist['name'])
        if normalized_filter:
            if normalized_name == normalized_filter:
                filtered_playlists.append(playlist)
        else:
            filtered_playlists.append(playlist)

    if normalized_filter and not filtered_playlists and not liked_songs_exported:
        logger.error(f"No playlist or Liked Songs matched the name: '{playlist_name_filter}' (normalized: '{normalized_filter}')")
        return 0, 0

    for playlist in filtered_playlists:
        playlist_name = playlist['name']
        owner_name = playlist['owner']['display_name']
        owner_id = playlist['owner']['id']
        logger.info(f"Exporting playlist: '{playlist_name}' (Owner: {owner_name} [{owner_id}])")

        tracks = get_playlist_tracks(sp, playlist['id'], logger)
        total_tracks += len(tracks)

        playlist_obj = {
            'playlist_name': playlist_name,
            'playlist_id': playlist['id'],
            'owner_id': owner_id,
            'owner': owner_name,
            'description': playlist.get('description', ''),
            'snapshot_id': playlist.get('snapshot_id', ''),
            'tracks': tracks
        }

        if split:
            export_filename = f"{output_prefix_split}{sanitize_playlist_name(playlist_name)}.json"
            filepath = output_dir / export_filename
            filepath.write_text(json.dumps([playlist_obj], ensure_ascii=False, indent=4), encoding='utf-8')
            logger.info(f"Saved playlist to {filepath}")
        else:
            export.append(playlist_obj)
        total_playlists += 1

    if not split and (filtered_playlists or liked_songs_exported):
        if normalized_filter:
            export_filename = f"{output_prefix_single}filtered_spotify_playlists.json"
        else:
            export_filename = f"{output_prefix_single}spotify_playlists.json"
        filepath = output_dir / export_filename
        filepath.write_text(json.dumps(export, ensure_ascii=False, indent=4), encoding='utf-8')
        logger.info(f"Export completed. File saved as {filepath}")

    return total_playlists, total_tracks


def main():
    """
    Entry point for script execution. Parses arguments, loads configuration,
    initializes logging and Spotify client, and runs export process.
    """
    start_time = time.time()

    config = load_env()

    parser = argparse.ArgumentParser(description="Download Spotify playlists and Liked Songs to JSON")
    parser.add_argument('--split', action='store_true',
                        help='Export each playlist as an individual JSON file')
    parser.add_argument('--output_dir', type=str, default=None,
                        help='Override the output directory path defined in .env or default.')
    parser.add_argument('--playlist_name', type=str, default=None,
                        help='Export only the playlist or Liked Songs with this name (case-insensitive, normalized).')
    parser.add_argument('--clean_output', action='store_true',
                        help='Delete all JSON files in the output directory before exporting playlists.')
    args = parser.parse_args()

    # Determine log directory and logging
    log_dir = Path(config["LOG_DIR"]).expanduser().resolve() if config["LOG_DIR"] else Path(__file__).parent
    logger = setup_logging(log_dir, config["LOG_LEVEL"])

    # Determine output directory
    output_dir = Path(args.output_dir).expanduser().resolve() if args.output_dir else Path(
        config["OUTPUT_DIR"]).expanduser().resolve() if config["OUTPUT_DIR"] else Path(__file__).parent / 'playlists'

    output_prefix_split = config["OUTPUT_PREFIX_SPLIT"] or ""
    output_prefix_single = config["OUTPUT_PREFIX_SINGLE"] or ""

    # Initialize Spotify client with OAuth
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=config["SPOTIFY_CLIENT_ID"],
        client_secret=config["SPOTIFY_CLIENT_SECRET"],
        redirect_uri=config["SPOTIFY_REDIRECT_URI"],
        scope="playlist-read-private user-library-read"  # Added user-library-read scope
    ))

    # Clean output directory if requested
    if args.clean_output:
        json_files = list(output_dir.glob('*.json'))
        for f in json_files:
            try:
                f.unlink()
                logger.debug(f"Deleted old output file: {f}")
            except Exception as e:
                logger.error(f"Failed to delete {f}: {e}")
        logger.info(f"Output directory cleaned: {output_dir}")

    # Pass playlist_name filter if provided and not blank
    playlist_name_filter = args.playlist_name if args.playlist_name and args.playlist_name.strip() else None

    # Export playlists and/or Liked Songs
    total_playlists, total_tracks = export_playlists(
        sp, args.split, output_dir, output_prefix_split, output_prefix_single, playlist_name_filter, logger)

    elapsed_time = time.time() - start_time
    logger.info(f"Script execution completed in: {elapsed_time:.2f} seconds.")
    logger.info(f"Total playlists exported: {total_playlists}")
    logger.info(f"Total tracks exported: {total_tracks}")


if __name__ == "__main__":
    main()
