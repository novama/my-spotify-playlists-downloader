#!/usr/bin/env python3
# -----------------------------------------------------------------------------
# my_spotify_playlists_downloader.py
#
# Exports your Spotify playlists to JSON files.
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
    python my_spotify_playlists_downloader.py [--split] [--output_dir /path/to/dir] [--playlist_name "Playlist Name"] [--liked_songs] [--all_playlists] [--html_report] [--clean_output]

Options:
    --split                    Export each playlist as an individual JSON file named after the playlist (sanitized).
    --output_dir DIR           Override the output directory path defined in .env or default.
    --playlist_name NAME       Export only the playlist with this name (case-insensitive, normalized).
    --liked_songs              Export liked songs (saved tracks). Can be combined with --playlist_name or --all_playlists.
    --all_playlists            Export all playlists. Can be combined with --liked_songs.
    --html_report              Generate a HTML report with export summary and statistics.
    --clean_output             Delete all JSON files in the output directory before exporting playlists.

Examples:
    python my_spotify_playlists_downloader.py                                    # Export all playlists
    python my_spotify_playlists_downloader.py --liked_songs                      # Export only liked songs
    python my_spotify_playlists_downloader.py --playlist_name "My Playlist"      # Export only "My Playlist"
    python my_spotify_playlists_downloader.py --liked_songs --playlist_name "My Playlist"  # Export liked songs + "My Playlist"
    python my_spotify_playlists_downloader.py --liked_songs --all_playlists      # Export liked songs + all playlists
    python my_spotify_playlists_downloader.py --all_playlists                    # Export all playlists (same as no flags)
    python my_spotify_playlists_downloader.py --all_playlists --html_report      # Export all playlists + generate HTML report
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

    # Remove emoji and non-printable characters
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


def _process_tracks_data(sp: spotipy.Spotify, tracks_data, logger, source_description: str) -> list:
    """
    Generic function to process tracks data from any Spotify source.
    
    Args:
        sp (spotipy.Spotify): Authenticated Spotify client for pagination
        tracks_data: Initial tracks data from Spotify API (playlist_items or current_user_saved_tracks)
        logger: Logger instance for logging
        source_description (str): Description of the source for logging (e.g., "playlist ID xyz", "liked songs")
    
    Returns:
        list: List of track dictionaries with selected metadata
    """
    tracks = []
    track_index = 0

    while tracks_data:
        items = tracks_data.get('items', [])
        for item in items:
            track = item.get('track')
            if not track:
                logger.debug(f"Skipping item at position {track_index}: no track data")
                continue
                
            try:
                # Safely extract track data with fallbacks
                track_name = track.get('name', 'Unknown Track')
                artists = track.get('artists', [])
                artist_names = ', '.join([artist.get('name', 'Unknown Artist') for artist in artists if artist.get('name')])
                if not artist_names:
                    artist_names = 'Unknown Artist'
                
                album = track.get('album', {})
                album_name = album.get('name', 'Unknown Album')
                album_release_date = album.get('release_date', '')
                
                external_urls = track.get('external_urls', {})
                spotify_url = external_urls.get('spotify', '')
                spotify_uri = track.get("uri", '')
                
                added_at = item.get('added_at', '')
                added_by = item.get('added_by', {})
                added_by_id = added_by.get('id') if added_by else None

                tracks.append({
                    'position': track_index,
                    'name': track_name,
                    'artist': artist_names,
                    'album': album_name,
                    'album_release_date': album_release_date,
                    'spotify_url': spotify_url,
                    'spotify_uri': spotify_uri,
                    'added_at': added_at,
                    'added_by': added_by_id,
                })
                track_index += 1
                
            except Exception as e:
                logger.warning(f"Error processing track at position {track_index} from {source_description}: {e}")
                continue

        # Get next page of results
        try:
            tracks_data = sp.next(tracks_data) if tracks_data and tracks_data.get('next') else None
        except:
            tracks_data = None

    logger.debug(f"Retrieved {len(tracks)} tracks from {source_description}.")
    return tracks


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
    try:
        tracks_data = sp.playlist_items(playlist_id)
    except Exception as e:
        logger.error(f"Failed to retrieve playlist items for playlist ID {playlist_id}: {e}")
        return []
    
    return _process_tracks_data(sp, tracks_data, logger, f"playlist ID {playlist_id}")


def get_user_saved_tracks(sp: spotipy.Spotify, logger) -> list:
    """
    Retrieve all liked songs (saved tracks) from the current user.

    Args:
        sp (spotipy.Spotify): Authenticated Spotify client.
        logger (Logger): Logger instance for logging.

    Returns:
        list: List of track dictionaries with selected metadata.
    """
    try:
        tracks_data = sp.current_user_saved_tracks()
    except Exception as e:
        logger.error(f"Failed to retrieve user saved tracks: {e}")
        return []
    
    return _process_tracks_data(sp, tracks_data, logger, "liked songs")


def generate_html_report(report_data: dict, output_dir: Path, logger) -> Path:
    """
    Generate a professional HTML report with export summary and statistics.
    
    Args:
        report_data (dict): Dictionary containing all report information
        output_dir (Path): Directory to save the report
        logger: Logger instance for logging
    
    Returns:
        Path: Path to the generated HTML report file
    """
    from datetime import datetime
    
    # Generate timestamp for report
    timestamp = datetime.now().strftime("%Y-%m-%d at %I:%M:%S %p")
    
    # Calculate additional statistics
    total_export_files = report_data.get('total_playlists', 0) + (1 if report_data.get('liked_songs_exported', False) else 0)
    
    # Create HTML content
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Spotify Playlists Downloader - Export Report- {timestamp}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: #0a0e27;
            color: #e4e6eb;
            line-height: 1.6;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1100px;
            margin: 0 auto;
        }}
        
        .header {{
            background: linear-gradient(135deg, #1ed760 0%, #1db954 100%);
            border-radius: 12px;
            padding: 32px 40px;
            margin-bottom: 24px;
            box-shadow: 0 4px 12px rgba(30, 215, 96, 0.15);
        }}
        
        .header h1 {{
            color: #ffffff;
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 8px;
            letter-spacing: -0.5px;
        }}
        
        .header .subtitle {{
            color: rgba(255, 255, 255, 0.85);
            font-size: 14px;
            font-weight: 500;
        }}
        
        .metrics {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }}
        
        .metric-card {{
            background: #151b3b;
            border-radius: 10px;
            padding: 24px;
            border: 1px solid #2a3150;
            transition: all 0.2s ease;
        }}
        
        .metric-card:hover {{
            border-color: #1db954;
            transform: translateY(-2px);
        }}
        
        .metric-value {{
            font-size: 32px;
            font-weight: 700;
            color: #1db954;
            margin-bottom: 4px;
            line-height: 1;
        }}
        
        .metric-label {{
            color: #9ca3af;
            font-size: 13px;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .section {{
            background: #151b3b;
            border-radius: 10px;
            padding: 28px;
            margin-bottom: 16px;
            border: 1px solid #2a3150;
        }}
        
        .section-title {{
            font-size: 18px;
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 20px;
            padding-bottom: 12px;
            border-bottom: 2px solid #2a3150;
        }}
        
        .info-grid {{
            display: grid;
            gap: 12px;
        }}
        
        .info-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 0;
            font-size: 14px;
        }}
        
        .info-label {{
            color: #9ca3af;
            font-weight: 500;
        }}
        
        .info-value {{
            color: #e4e6eb;
            font-weight: 600;
            text-align: right;
        }}
        
        .status-badge {{
            background: linear-gradient(135deg, #1db954 0%, #17a34a 100%);
            color: #ffffff;
            padding: 4px 12px;
            border-radius: 6px;
            font-size: 13px;
            font-weight: 600;
        }}
        
        .playlist-list {{
            display: grid;
            gap: 10px;
            max-height: 400px;
            overflow-y: auto;
            padding-right: 8px;
        }}
        
        .playlist-list::-webkit-scrollbar {{
            width: 8px;
        }}
        
        .playlist-list::-webkit-scrollbar-track {{
            background: #0a0e27;
            border-radius: 4px;
        }}
        
        .playlist-list::-webkit-scrollbar-thumb {{
            background: #2a3150;
            border-radius: 4px;
        }}
        
        .playlist-list::-webkit-scrollbar-thumb:hover {{
            background: #1db954;
        }}
        
        .playlist-card {{
            background: #0a0e27;
            border-radius: 8px;
            padding: 16px;
            border-left: 3px solid #1db954;
            transition: all 0.2s ease;
        }}
        
        .playlist-card:hover {{
            background: #1a1f3a;
        }}
        
        .playlist-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 6px;
        }}
        
        .playlist-name {{
            font-weight: 600;
            color: #ffffff;
            font-size: 15px;
        }}
        
        .playlist-tracks {{
            color: #1db954;
            font-weight: 600;
            font-size: 14px;
        }}
        
        .playlist-owner {{
            color: #9ca3af;
            font-size: 13px;
        }}
        
        .footer {{
            text-align: center;
            color: #6b7280;
            margin-top: 32px;
            padding-top: 20px;
            border-top: 1px solid #2a3150;
            font-size: 13px;
        }}
        
        @media (max-width: 768px) {{
            body {{ padding: 12px; }}
            .header {{ padding: 24px; }}
            .header h1 {{ font-size: 24px; }}
            .section {{ padding: 20px; }}
            .metrics {{ grid-template-columns: repeat(2, 1fr); }}
            .metric-card {{ padding: 16px; }}
            .metric-value {{ font-size: 28px; }}
        }}
        
        @media (max-width: 480px) {{
            .metrics {{ grid-template-columns: 1fr; }}
            .info-row {{ flex-direction: column; align-items: flex-start; gap: 4px; }}
            .info-value {{ text-align: left; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Spotify Playlists Downloader - Export Report</h1>
            <div class="subtitle">{timestamp}</div>
        </div>
        
        <div class="metrics">
            <div class="metric-card">
                <div class="metric-value">{report_data.get('total_playlists', 0)}</div>
                <div class="metric-label">Playlists</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{report_data.get('total_tracks', 0):,}</div>
                <div class="metric-label">Total Tracks</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{total_export_files}</div>
                <div class="metric-label">Files Created</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{report_data.get('execution_time', 0):.1f}s</div>
                <div class="metric-label">Execution Time</div>
            </div>
        </div>
        
        <div class="section">
            <div class="section-title">Execution Details</div>
            <div class="info-grid">
                <div class="info-row">
                    <span class="info-label">Output Directory</span>
                    <span class="info-value">{report_data.get('output_dir', 'N/A')}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Export Mode</span>
                    <span class="info-value">{"Individual Files" if report_data.get('split_mode', False) else "Combined Files"}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Liked Songs</span>
                    <span class="info-value">{"Exported" if report_data.get('liked_songs_exported', False) else "Not Exported"}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Status</span>
                    <span class="status-badge">Completed Successfully</span>
                </div>
            </div>
        </div>"""
    
    # Add playlist details section if playlists were exported
    if report_data.get('playlists_details'):
        html_content += f"""
        <div class="section">
            <div class="section-title">Exported Playlists ({len(report_data['playlists_details'])})</div>
            <div class="playlist-list">"""
        
        for playlist in report_data['playlists_details']:
            html_content += f"""
                <div class="playlist-card">
                    <div class="playlist-header">
                        <div class="playlist-name">{playlist.get('name', 'Unknown Playlist')}</div>
                        <div class="playlist-tracks">{playlist.get('track_count', 0)} tracks</div>
                    </div>
                    <div class="playlist-owner">Owner: {playlist.get('owner', 'Unknown')}</div>
                </div>"""
        
        html_content += """
            </div>
        </div>"""
    
    # Add liked songs section if exported
    if report_data.get('liked_songs_exported'):
        html_content += f"""
        <div class="section">
            <div class="section-title">Liked Songs</div>
            <div class="playlist-card">
                <div class="playlist-header">
                    <div class="playlist-name">Your Liked Songs</div>
                    <div class="playlist-tracks">{report_data.get('liked_songs_count', 0)} tracks</div>
                </div>
                <div class="playlist-owner">Personal collection from Spotify</div>
            </div>
        </div>"""
    
    html_content += f"""
        <div class="footer">
            <p>Generated by Spotify Playlists Downloader</p>
        </div>
    </div>
</body>
</html>"""
    
    # Save HTML report
    output_dir.mkdir(parents=True, exist_ok=True)
    report_filename = f"spotify_export_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    report_path = output_dir / report_filename
    
    report_path.write_text(html_content, encoding='utf-8')
    logger.info(f"HTML report generated: {report_path}")
    
    return report_path


def export_liked_songs(sp: spotipy.Spotify, split: bool, output_dir: Path,
                      output_prefix_split: str, output_prefix_single: str, logger, report_data=None):
    """
    Export liked songs (saved tracks) to JSON file.
    
    Args:
        sp (spotipy.Spotify): Authenticated Spotify client.
        split (bool): Whether to export as individual file (for consistency).
        output_dir (Path): Directory to save output files.
        output_prefix_split (str): Prefix for split output filenames.
        output_prefix_single (str): Prefix for single output filename.
        logger (Logger): Logger instance for logging.
        report_data (dict, optional): Dictionary to collect report statistics.
    
    Returns:
        tuple: (1, total_tracks_exported)
    """
    logger.info("Exporting liked songs (saved tracks)")
    
    tracks = get_user_saved_tracks(sp, logger)
    
    if not tracks:
        logger.warning("No liked songs found to export")
        if report_data is not None:
            report_data['liked_songs_exported'] = False
            report_data['liked_songs_count'] = 0
        return 0, 0
    
    # Get current user info
    try:
        user_info = sp.current_user()
        user_id = user_info.get('id', 'unknown')
        user_name = user_info.get('display_name') or user_id
    except Exception as e:
        logger.warning(f"Could not retrieve user info: {e}")
        user_id = 'unknown'
        user_name = 'Unknown User'
    
    liked_songs_obj = {
        'playlist_name': 'Liked Songs',
        'playlist_id': 'liked_songs',  # Special identifier
        'owner_id': user_id,
        'owner': user_name,
        'description': 'Your liked songs from Spotify',
        'snapshot_id': '',
        'tracks': tracks
    }
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if split:
        filename = f"{output_prefix_split}Liked_Songs.json"
    else:
        filename = f"{output_prefix_single}liked_songs.json"
    
    filepath = output_dir / filename
    filepath.write_text(json.dumps([liked_songs_obj], ensure_ascii=False, indent=4), encoding='utf-8')
    logger.info(f"Liked songs exported to: {filepath}")
    
    # Collect data for report
    if report_data is not None:
        report_data['liked_songs_exported'] = True
        report_data['liked_songs_count'] = len(tracks)
    
    return 1, len(tracks)


def export_playlists(sp: spotipy.Spotify, split: bool, output_dir: Path,
                     output_prefix_split: str, output_prefix_single: str, playlist_name_filter: str, logger, report_data=None):
    """
    Export all playlists to JSON files, either as individual files or a single combined file.
    Optionally filter by normalized playlist name.

    Args:
        sp (spotipy.Spotify): Authenticated Spotify client.
        split (bool): Whether to export each playlist as a separate file.
        output_dir (Path): Directory to save output files.
        output_prefix_split (str): Prefix for split output filenames.
        output_prefix_single (str): Prefix for single output filename.
        playlist_name_filter (str): Normalized playlist name to filter.
        logger (Logger): Logger instance for logging.
        report_data (dict, optional): Dictionary to collect report statistics.

    Returns:
        tuple: (total_playlists_exported (int), total_tracks_exported (int))
    """
    playlists = get_all_playlists(sp, logger)
    export = []
    total_playlists = 0
    total_tracks = 0

    output_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Output directory set to: {output_dir}")

    # Normalize filter if provided
    normalized_filter = normalize_playlist_name(playlist_name_filter) if playlist_name_filter else None
    if normalized_filter:
        logger.info(f"Running with playlist_name filter: '{playlist_name_filter}' (normalized: '{normalized_filter}')")
    filtered_playlists = []
    for playlist in playlists:
        normalized_name = normalize_playlist_name(playlist['name'])
        if normalized_filter:
            if normalized_name == normalized_filter:
                filtered_playlists.append(playlist)
        else:
            filtered_playlists.append(playlist)

    logger.info(f"Number of playlists to export: {len(filtered_playlists)}")

    if normalized_filter and not filtered_playlists:
        logger.error(f"No playlist matched the name: '{playlist_name_filter}' (normalized: '{normalized_filter}')")
        return 0, 0

    # Initialize report data for playlists
    if report_data is not None:
        report_data['playlists_details'] = []

    for playlist in filtered_playlists:
        playlist_name = playlist['name']
        owner_name = playlist.get('owner', {}).get('display_name', 'Unknown')
        owner_id = playlist.get('owner', {}).get('id', 'unknown')
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

        # Collect playlist data for report
        if report_data is not None:
            report_data['playlists_details'].append({
                'name': playlist_name,
                'owner': owner_name,
                'track_count': len(tracks)
            })

        if split:
            export_filename = f"{output_prefix_split}{sanitize_playlist_name(playlist_name)}.json"
            filename = export_filename
            filepath = output_dir / filename
            filepath.write_text(json.dumps([playlist_obj], ensure_ascii=False, indent=4), encoding='utf-8')
            logger.info(f"Saved playlist to {filepath}")
            total_playlists += 1
        else:
            export.append(playlist_obj)
            total_playlists += 1

    if not split and filtered_playlists:
        if normalized_filter:
            export_filename = f"{output_prefix_single}filtered_spotify_playlists.json"
        else:
            export_filename = f"{output_prefix_single}spotify_playlists.json"
        filename = export_filename
        filepath = output_dir / filename
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

    parser = argparse.ArgumentParser(description="Download Spotify playlists to JSON")
    parser.add_argument('--split', action='store_true',
                        help='Export each playlist as an individual JSON file')
    parser.add_argument('--output_dir', type=str, default=None,
                        help='Override the output directory path defined in .env or default.')
    parser.add_argument('--playlist_name', type=str, default=None,
                        help='Export only the playlist with this name (case-insensitive, normalized).')
    parser.add_argument('--liked_songs', action='store_true',
                        help='Export liked songs (saved tracks). Can be combined with other options.')
    parser.add_argument('--all_playlists', action='store_true',
                        help='Export all playlists. Can be combined with --liked_songs.')
    parser.add_argument('--html_report', action='store_true',
                        help='Generate a HTML report with export summary and statistics.')
    parser.add_argument('--clean_output', action='store_true',
                        help='Delete all JSON files in the output directory before exporting playlists.')
    args = parser.parse_args()

    # Validate argument combinations
    if args.playlist_name and args.all_playlists:
        parser.error("--playlist_name and --all_playlists cannot be used together. Use --playlist_name for a specific playlist, or --all_playlists for all playlists.")

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
        scope="playlist-read-private user-library-read"
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

    # Initialize report data collection if HTML report is requested
    report_data = None
    if args.html_report:
        report_data = {
            'total_playlists': 0,
            'total_tracks': 0,
            'execution_time': 0,
            'output_dir': str(output_dir),
            'split_mode': args.split,
            'liked_songs_exported': False,
            'liked_songs_count': 0,
            'playlists_details': []
        }

    # Handle liked songs and/or playlists export
    total_playlists = 0
    total_tracks = 0
    
    # Export liked songs if requested
    if args.liked_songs:
        logger.info("Exporting liked songs...")
        liked_playlists, liked_tracks = export_liked_songs(
            sp, args.split, output_dir, output_prefix_split, output_prefix_single, logger, report_data)
        total_playlists += liked_playlists
        total_tracks += liked_tracks
    
    # Export playlists based on filter, all_playlists flag, or default behavior
    # Skip playlist export only if --liked_songs is used alone (without --playlist_name or --all_playlists)
    should_export_playlists = not args.liked_songs or playlist_name_filter is not None or args.all_playlists
    
    if should_export_playlists:
        if playlist_name_filter:
            logger.info(f"Exporting playlist matching: '{playlist_name_filter}'")
        else:
            logger.info("Exporting all playlists...")
        
        playlist_count, playlist_tracks = export_playlists(
            sp, args.split, output_dir, output_prefix_split, output_prefix_single, playlist_name_filter, logger, report_data)
        total_playlists += playlist_count
        total_tracks += playlist_tracks

    elapsed_time = time.time() - start_time
    logger.info(f"Script execution completed in: {elapsed_time:.2f} seconds.")
    
    # Update report data with final statistics
    if report_data is not None:
        report_data['total_playlists'] = total_playlists
        report_data['total_tracks'] = total_tracks
        report_data['execution_time'] = elapsed_time
    
    # Log results based on what was exported
    if args.liked_songs and (playlist_name_filter or args.all_playlists):
        if args.all_playlists:
            logger.info(f"Total exports: {total_playlists} (including liked songs + all playlists)")
        else:
            logger.info(f"Total exports: {total_playlists} (including liked songs + filtered playlists)")
    elif args.liked_songs and not playlist_name_filter and not args.all_playlists:
        if total_playlists > 0:
            logger.info(f"Liked songs export completed successfully")
        else:
            logger.error(f"Liked songs export failed - no tracks found or export error occurred")
    else:
        logger.info(f"Total playlists exported: {total_playlists}")
    
    logger.info(f"Total tracks exported: {total_tracks}")
    
    # Generate HTML report if requested
    if args.html_report and report_data is not None:
        try:
            report_path = generate_html_report(report_data, output_dir, logger)
            logger.info(f"HTML report available at: {report_path}")
        except Exception as e:
            logger.error(f"Failed to generate HTML report: {e}")


if __name__ == "__main__":
    main()
