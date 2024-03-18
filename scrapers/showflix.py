import requests
from scrapers.embeds.streamwish import Streamwish

class Showflix:
    def __init__(self):
        self.headers = {
            "Accept": "*/*",
            "Accept-Language": "en-GB,en;q=0.9",
            "Connection": "keep-alive",
            "Content-Length": "257",
            "Content-Type": "text/plain",
            "Host": "parse.showflix.online",
            "Origin": "https://showflix.lol",
            "Referer": "https://showflix.lol/",
            "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Brave";v="122"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "Sec-GPC": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }

        self.url = "https://parse.showflix.online/parse/classes/movies"

    def fetch_sources(self, movie_name, user_ip):
        data = {
            "where": {
                "movieName": {
                    "$regex": movie_name,
                    "$options": "i"
                }
            },
            "order": "-updatedAt",
            "_method": "GET",
            "_ApplicationId": "SHOWFLIXAPPID",
            "_JavaScriptKey": "SHOWFLIXMASTERKEY",
            "_ClientVersion": "js3.4.1",
            "_InstallationId": "869613b0-4a8f-4a62-a8d1-6ed5e0282f1a"
        }

        try:
            response = requests.post(self.url, json=data, headers=self.headers)
            response.raise_for_status()  # Raise an error for bad response status codes
            json_data = response.json()

            if 'results' in json_data and len(json_data['results']) > 0:
                first_result = json_data['results'][0]
                streaming_ids = {
                    "streamlink": first_result.get("streamlink"),
                    "language": first_result.get("language"),
                    "hdlink": first_result.get("hdlink"),
                    "sharedisk": first_result.get("sharedisk"),
                    "streamhide": first_result.get("streamhide"),
                    "streamwish": first_result.get("streamwish"),
                    "filelions": first_result.get("filelions"),
                    "streamruby": first_result.get("streamruby"),
                    "uploadever": first_result.get("uploadever")
                }

                # Ensure streamwish key is not None before accessing it
                if streaming_ids.get('streamwish'):
                    showflix = Streamwish(f"https://embedwish.com/e/{streaming_ids['streamwish']}.html", user_ip)
                    hls_url = showflix.main()
                    return {'url': hls_url, 'source': 'ShowFlix', 'proxy': 'True', 'lang': streaming_ids['language'], 'type': 'hls'}
                else:
                    return "Streamwish link not found."
            else:
                return "Movie not found."
        except requests.exceptions.RequestException as e:
            print("Error fetching movie source:", e)
            return None

# Example usage:
# scraper = Showflix()
# movie_name = "Captain Miller"
# response_data = scraper.fetch_sources(movie_name)
# print(f"Movie URL: {response_data}")
