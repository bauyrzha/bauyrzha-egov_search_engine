# eGov Multilingual Search Engine
# Project Overview

The eGov Multilingual Search Engine is a custom search engine designed to crawl and index the content of the egov.kz website. The system is built using a Scrapy spider that crawls pages related to government services of Republic Kazakhstan. The search engine supports multilingual crawling for the Kazakh, Russian, and English sections of the website.

The backend stores the crawled data in an Elasticsearch index and processes it using the SentenceTransformer model. This model helps in ensuring semantic search capabilities, enhancing the relevance of the search results. 

The frontend allows users to query the indexed content, retrieving relevant URLs and their main headers. 

The project is containerized using Docker for ease of setup and deployment.

# Features

**Multilingual Support**: Crawls the egov.kz website in Kazakh, Russian, and English.

**Focused Crawling**: Only indexes URLs that contain the word "services" and ignores mobile-specific pages.

**Internal Link Filtering**: Only internal links from egov.kz are followed, avoiding external domains.

**HTTPS Only**: Only saves pages with https URLs in the Elasticsearch index.

**Duplicate Avoidance**: The system avoids indexing duplicate URLs.

**Automatic Index Cleanup**: The Elasticsearch index is cleared before each new crawl, ensuring fresh data.

**Frontend Search**: Users can search for relevant content by keyword and view the results, including the main headers from the page content.

# Prerequisites

Docker and Docker Compose

Internet access

# Setup and Running

1. Clone the repository:

   `git clone git@github.com:bauyrzha/bauyrzha-egov_search_engine.git` or `git clone https://github.com/bauyrzha/bauyrzha-egov_search_engine.git`

   `cd bauyrzha-egov_search_engine`

2. Build and run the project:

   `docker-compose up --build`

3. Running the Scrapy spider:
   
   First time or fresh crawled data run it manually:

   `docker-compose exec backend scrapy crawl egov_spider`

4. Access the frontend:
   
   Visit `http://localhost:5000` in your browser to use the search interface.

5. Clean the Elasticsearch index:
   
   The index is automatically cleared before each new crawl. However, you can also clear it manually:

   `curl -X DELETE "http://localhost:9200/egov_services"`

# Future Enhancements

Adding more advanced NLP for content relevance scoring.

Improving the frontend design for a better user experience.

# License

Apache-2.0 license

















