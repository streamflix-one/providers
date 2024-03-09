import requests
from bs4 import BeautifulSoup
import time

def get_subtitles(tmdb_id, season=None, episode=None):
    start_time = time.time()  # Record the start time

    base_url = "https://vidsrc.to/embed/"

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "accept-language": "en-GB,en;q=0.9",
        "sec-ch-ua": "\"Chromium\";v=\"122\", \"Not(A:Brand\";v=\"24\", \"Brave\";v=\"122\"",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "sec-gpc": "1",
        "upgrade-insecure-requests": "1"
    }

    try:
        url = f"{base_url}tv/{tmdb_id}/{season}/{episode}" if season and episode else f"{base_url}movie/{tmdb_id}"

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the <a> element within the <li> element under the 'episodes' class
        a_element = soup.select_one('.episodes li a')

        # Extract the data-id attribute value
        if a_element:
            data_id = a_element.get('data-id')
            print(f"data-id value: {data_id}")

            # Send request to subtitles endpoint
            subtitles_url = f"https://vidsrc.to/ajax/embed/episode/{data_id}/subtitles"
            subtitles_response = requests.get(subtitles_url)
            subtitles_response.raise_for_status()

            subtitles_data = subtitles_response.json()

            end_time = time.time()  # Record the end time
            elapsed_time = end_time - start_time
            print(f"Fetching subtitles took {elapsed_time:.4f} seconds")

            return subtitles_data

        else:
            print("Could not find the data-id attribute")
            return []

    except requests.exceptions.RequestException as e:
        print(f"Error making the request: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []
