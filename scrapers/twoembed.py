import requests
from bs4 import BeautifulSoup
import re

class TwoEmbed:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = "https://uqloads.xyz/e/"

        self.default_headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "accept-language": "en-GB,en;q=0.9",
            "sec-ch-ua": "\"Chromium\";v=\"122\", \"Not(A:Brand\";v=\"24\", \"Brave\";v=\"122\"",
            'Connection': 'keep-alive',
            'Cookie': '_ym_uid=1709594704938985430; _ym_d=1709594704; _ym_isad=2',
            'Host': 'uqloads.xyz',
            'Referer': 'https://streamsrcs.2embed.cc/',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Sec-Fetch-Dest': 'iframe',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-User': '?1',
            'Sec-GPC': '1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        }

    def fetch_content_with_id(self, video_id):
        url = f"{self.base_url}{video_id}"
        try:
            response = self.session.get(url, headers=self.default_headers)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None

    def tmdb_to_imdb(self, tmdb_id):
        tmdb_api_key = "f1dd7f2494de60ef4946ea81fd5ebaba"
        tmdb_url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={tmdb_api_key}"

        try:
            response = requests.get(tmdb_url)
            response.raise_for_status()
            data = response.json()
            imdb_id = data.get('imdb_id')
            return imdb_id
        except requests.exceptions.RequestException as e:
            print(f"Error fetching IMDb ID from TMDB: {e}")
            return None

    def fetch_sources(self, tmdb_id, season=None, episode=None):
        imdb_id = self.tmdb_to_imdb(tmdb_id)

        if imdb_id:
            url = f"https://1hd.store/embed/{imdb_id}"

            headers = {
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                "accept-language": "en-GB,en;q=0.9",
                "sec-ch-ua": "\"Chromium\";v=\"122\", \"Not(A:Brand\";v=\"24\", \"Brave\";v=\"122\"",
                'Connection': 'keep-alive',
                'Host': '1hd.store',
                'Referer': f'https://1hd.store/watch-the-marvels-2023-online-{tmdb_id}', # why not its not like they check lmao
                'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Brave";v="122"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'Sec-Fetch-Dest': 'iframe',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-GPC': '1',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
            }

            try:
                response = self.session.get(url, headers=headers)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                urls = [div['onclick'].split("'")[1] for div in soup.find_all('div', class_='btn-iframe')]
                stripped_urls = [url.replace('https://streamsrcs.2embed.cc/swish-autostream?id=', '') for url in urls]

                if stripped_urls:
                    uqcloud_content = self.fetch_content_with_id(stripped_urls[0])
                    m3u8_urls = re.findall(r'file:\s*"([^"]+)"', uqcloud_content)

                    if m3u8_urls:
                        return {'url': m3u8_urls[0], 'source': '2Embed', 'proxy': 'False', 'lang': 'en', 'type': 'hls'}

                    else:
                        print("M3U8 URL not found in the response.")
                else:
                    print("No URLs found in the response.")
            except requests.exceptions.RequestException as e:
                print(f"Error: {e}")
            return None
