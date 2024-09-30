from spotlistsync.helpers.logger_helper import get_logger


logger = get_logger(__name__)


class SpotifyPlaylist:

    def __init__(self, sp) -> None:
        self._sp = sp

    def print_playlists(self):
        playlists = self._sp.current_user_playlists()
        for playlist in playlists['items']:
            print(f"{playlist['name']} (ID: {playlist['id']})")

    def pretty_print_playlists(self):
        print("\n")
        print(f"{self._sp.current_user()['display_name']}'s playlists:")
        print("---------------------")
        self.print_playlists()
        print("---------------------")
        print("\n")

    def find_playlist(self, playlist_name=''):
        playlists = self._sp.current_user_playlists()
        for playlist in playlists['items']:
            if playlist['name'].strip().lower() == playlist_name.strip().lower():
                return playlist['id']
        return None

    def remove_playlist(self, playlist_name):
        if (playlist_id := self.find_playlist(playlist_name)):
            user_id = self._sp.current_user()['id']
            self._sp.user_playlist_unfollow(user_id, playlist_id)
            print(f"Playlist '{playlist_name}' has been removed.")
        else:
            print(f"Playlist '{playlist_name}' not found.")

    def create_or_get_playlist(self, playlist_name, playlist_description):
        if (playlist_id := self.find_playlist(playlist_name)):
            print(f"A playlist named '{playlist_name}' already exists.")
            return playlist_id

        user_id = self._sp.current_user()['id']
        new_playlist = self._sp.user_playlist_create(
            user=user_id,
            name=playlist_name,
            public=True,
            description=playlist_description
        )
        print(f"Playlist (ID: {new_playlist['id']}) {new_playlist['name']} created.")
        return new_playlist['id']

    def add_tracks_to_playlist(self, playlist_id, tracks):
        track_ids = [track['id'] for track in tracks]
        user_id = self._sp.current_user()['id']
        self._sp.user_playlist_add_tracks(
            user=user_id,
            playlist_id=playlist_id,
            tracks=track_ids
        )

    def clear_playlist(self, playlist_id):
        results = self._sp.playlist_tracks(playlist_id)
        track_ids = [item['track']['id'] for item in results['items']]
        if track_ids:
            self._sp.playlist_remove_all_occurrences_of_items(playlist_id, track_ids)
            print(f"Cleared {len(track_ids)} tracks from the playlist '{playlist_id}'.")
        else:
            print(f"The playlist '{playlist_id}' is already empty.")

    def update_playlist_description(self, playlist_id, desc=''):
        self._sp.playlist_change_details(playlist_id, description=desc)
