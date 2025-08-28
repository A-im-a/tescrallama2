import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode

async def main():
    # Define the URL you want to tes
    url = "https://laam.pk/nodes/women-eastern-unstitched-636?attrs=season.summer+wear&utm_source=google&utm_medium=paid&utm_campaign=pakistan_Search_Conversion_May10_mn&gad_campaignid=22545577321"

    # Set up the crawling configuration.
    # CacheMode.BYPASS ensures you get the freshest content
    # from the website instead of a cached version.
    run_config = CrawlerRunConfig(cache_mode=CacheMode.BYPASS)

    # Use 'async with' to automatically start and stop the browser session.
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url, config=run_config)

    # Print the extracted markdown content
    if result.success:
        print(result.markdown)
    else:
        print(f"Failed to crawl: {result.error_message}")

if __name__ == "__main__":
    asyncio.run(main())