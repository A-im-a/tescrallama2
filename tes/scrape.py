import asyncio
from crawl4ai import AsyncWebCrawler

async def main():
    # Create an instance of the asynchronous crawler
    async with AsyncWebCrawler() as crawler:
        # Run the crawler on a URL
        result = await crawler.arun(url="https://openai.com/api/pricing/")
        # Print the extracted content
        print(result.markdown)

if __name__ == "__main__":
    asyncio.run(main())
