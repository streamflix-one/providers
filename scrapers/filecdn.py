import requests
import re

class FileCDNScraper:
    def scrape_movie(self, tmdb_id):
        url = f'https://www.filecdn.cloud/e/tmdb{tmdb_id}dub'
        return self._scrape(url)

    def scrape_tv_show(self, tmdb_id, season, episode):
        url = f'https://www.filecdn.cloud/e/tvtmdb{tmdb_id}t{season}e{episode}dub'
        return self._scrape(url)

    def _scrape(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            iframe_match = re.search(r'<iframe src="(.*?)"', response.text)
            if iframe_match:
                iframe_source = iframe_match.group(1)
                return self._get_mp4_url(iframe_source)
            else:
                print("Could not find iframe source.")
        else:
            print(f"Failed to retrieve content. Status code: {response.status_code}")

    def _get_mp4_url(self, iframe_source):
        response = requests.get(iframe_source)
        if response.status_code == 200:
            mp4_match = re.search(r'<source src="(.*?)" type="video/mp4">', response.text)
            if mp4_match:
                mp4_url = mp4_match.group(1)
                return mp4_url
            else:
                print("Could not find MP4 URL.")
        else:
            print(f"Failed to retrieve content. Status code: {response.status_code}")

# Example usage:
# scraper = FileCDNScraper()
# movie_url = scraper.scrape_movie(872585)
# print("Movie URL:", movie_url)

# tv_show_url = scraper.scrape_tv_show(108978, 1, 1)
# print("TV Show URL:", tv_show_url)
