from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
import re
import json
import logging

# --- CONFIGURATION SECTION ---

# All document types extracted from your CLASSIFICATION_KEYWORDS dictionary
DOCUMENT_TYPES = [
    # Financial Statements
    "Balance Sheet", "Income Statement", "Cash Flow Statement",
    "Statement of Changes in Equity", "Notes to Accounts",

    # Invoices & Vouchers
    "Sales Invoice", "Purchase Invoice", "Receipt", "Payment Voucher",
    "Bank Statement", "Payroll", "Expense Voucher", "Credit Note", "Debit Note",

    # Journals & Ledgers
    "General Journal", "General Ledger", "Cash Book", "Petty Cash Book",
    "Accounts Payable Ledger", "Accounts Receivable Ledger",

    # Reports & MIS
    "Trial Balance", "Bank Reconciliation Statement", "Inventory Valuation Report",
    "Fixed Asset Register", "Accounts Aging Report", "Budget Report",
    "Cost Sheet", "Forecasting Statement", "MIS Report", "Performance Dashboard",

    # Tax & Compliance
    "Tax Return", "Audit Report", "Annual Report", "GST Compliance Reports",
    "Company Incorporation Docs", "Board Resolutions"
]

# Ollama model and endpoint configuration
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODELS = {
    "classification": "llama2:latest"
}

logger = logging.getLogger(__name__)


class DocumentClassifier:
    def __init__(self):
        # Step 1: Define response schema
        response_schemas = [
            ResponseSchema(
                name="document_type",
                description=f"Type of the document, one of {', '.join(DOCUMENT_TYPES)}"
            )
        ]
        self.parser = StructuredOutputParser.from_response_schemas(response_schemas)

        # Step 2: Create prompt
        format_instructions = self.parser.get_format_instructions()
        format_instructions = format_instructions.replace("{", "{{").replace("}", "}}")

        allowed_types = ", ".join(DOCUMENT_TYPES)

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    f"""You are a strict financial document classifier.
                    Classify the given document text into one of these allowed types:
                    {allowed_types}

                    If you are unsure, pick the most likely match.
                    Return ONLY valid JSON as per this format:
                    {format_instructions}
                    """,
                ),
                ("human", "{text}"),
            ]
        )

        # Step 3: Initialize LLM
        self.llm = ChatOllama(model=OLLAMA_MODELS["classification"], base_url=OLLAMA_BASE_URL)

    def classify(self, document_text: str):
        """Classify the given document text into a predefined type."""
        messages = self.prompt.format_prompt(text=document_text).to_messages()

        # Run LLM
        llm_output = self.llm.invoke(messages)
        llm_text = llm_output.content
        logger.info(f"Raw LLM output:\n{llm_text}")

        # Extract JSON safely
        match = re.search(r"\{.*\}", llm_text, re.DOTALL)
        if not match:
            raise ValueError("No JSON found in LLM output")

        json_text = match.group(0)

        # Validate JSON
        try:
            json.loads(json_text)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON from LLM: {e}")
            logger.error(f"JSON text:\n{json_text}")
            raise ValueError(f"Invalid JSON from LLM output: {e}")

        parsed_output = self.parser.parse(json_text)
        return parsed_output