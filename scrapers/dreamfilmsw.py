import requests
from bs4 import BeautifulSoup
import re

class DreamFilmSW:
    def __init__(self):
        self.php_session_id = self.get_php_session_id("https://dreamfilmsw.net/")

    def get_iframe_source(self, iframe_src):
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "accept-language": "en-GB,en;q=0.6",
            "sec-ch-ua": "\"Chromium\";v=\"122\", \"Not(A:Brand\";v=\"24\", \"Brave\";v=\"122\"",
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "\"Android\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "sec-gpc": "1",
            "upgrade-insecure-requests": "1",
            "cookie": f"PHPSESSID={self.php_session_id}",
            "Referer": iframe_src.replace(".to/", ".me/"),
            "Referrer-Policy": "strict-origin-when-cross-origin"
        }

        response = requests.get(iframe_src.replace(".to/", ".net/"), headers=headers)

        if response.status_code == 200:
            return response.text
        else:
            print(f"Request to iframe data-src failed with status code: {response.status_code}")
            return None

    def extract_m3u8_link(self, source):
        regex_pattern = r'sources: \[{file:"(.*?)"\}\]'
        match = re.search(regex_pattern, source)

        if match:
            return match.group(1)
        else:
            print("No m3u8 link found in the source.")
            return None

    def fetch_movie_details(self, slug):
        url = f'https://dreamfilmsw.net/{slug}'
        print(url)
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "accept-language": "en-GB,en;q=0.6",
            "sec-ch-ua": "\"Chromium\";v=\"122\", \"Not(A:Brand\";v=\"24\", \"Brave\";v=\"122\"",
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "\"Android\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "sec-gpc": "1",
            "upgrade-insecure-requests": "1",
            "cookie": f"PHPSESSID={self.php_session_id}",
            "Referer": "https://dreamfilmsw.net/",
            "Referrer-Policy": "strict-origin-when-cross-origin"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            iframe = soup.find('iframe', class_='moly-en') or soup.find('iframe', class_='Moly')

            if iframe:
                data_src = iframe.get('data-src')
                print(data_src)
                if data_src:
                    return data_src
                else:
                    print("No 'data-src' attribute found in the iframe.")
            else:
                print("No iframe with class 'moly-en' found.")
        else:
            print(f"Request failed with status code: {response.status_code}")

        return None

    def get_php_session_id(self, url):
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "accept-language": "en-GB,en;q=0.6",
            "cache-control": "max-age=0",
            "sec-ch-ua": "\"Chromium\";v=\"122\", \"Not(A:Brand\";v=\"24\", \"Brave\";v=\"122\"",
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "\"Android\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "sec-gpc": "1",
            "upgrade-insecure-requests": "1"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            if 'Set-Cookie' in response.headers:
                cookies = requests.utils.dict_from_cookiejar(response.cookies)
                php_session_id = cookies.get('PHPSESSID')
                return php_session_id
            else:
                print("Set-Cookie header not found in the response.")
        else:
            print(f"Request failed with status code: {response.status_code}")

    def search_with_php_session_id(self, query):
        search_url = "https://dreamfilmsw.net/search"

        headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "en-GB,en;q=0.6",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "sec-ch-ua": "\"Chromium\";v=\"122\", \"Not(A:Brand\";v=\"24\", \"Brave\";v=\"122\"",
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "\"Android\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "sec-gpc": "1",
            "x-requested-with": "XMLHttpRequest",
            "cookie": f"PHPSESSID={self.php_session_id}",
            "Referer": "https://dreamfilmsw.net/",
            "Referrer-Policy": "strict-origin-when-cross-origin"
        }

        data = {"query": query}

        response = requests.post(search_url, headers=headers, data=data)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Request failed with status code: {response.status_code}")
            return None


    def convert_tmdb_to_imdb(self, tmdb_id, is_tv_show=False):
      base_url = "https://api.themoviedb.org/3"
      endpoint = "tv" if is_tv_show else "movie"
      tmdb_api_key = "f1dd7f2494de60ef4946ea81fd5ebaba"
  
      tmdb_url = f"{base_url}/{endpoint}/{tmdb_id}/external_ids?api_key={tmdb_api_key}"
  
      response = requests.get(tmdb_url)
  
      if response.status_code == 200:
          tmdb_data = response.json()
          imdb_id = tmdb_data.get("imdb_id")
          return imdb_id
      else:
          print(f"Failed to convert TMDB ID to IMDb ID. Status code: {response.status_code}")
          return None
      
    def fetch_sources(self, tmdb_id, season=None, episode=None):
        imdb_id = self.convert_tmdb_to_imdb(tmdb_id, is_tv_show=(season is not None and episode is not None))
        search_result = self.search_with_php_session_id(imdb_id)

        if search_result:
            slug = search_result['result'][0]['slug']

            if season is not None and episode is not None:
                slug = f"series/{slug}/season-{season}/episode-{episode}"

            iframe_src = self.fetch_movie_details(slug)

            if iframe_src:
                iframe_content = self.get_iframe_source(iframe_src)

                if iframe_content:
                    m3u8_link = self.extract_m3u8_link(iframe_content)
                    return {'url': m3u8_link, 'source': 'DreamFilmSW', 'proxy': 'True', 'lang': 'en', 'type': 'hls'}

# Example usage
# scraper = DreamFilmSW()
# response_data = scraper.fetch_source(438631)
# print(f"Tv URL: {response_data}")
