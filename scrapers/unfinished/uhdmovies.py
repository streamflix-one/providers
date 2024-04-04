# No movie fetching logic yet- just the redirect scraper
# Starting to clean up code

import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import quote

class UHDRedirectScraper:
    def __init__(self):
        pass

    @staticmethod
    def parse_redirect_page(html):
        pattern = r'<meta\s+http-equiv="refresh"\s+content="0;url=(.*?)"\s*/?>'
        match = re.search(pattern, html)
        if match:
            redirect_url = match.group(1)
            return redirect_url
        else:
            return None

    @staticmethod
    def make_post_request(_wp_http):
        url = "https://tech.unblockedgames.world/"
        payload = {"_wp_http": _wp_http}
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-GB,en;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "tech.unblockedgames.world",
            "Origin": "null",
            "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Brave";v="122"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-GPC": "1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        }
        response = requests.post(url, data=payload, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        form = soup.find('form', id='landing')
        action_url = form['action']
        _wp_http2 = form.find('input', {'name': '_wp_http2'})['value']
        token = form.find('input', {'name': 'token'})['value']
        return action_url, _wp_http2, token

    @staticmethod
    def get_pepe_url(action_url, _wp_http2, token):
        url = action_url
        payload = {"_wp_http2": _wp_http2, "token": token}
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-GB,en;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "tech.unblockedgames.world",
            "Origin": "https://tech.unblockedgames.world",
            "Referer": "https://tech.unblockedgames.world/",
            "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Brave";v="122"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Sec-GPC": "1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        }
        response = requests.post(url, data=payload, headers=headers)
        return response.text

    @staticmethod
    def get_match(resp):
        pattern = r'https://tech\.unblockedgames\.world/\?go=[^"]+'
        matches = re.findall(pattern, resp)
        return matches

    @staticmethod
    def make_get_request(url, cookies, ref):
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-GB,en;q=0.8",
            "Connection": "keep-alive",
            "Host": "tech.unblockedgames.world",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Sec-GPC": "1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Referrer": ref,
            "Cookie": "; ".join([f"{key}={value}" for key, value in cookies.items()]),
        }
        response = requests.get(url, headers=headers, allow_redirects=True)
        return response.text

# Example usage:
url = "https://tech.unblockedgames.world/?sid=bnpxOTF5Uk9VOVFZM2lEMkxXUmp0Y1dhWTZGUU8vUkluNmtDZ0FITDhrL0tBSDVUTEdWTmdBNnpPajczek1EQ2lkYXc1b0IzQTJnc1MrbUhRRjJ3cU1Nc0pEYXNuNmwwcmNzMDJRVHZhd1BNMmtpV1RrRHE0dGxML3hHZEhKaGFjN1g4VWsvai9DTkV3a0JCT01ZZENnazVrdk9WV0Ixa2xYTVVLUWQ0aGtBM3d1RHBDQnJ4ZGVWd2xNcDBrRTlJbFJsb2ExT3ArMVpkZWlTb3JiUVh3TTN4MzVubE5Tem9kcnJQYlNsVU80VnU1WCtuWG82Ry9Qcy9OK25tdWZHTA=="
_wp_http = url.split('?sid=')[1]
scraper = UHDRedirectScraper()
action_url, _wp_http2, token = scraper.make_post_request(_wp_http)
print("Action URL:", action_url)
print("_wp_http2:", _wp_http2)
print("Token:", token)
print()

resp = scraper.get_pepe_url(action_url, _wp_http2, token)
matches = scraper.get_match(resp)
print(matches)
print()

pepe_url = matches[0]
cookies = {
    "__eoi": "ID=4a86dd07e2cfa744:T=1710970060:RT=1710970060:S=AA-AfjbVJgiJ3UbrHbBiGQPwwxlA",
    "__qca": "P0-1796148875-1710970059080",
}

if '?go=' in pepe_url:
    key = str(pepe_url.split('?go=')[1])
    cookies[key] = _wp_http2

print(cookies)
response = scraper.make_get_request(pepe_url, cookies, action_url)
final_url = scraper.parse_redirect_page(response)
print(final_url)

def get_zfile(url):
  headers = {
      "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
      "Accept-Language": "en-GB,en;q=0.8",
      "Cache-Control": "max-age=0",
      "Connection": "keep-alive",
      "Content-Type": "application/x-www-form-urlencoded",
      "Host": "driveleech.org",
      "Origin": "https://driveleech.org",
      "Referer": "https://driveleech.org/",
      "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Brave";v="122"',
      "sec-ch-ua-mobile": "?0",
      "sec-ch-ua-platform": '"Windows"',
      "Sec-Fetch-Dest": "document",
      "Sec-Fetch-Mode": "navigate",
      "Sec-Fetch-Site": "same-origin",
      "Sec-Fetch-User": "?1",
      "Sec-GPC": "1",
      "Upgrade-Insecure-Requests": "1",
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
  }
  
  driveleech = requests.get(final_url, headers=headers, allow_redirects=True)
  
  print(driveleech.text)
  pattern = r'/file/([a-zA-Z0-9]+)'

  matches = re.search(pattern, driveleech.text)

  if matches:
      file_id = matches.group(1)
      print("File ID:", file_id)
      return file_id
  else:
      print("File ID not found.")
      return None

file_id = get_zfile(final_url)

def get_mkv(id):
  headers = {
      "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
      "Accept-Language": "en-GB,en;q=0.8",
      "Cache-Control": "max-age=0",
      "Connection": "keep-alive",
      "Content-Type": "application/x-www-form-urlencoded",
      "Host": "driveleech.org",
      "Origin": "https://driveleech.org",
      "Referer": "https://driveleech.org/",
      "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Brave";v="122"',
      "sec-ch-ua-mobile": "?0",
      "sec-ch-ua-platform": '"Windows"',
      "Sec-Fetch-Dest": "document",
      "Sec-Fetch-Mode": "navigate",
      "Sec-Fetch-Site": "same-origin",
      "Sec-Fetch-User": "?1",
      "Sec-GPC": "1",
      "Upgrade-Insecure-Requests": "1",
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
  }

  driveleech = requests.get(f"https://driveleech.org/zfile/{id}", headers=headers, allow_redirects=True)
  
  
  soup = BeautifulSoup(driveleech.text, 'html.parser')
  links = soup.find_all('a', href=True)
  print(links)
  for link in links:
      href_link = link['href']
      if href_link.endswith(".mkv"):
          print("Extracted Href Link ending in .mkv")
        
          url_safe = quote(href_link.split('/')[-1], safe='')
          print("URL with spaces replaced by URL safe characters:")
          print(href_link.replace(href_link.split('/')[-1], url_safe))
          return href_link.replace(href_link.split('/')[-1], url_safe)


def get_video_proxy(id):
  headers = {
      "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
      "Accept-Language": "en-GB,en;q=0.8",
      "Cache-Control": "max-age=0",
      "Connection": "keep-alive",
      "Content-Type": "application/x-www-form-urlencoded",
      "Host": "driveleech.org",
      "Origin": "https://driveleech.org",
      "Referer": "https://driveleech.org/",
      "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Brave";v="122"',
      "sec-ch-ua-mobile": "?0",
      "sec-ch-ua-platform": '"Windows"',
      "Sec-Fetch-Dest": "document",
      "Sec-Fetch-Mode": "navigate",
      "Sec-Fetch-Site": "same-origin",
      "Sec-Fetch-User": "?1",
      "Sec-GPC": "1",
      "Upgrade-Insecure-Requests": "1",
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
  }

  driveleech = requests.get(f"https://driveleech.org/file/{id}", headers=headers, allow_redirects=True)


  soup = BeautifulSoup(driveleech.text, 'html.parser')
  links = soup.find_all('a', href=True)
  print(links)
  for link in links:
      href_link = link['href']
      if href_link.startswith("https://video-proxy.xyz/"):
          print("Extracted video-proxy url")


          return href_link



import random
import string

def generate_boundary():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

def fetch_data_v(key):
    url = "https://video-proxy.xyz/api"

    # Generate a random boundary string
    boundary = generate_boundary()

    headers = {
        "accept": "*/*",
        "accept-language": "en-GB,en;q=0.6",
        "content-type": f"multipart/form-data; boundary=----WebKitFormBoundary{boundary}",
        "sec-ch-ua": "\"Chromium\";v=\"122\", \"Not(A:Brand\";v=\"24\", \"Brave\";v=\"122\"",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-gpc": "1",
        "x-token": "video-proxy.xyz",
        "Referer": f"https://video-proxy.xyz/?url={key}",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }
    body = {
        "keys": key
    }

    response = requests.post(url, headers=headers, data=body)

    if response.status_code == 200:
        return response.json()
    else:
        return None
  
res = get_mkv(file_id)
if res is None:
  print("No mkv found, trying Instant Download")
  res = get_video_proxy(file_id)
  if res is None:
    print("No video proxy found")
    res = None
  else:
    res = fetch_data_v(res.split('?url=')[1])

print(res)