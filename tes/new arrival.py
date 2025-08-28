import asyncio
import json
import datetime
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from crawl4ai.extraction.json_css_extraction_strategy import (
    JsonCssExtractionStrategy,
    JsonCssSchema,
)
from pydantic import BaseModel, Field


# Pydantic models to define the desired data structure
class DressDetails(BaseModel):
    """Structured data for a single dress."""
    name: str = Field(..., description="Name of the dress")
    price: str = Field(..., description="Price of the dress")
    availability: str = Field(..., description="Availability of the dress")


class ScrapedData(BaseModel):
    """Structured data for the entire scrape job."""
    extraction_date: str = Field(..., description="The date the data was extracted.")
    products: list[DressDetails] = Field(..., description="List of dresses with their details")


async def main():
    """
    Main function to run the web scraping task.
    """
    # Define the URL to tes
    url = "https://laam.pk/new-arrivals"

    # Define the schema for JSON extraction using CSS selectors
    # We use a base selector to target each product card and then specify
    # the selectors for each field relative to that base.
    extraction_schema = JsonCssSchema(
        base_selector=".product-card",
        fields={
            "name": "h3.product-title a",
            "price": "div.product-price span",
            "availability": ".availability",
        }
    )

    # Set up the crawling configuration with the JSON extraction strategy
    run_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        extraction_strategy=JsonCssExtractionStrategy(schema=extraction_schema),
        # A simple prompt can help the LLM perform better extraction
        llm_prompt_override="Extract the name, price, and availability for all new arrival dresses on the page."
    )

    # Use 'async with' to automatically start and stop the browser session.
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url, config=run_config)

    # Process and print the extracted JSON data
    if result.success and result.extraction:
        # Create a dictionary to hold the final, structured data
        final_data = {
            "extraction_date": datetime.date.today().isoformat(),
            "products": result.extraction
        }

        # Define the output file name
        output_file = "new_arrivals.json"

        # Write the data to a JSON file with pretty printing
        with open(output_file, "w") as f:
            json.dump(final_data, f, indent=4)

        print(f"✅ Successfully scraped data and saved it to '{output_file}'")
    else:
        print(f"❌ Failed to crawl or extract data: {result.error_message}")


if __name__ == "__main__":
    asyncio.run(main())