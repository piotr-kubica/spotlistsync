import spotipy
from spotipy.oauth2 import SpotifyOAuth
import webbrowser
from spotlistsync.helpers.logger_helper import get_logger


logger = get_logger(__name__)


class SpotifyConnection:

    def __init__(self, config) -> None:
        self.client_id = config["spotify"]["client_id"]
        self.client_secret = config["spotify"]["client_secret"]
        self.redirect_uri = config["spotify"]["redirect_uri"]

    def connect(self):
        try:
            access_token = self._get_spotify_token()
            sp = spotipy.Spotify(auth=access_token)
            return sp
        except Exception:
            logger.error("Could not access spotify. Please try authenticating using web browser!")
            return None

    def _get_spotify_token(self):
        sp_oauth = self._create_spotify_oauth()
        token_info = sp_oauth.get_cached_token()

        # If token exists and is not expired, return it
        if token_info and not sp_oauth.is_token_expired(token_info):
            print("Using cached access token.")
            return token_info['access_token']

        # If the token is expired but we have a refresh token, refresh it
        elif token_info:
            print("Refreshing access token.")
            return sp_oauth.refresh_access_token(token_info['refresh_token'])['access_token']

        # If no token or refresh fails, prompt user to re-authenticate
        else:
            print("No valid token found. Starting re-authentication.")
            auth_url = sp_oauth.get_authorize_url()
            print(f"Please navigate to this URL to authorize: {auth_url}")
            webbrowser.open(auth_url)

            # The user will need to paste the URL they are redirected to
            response_url = input("Paste the URL you were redirected to here: ")
            code = sp_oauth.parse_response_code(response_url)

            # Get the access token after authorization
            token_info = sp_oauth.get_access_token(code)
            return token_info['access_token']

    def _create_spotify_oauth(self):
        sp_oauth = SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope='playlist-modify-public user-library-read',
            cache_path='.spotipy_cache'\
        )
        return sp_oauth