import requests
from bs4 import BeautifulSoup
import json
import re

class VixCloud:
    def __init__(self):
        self.base_url = "https://streamingcommunity.report"
        self.headers = {
            'Accept': 'text/html, application/xhtml+xml',
            'Accept-Language': 'en-GB,en;q=0.8',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Host': 'streamingcommunity.report',
            'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Brave";v="122"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-GPC': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        }
        self.xsrf_token, self.session_cookie = self.fingerprint()

    def search(self, query):
        url = f"{self.base_url}/search?q={query}"
        headers_search = {
            'X-Inertia': 'true',
            'X-Inertia-Version': '9f1517b00147fb7ff43b935a25c2b654',
            'X-Requested-With': 'XMLHttpRequest',
            'X-XSRF-TOKEN': self.xsrf_token,
        }
        try:
            response = requests.get(url, headers={**self.headers, **headers_search})
            response.raise_for_status()
            return response.json()['props']['titles'][0]['id']
        except requests.exceptions.RequestException as e:
            # print(f"Error sending request: {e}")
            return None

    def extract_video_info(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        script_tag = soup.find('script', string=lambda s: s and 'window.masterPlaylist =' in s)

        if script_tag:
            script_content = script_tag.string
            match = re.search(r'window\.masterPlaylist\s*=\s*{[^}]*}', script_content, re.DOTALL)

            if match:
                json_content = match.group(0).split('params:')[1]
                params_json_content = re.sub(r'\s+', '', json_content)
                json_content = params_json_content.replace("'", "\"")
                json_content = re.sub(r',\s*}', '}', json_content)
                try:
                    master_playlist_info = json.loads(json_content)
                    return master_playlist_info
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
                    return None
            else:
                print("Error extracting master playlist information.")
                return None
        else:
            print("Script tag containing master playlist information not found.")
            return None

    def get_iframe_src(self, url):
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-GB,en;q=0.8",
            "Connection": "keep-alive",
            "Host": "vixcloud.co",
            "Referer": "https://streamingcommunity.report/",
            "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Brave";v="122"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "Sec-Fetch-Dest": "iframe",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "cross-site",
            "Sec-GPC": "1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            # print("Request successful")
            return response.text
        else:
            print(f"Request failed with status code {response.status_code}")
            return None

    def extract_iframe_src(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        iframe_tag = soup.find('iframe', {'src': True})

        if iframe_tag:
            return iframe_tag['src']
        else:
            return None

    def send_api_request(self, start_id):
        url = f"https://streamingcommunity.report/iframe/{start_id}"
        # print(url)
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-GB,en;q=0.8",
            "Connection": "keep-alive",
            "Host": "streamingcommunity.report",
            "Referer": "https://streamingcommunity.report/watch/6814",
            "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Brave";v="122"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-GPC": "1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        }

        headers["Cookie"] = f"XSRF-TOKEN={self.xsrf_token}; streamingcommunity_session={self.session_cookie}"

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            # print("API Request successful")
            return response.text
        else:
            print(f"API Request failed with status code {response.status_code}")
            return None

    def fingerprint(self):
        url = "https://streamingcommunity.report/watch/6814"
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-GB,en;q=0.8",
            "Connection": "keep-alive",
            "Host": "streamingcommunity.report",
            "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Brave";v="122"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-GPC": "1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            # print("Fingerprinting successful")

            xsrf_token_cookie = response.cookies.get("XSRF-TOKEN")
            streamingcommunity_session_cookie = response.cookies.get("streamingcommunity_session")

            # print(f"XSRF-TOKEN: {xsrf_token_cookie}")
            # print(f"streamingcommunity_session: {streamingcommunity_session_cookie}")

            return xsrf_token_cookie, streamingcommunity_session_cookie
        else:
            print(f"Request failed with status code {response.status_code}")
            return None, None

    def construct_video_url(self, base_url, video_info):
        url = f"{base_url}?token={video_info['token']}&token480p={video_info['token480p']}&token720p={video_info['token720p']}&token1080p={video_info['token1080p']}&expires={video_info['expires']}"
        return url

    def fetch_sources(self, tmdb_id):
        start_id = self.search(str(tmdb_id))
        response_data = self.send_api_request(start_id)
        iframe = self.extract_iframe_src(response_data)
        videoid = iframe.split('/embed/')[1].split('?')[0]
        response_html = self.get_iframe_src(iframe)
        stream_info = self.extract_video_info(response_html)
        video_url = self.construct_video_url(f'https://vixcloud.co/playlist/{videoid}', stream_info)
        return video_url


# Example usage:
# scraper = VixCloud()
# response_data = scraper.fetch_sources("Barbie")
# # print(f"Movie URL: {response_data}")
