from spotlistsync.spotify.spotify_connection import SpotifyConnection
from spotlistsync.spotify.spotify_playlist import SpotifyPlaylist
from spotlistsync.spotify.spotify_track import SpotifyTrack
from spotlistsync.turbotop.turbotop_fetch import fetch_and_parse_turbotop
from datetime import datetime
from spotlistsync.helpers.logger_helper import get_logger
from spotlistsync.helpers.mail_helper import GMailSender
from spotlistsync.config import Config


logger = get_logger(__name__)


def main():
    config = Config()
    config.load()
    sender = GMailSender(config)

    if (not update_turbo_top_spotify_list(config)):
        sender.send_email(
            topic=config['mail']['failed_message_topic'],
            message=config['mail']['failed_message'],
            recepient=config['mail']['recepient'],
        )


def update_turbo_top_spotify_list(config):
    try:
        now = datetime.now()
        playlist_name = 'Turbo Top'
        playlist_desc = f'Updated: {now.strftime("%Y-%m-%d")}'

        print("Fetch playlist tracks")
        turbotop_df = fetch_and_parse_turbotop()

        if turbotop_df.empty:
            print("No data fetched from data source. Can't update Turbo Top playlist.")
            return False

        sp = SpotifyConnection(config).connect()
        playlist = SpotifyPlaylist(sp)
        tracks = SpotifyTrack(sp)

        playlist.pretty_print_playlists()

        print("Updating Turbo-Top playlist.")
        playlist_id = playlist.create_or_get_playlist(playlist_name, playlist_desc)

        print("Clearing Turbo-Top playlist.")
        playlist.clear_playlist(playlist_id)

        print("Search Turbo-Top tracks.")
        tracks = tracks.search_all_tracks(turbotop_df)

        print("Add tracks to playlist.")
        playlist.add_tracks_to_playlist(playlist_id, tracks)

        print(f"Updated playlist {playlist_id} description to: {playlist_desc}")
        playlist.update_playlist_description(playlist_id, playlist_desc)
        
    except Exception:
        print("Failed to connect to spotify or update spotify list. Can't update Turbo Top playlist.")
        return False
    else:
        return True
    

if __name__ == "__main__":
    main()
