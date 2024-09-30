import requests
from lxml import html
import pandas as pd
from spotlistsync.helpers.logger_helper import get_logger


logger = get_logger(__name__)


def parse_html(url):
    # Fetch the HTML content
    response = requests.get(url)
    if response.status_code == 200:
        tree = html.fromstring(response.content)
        return tree
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None


def parse_turbo_top(tree):
    # Extract the list-element track divs
    track_elements = tree.xpath('//div[contains(@class, "list-element track list")]')

    # Extract all artist and title track text values within those elements
    tracks = []
    for element in track_elements:
        artist = element.xpath('.//div[@class="artist-track"]/text()')
        title = element.xpath('.//div[@class="title-track"]/text()')

        # Ensure both artist and title are found and strip any whitespace
        if artist and title:
            tracks.append({'artist': artist[0].strip(), 'title': title[0].strip()})

    # Convert the list of tracks to a DataFrame
    tracks_df = pd.DataFrame(tracks)

    # Display the DataFrame
    print(tracks_df)
    return tracks_df


def fetch_and_parse_turbotop():
    url = "https://player.antyradio.pl/Turbo-Top"
    tree = parse_html(url)
    tracks_df = parse_turbo_top(tree)
    return tracks_df

