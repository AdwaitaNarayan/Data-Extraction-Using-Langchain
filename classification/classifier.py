from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from config import config  # Import your Config class
import re
import json
import logging

logger = logging.getLogger(__name__)


class DocumentClassifier:
    def __init__(self):
        # Step 1: Define response schema dynamically from config
        response_schemas = [
            ResponseSchema(
                name="document_type",
                description=f"Type of the document, one of {', '.join(config.DOCUMENT_TYPES)}"
            )
        ]
        self.parser = StructuredOutputParser.from_response_schemas(response_schemas)

        # Step 2: Create system prompt with escaped curly braces
        format_instructions = self.parser.get_format_instructions()
        format_instructions = format_instructions.replace("{", "{{").replace("}", "}}")

        allowed_types = ", ".join(config.DOCUMENT_TYPES)

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    f"""You are a strict document classifier.
                    Classify the document into one of the allowed types:
                    {allowed_types}

                    Return ONLY valid JSON as per the following format:
                    {format_instructions}
                    """,
                ),
                ("human", "{text}"),
            ]
        )

        # Step 3: Initialize LLM using config
        self.llm = ChatOllama(model=config.OLLAMA_MODELS["classification"], base_url=config.OLLAMA_BASE_URL)

    def classify(self, document_text: str):
        # Format prompt with document text
        messages = self.prompt.format_prompt(text=document_text).to_messages()

        # Run LLM
        llm_output = self.llm.invoke(messages)
        llm_text = llm_output.content

        logger.info(f"Raw LLM output:\n{llm_text}")

        # Try to extract JSON using regex
        match = re.search(r"\{.*\}", llm_text, re.DOTALL)
        if not match:
            raise ValueError("No JSON found in LLM output")

        json_text = match.group(0)

        # Quick validation of JSON before passing to parser
        try:
            json.loads(json_text)  # ensure JSON is valid
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON from LLM: {e}")
            logger.error(f"JSON text:\n{json_text}")
            raise ValueError(f"Invalid JSON from LLM output: {e}")

        # Parse LLM output to structured JSON
        parsed_output = self.parser.parse(json_text)
        return parsed_output


# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

