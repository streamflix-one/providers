<p align="center">
  <img src="/assets/logo.webp" alt="StreamFlix Providers" width="300"/>
</p>



**StreamFlix Providers**

StreamFlix Providers is a collection of scraper scripts that fetch streaming URLs from various online streaming platforms. These scripts allow you to extract video URLs from platforms like FileCDN and Vidsrc.to, facilitating the process of integrating streaming functionality into your applications or projects.


## Features

- **Streaming URL Retrieval**: Fetch streaming URLs from popular online streaming platforms.
- **Subtitle Support**: Retrieve subtitles for movies and TV shows.
- **Download Options**: Provide direct download links for content.
- **Scalable and Efficient**: Designed to handle multiple requests with minimal latency.

## Getting Started

### Installation

To use StreamFlix API, follow these steps:

1. Clone this repository to your local machine.
2. Install the required dependencies by running `pip install -r requirements.txt`.
3. Run the Flask server using `python3 main.py`.

### Usage

#### Fetching Streaming URLs for Movies

To fetch streaming URLs for a movie, make a GET request to the `/api/sources/<tmdb_id>` endpoint, where `<tmdb_id>` is the TMDB ID of the movie.

Example:

```http
GET /api/sources/12345
```

#### Fetching Streaming URLs for TV Shows

To fetch streaming URLs for a TV show episode, make a GET request to the `/api/sources/<tmdb_id>/<season>/<episode>` endpoint, where `<tmdb_id>` is the TMDB ID of the TV show, `<season>` is the season number, and `<episode>` is the episode number.

Example:

```http
GET /api/sources/67890/1/1
```

### API Responses

The API will respond with a JSON object containing the streaming URLs, subtitles (if available), and download options (if configured).

Example Response:

```json
{
  "sources": [
    {
      "server": 1,
      "url": "https://example.com/stream1"
    },
    {
      "server": 2,
      "url": "https://example.com/stream2"
    }
  ],
  "captions": [
    {
      "language": "English",
      "url": "https://example.com/subtitles/en.srt"
    }
  ],
  "downloads": [
    {
      "quality": "1080p",
      "url": "https://example.com/downloads/movie.mp4"
    }
  ]
}
```


### How to Use the Scrapers

1. **Download and Set Up**
   - Download the StreamFlix Providers `scrapers` folder from the repository.
   - Drag and drop the folder into your workspace or project directory.

2. **Importing**
   - To use the scrapers in your code, import them as follows:
     ```python
     import scrapers.flixhq
     import scrapers.vidsrcto
     ```
   - Once imported, you can instantiate the scraper classes and use their methods to fetch streaming URLs.

3. **Fetching Streaming URLs**
   - Use the appropriate methods provided by each scraper to fetch streaming URLs based on the title or TMDB ID of the content.
   - For example:
     ```python
     scraper = VidsrcTo()
     response_data = scraper.fetch_source(108978, season=1, episode=1) 
     print(f"Tv Show URL: {response_data}")

     ```
### Deploy on cloud providers
[![Run on Replit](https://binbashbanana.github.io/deploy-buttons/buttons/remade/replit.svg)](https://replit.com/github/streamflix-one/providers)
[![Remix on Glitch](https://binbashbanana.github.io/deploy-buttons/buttons/remade/glitch.svg)](https://glitch.com/edit/#!/import/github/streamflix-one/providers)
[![Deploy on Railway](https://binbashbanana.github.io/deploy-buttons/buttons/remade/railway.svg)](https://railway.app/new/template?template=https://github.com/streamflix-one/providers)
[![Deploy to Cyclic](https://binbashbanana.github.io/deploy-buttons/buttons/remade/cyclic.svg)](https://app.cyclic.sh/api/app/deploy/streamflix-one/providers)
[![Deploy to Koyeb](https://binbashbanana.github.io/deploy-buttons/buttons/remade/koyeb.svg)](https://app.koyeb.com/deploy?type=git&repository=github.com/streamflix-one/providers&branch=main&name=Streamflix)
[![Deploy to Render](https://binbashbanana.github.io/deploy-buttons/buttons/remade/render.svg)](https://render.com/deploy?repo=https://github.com/streamflix-one/providers)
### Contributing

Contributions to StreamFlix Providers are welcome! If you'd like to contribute, follow these steps:

1. **Fork the Repository**
   - Fork the StreamFlix Providers repository on GitHub.

2. **Clone the Forked Repository**
   - Clone your forked repository to your local machine.

3. **Make Changes**
   - Make the necessary changes or additions to the scraper scripts.
   - Ensure that your code follows the existing coding style and conventions.

4. **Commit and Push**
   - Commit your changes and push them to your forked repository.

5. **Create a Pull Request**
   - Create a pull request from your forked repository to the main StreamFlix Providers repository.
   - Provide a clear description of the changes you've made and the rationale behind them.
   - Include any relevant details or documentation updates.

6. **Review and Collaborate**
   - Collaborate with other contributors and maintainers to review and refine your changes.
   - Address any feedback or suggestions provided during the review process.
   - Once your pull request is approved, it will be merged into the main repository.

### Contributors

Acknowledgment and gratitude to all contributors who help improve StreamFlix Providers and make it more robust and versatile.

---

Feel free to explore and utilize StreamFlix Providers in your projects. If you encounter any issues or have suggestions for improvement, don't hesitate to open an issue or submit a pull request. Happy streaming!
