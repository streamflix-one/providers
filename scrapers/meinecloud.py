import cloudscraper
import re
import requests
from scrapers.embeds.dood import Doodstream

class MeineCloud:
    def __init__(self, tmdb_api_key):
        self.scraper = cloudscraper.create_scraper()
        self.tmdb_api_key = tmdb_api_key

    def fetch_sources(self, user_ip, tmdb_id):
        imdb_id = self._get_imdb_id(tmdb_id)
        html_content = self.scraper.get(f"https://meinecloud.click/movie/{imdb_id}").text
        pattern = r'<li class data-link="(//dood\.to/e/[a-zA-Z0-9]+)">'

        matches = re.findall(pattern, html_content)
        if matches:
            dood_id = matches[0].split("/e/")[1]
            formatted_url = f"https://d0o0d.com/e/{dood_id}?"
            doodstream = Doodstream(formatted_url, user_ip)
            r = doodstream.main().split("\n")[0]
            print(r)
            return {'url': f'{r}', 'source': 'MeineCloud', 'proxy': 'False', 'lang': 'de', 'type': 'mp4'}
        else:
            return None

    def _get_imdb_id(self, tmdb_id):
        tmdb_api_url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={self.tmdb_api_key}"
        response = requests.get(tmdb_api_url)
        if response.status_code == 200:
            data = response.json()
            imdb_id = data.get("imdb_id", "")
            return imdb_id
        else:
            raise ValueError(f"Error fetching IMDb ID from TMDB API. Status Code: {response.status_code}")
