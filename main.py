from flask import Flask, request, jsonify
from flask_cors import CORS
import concurrent.futures
import time
from scrapers.vidsrcto import VidsrcTo
from scrapers.vidsrcme import VidSrcMe
from scrapers.filecdn import FileCDNScraper
from scrapers.dreamfilmsw import DreamFilmSW
from scrapers.frembed import FrEmbed
from scrapers.twoembed import TwoEmbed
from scrapers.azm import AzmTo
from scrapers.meinecloud import MeineCloud
from scrapers.vixcloud import VixCloud
from scrapers.showflix import Showflix
from scrapers.streamium import Streamium
from scrapers.subtitles import get_subtitles
from scrapers.downloads import Downloads
import requests


app = Flask(__name__)
CORS(app)

def get_ip(request):
    x_forwarded_for = request.headers.get('X-Forwarded-For')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
        return ip

    cf_connecting_ip = request.headers.get('CF-Connecting-IP')
    if cf_connecting_ip:
        return cf_connecting_ip

    return request.remote_addr


def get_movie_name(tmdb_movie_id):
    base_url = "https://api.themoviedb.org/3/movie/"
    api_key_param = f"?api_key=f1dd7f2494de60ef4946ea81fd5ebaba"

    start_time = time.time()  # Record the start time

    response = requests.get(f"{base_url}{tmdb_movie_id}{api_key_param}")

    end_time = time.time()  # Record the end time
    elapsed_time = end_time - start_time

    if response.status_code == 200:
        movie_data = response.json()
        print(f"Fetching movie name for TMDB ID {tmdb_movie_id} took {elapsed_time:.4f} seconds")
        return movie_data['title'], movie_data['release_date'].split("-")[0]
    else:
        print(f"Error: {response.status_code}. Fetching movie name for TMDB ID {tmdb_movie_id} took {elapsed_time:.4f} seconds")
        return f"Error: {response.status_code}"

def add_server_num(server_num, source):
    try:
        source['server'] = server_num
    except Exception as e:
        print(f"Error while adding server number {server_num} to source: {e}")
    return source


def scrape_sources(ip, tmdb_id, season=None, episode=None):
    start_time = time.time()  # Record the start time
    if season is None and episode is None:
        title, year = get_movie_name(tmdb_id)
    else:
        title, year = None, None    
    print(title)
    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []

            vidsrcto_scraper = VidsrcTo()
            futures.append(executor.submit(vidsrcto_scraper.fetch_sources, tmdb_id, season, episode))
            vidsrcme_scraper = VidSrcMe()
            futures.append(executor.submit(vidsrcme_scraper.fetch_sources, tmdb_id, season, episode))

            if season is None and episode is None:

                streamium_scraper = Streamium("f1dd7f2494de60ef4946ea81fd5ebaba")
                futures.append(executor.submit(streamium_scraper.fetch_sources, tmdb_id))

                meinecloud_scraper = MeineCloud(tmdb_api_key="f1dd7f2494de60ef4946ea81fd5ebaba")
                futures.append(executor.submit(meinecloud_scraper.fetch_sources, ip, tmdb_id))

                filecdn_movie_scraper = FileCDNScraper()
                futures.append(executor.submit(filecdn_movie_scraper.scrape_movie, tmdb_id))

                frembed_scraper = FrEmbed()
                futures.append(executor.submit(frembed_scraper.fetch_sources, tmdb_id, season, episode))

                vixcloud_scraper = VixCloud()
                futures.append(executor.submit(vixcloud_scraper.fetch_sources, title))

                twoembed_scraper = TwoEmbed()
                futures.append(executor.submit(twoembed_scraper.fetch_sources, tmdb_id, ip, season, episode))

                showflix_scraper = Showflix()
                futures.append(executor.submit(showflix_scraper.fetch_sources, title, ip))

                azmto_scraper = AzmTo()
                futures.append(executor.submit(azmto_scraper.fetch_sources, ip, title))
                
            else:
                filecdn_tv_show_scraper = FileCDNScraper()
                futures.append(executor.submit(filecdn_tv_show_scraper.scrape_tv_show, tmdb_id, season, episode))

            dreamfilmsw_scraper = DreamFilmSW()
            futures.append(executor.submit(dreamfilmsw_scraper.fetch_sources, tmdb_id, season, episode))

            concurrent.futures.wait(futures)

            sources = []
            server = 1
            for future in futures:
                try:
                    result = future.result()
                    if result:
                        # print(result)
                        sources.append(add_server_num(server, result))
                    server += 1    
                except Exception as e:
                    print(f"Error in scraper: {e}")
                    server += 1

            end_time = time.time() 
            elapsed_time = end_time - start_time
            print(f"Scraping for {len(sources)} sources took {elapsed_time:.2f} seconds")  # Print the elapsed time

            return sources

    except Exception as e:
        print(f"Error scraping sources: {e}")
        return None


@app.route('/api/sources/<tmdb_id>', methods=['GET'])
def scrape_movie_endpoint(tmdb_id):
    movie_name, year = get_movie_name(tmdb_id)
    start_time = time.time()
    ip = get_ip(request)

    if not tmdb_id:
        return "Error: TMDB ID is required.", 400
    dl_scraper = Downloads()
    sources = scrape_sources(ip, tmdb_id)
    downloads = dl_scraper.scrape_movies(movie_name, year)
    subtitles = get_subtitles(tmdb_id)
    formatted_json = {
        'sources': sources,
        'captions': subtitles,
        'downloads': downloads
    }
    end_time = time.time()  # record the end time
    elapsed_time = end_time - start_time
    print(f"Scraping for {len(sources)} sources and {len(subtitles)} subtitles took {elapsed_time:.2f} seconds")  # Print the elapsed time
    if sources:
        return jsonify(formatted_json)
    else:
        return "Error scraping sources.", 500

@app.route('/api/sources/<tmdb_id>/<season>/<episode>', methods=['GET'])
def scrape_tv_show_endpoint(tmdb_id, season, episode):
    start_time = time.time()
    ip = get_ip(request)

    if not tmdb_id:
        return "Error: TMDB ID is required.", 400

    sources = scrape_sources(ip, tmdb_id, season, episode)
    subtitles = get_subtitles(tmdb_id, season, episode)
    formatted_json = {
        'sources': sources,
        'captions': subtitles
    }
    end_time = time.time()  # record the end time
    elapsed_time = end_time - start_time
    print(f"Scraping for {len(sources)} sources and {len(subtitles)} subtitles took {elapsed_time:.2f} seconds")  # Print the elapsed time
    if sources:
        return jsonify(formatted_json)
    else:
        return "Error scraping sources.", 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
