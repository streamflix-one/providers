import requests
from bs4 import BeautifulSoup
import base64
from urllib.parse import unquote
from typing import Union
import re
import time
from urllib.parse import quote

class VidsrcTo:
    def __init__(self):
        self.base_url = "https://vidsrc.to/embed/"
        self.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "accept-language": "en-GB,en;q=0.9",
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


    def get_embed_sources(self, id):
      url = f"https://vidsrc.to/ajax/embed/episode/{id}/sources"
  

      response = requests.get(url, headers=self.headers)
  
      if response.status_code == 200:
          # print("Request successful")
          # print(response.text)
          return response.json()["result"][0]["id"]
      else:
          # print(f"Request failed with status code {response.status_code}")
          return None
  
    
    def get_vidsrc_keys(self):
      # print("Getting keys...")
      url = "https://github.com/Ciarands/vidsrc-keys/blob/main/keys.json"
      response = requests.get(url)
      if response.status_code != 200:
          # print(f"Failed to fetch content from {url}. Status code: {response.status_code}")
          return None
  
      pattern = re.compile(r'"blob":{"rawLines":\["(.*?)"\]')
      match = pattern.search(response.text)
  
      if match:
          result_str = match.group(1)
  
          extracted_values = result_str.replace('\\', '').replace('"', '').strip("[").split(',')
          return extracted_values[0], extracted_values[1]
  
      else:
          # print("Pattern not found in the content.")
          return None

    def get_id(self, tmdb_id, season=None, episode=None):
        # print(f"Getting id for tmdb_id: {tmdb_id}")
        base_url = self.base_url

        if season and episode:
            url = f"{base_url}tv/{tmdb_id}/{season}/{episode}"
        else:
            url = f"{base_url}movie/{tmdb_id}"
        # print(url)
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            a_element = soup.select_one('.episodes li a')

            if a_element:
                data_id = a_element.get('data-id')
                r = self.get_embed_sources(data_id)
                return r
            else:
                raise ValueError("Could not find the data-id attribute")

        else:
            raise ValueError(f"Request failed with status code {response.status_code}")

    def get_encrypted_sources(self, data_id):
        url = f"https://vidsrc.to/ajax/embed/source/{data_id}"
        # print(url)
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            # print(response.text)
            return response.json()["result"]["url"]  # Assuming the response is JSON
        else:
            raise ValueError(f"Failed to fetch data: {response.status_code}")

    def decode_data(self, key: str, data: Union[bytearray, str]) -> bytearray:
        key_bytes = bytes(key, 'utf-8')
        s = bytearray(range(256))
        j = 0

        for i in range(256):
            j = (j + s[i] + key_bytes[i % len(key_bytes)]) & 0xff
            s[i], s[j] = s[j], s[i]

        decoded = bytearray(len(data))
        i = 0
        k = 0

        for index in range(len(data)):
            i = (i + 1) & 0xff
            k = (k + s[i]) & 0xff
            s[i], s[k] = s[k], s[i]
            t = (s[i] + s[k]) & 0xff

            if isinstance(data[index], str):
                decoded[index] = ord(data[index]) ^ s[t]
            elif isinstance(data[index], int):
                decoded[index] = data[index] ^ s[t]
            else:
                raise TypeError("Invalid data type")

        return decoded

    def handle_vidplay(self, url) -> str:
        furl = url
        url = url.split("?")

        key1, key2 = self.get_vidsrc_keys()

        decoded_id = self.decode_data(key1, url[0].split('/e/')[-1])
        encoded_result = self.decode_data(key2, decoded_id)
        encoded_base64 = base64.b64encode(encoded_result)
        key = encoded_base64.decode('utf-8').replace('/', '_')

        req = requests.get("https://vidplay.online/futoken", {"Referer": url})
        # print(req.text)
        fu_key = re.search(r"var\s+k\s*=\s*'([^']+)'", req.text).group(1)
        data = f"{fu_key},{','.join([str(ord(fu_key[i % len(fu_key)]) + ord(key[i])) for i in range(len(key))])}"

        req = requests.get(
            f"https://vidplay.online/mediainfo/{data}?{url[1]}&autostart=true",
            headers={"Referer": furl}
        )
        req_data = req.json()

        if type(req_data.get("result")) == dict:
            src = req_data.get("result").get("sources", [{}])[0].get("file").replace("#.mp4", "")
            return  {'url': f'https://resp.streamflix.one/proxy/m3u8/{quote(src, safe="")}', 'source': 'VidsrcTo', 'proxy': 'True', 'lang': 'en', 'type': 'hls'}
        return 1401


    def get_tmdb_id(self, tmdb_id):
        return tmdb_id

    def fetch_sources(self, tmdb_id, season=None, episode=None):
        try:
            data_id = self.get_id(tmdb_id, season, episode)
            encrypted_source_url = self.get_encrypted_sources(data_id)

            standardized_input = encrypted_source_url.replace('_', '/').replace('-', '+')
            binary_data = base64.b64decode(standardized_input)

            encoded = bytearray(binary_data)

            # SPECIAL [KEY]
            key_bytes = bytes('8z5Ag5wgagfsOuhz', 'utf-8')
            j = 0
            s = bytearray(range(256))

            for i in range(256):
                j = (j + s[i] + key_bytes[i % len(key_bytes)]) & 0xff
                s[i], s[j] = s[j], s[i]

            decoded = bytearray(len(encoded))
            i = 0
            k = 0

            for index in range(len(encoded)):
                i = (i + 1) & 0xff
                k = (k + s[i]) & 0xff
                s[i], s[k] = s[k], s[i]
                t = (s[i] + s[k]) & 0xff
                decoded[index] = encoded[index] ^ s[t]

            decoded_text = decoded.decode('utf-8')
            unquoted_text = unquote(decoded_text)

            return self.handle_vidplay(unquoted_text)

        except Exception as e:
            return f"Error fetching sources: {e}"