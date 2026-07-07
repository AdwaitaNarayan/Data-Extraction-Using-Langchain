import time
import logging
from typing import Any, Dict, Optional, Type

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_ollama import ChatOllama
from pydantic import BaseModel, ValidationError

from config import config

logger = logging.getLogger(__name__)


class OllamaExtractionUtils:
    """Utility class for schema-based extraction with Ollama"""

    def __init__(self):
        self.model = ChatOllama(
            base_url=config.OLLAMA_BASE_URL,
            model=config.OLLAMA_MODELS["extraction"],
            temperature=config.TEMPERATURE,
            top_p=config.TOP_P,
            top_k=config.TOP_K,
        )

    def extract_with_retry(
        self,
        text: str,
        schema: Type[BaseModel],
        document_type: str,
        additional_instructions: Optional[str] = None,
    ) -> Optional[BaseModel]:
        """Run extraction with retries, schema validation"""

        parser = JsonOutputParser(pydantic_object=schema)

        # Prompt for extraction
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    f"""You are an information extraction system.
Extract structured {document_type} data from the text.

- Follow EXACT schema provided
- Output ONLY valid JSON
- If a field is missing, set it to null
{additional_instructions or ""}
""",
                ),
                ("human", "{text}"),
            ]
        )

        chain = prompt | self.model

        for attempt in range(config.MAX_RETRIES):
            try:
                logger.info(f"🔍 Extracting {document_type} (attempt {attempt+1})")

                # Get raw output
                raw_output = chain.invoke({"text": text})
                logger.debug(f"Raw model output: {raw_output}")

                # Parse with JSON parser
                result: Dict[str, Any] = parser.invoke(raw_output)

                if not result:
                    logger.error("❌ Model returned no JSON (None).")
                    continue

                # Validate using schema
                validated = schema(**result)
                validated.document_type = document_type
                logger.info(f"✅ Extraction successful for {document_type}")
                return validated

            except ValidationError as ve:
                logger.error(f"Schema validation failed: {ve}")
            except Exception as e:
                logger.error(f"Extraction error: {str(e)}")

            time.sleep(config.RETRY_DELAY)

        logger.error(f"❌ Extraction failed after {config.MAX_RETRIES} attempts")
        return None
