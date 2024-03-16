import re
import requests

class Uqload:
    def __init__(self, url):
        self.url = url.replace("uqload.co", "uqload.to")
        self.domain = "uqload.to"
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-GB,en;q=0.6",
            "Connection": "keep-alive",
            "Host": self.domain,
            "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Brave";v="122"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Sec-GPC": "1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        }

    def make_request(self):
        if not self.url.startswith("https://" + self.domain) or not self.url.endswith(".html"):
            print(f"URL must start with 'https://{self.domain}' and end with '.html'")
            return None

        try:
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()
            print("Response Status Code:", response.status_code)
            return response.text
        except requests.exceptions.RequestException as e:
            print("Error making request:", e)
            return None

    def extract_mp4_url(self, html_content):
        mp4_url_pattern = r'(?<=sources: \[")https://[^"]+\.mp4(?="\])'
        match = re.search(mp4_url_pattern, html_content)
        if match:
            return match.group(0)
        else:
            return None

    def main(self):
        html_content = self.make_request()
        if html_content:
            mp4_url = self.extract_mp4_url(html_content)
            return mp4_url
        else:
            return None

# uqload = Uqload("https://uqload.to/embed-j8u0gyunkxdb.html")
# mp4_url = uqload.main()
# print(mp4_url)