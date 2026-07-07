import logging
from pathlib import Path
from loader_all import DocumentLoader
from classifier_all import DocumentClassifier
from extra.extractor_factory import get_extractor

# def classify_document(file_path: str):
#     """Extract text from a document and classify it."""
#     loader = DocumentLoader()
#     classifier = DocumentClassifier()
#
#     # Step 1: Extract text
#     text = loader.get_document_text(file_path)
#
#     # Step 2: Classify
#     result = classifier.classify(text)
#
#     print("\n📄 File:", Path(file_path).name)
#     print("🧾 Classified as:", result.get("document_type", "Unknown"))
#
#     doc_type = result.get("document_type")
#     extractor_func = get_extractor(doc_type)
#     structured_data = extractor_func(text)
#
#     return structured_data
#
# if __name__ == "__main__":
#     # Example usage: classify a single file
#     test_file = r"C:\Users\user\Desktop\langchain\input_docs\sample_payroll.pdf"  # change path
#
#     classify_document(test_file)

# import logging
# from pathlib import Path
# from loader_all import DocumentLoader
# # from classify_all import DocumentClassifier
# from extra.extractor_factory import get_extractor

# logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def classify_and_extract(file_path: str):
    """Extract text from a document, classify it, and extract structured data."""
    loader = DocumentLoader()
    classifier = DocumentClassifier()

    # Step 1: Extract text
    text = loader.get_document_text(file_path)

    # Step 2: Classify the document type
    classification_result = classifier.classify(text)
    document_type = classification_result.get("document_type", "Unknown")

    print("\n📄 File:", Path(file_path).name)
    print("🧾 Classified as:", document_type)

    if document_type == "Unknown":
        logging.warning("⚠️ Could not determine document type. Skipping extraction.")
        return None

    # Step 3: Get appropriate extractor from factory
    extractor_func = get_extractor(document_type)

    if not extractor_func:
        logging.warning(f"⚠️ No extractor found for document type: {document_type}")
        return None

    # Step 4: Extract structured data using local LLM
    structured_data = extractor_func(text)

    print("\n📊 Extracted Structured Data:")
    print(structured_data)

    return {
        "file_name": Path(file_path).name,
        "document_type": document_type,
        "extracted_data": structured_data,
    }


if __name__ == "__main__":
    # Example usage: classify and extract one file
    test_file = r"C:\Users\user\Desktop\langchain\input_docs\meesho6.pdf"

    result = classify_and_extract(test_file)

    # # Optional: Save output as JSON for review
    # if result:
    #     import json, os
    #     output_path = Path(r"C:\Users\user\Desktop\langchain\output_data")
    #     output_path.mkdir(parents=True, exist_ok=True)
    #
    #     out_file = output_path / f"{Path(test_file).stem}_output.json"
    #     with open(out_file, "w", encoding="utf-8") as f:
    #         json.dump(result, f, indent=2, ensure_ascii=False)
    #
    #     print(f"\n✅ Extraction result saved to: {out_file}")
