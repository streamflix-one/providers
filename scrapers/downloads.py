import requests
from bs4 import BeautifulSoup

class Downloads:
    def __init__(self):
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-GB,en;q=0.9",
            "Connection": "keep-alive",
            "Host": "vadapav.mov",
            "sec-ch-ua": "\"Chromium\";v=\"122\", \"Not(A:Brand\";v=\"24\", \"Brave\";v=\"122\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Sec-GPC": "1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }
        self.base_url = "https://vadapav.mov"

    def fetch_download_info(self, url):
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            response_text = response.text
        else:
            return None, None

        soup = BeautifulSoup(response_text, 'html.parser')
        file_entries = soup.find_all('a', class_='file-entry wrap', href=True)

        for file_entry in file_entries:
            href = file_entry['href']
            file_name = file_entry.text
            if file_name.endswith('.mp4') or file_name.endswith('.mkv'):
                download_url = f'{self.base_url}{href}'
                return file_name, download_url
        return None, None

    def fetch_data(self, name, year):
        url = f"{self.base_url}/s/{name} ({year})"
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "accept-language": "en-GB,en;q=0.8",
            "cache-control": "max-age=0",
            "if-modified-since": "Wed, 13 Mar 2024 21:16:23 GMT",
            "sec-ch-ua": "\"Chromium\";v=\"122\", \"Not(A:Brand\";v=\"24\", \"Brave\";v=\"122\"",
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "\"Android\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "sec-gpc": "1",
            "upgrade-insecure-requests": "1",
            "Referer": f"{self.base_url}/",
            "Referrer-Policy": "strict-origin-when-cross-origin"
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.text
        else:
            return None

    def scrape_movies(self, name, year):
        data = self.fetch_data(name, year)
        if data:
            soup = BeautifulSoup(data, 'html.parser')
            movie_list = []

            for div in soup.find_all('div', class_='centerflex name-div'):
                link = div.find('a')['href']
                movie_name = div.find('a', class_='directory-entry wrap').text
                movie_list.append({'name': movie_name, 'link': link})

            movie_info_list = []
            for movie in movie_list:
                file_name, download_url = self.fetch_download_info(f"{self.base_url}{movie['link']}")
                if file_name and download_url:
                    movie_info_list.append({'file_name': file_name, 'download_url': download_url})

            return movie_info_list
        else:
            return None