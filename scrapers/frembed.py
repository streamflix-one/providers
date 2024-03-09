import requests
import re

class FrEmbed:
    def __init__(self):
        self.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "accept-language": "en-GB,en;q=0.9",
            "sec-ch-ua": "\"Chromium\";v=\"122\", \"Not(A:Brand\";v=\"24\", \"Brave\";v=\"122\"",
            "Connection": "keep-alive",
            "Host": "frembed.fun",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "Sec-Fetch-Dest": "iframe",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Sec-GPC": "1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        }

    def fetch_sources(self, tmdb_id, season=None, episode=None):
        url = f"https://frembed.fun/player/test.php?id={tmdb_id}"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            m3u8_url = self.extract_m3u8_url(response.text)
            return m3u8_url
        else:
            print("Failed to retrieve content. Status Code:", response.status_code)
            return None

    def extract_m3u8_url(self, content):
        pattern = r"src:\s*'([^']*\bmaster\.m3u8\b[^']*)'"
        match = re.search(pattern, content)

        if match:
            return {'url': match.group(1), 'source': 'FrEmbed', 'proxy': 'False', 'lang': 'fr', 'type': 'hls'}
        else:
            print("M3U8 URL not found in the response content.")
            return None