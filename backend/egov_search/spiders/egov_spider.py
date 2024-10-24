import scrapy
from elasticsearch import Elasticsearch
from urllib.parse import urlparse

class EgovSpider(scrapy.Spider):
    name = "egov_spider"
    start_urls = ['https://egov.kz/cms/en', 'https://egov.kz/cms/ru', 'https://egov.kz/cms/kk']

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'  # Replace with your desired User-Agent
    }

    def __init__(self):
        self.es = Elasticsearch(['http://elasticsearch:9200'])
        self.clear_elasticsearch_index()

    def parse(self, response):
        # Get the base URL to check for internal links
        base_url = urlparse(response.url).netloc

        for link in response.css('a::attr(href)').getall():
            # Parse the link to extract its host
            link_url = urlparse(link)
            link_host = link_url.netloc

            # Only follow links from the egov.kz domain
            if link_host == "egov.kz" or not link_host:  # Handle relative URLs
                if "mobile=yes" not in link:
                    # Yield the link if it contains "services" in the URL
                    if "services" in link:
                        yield response.follow(link, self.parse_service)
                    else:
                        yield response.follow(link, self.parse)

    def parse_service(self, response):
        # Store the URL and its content if it contains "services" in the URL
        url = response.url
        if url.startswith("https://") and "services" in url:
            content = ' '.join(response.css('body *::text').getall())
            h1_header = response.css('h1::text').get(default='No Title')  # Extract the h1 header
            self.store_in_elasticsearch(url, content, h1_header)

    def store_in_elasticsearch(self, url, content, h1_header):
        doc = {
            'url': url,
            'main_content': content,
            'h1_header': h1_header  # Store the h1 header
        }
        self.es.index(index='egov_services', id=url, document=doc)

    def clear_elasticsearch_index(self):
        self.es.delete_by_query(index='egov_services', body={"query": {"match_all": {}}})

