from spotlistsync.helpers.logger_helper import get_logger


logger = get_logger(__name__)


class SpotifyTrack:

    def __init__(self, sp) -> None:
        self._sp = sp

    def search_all_tracks(self, df_track_artist) -> list:  # track info list
        # Convert DataFrame to a list of tuples (title, artist)
        items = list(df_track_artist[['title', 'artist']].itertuples(index=False, name=None))
        found_tracks = []

        for title, artist in items:
            track = self.search_track(title, artist)
            if track:
                found_tracks.append(track)

        return found_tracks

    def search_track(self, title, artist):
        query = f"track:{title} artist:{artist}"
        result = self._sp.search(q=query, type='track', limit=1)

        if result['tracks']['items']:
            track = result['tracks']['items'][0]
            return {
                'id': track['id'],
                'name': track['name'],
                'artist': ', '.join([artist['name'] for artist in track['artists']]),
                'album': track['album']['name'],
                'release_date': track['album']['release_date'],
                'spotify_url': track['external_urls']['spotify']
            }
        else:
            return None

    def print_track_info(self, track_info):
        if track_info:
            print(f"Track: {track_info['name']}")
            print(f"Artist: {track_info['artist']}")
            print(f"Album: {track_info['album']}")
            print(f"Release Date: {track_info['release_date']}")
            print(f"Spotify URL: {track_info['spotify_url']}")
        else:
            print("Track not found.")


