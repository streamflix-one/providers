import requests
import re
import random
import string
import time

class Doodstream:
    def __init__(self, doodstream_url, my_ip):
        self.doodstream_url = doodstream_url
        self.url = doodstream_url.replace("d0o0d.com", "d0000d.com")
        self.my_ip = my_ip

        self.base_headers = {
            "Host": "d0000d.com",
            "Connection": "keep-alive",
            "sec-ch-ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"",
            "DNT": "1",
            "sec-ch-ua-mobile": "?0",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "sec-ch-ua-platform": "\"macOS\"",
            "Accept": "*/*",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-Mode": "no-cors",
            "Sec-Fetch-Dest": "video",
            "Referer": self.url,
            "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "X-Requested-With": "XMLHttpRequest",
            "X-Forwarded-For": self.my_ip
        }

        self.md5_headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-GB,en;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Cookie': 'lang=1',
            'Host': 'd0000d.com',
            'Pragma': 'no-cache',
            'Referer': self.url,
            'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Brave";v="122"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-GPC': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            "X-Forwarded-For": self.my_ip,
        }

    def generate_random_string(self, length):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

    def solve_captcha(self):
        endpoint = "https://turn.seized.live/solve"
        headers = {"Content-Type": "application/json"}
        data = {"sitekey": "0x4AAAAAAALn0BYsCrtFUbm_", "invisible": True, "url": self.url}

        try:
            response = requests.post(endpoint, json=data, headers=headers)

            if response.status_code == 200:
                print(f"captcha solved: {response.json()}")
                verify = self.validate_captcha(response.json()["token"])
                return response.json()
            else:
                print(f"Error: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"Error: {e}")

        return None

    def validate_captcha(self, token):
        headers = self.base_headers.copy()
        response = requests.get(f"https://d0000d.com/dood?op=validate&gc_response={token}", headers=headers)
        return response.text

    def extract_md5_url(self, html_response):
        match = re.search(r"\$\.get\('\/pass_md5([^']+)", html_response)
        return match.group().replace("$.get('", "") if match else None

    def get_data_for_later(self, html_response):
        data_for_later = re.search(r'\?token=([^&]+)&expiry=', html_response)
        return data_for_later.group(1) if data_for_later else None

    def main(self):
        response = requests.get(f"{self.url}", headers=self.base_headers)
        html_response = response.text
        print("extracting md5 url")
        md5_url = self.extract_md5_url(html_response)
  
        if md5_url is None:
            print("solving captcha")
            html_response = self.solve_captcha()
            response = requests.get(f"{self.url}", headers=self.base_headers)
            html_response = response.text
            md5_url = self.extract_md5_url(html_response)

            if md5_url is None:
                exit()
              
        print("md5 extracted")
        data_for_later = self.get_data_for_later(html_response)

        md5_url = f"https://d0000d.com{md5_url}"

        response = requests.get(f"{md5_url}", headers=self.md5_headers)
        expiry_timestamp = int(time.time() * 1000)

        constructed_url = f"{response.text}{self.generate_random_string(10)}?token={data_for_later}&expiry={expiry_timestamp}#.mp4"
        # print(constructed_url)
        return constructed_url
