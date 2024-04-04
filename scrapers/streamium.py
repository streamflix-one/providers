import requests
import re

class Streamium:
    def __init__(self, api_key):
        self.api_key = api_key

    def extract_video_src(self, html_content):
        pattern = r'<source\s+src="([^"]+)"\s+type="video/mp4">'
        match = re.search(pattern, html_content)
        if match:
            return match.group(1)
        else:
            return None

    def get_imdb_id(self, tmdb_id, media_type):
        url = f"https://api.themoviedb.org/3/{media_type}/{tmdb_id}/external_ids?api_key={self.api_key}"
        response = requests.get(url)
        data = response.json()
        return data.get("imdb_id")

    def fetch_response_text(self, imdb_id, media_type, season="", episode=""):
        if media_type == "movie":
            url = f"https://s1.goquick.st/play/{imdb_id}/dw"
        elif media_type == "tv":
            url = f"https://s1.goquick.st/play/{imdb_id}/dw?season={season}&episode={episode}"
        else:
            return None

        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return None

    def fetch_sources(self, tmdb_id, media_type="movie", season="", episode=""):
        imdb_id = self.get_imdb_id(tmdb_id, media_type) # TODO - Fix TV Shows (they use imdb season ids, not show ids)
        if imdb_id:
            resp_text = self.fetch_response_text(imdb_id, media_type, season, episode)
            if resp_text:
                video_src = self.extract_video_src(resp_text)
                if video_src:
                    return {'url': f"https://s1.goquick.st{video_src}#.mp4", 'source': 'Streamium', 'proxy': 'False', 'lang': 'en', 'type': 'mp4'}
        return None

# Example usage:
# api_key = "f1dd7f2494de60ef4946ea81fd5ebaba"
# scraper = Streamium(api_key)
# response_data = scraper.fetch_sources(tmdb_id="108978", media_type="movie")
# print(f"URL: {response_data}")