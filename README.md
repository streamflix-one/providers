<p align="center">
  <img src="/assets/logo.webp" alt="StreamFlix Providers" width="300"/>
</p>



**StreamFlix Providers**

StreamFlix Providers is a collection of scraper scripts that fetch streaming URLs from various online streaming platforms. These scripts allow you to extract video URLs from platforms like FileCDN and Vidsrc.to, facilitating the process of integrating streaming functionality into your applications or projects.

### How to Use

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
     print(f"Movie URL: {response_data}")

     ```

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
