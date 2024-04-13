import requests
import re

class Streamwish:
    def __init__(self, url, ip):
        self.url = url
        self.user_ip = ip

    def main(self):
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-GB,en;q=0.9",
            "Connection": "keep-alive",
            "Host": f"{self.url.split('/e/')[0].strip('https://')}",
            "Referer": "https://showflix.lol/", # showflix for everything cause why not 
            "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Brave";v="122"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "Sec-Fetch-Dest": "iframe",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-User": "?1",
            "Sec-GPC": "1",
            "Upgrade-Insecure-Requests": "1",
            "X-Forwarded-For": self.user_ip,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }

        response = requests.get(self.url, headers=headers)
        html_content = response.text
        m3u8_url_match = re.search(r'sources: \[\{[^}]*file:\s*"([^"]+)"[^}]*\}\]', html_content)
        if m3u8_url_match:
            m3u8_url = m3u8_url_match.group(1)
            return m3u8_url
        else:
            return None

