import requests
import re
import random
import string
import time

class AzmTo:
    def __init__(self):
        self.sitekey = "0x4AAAAAAALn0BYsCrtFUbm_" # dood site key
        self.invisible = True
        self.base_url = "https://azm.to/live" # website with dood urls, low protection asw
        self.headers = {
            "accept": "*/*",
            "accept-language": "en-GB,en;q=0.9",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "sec-ch-ua": "\"Not A(Brand\";v=\"99\", \"Brave\";v=\"121\", \"Chromium\";v=\"121\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "sec-gpc": "1",
            "x-requested-with": "XMLHttpRequest",
            "Referer": "https://azm.to/",
            "Referrer-Policy": "strict-origin",
        }

    def generate_random_string(self, length):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

    def solve_and_validate_captcha(self, url):
      sitekey = "0x4AAAAAAALn0BYsCrtFUbm_" # Doodstream site key
      invisible = True
  
      def solve_captcha(sitekey, invisible, url):
          endpoint = "https://turn.seized.live/solve"
  
          headers = {
              "Content-Type": "application/json",
          }
  
          data = {
              "sitekey": sitekey,
              "invisible": invisible,
              "url": url,
          }
  
          try:
              response = requests.post(endpoint, json=data, headers=headers)
  
              if response.status_code == 200:
                  return response.json()
              else:
                  print(f"Error: {response.status_code}, {response.text}")
                  return None
          except Exception as e:
              print(f"Error: {e}")
              return None
  
      captcha_result = solve_captcha(sitekey, invisible, url)
  
      if captcha_result:
          print(f"Captcha solved successfully! Token: {captcha_result['token']}")
      else:
          print("Failed to solve captcha.")
          return None
  
      token = captcha_result["token"]
  
      headers = {
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
          "Referer": "https://d0000d.com/",
          "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
          "Pragma": "no-cache",
          "Cache-Control": "no-cache"
      }
  
      print(url)
      response = requests.get(f"https://d0000d.com/dood?op=validate&gc_response={token}", headers=headers)
      html_response = response.text
  
      # You can return or process the html_response as needed
      return html_response

    def fetch_sources(self, user_ip, movie_name):
        data = {"q": movie_name}
        response = requests.post(self.base_url, headers=self.headers, data=data)

        html_response = response.text
        pattern = r'<a href="(/movie/[^"]+)" class="result[^>]+>\s*<h2 class="result__title">\s*([^<]+)\s*</h2>'
        matches = re.findall(pattern, html_response)

        movies_list = [{"name": name.strip(), "link": link} for link, name in matches]

        url = f"https://azm.to{movies_list[0]['link']}"
        response = requests.get(url, headers=self.headers)
        html_response = response.text

        match = re.search(r'https://d0o0d\.com/e/[^\'"]+', html_response)

        if match:
            d00d_url = match.group()
            print(f"d00d URL: {d00d_url}")
        else:
            print("d00d URL not found in the HTML response.")
            
            return None

        url = d00d_url.replace("d0o0d.com", "d0000d.com")
        base_url = url
        headers = {
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
            "Referer": url,
            "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "X-Requested-With": "XMLHttpRequest",
            "X-Forwarded-For": user_ip
  
        }

        response = requests.get(url, headers=headers)
        html_response = response.text

        match = re.search(r"\$\.get\('\/pass_md5([^']+)", html_response)

        if match:
            d00d_url = match.group().replace("$.get('", "")
            print(f"md5 URL: {d00d_url}")
        else:
            print("md5 URL not found in the HTML response, trying to solve captcha...")
            self.solve_and_validate_captcha(url)
            response = requests.get(url, headers=headers)
            html_response = response.text
            match = re.search(r"\$\.get\('\/pass_md5([^']+)", html_response)
            if match:
              d00d_url = match.group().replace("$.get('", "")
              print(f"md5 URL: {d00d_url}")
            else:
              return None

        data_for_later = re.search(r'\?token=([^&]+)&expiry=', html_response)
        if data_for_later:
            data_for_later = data_for_later.group(1)
            print(f"data_for_later: {data_for_later}")

        md5_url = f"https://d0000d.com{d00d_url}"
      
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-GB,en;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Cookie': 'lang=1',
            'Host': 'd0000d.com',
            'Pragma': 'no-cache',
            'Referer': base_url,
            'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Brave";v="122"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-GPC': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            "X-Forwarded-For": user_ip,
        }

        response = requests.get(md5_url, headers=headers)
        expiry_timestamp = int(time.time() * 1000)
        constructed_url = f"{response.text}{self.generate_random_string(10)}?token={data_for_later}&expiry={expiry_timestamp}"
        return  {'url': constructed_url, 'source': 'AzmTo', 'proxy': 'False', 'lang': 'en', 'type': 'mp4'}

# Example usage:
# scraper = AzmTo()
# user_ip = "86.16.28.244"
# movie_name = "the beekeeper"
# response_data = scraper.fetch_source(user_ip, movie_name)
# print(f"Movie URL: {response_data}")
