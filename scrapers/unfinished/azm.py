import requests
import re
import random
import time


def make_play():
  characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
  random_string = ''.join(random.choice(characters) for _ in range(10))

  token = "n6lr02330qzmx57ewkqli2gv"
  expiry = int(time.time() * 1000)  # convert seconds to milliseconds

  return f"{random_string}?token={token}&expiry={expiry}"


url = "https://azm.to/live"
headers = {
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
    "Referrer-Policy": "strict-origin"
}

data = {"q": "the beekeeper"}

response = requests.post(url, headers=headers, data=data)

print(response.text)


html_response = response.text
pattern = r'<a href="(/movie/[^"]+)" class="result[^>]+>\s*<h2 class="result__title">\s*([^<]+)\s*</h2>'

# use regex
matches = re.findall(pattern, html_response)

# create a list of dictionaries to store the results
movies_list = [{"name": name.strip(), "link": link} for link, name in matches]

print(movies_list)

print("\n\n\n\n")

url = f"https://azm.to{movies_list[0]['link']}"
print(url)
response = requests.get(url, headers=headers)
html_response = response.text

pattern = r'https://d0o0d\.com/e/[^\'"]+'

match = re.search(pattern, html_response)

if match:
  d00d_url = match.group()
  print(f"d00d URL: {d00d_url}")
else:
  print("d00d URL not found in the HTML response.")
  exit()

url = d00d_url.replace("d0o0d.com", "d000d.com")

headers_d000d = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "accept-language": "en-GB,en;q=0.7",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "sec-ch-ua": "\"Chromium\";v=\"122\", \"Not(A:Brand\";v=\"24\", \"Brave\";v=\"122\"",
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": "\"Android\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "sec-gpc": "1",
    "upgrade-insecure-requests": "1",
    "cookie": "file_id=142189556; aff=6790; ref_url=; lang=1" # TODO extract from html
}

print(url)
response = requests.get(f"{url}", headers=headers_d000d)
html_response = response.text
print(html_response)
# define a regex pattern to match the md5 hash URL
pattern = re.compile(r"/pass_md5/([^'\"/]+)")
match = re.search(pattern, html_response)

if match:
  d00d_url = match.group()
  print(f"md5 URL: {d00d_url}")
else:
  print("md5 URL not found in the HTML response.")
  exit()

