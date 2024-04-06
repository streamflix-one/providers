import requests
import re

class Streamium:
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "accept-language": "en-GB,en;q=0.8",
            "cache-control": "max-age=0",
            "if-modified-since": "Wed, 13 Mar 2024 21:16:23 GMT",
            "sec-ch-ua": "\"Chromium\";v=\"122\", \"Not(A:Brand\";v=\"24\", \"Brave\";v=\"122\"",
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "\"Android\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "sec-gpc": "1",
            "upgrade-insecure-requests": "1",
            "Referer": f"https://streamium.st/",
            "Referrer-Policy": "strict-origin-when-cross-origin"
        }
      
    def extract_video_src(self, html_content):
        pattern = r'<source\s+src="([^"]+)"\s+type="video/mp4">'
        match = re.search(pattern, html_content)
        if match:
            return match.group(1)
        else:
            return None

    def get_imdb_id(self, tmdb_id, media_type):
        url = f"https://api.themoviedb.org/3/{media_type}/{tmdb_id}/external_ids?api_key={self.api_key}"
        response = requests.get(url, headers=self.headers)
        data = response.json()
        return data.get("imdb_id")

    def fetch_response_text(self, imdb_id, media_type, season="", episode=""):
        if media_type == "movie":
            url = f"https://s1.goquick.st/play/{imdb_id}/Road%20House"
        elif media_type == "tv":
            url = f"https://s1.goquick.st/play/{imdb_id}/Road%20House?season={season}&episode={episode}"
        else:
            return None

        response = requests.get(url, headers=self.headers)
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