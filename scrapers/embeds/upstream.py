import re
import requests
from scrapers.utils.unpacker import detect, unpack


class Upstream:
    def __init__(self, url):
        self.url = url
        self.domain = "upstream.to"
        self.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "accept-language": "en-GB,en;q=0.9",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "sec-ch-ua": "\"Brave\";v=\"123\", \"Not:A-Brand\";v=\"8\", \"Chromium\";v=\"123\"",
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "\"Android\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "sec-gpc": "1",
            "upgrade-insecure-requests": "1",
        }

    def make_request(self):
        if not self.url.startswith("https://" + self.domain + "/embed"):
            print(f"URL must start with 'https://{self.domain}/embe'")
            return None

        try:
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()
            print("Response Status Code:", response.status_code)
            return response.text
        except requests.exceptions.RequestException as e:
            print("Error making request:", e)
            return None

  
  
    def extract_source_url(self, input_string):
        pattern = r'sources:\[\{file:"(.*?)"\}\]'
        match = re.search(pattern, input_string)
        if match:
            return match.group(1)
        else:
            return None
        
    def unpack_html(self, html_content):
        if detect(html_content):
          print("Detected")
          unpacked = unpack(html_content)
          return self.extract_source_url(unpacked) 
        return None

    def main(self):
        html_content = self.make_request()
        if html_content:
            hls = self.unpack_html(html_content)
            return hls
        else:
            return None

# Example usage:
# upstream = Upstream("https://upstream.to/embed-wzkr7jkwl45f.html")
# url = upstream.main()
# print(url)

