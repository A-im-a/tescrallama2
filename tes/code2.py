import os
import asyncio
from crawl4ai import AsyncWebCrawler, LLMConfig
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from pydantic import BaseModel, Field
from typing import List

# Define the data structure for a single model's fee
class OpenAIModelFee(BaseModel):
    model_name: str = Field(..., description="Name of the OpenAI model.")
    input_fee: str = Field(..., description="Fee for input token for the OpenAI model.")
    output_fee: str = Field(..., description="Fee for output token for the OpenAI model.")

# Define a list of these models, which the LLM will extract
class OpenAIModelList(BaseModel):
    models: List[OpenAIModelFee] = Field(..., description="A list of OpenAI models and their fees.")

async def main():
    url = 'https://openai.com/api/pricing/'

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=url,
            word_count_threshold=1,
            extraction_strategy=LLMExtractionStrategy(
                llm_config=LLMConfig(
                    provider="openai/gpt-4o",
                    api_token=os.getenv('OPENAI_API_KEY')
                ),
                # Use the new list schema. Also, use the recommended model_json_schema().
                schema=OpenAIModelList.model_json_schema(),
                extraction_type="schema",
                instruction="""From the crawled content, extract all mentioned model names along with their fees for input and output tokens. 
                Do not miss any models in the entire content. Return a list of JSON objects where each object represents a model and its fees."""
            ),
            bypass_cache=True,
        )
    # The extracted content will now be a JSON string of a list
    print(result.extracted_content)

if __name__ == "__main__":
    asyncio.run(main())