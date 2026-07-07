# extraction/extractor.py
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain_community.chat_models import ChatOllama

from schemas.invoice_schema import InvoiceSchema  # Example schema

def extract_with_schema(text: str, schema, model="llama2"):
    """
    Extract structured JSON from document text using a schema.
    Schema = any Pydantic model (InvoiceSchema, BankStatementSchema, etc.)
    """
    parser = PydanticOutputParser(pydantic_object=schema)

    prompt = prompt = PromptTemplate(
    template=(
        "You are an information extractor.\n"
        "Extract ONLY the fields defined in the schema below.\n\n"
        "Schema:\n{format_instructions}\n\n"
        "Document:\n{text}\n\n"
        "Return ONLY valid JSON, no explanations, no code, no text outside JSON."
    ),
    input_variables=["text"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

    llm = ChatOllama(model=model, temperature=0)

    chain = prompt | llm | parser
    try:
        result = chain.invoke({"text": text})
        return result.dict()
    except Exception as e:
        print(f"[ERROR] Extraction failed: {e}")
        return {}
