import requests
import re
import base64
from bs4 import BeautifulSoup

# Love to Ciarands for a tonne of the logic

class VidSrcMe:
    def __init__(self):
        pass

    def decode_src(self, encoded, seed):
        encoded_buffer = bytes.fromhex(encoded)
        decoded = ""
        for i in range(len(encoded_buffer)):
            decoded += chr(encoded_buffer[i] ^ ord(seed[i % len(seed)]))
        return decoded

    def decode_base64_url_safe(self, s):
        standardized_input = s.replace('_', '/').replace('-', '+')
        binary_data = base64.b64decode(standardized_input)
        return bytearray(binary_data)

    def decode_hls_url(self, encoded_url):
        def format_hls_b64(data):
            encoded_b64 = re.sub(r"\/@#@\/[^=\/]+==", "", data)
            if re.search(r"\/@#@\/[^=\/]+==", encoded_b64):
                return format_hls_b64(encoded_b64)
            return encoded_b64

        formatted_b64 = format_hls_b64(encoded_url[2:])
        b64_data = self.decode_base64_url_safe(formatted_b64)
        return b64_data.decode("utf-8")

    def resolve_source(self, url, referrer):
        req = requests.get(url, headers={"Referer": referrer})
        if req.status_code != 200:
            print(f"[Vidsrc] Failed to retrieve media, status code: {req.status_code}...")
            return None

        encoded_hls_url = re.search(r'file:"([^"]*)"', req.text)
        hls_password_url = re.search(r'var pass_path = "(.*?)";', req.text)

        if not encoded_hls_url or not hls_password_url:
            print("[Vidsrc] Failed to extract hls or password url...")
            return None

        hls_password_url = hls_password_url.group(1)
        if hls_password_url.startswith("//"):
            hls_password_url = f"https:{hls_password_url}"

        hls_url = self.decode_hls_url(encoded_hls_url.group(1))
        requests.get(hls_password_url, headers={"Referer": referrer})

        return hls_url
        
    def fetch_sources(self, tmdb_id, season=None, episode=None):
        if season is None and episode is None:
          url = f"https://vidsrc.xyz/embed/movie/{tmdb_id}"
        else:
          url = f"https://vidsrc.xyz/embed/tv/{tmdb_id}/{season}-{episode}"
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-GB,en;q=0.6",
            "Connection": "keep-alive",
            "Host": "vidsrc.xyz",
            "sec-ch-ua": '"Brave";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Sec-GPC": "1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        }

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"[Vidsrc] Failed to fetch sources, status code: {response.status_code}")
            return None

        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        iframe_tag = soup.find('iframe', id='player_iframe')
        iframe_src = f"https:{iframe_tag['src']}"
        print(iframe_src)
        src = self.fetch(iframe_src)
        soup = BeautifulSoup(src, 'html.parser')
        cf_turnstile_div = soup.find('div', class_='cf-turnstile', attrs={'data-sitekey': '0x4AAAAAAATD6DukOTUdZEnE', 'data-callback': 'cftCallback'})

        if cf_turnstile_div:
            print("Found cf-turnstile div. Executing turnstile solver...")
            body = {
              "sitekey": "0x4AAAAAAATD6DukOTUdZEnE",
              "url": iframe_src,
              "invisible": True
            }
            r = requests.post("https://turn.seized.live/solve", json=body)
            token = r.json()["token"]
            print("Solved :: " + token)
            rcp_verify_result = self.rcp_verify(iframe_src, token)
            if not rcp_verify_result:
                print("Failed to verify captcha.")
                return None

            src = self.fetch(iframe_src)

        # soup = BeautifulSoup(src, "html.parser")
        # encoded = soup.find("div", {"id": "hidden"}).get("data-h")
        # seed = soup.find("body").get("data-i")

        # source = self.decode_src(encoded, seed)
        match = re.search(r"src:\s*'([^']+)'", src)
  
        if match:
            source = match.group(1)
            print("Source URL:", source)
        else:
            print("Source URL not found.")
            source = ""
        if source.startswith("//"):
            source = f"https:{source}"

        req = requests.get(source, allow_redirects=False, headers={"Referer": "https://vidsrc.stream/"})

        prorcp = req.headers.get("location")

        final = self.resolve_source(url=prorcp, referrer=iframe_src)

        return {'url': final, 'source': 'VidSrcMe', 'proxy': 'False', 'lang': 'en', 'type': 'hls'}

    def fetch(self, url):
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-GB,en;q=0.6",
            "Connection": "keep-alive",
            "Host": "vidsrc.stream",
            "Referer": "https://vidsrc.xyz/",
            "sec-ch-ua": '"Brave";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "Sec-Fetch-Dest": "iframe",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "cross-site",
            "Sec-GPC": "1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        return response.text

    def rcp_verify(self, referer, token):
        url = "https://vidsrc.stream/rcp_verify"
        headers = {
            "Accept": "*/*",
            "Accept-Language": "en-GB,en;q=0.6",
            "Connection": "keep-alive",
            "Content-Length": "544",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Host": "vidsrc.stream",
            "Origin": "https://vidsrc.stream",
            "Referer": referer,
            "sec-ch-ua": '"Brave";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Sec-GPC": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }

        data = {"token": token}
        response = requests.post(url, data=data, headers=headers)
        if response.status_code == 200:
            result = response.text
            print(result)
            if result == "1":
                print("Captcha solved successfully!")
                return True
            else:
                print("Result length is not 1, scraping failed.")
                return False
        else:
            print("Failed to make POST request:", response.status_code)


# scraper = Vidsrc()
# response_data = scraper.fetch_sources(tmdb_id="1399", season="1", episode="1")
# print(f"URL: {response_data}")
