import os
import asyncio
from crawl4ai import AsyncWebCrawler, LLMConfig
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from pydantic import BaseModel, Field
# Ensure this line is correct
from praisonai import BaseTool
from typing import List

class ModelFee(BaseModel):
    llm_model_name: str = Field(..., description="Name of the model.")
    input_fee: str = Field(..., description="Fee for input token for the model.")
    output_fee: str = Field(..., description="Fee for output token for the model.")

class ModelFeeList(BaseModel):
    models: List[ModelFee] = Field(..., description="A list of OpenAI models and their fees.")

class ModelFeeTool(BaseTool):
    name: str = "ModelFeeTool"
    description: str = "Extracts model fees for input and output tokens from the given pricing page."

    async def _run(self, url: str):
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(
                url=url,
                word_count_threshold=1,
                extraction_strategy=LLMExtractionStrategy(
                    llm_config=LLMConfig(
                        provider="openai/gpt-4o",
                        api_token=os.getenv('OPENAI_API_KEY')
                    ),
                    schema=ModelFeeList.model_json_schema(),
                    extraction_type="schema",
                    instruction="""From the crawled content, extract all mentioned model names along with their fees for input and output tokens. 
                    Do not miss any models in the entire content. Return a list of JSON objects where each object represents a model and its fees."""
                ),
                bypass_cache=True,
            )
            return result.extracted_content

async def main():
    tool = ModelFeeTool()
    url = "https://openai.com/api/pricing/"
    result = await tool._run(url)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())