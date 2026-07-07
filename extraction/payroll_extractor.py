from typing import Optional
from schemas.payroll_schema import PayrollSchema
from extraction.extractor_utils import OllamaExtractionUtils


class PayrollExtractor:
    """Payroll extractor using exact field specifications"""

    def __init__(self):
        self.utils = OllamaExtractionUtils()

    def extract(self, text: str) -> Optional[PayrollSchema]:
        """Extract payroll data matching schema exactly"""

        additional_instructions = """
PAYROLL EXTRACTION GUIDELINES:
- Extract employee_id, employee_name, department, designation
- Get salary details: gross_salary, net_salary, basic_salary
- Extract allowances: DA, HRA, conveyance, medical, other allowances
- Find deductions: PF, ESI, income tax, professional tax, other deductions
- Get pay period dates and bank details
- Dates in DD-MM-YYYY format
- Numbers without currency symbols

IMPORTANT:
- Calculate net salary = gross salary - total deductions
- Extract all allowance and deduction components
- Bank details: name, account number, IFSC code
"""

        return self.utils.extract_with_retry(
            text=text,
            schema=PayrollSchema,
            document_type="payroll",
            additional_instructions=additional_instructions
        )
