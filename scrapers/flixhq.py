import requests
from bs4 import BeautifulSoup
import re

# WARNING SOURCES ARE ENCRYPTED AND KEYS ARE IP LOCKED SO YOU NEED TO HOST YOUR OWN KEY EXTRACTOR ON THE SAME IP AS UR SCRAPER

class FlixHQMovies:
    def __init__(self):
        self.base_url = "https://flixhq.to"
        self.headers = {
            "Accept": "*/*",
            "accept-language": "en-GB,en;q=0.8",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": "prefetchAd_6186241=true; _ga_SLT5RHZ3PC=GS1.1.1708987327.1.0.1708987327.0.0.0; _ga=GA1.1.1942035551.1708987327",
            "Host": "flixhq.to",
            "Origin": "https://flixhq.to",
            "Referer": "https://flixhq.to/",
            "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Brave";v="122"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Sec-GPC": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }

    def make_post_request(self, keyword):
        url = f"{self.base_url}/ajax/search"
        data = {"keyword": keyword}
        response = requests.post(url, headers=self.headers, data=data)
        if response.status_code == 200:
            return response.text
        else:
            return f"Failed to fetch data: {response.status_code}"

    def get_upcloud_and_vidcloud_id(self, id):
        url = f"{self.base_url}/ajax/episode/list/{id}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.text
        else:
            return f"Failed to fetch data: {response.status_code}"

    def get_rabbitstream_embed(self, id):
        url = f"{self.base_url}/ajax/episode/sources/{id}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            return f"Failed to fetch data: {response.status_code}"

    def extract_number_from_url(self, url):
        return re.search(r'\d+$', url).group()



    def fetch_source_data(self, id):
        url = f"https://rabbitstream.net/ajax/v2/embed-4/getSources?id={id}&v=30061&h=cee6762ddfab4706a1045c519fdbc047ed85a4fe&b=1878522368"
        headers = {
            "accept": "*/*",
            "accept-language": "en-GB,en;q=0.8",
            "sec-ch-ua": "\"Not A(Brand\";v=\"99\", \"Brave\";v=\"121\", \"Chromium\";v=\"121\"",
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "\"Android\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "sec-gpc": "1",
            "Host": "rabbitstream.net",
            "Referer": f"https://rabbitstream.net/v2/embed-4/{id}?z=",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()  # If the response is JSON
        else:
            return "Failed to fetch data: " + str(response.status_code)

    def fetch_sources(self, keyword):
        def extract_id_from_link(link):
          if "rabbitstream.net" in link:
              start_index = link.find("/embed-4/") + len("/embed-4/")
              end_index = link.find("?z=")
              if start_index != -1 and end_index != -1:
                  return link[start_index:end_index]
          return None
        response_data = self.make_post_request(keyword)
        soup = BeautifulSoup(response_data, 'html.parser')
        first_url = soup.find('a', class_='nav-item')['href']
        number = self.extract_number_from_url(first_url)
        get_ids_content = self.get_upcloud_and_vidcloud_id(number)
        soup = BeautifulSoup(get_ids_content, 'html.parser')
        links = soup.find_all('a', class_='nav-link')
        numbers = [self.extract_number_from_url(link['href']) for link in links]
        sources = []
        for number in numbers:
            response_data = self.get_rabbitstream_embed(number)
            # print(response_data)
            rabbitstream_id = extract_id_from_link(response_data["link"])
            resp = self.fetch_source_data(rabbitstream_id)
            # print(resp)
            sources.append(resp)
        return sources


class FlixHQTvShows:
  def __init__(self):
      self.headers = {
          "Accept": "*/*",
          "accept-language": "en-GB,en;q=0.8",
          "Connection": "keep-alive",
          "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
          "Cookie": "prefetchAd_6186241=true; _ga_SLT5RHZ3PC=GS1.1.1708987327.1.0.1708987327.0.0.0; _ga=GA1.1.1942035551.1708987327",
          "Host": "flixhq.to",
          "Origin": "https://flixhq.to",
          "Referer": "https://flixhq.to/",
          "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Brave";v="122"',
          "sec-ch-ua-mobile": "?0",
          "sec-ch-ua-platform": '"Windows"',
          "Sec-Fetch-Dest": "empty",
          "Sec-Fetch-Mode": "cors",
          "Sec-Fetch-Site": "same-origin",
          "Sec-GPC": "1",
          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
          "X-Requested-With": "XMLHttpRequest"
      }

  def make_post_request(self, keyword):
      url = "https://flixhq.to/ajax/search"
      data = {"keyword": keyword}
      response = requests.post(url, headers=self.headers, data=data)
      if response.status_code == 200:
          return response.text
      else:
          return f"Failed to fetch data: {response.status_code}"

  def get_upcloud_and_vidcloud_id(self, id):
      url = f"https://flixhq.to/ajax/season/list/{id}"
      response = requests.get(url, headers=self.headers)
      if response.status_code == 200:
          return response.text
      else:
          return f"Failed to fetch data: {response.status_code}"

  def get_episodes(self, id):
      url = f"https://flixhq.to/ajax/season/episodes/{id}"
      response = requests.get(url, headers=self.headers)
      if response.status_code == 200:
          return response.text
      else:
          return f"Failed to fetch data: {response.status_code}"

  def get_episode_servers(self, id):
      url = f"https://flixhq.to/ajax/episode/servers/{id}"
      response = requests.get(url, headers=self.headers)
      if response.status_code == 200:
          return response.text
      else:
          return f"Failed to fetch data: {response.status_code}"

  def get_rabbitstream_embed(self, id):
      url = f"https://flixhq.to/ajax/episode/sources/{id}"
      response = requests.get(url, headers=self.headers)
      if response.status_code == 200:
          return response.json()
      else:
          return f"Failed to fetch data: {response.status_code}"

  def fetch_source_data(self, link):
      # Function to extract ID from the link
      def extract_id_from_link(link):
          if "rabbitstream.net" in link:
              start_index = link.find("/embed-4/") + len("/embed-4/")
              end_index = link.find("?z=")
              if start_index != -1 and end_index != -1:
                  return link[start_index:end_index]
          return None

      # Extract ID from the link
      id = extract_id_from_link(link)

      # If ID is extracted successfully
      if id:
            url = f"https://rabbitstream.net/ajax/v2/embed-4/getSources?id={id}&v=30061&h=cee6762ddfab4706a1045c519fdbc047ed85a4fe&b=1878522368"
            headers = {
                "accept": "*/*",
                "accept-language": "en-GB,en;q=0.8",
                "sec-ch-ua": "\"Not A(Brand\";v=\"99\", \"Brave\";v=\"121\", \"Chromium\";v=\"121\"",
                "sec-ch-ua-mobile": "?1",
                "sec-ch-ua-platform": "\"Android\"",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-site",
                "sec-gpc": "1",
                "Host": "rabbitstream.net",
                "Referer": f"https://rabbitstream.net/v2/embed-4/{id}?z=",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest"
            }


            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                return response.json()  # If the response is JSON
            else:
                return f"Failed to fetch data: {response.status_code}"
      else:
          return "Failed to extract ID from the link"

  def fetch_sources(self, keyword, season, episode):
      response_data = self.make_post_request(keyword)
      soup = BeautifulSoup(response_data, 'html.parser')
      first_url = soup.find('a', class_='nav-item')['href']
      number = re.search(r'\d+$', first_url).group()

      get_ids_content = self.get_upcloud_and_vidcloud_id(number)
      soup = BeautifulSoup(get_ids_content, 'html.parser')
      season_links = soup.find_all('a', class_='ss-item')
      season_ids = {}
      for link in season_links:
          season_id = link['data-id']
          season_number = link.text.strip().split()[-1]
          season_ids[season_number] = season_id

      season_id = season_ids[str(season)]
      episodes_content = self.get_episodes(season_id)
      soup = BeautifulSoup(episodes_content, 'html.parser')
      episode_links = soup.find_all('a', class_='eps-item')
      episode_info = {}
      for link in episode_links:
          episode_id = link['data-id']
          episode_title = link.text.strip()
          episode_number = episode_title.split(':')[0].split()[-1]
          episode_info[episode_number] = episode_id

      episode_id = episode_info[str(episode)]
      episode_servers_content = self.get_episode_servers(episode_id)
      soup = BeautifulSoup(episode_servers_content, 'html.parser')
      link_items = soup.find_all('a', class_='link-item')
      server_ids = []
      for item in link_items:
          server_id = item['data-id']
          server_ids.append(server_id)

      sources = []
      for server_id in server_ids:
          rabbitstream_embed_content = self.get_rabbitstream_embed(server_id)
          res = self.fetch_source_data(rabbitstream_embed_content["link"])
          sources.append(res)

      return sources



